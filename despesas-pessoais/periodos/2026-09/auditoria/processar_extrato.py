"""Normaliza o extrato recebido em 09/10, preservando só setembro no orçamento."""
from pathlib import Path
from datetime import datetime
from decimal import Decimal as D
from collections import defaultdict
import json
import re
import sys
import pdfplumber

PERIOD = Path(__file__).resolve().parents[1]
ROOT = PERIOD.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import mensal


def main():
    config = mensal.read(PERIOD / 'periodo.json')
    entry = next(f for f in config['arquivos'] if 'itau_extrato_082026' in f['arquivo'])
    all_rows, balances = [], {}
    with pdfplumber.open(PERIOD / entry['arquivo']) as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            text = page.extract_text(x_tolerance=1)
            for line_number, text_line in enumerate(text.splitlines(), 1):
                match = re.fullmatch(r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?[\d.]+,\d{2})', text_line)
                if not match:
                    continue
                date = datetime.strptime(match[1], '%d/%m/%Y').date().isoformat()
                value = match[3].replace('.', '').replace(',', '.')
                row = {'data': date, 'descricao': match[2], 'valor_original': value,
                       'pagina': page_number, 'linha_extraida': line_number, 'texto_fonte': text_line}
                if match[2] == 'SALDO DO DIA':
                    assert date not in balances or balances[date]['valor_original'] == value
                    balances[date] = row
                else:
                    row['id_extracao'] = f'BANCO-P{page_number}-L{line_number}'
                    all_rows.append(row)
    mensal.write(PERIOD / 'auditoria/dados/extrato_extraido.json', {
        'arquivo': entry['arquivo'], 'sha256': entry['sha256'], 'periodo_documento': ['2026-08-10', '2026-10-09'],
        'movimentos_todos': all_rows, 'saldos_todos': balances,
        'criterio': 'Datas contábeis na primeira coluna; só 01 a 30/09 integram lancamentos.json.'})
    selected = [r for r in all_rows if config['extrato_inicio'] <= r['data'] <= config['extrato_fim']]
    source = dict(entry, id='EXTRATO', nome='Extrato Itaú', tipo='extrato',
                  saldo_inicial=balances['2026-08-31']['valor_original'], saldo_final=balances['2026-09-30']['valor_original'],
                  saldo_inicial_fonte={'data': '2026-08-31', 'pagina': balances['2026-08-31']['pagina']},
                  saldos_diarios={day: r['valor_original'] for day, r in sorted(balances.items()) if '2026-09-01' <= day <= '2026-09-30'})
    for index, row in enumerate(selected, 1):
        row.update(id=f'EXT-{index:03}', fonte_id='EXTRATO', origem='Extrato Itaú',
                   valor_pessoal_exato='0', linha=None, status='excluido_receita', observacao='Entrada bancária: fora do quadro de despesas; nenhum abatimento sem vínculo confirmado.')
        name, value = row['descricao'].upper(), D(row['valor_original'])
        if value > 0:
            if 'PALOMA' in name:
                row.update(status='credito_sem_vinculo', observacao='Crédito de Paloma sem vínculo confirmado; preservado na conciliação, sem abater despesa ou comprovar quitação por coincidência de valor/data.')
            elif 'LUIZ CO' in name or 'TED 033.2062.LUIZ C N' in name:
                row.update(status='excluido_transferencia_propria', observacao='Transferência própria/portabilidade pelo padrão já identificado; fora das despesas e sem nova contagem de receita na passagem entre contas.')
            continue
        row.update(valor_pessoal_exato=str(-value), linha='46', status='provisoria', observacao='Saída não identificada: Outros básicos provisório.')
        if any(x in name for x in ['ITAU BLACK', 'PERS INFINIT']):
            row.update(linha=None, valor_pessoal_exato='0', status='excluido_pagamento_fatura', observacao='Pagamento de fatura: não duplicar compras já apuradas nos cartões. Mantido na conciliação bancária.')
        elif 'PIX TRANSF LUIZ CO' in name:
            row.update(linha=None, valor_pessoal_exato='0', status='excluido_transferencia_propria', observacao='Transferência entre contas próprias, conforme base vigente; fora do orçamento.')
        elif any(x in name for x in ['PIX TRANSF MARIO P', 'PIX TRANSF NAOMI', 'PIX TRANSF SP SERV']):
            row.update(linha=None, valor_pessoal_exato='0', status='excluido_tratamento_reembolsado', observacao='Tratamento do filho: exclusão do orçamento por decisão vigente de Luiz; reembolso via Santander. Não inventar crédito ou data de recebimento no Itaú.')
        elif 'PIX TRANSF MAGALI' in name or 'PIX TRANSF WALTER' in name:
            row.update(linha='31', status='pendente_extrato', rateio_status='aguardando_confirmacao',
                       observacao='Categoria babá confirmada na base. Integral provisório até confirmar participação/vínculo do crédito de Paloma; coincidência de valor/data é indício, não quitação.')
            if 'WALTER' in name:
                row.update(parcela='02/02', observacao=row['observacao'] + ' Segunda parcela do acordo judicial localizada em 21/09, R$ 1.750,00; não projetar terceira parcela.')
        elif 'PIX TRANSF PALOMA' in name and -value in [D('210'), D('220')]:
            row.update(linha='28', status='regra_kb', observacao='Faxina semanal: padrão de PIX para Paloma de R$ 210/220 confirmado na base. Valor integral no quadro, sem aplicar regra de cartões ao PIX.')
        elif 'PIX TRANSF PALOMA' in name and -value in [D('1208'), D('1219.50')]:
            row.update(linha='21', status='regra_kb', observacao='Financiamento Apt Lapa: padrão de valor/destinatária já confirmado. Valor atual R$ 1.208,00; não reutilizar ajuste manual de agosto.')
        else:
            rules = [('DA VIVO-SP', '25'), ('DA ELETROPAULO', '24'), ('PIX AUT CLARO', '26'),
                     ('DA PMSP', '23'), ('PIX TRANSF SONIA', '29'), ('PIX TRANSF LUIZ FE', '29'),
                     ('PAG BOLETO ASSOCIACAO ATLETICA BANCO DO', '57'), ('JUROS LIMITE DA CONTA', '45')]
            if name == 'IOF':
                rules.append(('IOF', '45'))
            for pattern, line in rules:
                if name.startswith(pattern):
                    row.update(linha=line, status='regra_kb', observacao='Categoria pela base e descritor atual. Valor efetivamente debitado em setembro, sem importar valores históricos.')
                    break
    revision_path = PERIOD / 'auditoria/dados/revisao_extrato_usuario.json'
    if revision_path.exists():
        updates = mensal.read(revision_path).get('lancamentos', {})
        for row in selected:
            row.update(updates.get(row['id'], {}))
    mensal.write(PERIOD / 'auditoria/dados/extrato_normalizado.json', {'fonte': source, 'lancamentos': selected})
    ledger = mensal.read(PERIOD / 'auditoria/dados/lancamentos.json')
    ledger['fontes'] = [f for f in ledger['fontes'] if f['tipo'] != 'extrato'] + [source]
    ledger['lancamentos'] = [r for r in ledger['lancamentos'] if r['fonte_id'] != 'EXTRATO'] + selected
    ledger['observacoes'] = [n for n in ledger['observacoes'] if not n.startswith(('Processamento parcial:', 'Ausência do extrato'))]
    ledger['observacoes'] = [n for n in ledger['observacoes'] if not n.startswith(('Extrato de setembro:', 'Banco e cartões:', 'Condomínio, eSocial', 'AABB:'))]
    ledger['observacoes'] += [
        'Extrato de setembro: documento de 10/08 a 09/10/2026 recebido e conferido; só datas contábeis de 01 a 30/09 entram no resumo. Saldo anterior de 31/08: -R$ 3.887,74; saldo final de 30/09: -R$ 2.084,82. O saldo de -R$ 11.235,07 do cabeçalho é de outubro, fora deste fechamento.',
        'Banco e cartões: fontes conciliadas. Reembolsos de WALTER (R$ 1.750,00) e da babá atual (R$ 1.619,00) confirmados e aplicados uma única vez. R$ 2.467,00 de Paloma é acerto de agosto, fora das despesas de setembro.',
        'Condomínio, eSocial e provisão: condomínio segue sem lançamento identificado ou confirmação; Bruna não tem eSocial segundo Luiz, e não houve aporte à provisão neste mês. Não copiar valores de agosto.',
        'AABB: boleto de R$ 651,00 duplicado e compensado pelo clube segundo Luiz; débito preservado na conciliação, sem despesa duplicada nem estorno fictício. Despesa confirmada de setembro: complemento de R$ 2,00.'
    ]
    mensal.write(PERIOD / 'auditoria/dados/lancamentos.json', ledger)
    result = mensal.validate(PERIOD)
    details = PERIOD / 'resultados/detalhes'
    by_date = defaultdict(D)
    for row in selected:
        by_date[row['data']] += D(row['valor_original'])
    daily = []
    running = D(source['saldo_inicial'])
    for day, balance in source['saldos_diarios'].items():
        before = running
        running += by_date[day]
        assert running == D(balance)
        daily.append([day, mensal.br(before), mensal.br(by_date[day]), mensal.br(running), '0,00'])
    inflows = sum((D(r['valor_original']) for r in selected if D(r['valor_original']) > 0), D(0))
    outflows = -sum((D(r['valor_original']) for r in selected if D(r['valor_original']) < 0), D(0))
    bank_personal = sum((D(r['valores']['EXTRATO']) for r in result['linhas']), D(0))
    text = '# Setembro/2026 — extrato Itaú conferido\n\n'
    text += f'Documento de 10/08 a 09/10/2026; orçamento restrito a 01–30/09. {len(selected)} movimentos e {len(daily)} saldos diários, todos conciliados. O nome do arquivo não define o mês.\n\n'
    text += mensal.table(['Controle', 'Valor R$'], [
        ['Saldo inicial — 31/08, página 2', mensal.br(D(source['saldo_inicial']))],
        ['Entradas de setembro', mensal.br(inflows)], ['Saídas de setembro', mensal.br(outflows)],
        ['Saldo final — 30/09, página 1', mensal.br(running)], ['Diferença', '0,00'],
        ['Despesas pessoais do extrato — provisórias', mensal.br(bank_personal)]])
    text += '\n\nO saldo atual de -R$ 11.235,07, no cabeçalho, pertence a 09/10 e não foi usado como fechamento de setembro. Transferências próprias, entradas, tratamentos excluídos por decisão de Luiz e pagamentos de faturas integram o saldo bancário, mas não são somados como novas despesas.\n\n'
    text += '## Saldos diários\n\n' + mensal.table(['Data', 'Saldo anterior R$', 'Movimentos líquidos R$', 'Saldo final R$', 'Diferença R$'], daily)
    text += '\n\n## Movimentos de setembro\n\n' + mensal.table(['ID', 'Data contábil', 'Descrição', 'Original R$', 'Linha', 'Pessoal R$', 'Página', 'Decisão'],
        [[r['id'], r['data'], r['descricao'], mensal.br(D(r['valor_original'])), r['linha'] or 'Excluído', mensal.br(D(r['valor_pessoal_exato'])), r['pagina'], r['observacao']] for r in selected])
    text += '\n\n## Itens de acompanhamento\n\n- WALTER: 02/02 localizada em 21/09, R$ 1.750,00, reembolsada integralmente por Paloma; pessoal zero. Acordo encerrado quanto às duas parcelas documentadas, sem terceira parcela prevista.\n- Babá atual via Magali: débito R$ 3.237,09 menos crédito confirmado R$ 1.619,00 = R$ 1.618,09 pessoais. Não dividir novamente.\n- Acerto de agosto: crédito R$ 2.467,00 confirmado; não aplicado a setembro.\n- Bruna não tem eSocial segundo Luiz; nenhum aporte à provisão foi feito em setembro. Condomínio permanece não localizado.\n- AABB: boleto R$ 651,00 duplicado e compensado pelo clube, conforme confirmação; não cria despesa de setembro nem estorno bancário. Complemento efetivo do mês R$ 2,00. Destino/competência da compensação não informado; não criar despesa futura automática.\n- Débito Visa de R$ 653,42 em 01/10 pertence ao mês seguinte no banco; é evidência documental de pagamento da fatura, não nova despesa de setembro.\n'
    mensal.write(details / 'EXTRATO.md', text)
    candidates = [
        {'credito_id': 'EXT-009', 'despesa_id': 'EXT-010', 'valor_credito': '1750.00', 'valor_despesa': '1750.00', 'hipotese': 'Reembolso integral de WALTER 02/02; mesma data contábil e valor.', 'status': 'aguardando_confirmacao'},
        {'credito_id': 'EXT-004', 'despesa_id': 'EXT-003', 'valor_credito': '1619.00', 'valor_despesa': '3237.09', 'hipotese': 'Reembolso de Magali no mesmo dia. Metade exata R$ 1.618,545; crédito é R$ 0,455 maior. Não ajustar o original nem presumir vínculo.', 'status': 'aguardando_confirmacao'},
        {'credito_id': 'EXT-022', 'despesa_id': None, 'valor_credito': '2467.00', 'valor_despesa': None, 'hipotese': 'Possível acerto do quadro de agosto de R$ 2.466,97; diferença R$ 0,03. Não usar como abatimento de setembro sem confirmação.', 'status': 'aguardando_confirmacao'},
    ]
    candidates[0].update(status='confirmado_usuario', hipotese='Reembolso integral de WALTER 02/02 confirmado por Luiz; R$ 1.750,00 aplicados a EXT-010, pessoal zero.')
    candidates[1].update(status='confirmado_usuario', hipotese='Reembolso da babá atual confirmado. Débito R$ 3.237,09 menos R$ 1.619,00 = R$ 1.618,09 pessoais. Preservar crédito efetivo, sem impor metade exata nem novo rateio.')
    candidates[2].update(status='confirmado_acerto_agosto', hipotese='Acerto de agosto confirmado por Luiz. Diferença documental de R$ 0,03; crédito não aplicado às despesas de setembro.')
    mensal.write(PERIOD / 'auditoria/dados/conferencia_reembolsos_babas.json', {'mes_referencia': '2026-09', 'vinculos_confirmados': candidates, 'creditos_aplicados': result['creditos_utilizados']})
    text = '# Setembro/2026 — créditos de Paloma e acerto\n\nFinalidades confirmadas por Luiz em 09/10/2026. Reembolsos de R$ 3.369,00 aplicados uma única vez; crédito de R$ 2.467,00 reservado ao acerto de agosto.\n\n'
    text += mensal.table(['Crédito', 'Valor R$', 'Despesa candidata', 'Valor R$', 'Hipótese / limite'],
        [[r['credito_id'], mensal.br(D(r['valor_credito'])), r['despesa_id'] or 'Quadro de agosto', mensal.br(D(r['valor_despesa'])) if r['valor_despesa'] else '2.466,97', r['hipotese']] for r in candidates])
    text += '\n\nWALTER: pessoal zero; babá atual via Magali: pessoal R$ 1.618,09. Gestão Magali no cartão é outra compra, integral de Luiz pela decisão anterior, e não recebe abatimento desses créditos. O acerto de agosto não reduz novamente despesas de setembro nem reabre o fechamento anterior.\n'
    mensal.write(details / 'CONFERENCIA_REEMBOLSOS_BABAS.md', text)
    print(f'Extrato: {len(selected)} movimentos de setembro; {len(source["saldos_diarios"])} saldos diários conferidos; total pessoal R$ {mensal.br(result["total"])}')
    for row in selected:
        print(row['id'], row['data'], row['descricao'], row['valor_original'], row['linha'], row['valor_pessoal_exato'])


if __name__ == '__main__':
    main()

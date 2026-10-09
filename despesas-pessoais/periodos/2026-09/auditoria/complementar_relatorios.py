"""Complementa os relatórios do CLI com o escopo parcial e controles deste ciclo."""
from pathlib import Path
from decimal import Decimal as D
from collections import defaultdict
import json
import sys

PERIOD = Path(__file__).resolve().parents[1]
ROOT = PERIOD.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import mensal
from processar_cartoes import norm


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    result = mensal.validate(PERIOD)
    records = result['ledger']['lancamentos']
    out = PERIOD / 'resultados'
    cfg = result['config']
    bank = next((f for f in result['fontes'].values() if f['tipo'] == 'extrato'), None)
    cfg.update(status='provisorio_conciliado' if bank else 'parcial_faturas', fontes_ausentes=[] if bank else ['Extrato Itaú de 01 a 30/09/2026'],
               pasta_recebida='2026-09-ref_ago',
               observacao_referencia='Mês 2026-09 pelo prefixo da pasta e convenção vigente; ciclo 2026-10 pelos vencimentos. Sufixo ref_ago não usado para reabrir agosto.')
    mensal.write(PERIOD / 'periodo.json', cfg)

    # O gerador genérico não detecta fontes esperadas que ainda não chegaram.
    path = out / 'RESUMO_MENSAL.md'
    text = path.read_text(encoding='utf-8')
    if bank:
        text = text.replace('**Consolidado. Total pessoal:', '**Provisório — condomínio ainda não confirmado. Total pessoal:')
    if not bank:
        text = text.replace('**Provisório — ver pendências. Total pessoal:', '**Parcial — somente cartões; classificação pendente. Total pessoal dos documentos recebidos:')
        text = text.replace('**Consolidado. Total pessoal:', '**Parcial — somente cartões. Total pessoal dos documentos recebidos:')
        text = text.replace('Extrato: 2026-09-01 a 2026-09-30, pela data contábil.',
                            'Extrato bancário de 01 a 30/09/2026 ainda não recebido. Contas, PIX, babás e reembolsos bancários ainda não apurados.')
    mensal.write(path, text)
    pending_path = out / 'PENDENCIAS.md'
    text = pending_path.read_text(encoding='utf-8')
    if '## Parcelas e quadro de Paloma' not in text:
        text += ('\n\n## Condomínio e confirmações bancárias\n\nExtrato completo recebido e conciliado. Condomínio de setembro não localizado e sem resposta específica; ausência não comprova valor zero. Bruna não tem eSocial segundo Luiz e não houve provisão neste mês: perguntas resolvidas. Reembolsos de WALTER e da babá atual aplicados, acerto de agosto identificado. AABB duplicado compensado pelo clube, conforme Luiz: só R$ 2,00 como despesa deste mês, preservando o débito compensado na conciliação.\n' if bank else '\n\n## Documentação pendente\n\nExtrato Itaú completo de 01 a 30/09/2026, com saldo de abertura e fechamento. Sem ele, não há total mensal completo nem conciliação bancária. Conferir WALTER 02/02 e provisão de Bruna somente quando documentados.\n')
        text += '\n## Parcelas e quadro de Paloma\n\nVer [conferência de cartões](detalhes/CONFERENCIA_CARTOES.md) para parcelas atuais/futuras e [critérios do quadro de Paloma](detalhes/CONFERENCIA_PALOMA.md). A projeção Mastercard para a próxima fatura difere da soma das parcelas listadas no próprio PDF em R$ 285,46; isso não afeta o fechamento da fatura atual.\n'
    mensal.write(pending_path, text)

    controls = []
    future_data = read(PERIOD / 'auditoria/dados/parcelas_futuras.json')
    for brand, shown_next, shown_later in [('MASTERCARD', D('2126.67'), D('6983.18')), ('VISA', D('143.53'), D('123.86'))]:
        listed = sum((D(r['valor_original']) for r in future_data['fontes'][brand]), D(0))
        controls.append({'fonte_id': brand, 'soma_parcelas_listadas': str(listed), 'proxima_fatura_informada': str(shown_next),
                         'diferenca_projecao': str(shown_next - listed), 'demais_faturas_informadas': str(shown_later),
                         'total_futuro_informado': str(shown_next + shown_later), 'incluido_no_gasto_atual': False})
    mensal.write(PERIOD / 'auditoria/dados/conferencia_parcelas_futuras.json', controls)

    old = read(ROOT / 'periodos/2026-08/auditoria/dados/lancamentos.json')['lancamentos']
    previous = [r for r in old if r.get('cartao') and r.get('parcela')]
    continuation = []
    for r in previous:
        current, maximum = map(int, r['parcela'].split('/'))
        if current >= maximum:
            continue
        expected = f'{current + 1:02}/{maximum:02}'
        matching = [n for n in records if n.get('cartao') == r['cartao'] and norm(n['descricao']) == norm(r['descricao'])
                    and n['data'] == r['data'] and n.get('parcela') == expected]
        continuation.append([r['cartao'], r['descricao'], r['parcela'], expected,
                             ', '.join(n['id'] for n in matching) or 'Não localizado',
                             ', '.join(mensal.br(D(n['valor_original'])) for n in matching)])
    assert all(row[4] != 'Não localizado' for row in continuation), continuation
    current_parts = []
    for source in result['fontes'].values():
        if source['tipo'] != 'cartao':
            continue
        for subtotal in source['subtotais']:
            selected = [r for r in records if r['fonte_id'] == source['id'] and r['cartao'] == subtotal['cartao']
                        and ('internacional' if r['tipo'] in ['internacional', 'iof'] else 'nacional') == subtotal['tipo']]
            current_parts.append([source['nome'], subtotal['cartao'], subtotal['tipo'], len(selected), mensal.br(D(subtotal['valor'])), '0,00'])
    text = '# Setembro/2026 — conferência das faturas de outubro\n\n'
    text += '136 lançamentos atuais (incluindo créditos e dois repasses efetivos de IOF), com valores originais e páginas preservados. Todos os subtotais por cartão e os totais das faturas fecham sem diferença.\n\n'
    text += mensal.table(['Fonte', 'Cartão', 'Tipo', 'Registros', 'Integral R$', 'Diferença R$'], current_parts)
    text += '\n\n**Total integral das duas faturas: R$ 8.755,58.** São obrigações integrais dos cartões; o total pessoal usa as participações aplicáveis. ' + ('No extrato recebido, a Visa de R$ 653,42 foi debitada em 01/10, fora da janela contábil de setembro; Mastercard do ciclo outubro ainda não consta como paga. Os débitos de faturas dentro de setembro pertencem ao ciclo anterior e foram excluídos das despesas para não duplicar as compras.' if bank else 'Não há comprovação de pagamento destas faturas nos documentos recebidos.') + '\n\n'
    text += '## Continuidade das parcelas\n\n' + mensal.table(['Cartão', 'Compra', 'Ciclo anterior', 'Esperada agora', 'ID atual', 'Valor atual R$'], continuation)
    text += '\n\nAs parcelas Itaú Shop 14/15 e 15/15 também foram efetivamente cobradas, além da 07/15. Não são duplicatas. Luiz não reconheceu a origem do desconto DESC ANTECIPA PARCELAS de R$ 31,48: crédito preservado em Outros, sem vínculo presumido nem repetição da pergunta. Magali segue integral para Luiz; a indicação 03/14 de Samsung vem do PDF, sem reaproveitar o rótulo manual 02/13 usado no quadro de agosto.\n\n'
    text += '## Projeções impressas no PDF — fora do gasto atual\n\n' + mensal.table(
        ['Fonte', 'Soma das parcelas listadas R$', 'Próxima fatura informada R$', 'Diferença R$', 'Demais faturas R$', 'Total futuro R$'],
        [[r['fonte_id']] + [mensal.br(D(r[k])) for k in ['soma_parcelas_listadas', 'proxima_fatura_informada', 'diferenca_projecao', 'demais_faturas_informadas', 'total_futuro_informado']] for r in controls])
    text += '\n\nNa Mastercard, as 14 parcelas listadas na página 4 somam R$ 1.841,21, enquanto o total impresso para a próxima fatura é R$ 2.126,67. Diferença de R$ 285,46, igual ao valor de uma parcela Itaú Shop, mas sem linha correspondente no quadro de futuras. Não foi criada parcela para ajustar essa projeção. Conferir na próxima fatura/aplicativo; a fatura atual fecha integralmente.\n\n'
    for brand, rows in future_data['fontes'].items():
        text += '### ' + brand + '\n\n' + mensal.table(['Data original', 'Compra', 'Parcela futura', 'Valor R$', 'Página'],
            [[r['data'], r['descricao'], r['parcela'], mensal.br(D(r['valor_original'])), r['pagina']] for r in rows]) + '\n\n'
    mensal.write(out / 'detalhes/CONFERENCIA_CARTOES.md', text)

    # Quadro parcial para conferência; os 50% de manutenção abaixo são comparação
    # da continuidade das mesmas compras do quadro de agosto, sem afirmar dívida.
    family = [r for r in records if r['linha'] == '56']
    maintenance = [r for r in records if norm(r['descricao']) in ['MP*ASSTECNICAELE', 'SAMSUNGNOITAU']]
    gross = sum((D(r['valor_original']) for r in family), D(0))
    paloma_rows = [{'item': 'Cartões de Paloma (3878 / 6553)', 'forma': 'Cartão', 'parcela': 'Fatura atual',
                    'valor_integral': str(gross), 'participacao_exata': str(gross / 2),
                    'ids': [r['id'] for r in family], 'criterio': 'Metade confirmada do cartão familiar; não é comprovação de saldo a receber.'}]
    for r in maintenance:
        paloma_rows.append({'item': 'Manutenção lava e seca antiga' if 'ASSTEC' in norm(r['descricao']) else 'Lava e seca nova',
                           'forma': 'Cartão', 'parcela': r['parcela'], 'valor_integral': r['valor_original'],
                           'participacao_exata': str(D(r['valor_original']) / 2), 'ids': [r['id']],
                           'criterio': 'Comparação provisória: continuidade da mesma compra que constava a 50% no quadro validado de agosto. Recebimento e acerto atual não confirmados.'})
    if bank:
        cleaning = [r for r in records if r['fonte_id'] == bank['id'] and r['linha'] == '28']
        amount = sum((-D(r['valor_original']) for r in cleaning), D(0))
        if cleaning:
            paloma_rows.insert(0, {'item': 'Faxina semanal — comparação', 'forma': 'PIX', 'parcela': '4 pagamentos de R$ 220,00',
                                  'valor_integral': str(amount), 'participacao_exata': str(amount / 2), 'ids': [r['id'] for r in cleaning],
                                  'criterio': 'Comparação de 50% pelo quadro anterior; rateio/acerto de setembro não confirmado. Não abater novamente no resumo pessoal.'})
    total_gross = sum((D(r['valor_integral']) for r in paloma_rows), D(0))
    total_share = sum((D(r['participacao_exata']) for r in paloma_rows), D(0))
    snacks = sum((D(r['total']) for r in result['linhas'] if r['linha'] in ['53', '54', '55']), D(0))
    mensal.write(PERIOD / 'auditoria/dados/resumo_paloma.json', {
        'mes_referencia': '2026-09', 'status': 'comparacao_parcial_nao_confirmada', 'itens': paloma_rows,
        'total_integral': str(total_gross), 'total_participacao_exata': str(total_share),
        'total_rateado_arredondado': str(mensal.cents(total_share)), 'snacks_restaurantes_informativo': str(snacks),
        'exclusoes': ['Gestão Magali no cartão: parcela e crédito integralmente de Luiz.', 'WALTER e babá atual via Magali: já reembolsados por Paloma, sem nova cobrança; crédito de R$ 2.467,00 é acerto de agosto.' if bank else 'Movimentos bancários: extrato ausente.']})
    text = '# Paloma — setembro/2026\n\n**Comparação parcial para conferência; acerto do mês ainda não confirmado.**\n\n'
    text += mensal.table(['Gastos totais', 'Forma', 'Condição / parcela', 'Valor total R$', 'Valor rateado R$'],
        [[r['item'], r['forma'], r['parcela'], mensal.br(D(r['valor_integral'])), mensal.br(D(r['participacao_exata']))] for r in paloma_rows]
        + [['**Total da comparação**', '', '', '**' + mensal.br(total_gross) + '**', '**' + mensal.br(total_share) + '**']])
    text += '\n\nCartões de Paloma: divisão de 50% confirmada. ' + ('Faxina e manutenção: comparação de 50%, sujeita ao acerto atual. WALTER e babá atual já reembolsados, fora do total acima. Acerto de agosto separado.' if bank else 'Manutenção: comparação de 50% das mesmas compras do quadro anterior, sujeita à conferência do acerto atual. Movimentos bancários ainda fora deste quadro.') + ' Não representa saldo devido.\n\n'
    if sum((mensal.cents(D(r['participacao_exata'])) for r in paloma_rows), D(0)) != mensal.cents(total_share):
        text += '*Total calculado pelas metades exatas; pode diferir da soma das linhas exibidas por arredondamento.*\n\n'
    text += '## Snacks e restaurantes — informativo\n\n' + mensal.table(['Mês', 'Valor gasto R$'], [['set/2026 — parcial', mensal.br(snacks)]])
    text += '\n\nIfood + snacks + Padaria + Mercadão + feira + Bebida + rest. AABB + Restaurantes (54+55+53). Informativo fora do total rateado; classificações pendentes podem alterar o valor.\n\n[Detalhes de conferência](detalhes/CONFERENCIA_PALOMA.md).\n'
    mensal.write(out / 'RESUMO_PALOMA.md', text)
    details = '# Critérios do quadro parcial de Paloma — setembro/2026\n\n'
    details += '- Cartões de Paloma 3878 e 6553: única metade do total conjunto de R$ 4.250,57, conforme confirmação de Luiz em 09/10/2026. A mesma participação já aparece no resumo pessoal. Não somar novamente.\n'
    details += '- Manutenção antiga (03/08, R$ 137,50) e Samsung (03/14, R$ 300,04): projeção comparativa de 50%, pela continuidade das mesmas compras do quadro de agosto. As despesas permanecem integrais na linha 27 do quadro pessoal, conforme os registros dos cartões; nenhum crédito ou abatimento novo foi presumido. Confirmar o acerto do período antes de tratar os valores como saldo de Paloma.\n'
    details += '- Gestão Magali (02/04) e crédito de R$ 0,06 ficam integralmente com Luiz, conforme a decisão vigente para essa compra.\n'
    details += '- AABB SP, R$ 50,00, cartão 6553: divisão de 50% confirmada. R$ 25,00 pessoais na linha 56, independentemente da categoria do estabelecimento; sem segunda inclusão em AABB.\n'
    if bank:
        details += '- Extrato recebido e conciliado. Quatro PIX de R$ 220,00 para faxina: R$ 880,00 integrais; comparação de 50% = R$ 440,00, conforme formato do quadro anterior, sem confirmação do acerto atual. O resumo pessoal mantém R$ 880,00 até eventual confirmação de recebimento/participação.\n'
        details += '- WALTER 02/02 de R$ 1.750,00: reembolso integral confirmado, pessoal zero. Babá atual via Magali R$ 3.237,09: crédito de R$ 1.619,00 confirmado, pessoal líquido R$ 1.618,09. Nenhuma nova cobrança desses valores a Paloma.\n'
        details += '- Crédito de R$ 2.467,00 confirmado como acerto de agosto (quadro R$ 2.466,97); não abater em setembro. AABB de R$ 651,00 compensada pelo clube; complemento R$ 2,00 no orçamento.\n'
        details += '- Ver [conferência de créditos](CONFERENCIA_REEMBOLSOS_BABAS.md). Luiz informou que Bruna não tem eSocial e não houve aporte à provisão neste mês; perguntas resolvidas.\n'
    else:
        details += '- Sem extrato bancário não há prova de PIX, reembolsos ou acerto. WALTER, provisão de Bruna, faxinas e eSocial não foram repetidos a partir de agosto.\n'
    mensal.write(out / 'detalhes/CONFERENCIA_PALOMA.md', details)

    control_path = PERIOD / 'auditoria/dados/conferencia_mensal.json'
    control = read(control_path)
    control.update(status=cfg['status'], fontes_ausentes=cfg['fontes_ausentes'], conciliacao_bancaria_realizada=bool(bank),
                   diferenca_fontes_recebidas='0.00', projecoes_futuras=controls)
    mensal.write(control_path, control)
    print('Relatórios complementados: escopo parcial, cartões, parcelas e comparação de Paloma.')


if __name__ == '__main__':
    main()

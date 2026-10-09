"""Normalização conferida visualmente do recibo de setembro/2026."""
from pathlib import Path
from decimal import Decimal as D
import hashlib, json, shutil
import pdfplumber

periodo = Path(__file__).resolve().parents[1]
projeto = periodo.parents[1]
nome = 'Payslip_Recibo_para_30_de_set_de_2026.pdf'
origem = projeto / '2026-09-ref_ago' / nome
destino = periodo / 'entradas' / nome
digest = hashlib.sha256(origem.read_bytes()).hexdigest()
if destino.exists():
    assert hashlib.sha256(destino.read_bytes()).hexdigest() == digest
else:
    shutil.copy2(origem, destino)
with pdfplumber.open(destino) as pdf:
    texto = '\n'.join(p.extract_text() or '' for p in pdf.pages)
extracao = periodo / 'auditoria/extracao/holerite.txt'
extracao.parent.mkdir(parents=True, exist_ok=True)
extracao.write_text(texto, encoding='utf-8')
rubricas = [
    ('1000', 'Salário', 'provento', '15921.97', 'O3'),
    ('315A', 'Reemb. APAE/APDEX', 'provento', '900.00', 'O4'),
    ('/314', 'Contr. INSS Remuneração', 'desconto', '988.07', 'O12'),
    ('/401', 'Tributo IRRF', 'desconto', '2013.87', 'O13'),
    ('/B02', 'Adiantamento pago', 'adiantamento', '6368.79', None),
    ('71B0', 'Plano bradesco dental', 'desconto', '58.90', 'O16'),
    ('72B0', 'Copart bradesco dental', 'desconto', '20.08', 'O17'),
    ('MG11', 'Pagamento Pensão Reg.', 'desconto', '4306.25', 'O14'),
]
def br(v):
    return f'{D(v):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
for codigo, descricao, tipo, valor, celula in rubricas:
    assert codigo in texto and br(valor) in texto, (codigo, valor)
proventos = sum((D(r[3]) for r in rubricas if r[2] == 'provento'), D(0))
efetivos = sum((D(r[3]) for r in rubricas if r[2] == 'desconto'), D(0))
adiantamento = D('6368.79')
assert proventos == D('16821.97')
assert efetivos + adiantamento == D('13755.96')
assert proventos - efetivos - adiantamento == D('3066.01')
assert proventos - efetivos == D('9434.80')
extrato = json.loads((periodo/'auditoria/dados/extrato_normalizado.json').read_text(encoding='utf-8'))
por_id = {r['id']: r for r in extrato['lancamentos']}
assert D(por_id['EXT-016']['valor_original']) == adiantamento
assert D(por_id['EXT-002']['valor_original']) == D('3066.01')
manifesto_path = periodo / 'periodo.json'
manifesto = json.loads(manifesto_path.read_text(encoding='utf-8'))
relative = 'entradas/' + nome
manifesto['arquivos'] = [r for r in manifesto['arquivos'] if r['arquivo'] != relative]
complementares = manifesto.setdefault('documentos_complementares', [])
if not any(r['arquivo'] == relative for r in complementares):
    complementares.append({'tipo':'holerite', 'arquivo': relative, 'sha256': digest, 'dados':'auditoria/dados/holerite.json'})
manifesto_path.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
dados = {
    'mes_referencia': '2026-09', 'data_pagamento': '2026-09-30',
    'fonte': {'arquivo': relative, 'sha256': digest, 'pagina': 1},
    'rubricas': [dict(codigo=c, descricao=n, tipo=t, valor=v, celula_excel=e, pagina=1) for c,n,t,v,e in rubricas],
    'totais': {'proventos':'16821.97','descontos_recibo':'13755.96','descontos_efetivos':'7387.17',
               'adiantamento':'6368.79','liquido_pagamento':'3066.01','liquido_mensal':'9434.80'},
    'informativos': {'base_ir':'10627.65','base_inss':'15921.97','base_fgts':'15921.97','fgts_mes':'1273.75'},
    'conferencia_extrato': {'ids':['EXT-016','EXT-002'],'soma':'9434.80','diferenca':'0.00'},
    'beneficios_fora_holerite': {'alelo': '1010.82', 'componentes': ['910.82','100.00'], 'fonte':'Confirmação de Luiz em 09/10/2026', 'celula_excel':'O5'},
    'auxilio_creche': {'valor_esperado':'720.00','status':'recebimento_nao_identificado','fontes_verificadas':['holerite','extrato_itau_setembro'],'incluir_receita':False,'acao':'Avisar Luiz e conferir solicitação/comprovante; não presumir vínculo dos créditos Avanade de 895.00 e 35.00.'},
    'confirmacao_auxilio_creche': {'data':'2026-10-09','solicitacao_setembro':'Luiz esqueceu de solicitar','intencao':'Solicitar em outubro/2026','recebimento_confirmado':False},
}
(periodo/'auditoria/dados/holerite.json').write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
linhas = '\n'.join(f'| {c} | {n} | {t} | {br(v)} | {e or "Não lançar novamente"} |' for c,n,t,v,e in rubricas)
relatorio = f'''# Holerite — setembro/2026

Competência **09/2026**, pagamento **30/09/2026**, Avanade do Brasil. Fonte: recibo original, página 1.

**Líquido mensal confirmado pela folha: R$ 9.434,80**, composto pelo adiantamento de R$ 6.368,79 e saldo de R$ 3.066,01. Benefícios fora do holerite são conferidos separadamente.

## Rubricas e destino na aba Gastos

| Código | Descrição | Tipo | Valor R$ | Célula de setembro |
| --- | --- | --- | --- | --- |
{linhas}

## Conferência

| Controle | Valor R$ |
| --- | --- |
| Total de proventos | 16.821,97 |
| Total de descontos do recibo, incluindo adiantamento | 13.755,96 |
| Líquido pago em 30/09 | 3.066,01 |
| Adiantamento já pago | 6.368,79 |
| Descontos efetivos do mês, sem adiantamento | 7.387,17 |
| Líquido mensal: proventos menos descontos efetivos | 9.434,80 |
| Extrato: EXT-016 em 15/09 + EXT-002 em 30/09 | 9.434,80 |
| Diferença | 0,00 |

As duas TEDs Santander–Itaú correspondem aos valores do recibo e ao padrão de portabilidade já confirmado. Não são receitas adicionais ao salário lançado. O adiantamento descontado no recibo final já foi recebido durante o mês: não inserir como nova despesa nem descontá-lo novamente do líquido mensal.

## Aplicação na planilha

- O3 recebe o salário **bruto** de R$ 15.921,97, pois a estrutura subtrai os descontos nas linhas 12–17. O rótulo legado “Salário Mensal - Líquido” não muda essa base de cálculo. Meses anteriores preservados.
- O4 recebe R$ 900,00 de APAE/APDEX, uma vez. O recibo não comprova auxílio-creche adicional.
- **Alerta: auxílio-creche de R$ 720,00 não identificado no holerite nem no extrato Itaú fornecido.** Conferir solicitação e eventual comprovante em outra conta. Não incluído na receita. Os créditos Avanade de R$ 895,00 e R$ 35,00 não têm vínculo confirmado com esse benefício. Luiz pediu esse aviso a cada mês sem recebimento identificado.
- Luiz confirmou em 09/10/2026 que esqueceu de solicitar o reembolso de setembro e pretende solicitá-lo em outubro. Acompanhar o recebimento posterior sem antecipá-lo como receita nem duplicar competências.
- O17 recebe a coparticipação **odontológica** de R$ 20,08, em linha própria; não confundir com coparticipação médica.
- VA/Alelo (O5) não consta no recibo: Luiz confirmou em 09/10/2026 R$ 910,82 + R$ 100,00 = **R$ 1.010,82**. Perguntar o valor efetivo a cada mês. A planilha soma esse benefício à folha líquida, totalizando **R$ 10.445,62**; distinguir benefício de dinheiro em conta.
- Proventos com Alelo: R$ 17.832,79; descontos efetivos: R$ 7.387,17; receitas após descontos com Alelo: R$ 10.445,62. Menos despesas apuradas de R$ 12.018,72: saldo orçamentário provisório **-R$ 1.573,10**, ainda sem condomínio. Não representa o saldo bancário.
- FGTS do mês (R$ 1.273,75), base FGTS/INSS (R$ 15.921,97) e base IR (R$ 10.627,65) são informativos. Não somar FGTS a dinheiro disponível.
- As despesas pessoais apuradas permanecem R$ 12.018,72; condomínio segue pendente. Os descontos da folha não são adicionados novamente ao relatório de despesas.

## Fonte

[Recibo original](../entradas/{nome}) — página 1. SHA-256: `{digest}`.
'''
(periodo/'resultados/HOLERITE.md').write_text(relatorio,encoding='utf-8')
print('Holerite validado: 16.821,97 - 7.387,17 = 9.434,80; saldo 3.066,01; manifesto e relatório atualizados.')

"""Registra somente os ajustes finais expressamente confirmados por Luiz."""
from pathlib import Path
from decimal import Decimal as D
import json

p=Path(__file__).resolve().parents[2]
def read(path): return path.read_text(encoding='utf-8')
def write(path,value): path.write_text(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert D('12018.72')+D('1127.81')+D('806.17')-D('2.00')==D('13950.70')
assert D('10445.62')-D('13950.70')==D('-3505.08')
manual={'status':'fechado_confirmado_usuario','data_confirmacao':'2026-10-09',
 'fonte':'Confirmação explícita de Luiz na conversa; condomínio conferido no arquivo local.',
 'mensagem':'atualizei agora, pode deixar que esta certo esses 2 itens',
 'ajustes_por_id':{'22':'1127.81','57':'806.17'},
 'total_original_documentos':'12018.72','subtotal_basicas':'7531.66','subtotal_estilo_vida':'6419.04',
 'total_blocos_planilha':'13950.70','receitas_apos_descontos_com_alelo':'10445.62','saldo_orcamentario':'-3505.08',
 'observacao':'AABB substitui os 2.00 pelo valor confirmado de 806.17, igual a agosto, sem somar o complemento novamente. Condomínio pago segundo Luiz, sem data bancária presumida. Ajustes orçamentários específicos de setembro; extrato e faturas originais preservados. Auxílio-creche 720.00 segue para acompanhamento em outubro, sem receita antecipada.',
 'conferencia_arquivo_local':{'O22':'1127.81','O57':'2.00','observacao':'Última leitura local ainda mostrava O57=2.00; Luiz confirmou atualização e pediu considerar os dois itens corretos. Fechamento baseado nessa confirmação; arquivo Excel não modificado pelo agente.'}}
write(p/'output/.auditoria/dados/fechamento_manual.json',manual)
config=json.loads(read(p/'periodo.json'));config['status']='fechado_confirmado_usuario';config['fechamento_manual']={'arquivo':'output/.auditoria/dados/fechamento_manual.json','data_confirmacao':'2026-10-09','preservar':True};write(p/'periodo.json',config)
path=p/'output/RESUMO_MENSAL.md';t=read(path)
t=t.replace('**Provisório — condomínio ainda não confirmado. Total pessoal: R$ 12.018,72.**','**Fechado conforme ajustes confirmados por Luiz em 09/10/2026. Total pessoal: R$ 13.950,70.**\n\nReceitas após descontos, incluindo Alelo: **R$ 10.445,62**. Saldo orçamentário: **-R$ 3.505,08**. Auxílio-creche de R$ 720,00 não recebido/solicitado em setembro; acompanhamento em outubro, sem receita antecipada. O fechamento incorpora os ajustes manuais abaixo e não altera os documentos bancários originais.')
t=t.replace('| 22 | Condomínio | Casa / Moradia | — |','| 22 | Condomínio | Casa / Moradia | 1.127,81 |').replace('| 57 | CLUBE AABB | Lazer / Viagens | 2,00 |','| 57 | CLUBE AABB | Lazer / Viagens | 806,17 |').replace('**6.403,85**','**7.531,66**').replace('**5.614,87**','**6.419,04**')
t=t.replace('| **TOTAL** | **12.018,72** |','| Subtotal dos documentos originais | 12.018,72 |\n| Ajuste manual: condomínio pago e confirmado | 1.127,81 |\n| Ajuste manual: AABB, substituição de 2,00 por 806,17 | 804,17 |\n| **TOTAL FINAL** | **13.950,70** |')
t=t.replace('- Condomínio, eSocial e provisão: condomínio segue sem lançamento identificado ou confirmação; Bruna não tem eSocial segundo Luiz, e não houve aporte à provisão neste mês. Não copiar valores de agosto.','- Condomínio: Luiz confirmou pagamento e valor de R$ 1.127,81, conferido na planilha, atribuído ao orçamento de setembro. Data efetiva de pagamento não informada; não criar débito no extrato de setembro. Bruna sem eSocial e sem provisão no mês, conforme confirmação anterior.')
t=t.replace('Despesa confirmada de setembro: complemento de R$ 2,00.','Apuração documental inicial: complemento de R$ 2,00. Na conferência final, Luiz corrigiu a linha AABB para R$ 806,17, igual a agosto; esse valor substitui R$ 2,00 no orçamento. Não inferir data, composição ou outro débito bancário.')
t=t.replace('## Detalhamento por item','## Detalhamento dos documentos originais por item\n\nOs valores abaixo preservam a extração original. Os ajustes finais de condomínio e AABB estão no quadro principal e em `output/.auditoria/dados/fechamento_manual.json`; não somar novamente este detalhamento ao fechamento.')
write(path,t)
path=p/'output/PENDENCIAS.md';t=read(path);t=t.replace('## Condomínio e confirmações bancárias','## Condomínio e AABB — resolvidos no fechamento manual');start=t.index('Extrato completo recebido e conciliado.');end=t.index('\n\n## Parcelas',start);t=t[:start]+'Extrato e cartões conciliados. Luiz confirmou condomínio pago de R$ 1.127,81 e AABB de R$ 806,17 no orçamento de setembro. Ajustes finais registrados sem alterar débitos originais nem inventar data de pagamento. Fechamento confirmado em 09/10/2026. Auxílio-creche segue como acompanhamento de recebimento, sem impedir o fechamento dos gastos.'+t[end:];write(path,t)
path=p/'output/HOLERITE.md';t=read(path).replace('saldo orçamentário provisório **-R$ 1.573,10**, ainda sem condomínio','saldo orçamentário anterior aos ajustes finais **-R$ 1.573,10**').replace('- As despesas pessoais apuradas permanecem R$ 12.018,72; condomínio segue pendente. Os descontos da folha não são adicionados novamente ao relatório de despesas.','- Fechamento manual confirmado em 09/10/2026: despesas pessoais de R$ 13.950,70, incluindo condomínio R$ 1.127,81 e AABB R$ 806,17. Receitas com Alelo de R$ 10.445,62 menos despesas: saldo orçamentário **-R$ 3.505,08**. Os descontos da folha não são adicionados novamente às despesas.');write(path,t)
print('Fechamento manual registrado: despesas 13950.70, receitas com Alelo 10445.62, saldo -3505.08. Excel e documentos originais preservados.')

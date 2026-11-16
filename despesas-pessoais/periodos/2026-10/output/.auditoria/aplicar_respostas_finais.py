from pathlib import Path
from decimal import Decimal as D
import json,importlib.util,re
P=Path(__file__).resolve().parents[2]; ROOT=P.parents[1]; OUT=P/'output'; DATA=OUT/'.auditoria/dados'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text((v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2))+'\n',encoding='utf-8')
def br(v):return f'{D(v):,.2f}'.replace(',','_').replace('.',',').replace('_','.')
config=read(P/'periodo.json');assert not config.get('fechamento_manual')
model=read(ROOT/'.core/modelos/planilha.json')
if not any(x['linha']=='novo-projetos-empresa' for x in model['linhas']):
    model['linhas'].append({'bloco':'Itens complementares (sem linha na imagem)','linha':'novo-projetos-empresa','item':'Projetos/Empresa','categoria':'Projetos/Empresa','linha_excel':None})
    model['observacoes'].append('Projetos/Empresa criada por Luiz em 16/11/2026 para ANG Studio. ID novo-projetos-empresa; posição Excel ainda não definida, sem deslocar linhas existentes.')
write(ROOT/'.core/modelos/planilha.json',model)
ledger=read(DATA/'lancamentos.json');decisions=read(DATA/'confirmacoes_usuario.json')
patches={
'EXT-015':{'linha':'64','grupo':'Viagem Rio','status':'confirmada_usuario','observacao':'Luiz confirmou: PIX R$ 72 para Paloma em 23/10 foi Uber da viagem Rio; integralmente de Luiz.'},
'EXT-021':{'linha':'66','status':'confirmada_usuario','observacao':'Luiz confirmou: PIX R$ 1 foi somente teste; manter em Outros.'},
'EXT-037':{'linha':'66','status':'confirmada_usuario','observacao':'Luiz não reconhece TANKO. Nova consulta completa a entries do site em 16/11, 147 registros, sem correspondência. Manter em Outros por decisão do usuário.'},
'EXT-040':{'linha':'66','status':'confirmada_usuario','observacao':'Luiz não reconhece PagSeguro. Nova consulta completa a entries do site em 16/11, 147 registros, sem correspondência. Manter em Outros por decisão do usuário.'},
'MASTERCARD-045':{'linha':'66','status':'confirmada_usuario','observacao':'Luiz não reconhece SAO JUDAS. Nova consulta completa a entries do site em 16/11, 147 registros, sem correspondência. Manter em Outros por decisão do usuário.'},
'MASTERCARD-046':{'linha':'53','status':'confirmada_usuario','observacao':'Luiz confirmou restaurante. Mantido integral; nenhum reembolso informado.'},
'MASTERCARD-053':{'linha':'53','status':'provisoria','observacao':'Luiz acha que foi restaurante no aniversário da mãe; classificado em Restaurantes conforme hipótese expressa. Não repetir pergunta sem nova evidência.'},
'MASTERCARD-127':{'linha':'novo-projetos-empresa','status':'confirmada_usuario','observacao':'Luiz confirmou gasto do ANG Studio e pediu nova categoria Projetos/Empresa. Valor cobrado R$ 26,50; não criar crédito/reembolso empresarial.'},
'EXT-019':{'status':'confirmada_usuario','observacao':'Auxílio-creche de R$ 720 da Avanade recebido em 20/10: competência outubro confirmada por Luiz em 16/11. Separado de APAE/APDEX.'}}
shared=['EXT-001','EXT-016','EXT-022','EXT-036','EXT-041','MASTERCARD-002','MASTERCARD-003']
for r in ledger['lancamentos']:
    if r['id'] in shared:
        patches[r['id']]={'valor_pessoal_exato':str(abs(D(r['valor_original']))/2),'status':'confirmada_usuario','rateio_status':'confirmado_50_porcento','recebimento_status':'nao_confirmado','observacao':'Luiz confirmou divisão de 50% com Paloma e inclusão no quadro para a aba da planilha. Participação pessoal calculada uma vez; recebimento não confirmado, sem crédito inventado.'}
    if r.get('grupo')=='Viagem Rio' and r.get('cartao')!='3878':
        patches.setdefault(r['id'],{}).update(rateio_status='confirmado_manter_integral')
        if r['id']!='EXT-015':patches[r['id']]['observacao']=r['observacao'].replace('Valor integral mantido; divisão/recebimento não confirmados.','Luiz confirmou que o gasto fica integralmente com ele, sem divisão com Paloma.')
    r.update(patches.get(r['id'],{}))
# Sonia: uma participação em loterias e uma entrada devolvida, sem renda nova.
sonia={
 'EXT-010':{'linha':None,'valor_pessoal_exato':'0.00','status':'confirmada_usuario','devolucao_vinculada':'EXT-011','observacao':'Luiz confirmou que devolveu um dos créditos de R$ 42 de Sonia. PIX de 29/10 é devolução, não gasto dos meninos. Pareamento ao crédito de 28/10 por sequência cronológica; datas individuais não especificadas pelo usuário.'},
 'EXT-011':{'status':'confirmada_usuario','tipo_recebimento':'devolvido','devolucao_vinculada':'EXT-010','observacao':'Um dos dois créditos de Sonia foi devolvido. Pareamento cronológico 28/10 → saída 29/10; não abater loterias nem outra despesa.'},
 'EXT-012':{'status':'confirmada_usuario','tipo_recebimento':'reembolso','credito_vinculado':'MASTERCARD-060','observacao':'Luiz confirmou R$ 42 de participação de Sonia nas loterias pagas por ele. Vinculado à única compra de loterias do período, R$ 90 em 27/10; distribuição entre os dois créditos iguais por sequência cronológica.'},
 'MASTERCARD-060':{'valor_pessoal_exato':'48.00','status':'confirmada_usuario','credito_vinculado':'EXT-012','observacao':'Loterias R$ 90 menos participação de Sonia R$ 42 recebida no Itaú = R$ 48 pessoais. Crédito aplicado uma vez; o segundo crédito foi devolvido e não reduz esta compra.'}}
for r in ledger['lancamentos']:r.update(sonia.get(r['id'],{}))
patches.update(sonia)
assert D('90.00')-D('42.00')==D('48.00')
assert D('42.00')+D('-42.00')==0
write(DATA/'conferencia_sonia.json',{'confirmacao':'Luiz, 16/11/2026','creditos':['EXT-011','EXT-012'],'reembolso_loterias':'42.00','despesa_loterias':'MASTERCARD-060','loterias_original':'90.00','loterias_pessoal':'48.00','devolucao':'EXT-010','valor_devolvido':'42.00','criterio_pareamento':'Créditos iguais: 27/10 usado como reembolso e 28/10 como devolvido pela sequência; usuário confirmou finalidade do conjunto, não especificou qual data. Inversão não altera nenhum total.','conferencia':'Crédito reembolsado usado uma vez; crédito devolvido não aplicado a despesas. Conferência complementar ao CLI para vínculo cartão/extrato.'})
decisions['lancamentos'].update(patches)
decisions['auxilio_creche']['competencia']='2026-10'
decisions['reembolsos_tratamentos']={'status':'recebido_confirmado_usuario','conta':'Santander','escopo':'tratamentos do filho, item 13 da conferência de outubro','data_recebimento':None,'observacao':'Luiz confirmou reembolso em resposta ao item de R$ 6.875. Sem data ou comprovante Santander; não vincular automaticamente às transferências próprias Itaú e não tratar como renda nova.'}
decisions['revisao_final_aplicada']=True
write(DATA/'confirmacoes_usuario.json',decisions)
ledger['observacoes']=[x for x in ledger['observacoes'] if not x.startswith('Cartões: total')]
ledger['observacoes']=[x.replace('auxílio-creche de R$ 720 (competência não especificada)','auxílio-creche de R$ 720 (competência outubro confirmada)') for x in ledger['observacoes']]
ledger['observacoes'].append('Faxinas e parcelas de lava e seca divididas 50% por confirmação de Luiz; recebimento não confirmado. Viagem Rio integralmente de Luiz, incluindo PIX Uber R$ 72. Tratamentos reembolsados no Santander conforme declaração; não são renda nova. Categoria Projetos/Empresa criada para ANG Studio.')
write(DATA/'lancamentos.json',ledger)
h=read(DATA/'holerite.json');h['beneficios']['competencia_auxilio_creche']='2026-10';write(DATA/'holerite.json',h)
report=(OUT/'HOLERITE.md').read_text(encoding='utf-8')
report=report.replace('competência não especificada','competência outubro confirmada').replace('competência pendente','competência outubro confirmada')
report=report.replace('A confirmação da natureza do auxílio não esclarece se quita setembro ou outubro; o acompanhamento anterior fica com competência a conciliar.','Luiz confirmou competência outubro. O auxílio de setembro continua em acompanhamento separado, sem recebimento confirmado.')
write(OUT/'HOLERITE.md',report)
spec=importlib.util.spec_from_file_location('mensal',ROOT/'.core/scripts/mensal.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
result=mod.validate(P);mod.render(P,result)
pending=(OUT/'PENDENCIAS.md').read_text(encoding='utf-8')
pending+='''\n## Falta responder para concluir a conferência

Nenhuma pergunta de classificação ou rateio ainda sem resposta. Sonia confirmou por Luiz: R$ 42 para loterias e R$ 42 devolvidos em 29/10. Loterias pessoais R$ 48; devolução fora dos gastos dos meninos. O pareamento dos créditos iguais de 27/10 e 28/10 segue a sequência cronológica e não muda totais. Resta confirmar o total final para marcar o mês como fechado; a classificação de AV Robert Kennedy como restaurante permanece hipótese expressa já aceita por Luiz.

## Decisões já aplicadas — não repetir perguntas

Uber R$ 72 em Viagem Rio; PIX teste R$ 1 em Outros; TANKO R$ 50, PagSeguro R$ 57,59 e SAO JUDAS R$ 24 mantidos em Outros após consulta ao site sem correspondência; SantaFe em Restaurantes; AV Robert Kennedy R$ 24,80 em Restaurantes como hipótese de aniversário da mãe; TRIPO AI R$ 26,50 em Projetos/Empresa (ANG Studio). Viagem integral de Luiz. Faxina e lava e seca divididas 50% para quadro de Paloma, sem recebimento confirmado. Auxílio-creche de outubro confirmado. Tratamentos do filho reembolsados no Santander, sem vínculo inventado com PIX próprios.

Auxílio-creche de setembro continua acompanhamento separado, sem impedir fechamento de outubro. Recebimento do quadro de Paloma também não precisa ocorrer para confirmar a participação no orçamento.
'''
write(OUT/'PENDENCIAS.md',pending)
food=sum(D(x['total']) for x in result['linhas'] if x['linha'] in ['53','54','55'])
pal=(OUT/'RESUMO_PALOMA.md').read_text(encoding='utf-8')
pal=pal.replace('Faxina semanal — comparação','Faxina semanal').replace('Manutenção lava e seca antiga — comparação','Manutenção lava e seca antiga').replace('Lava e seca nova — comparação','Lava e seca nova').replace('Total da comparação','Total do quadro')
pal=pal.replace('Faxina e manutenção usam comparação de 50% como no quadro anterior, ainda sem confirmação do acerto; no orçamento pessoal permanecem integrais.','Faxina e manutenção: divisão de 50% confirmada por Luiz; orçamento pessoal já contém somente sua metade. Quadro para conferência/aba de Paloma, sem recebimento confirmado.')
pal=pal.replace('Eventual divisão da viagem ainda não entra no quadro.','Viagem Rio integralmente de Luiz, fora do rateio com Paloma.')
pal=pal.replace('PIX para Paloma de R$ 72 em 23/10 e R$ 1 em 16/10: finalidade não identificada.','PIX para Paloma de R$ 72: Uber Viagem Rio, integral de Luiz. PIX de R$ 1: teste, em Outros; ambos fora do rateio.')
pal=re.sub(r'\| out/2026 — provisório \| [\d.,]+ \|',f'| out/2026 — provisório | {br(food)} |',pal)
pal=pal.replace('Reclassificação de gastos de viagem pode alterar o informativo.','Viagem Rio já separada conforme confirmação; restaurante do aniversário da mãe permanece hipótese explícita.')
write(OUT/'RESUMO_PALOMA.md',pal)
for name in ['CONFERENCIA_CARTOES.md','CONFERENCIA_DOCUMENTAL.md']:
    p=OUT/'detalhes'/name;s=p.read_text(encoding='utf-8')
    s=s.replace('R$ 13.942,11',f'R$ {br(result["total"])}').replace('R$ 14.700,38',f'R$ {br(result["total"])}').replace('Cartões pessoais: R$ 7.015,67. Extrato pessoal: R$ 7.684,71.','Cartões pessoais: R$ 6.754,90. Extrato pessoal: R$ 7.103,21.')
    s=s.replace('Cartões pessoais: R$ 6.796,90. Extrato pessoal: R$ 7.145,21.','Cartões pessoais: R$ 6.754,90. Extrato pessoal: R$ 7.103,21.')
    write(p,s)
config['status']='conferido_aguardando_confirmacao_fechamento';write(P/'periodo.json',config)
print('Total pessoal:',result['total'],'alimentação:',food,'Viagem Rio Luiz:',sum(D(r['valor_pessoal_exato']) for r in ledger['lancamentos'] if r.get('grupo')=='Viagem Rio' and r.get('cartao')!='3878'))

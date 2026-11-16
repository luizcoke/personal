"""Importação documental de outubro/2026; não é parser para outros layouts."""
from pathlib import Path
from decimal import Decimal as D
import json, hashlib, re, importlib.util
import pymupdf

P=Path(__file__).resolve().parents[2]
ROOT=P.parents[1]
OUT=P/'output'
DATA=OUT/'.auditoria/dados'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text((x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2))+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def br(v): return f'{D(v):,.2f}'.replace(',','_').replace('.',',').replace('_','.')
config=read(P/'periodo.json')
assert not config.get('fechamento_manual')
assert len(config.get('arquivos',[]))==1, 'Importação inicial já concluída; preservar cartões e usar os dados atuais/rotina de cartões.'
config.update(status='provisorio_documentos_incompletos',fontes_ausentes=['Mastercard ciclo 2026-11','Visa ciclo 2026-11'],observacao_referencia='Extrato contábil de outubro; ciclo novembro esperado pela convenção do fechamento anterior. Faturas ciclo outubro recebidas são cópias exatas das já contabilizadas em setembro; não reimportadas.')
previous=read(ROOT/'periodos/2026-09/periodo.json')
duplicates=[]
for f in sorted((P/'input').glob('Fatura*.pdf')):
    match=next(a for a in previous['arquivos'] if a['sha256']==sha(f))
    duplicates.append({'arquivo':'input/'+f.name,'sha256':sha(f),'mes_ja_contabilizado':'2026-09','arquivo_anterior':match['arquivo'],'tratamento':'preservado em input; não importado como nova despesa'})
config['documentos_nao_importados']=duplicates
write(DATA/'duplicidades.json',duplicates)

# Ordem visual do PDF; a data contábil dos movimentos de fim de semana
# segue o bloco de saldo do dia útil, preservando também a data impressa.
raw='''30|1|-220.00|PIX ENVIADO PALOMA PAIXAO COKE|28
30|2|-2438.53|PIX ENVIADO MAGALI DA CONCEIÇÃO DE JESUS SILVA|31
30|2|3983.02|PIX RECEBIDO LUIZ COKE NETO|-
30|2|-1208.00|PIX ENVIADO PALOMA PAIXAO COKE|21
30|2|2965.24|TED RECEBIDA LUIZ COKE NETO|-
29|2|1219.26|PIX RECEBIDO PALOMA PAIXAO COKE|-
29|2|130.00|PIX RECEBIDO PALOMA PAIXAO COKE|-
29|2|-130.00|PIX QR ASSOCIACAO ATLETICA DO BANCO DO BRASIL - SAO PAULO|55
29|2|-270.00|PIX QR ASSOCIACAO ATLETICA DO BANCO DO BRASIL - SAO PAULO|66
29|2|-42.00|PIX ENVIADO SONIA PEIXE|29
28|2|42.00|PIX RECEBIDO SONIA PEIXE|-
27|2|42.00|PIX RECEBIDO SONIA PEIXE|-
26|2|-64.00|DA VIVO-SP 11280214|25
26|2|-80.00|PIX ENVIADO SONIA PEIXE|29
23|2|-72.00|PIX ENVIADO PALOMA PAIXAO COKE|66
23|2|-220.00|PIX ENVIADO PALOMA PAIXAO COKE|28
20|2|-419.50|DA ELETROPAULO 1372|24
20|2|3880.00|PIX RECEBIDO LUIZ COKE NETO|-
20|2|720.00|TED RECEBIDA AVANADE DO BRASIL LTDA|-
20|3|-653.00|BOLETO ASSOCIACAO ATLETICA BANCO DO BRASIL|57
16|3|-1.00|PIX ENVIADO PALOMA PAIXAO COKE|66
16|3|-220.00|PIX ENVIADO PALOMA PAIXAO COKE|28
16|3|9307.80|TED RECEBIDA LUIZ COKE NETO|-
15|3|-519.25|JUROS LIMITE DA CONTA|45
15|3|-8102.16|ITAU BLACK 3104-7969|-
15|3|-80.00|PIX ENVIADO SONIA PEIXE|29
15|3|-50.00|PIX ENVIADO LUIZ FELIPE CANTELLI COKE|29
15|3|5307.33|TED RECEBIDA LUIZ COKE NETO|-
15|3|-94.90|PIX AUTOMATICO CLARO|26
14|3|-418.87|DA PMSP 09525000000|23
13|3|-1127.81|BOLETO EDIFICIO NEW LAPA|22
12|3|-100.00|PIX ENVIADO LUIZ FELIPE CANTELLI COKE|29
09|3|2784.06|PIX RECEBIDO PALOMA PAIXAO COKE|-
09|3|-1161.09|BOLETO EDIFICIO NEW LAPA|22
08|3|-1050.00|PIX ENVIADO LUIZ COKE NETO|-
08|3|-199.00|PIX ENVIADO SOS DIARISTAS|28
07|3|-50.00|PIX ENVIADO TANKO OURO ADOYI|66
04|4|-2125.00|PIX ENVIADO NAOMI YONEDA - TERAPEUTA OCUPACIONAL E ACUPUNTURISTA LTDA|-
02|4|-45.24|IOF|45
02|4|-57.59|PIX QR PAGSEGURO INTERNATIONAL|66
02|4|-220.00|PIX ENVIADO PALOMA PAIXAO COKE|28
01|4|-653.42|PERS INFINIT 7609-0717|-
01|4|-3000.00|PIX ENVIADO SP SERVICOS DE PSICOLOGIA|-
01|4|-1750.00|PIX ENVIADO MARIO PINHEIRO|-'''
notes={2:'Categoria babá conhecida. Crédito EXT-006 de R$ 1.219,26 é candidato a reembolso; vínculo não confirmado. Integral provisório, sem segundo rateio.',
6:'Candidato a reembolso de EXT-002; sem abatimento até confirmação.',7:'Possível devolução de EXT-008; coincidência de data/valor não confirma vínculo.',
8:'Refeição AABB até R$ 250 pela regra; confirmar vínculo do crédito EXT-007 antes de abater.',9:'AABB acima de R$ 250: natureza não identificada. Separado da mensalidade de R$ 653.',
11:'Possível troco/estorno de gastos dos meninos; destino não confirmado.',12:'Possível troco/estorno de gastos dos meninos; destino não confirmado.',
15:'Finalidade do PIX de R$ 72 não identificada.',19:'Crédito Avanade de R$ 720 compatível com auxílio-creche; competência setembro/outubro pendente. Separado de APAE/APDEX.',
21:'Finalidade do PIX de R$ 1 não identificada.',31:'Possível pagamento do condomínio de setembro já incluído no fechamento manual. Mantido integral provisoriamente no recorte contábil até confirmar competência; pode reduzir outubro em R$ 1.127,81.',
33:'Candidato ao acerto do quadro de setembro de R$ 2.784,06; recebimento bancário comprovado, finalidade pendente.',
34:'Condomínio identificado; confirmar competência em conjunto com EXT-031.',37:'Beneficiário não identificado; finalidade pendente.',40:'PagSeguro genérico: finalidade pendente.'}
records=[]
for i,line in enumerate(raw.splitlines(),1):
    day,page,value,desc,cat=line.split('|'); original=D(value)
    accounting={'04':'05','12':'13'}.get(day,day)
    note='Regra vigente aplicada ao descritor.'
    status='regra_kb'
    if cat=='-':
        status='excluido_orcamento'
        if 'ITAU BLACK' in desc or 'PERS INFINIT' in desc: note='Pagamento de fatura já contabilizada no ciclo outubro/setembro; somente fluxo de caixa.'
        elif any(s in desc for s in ['SP SERVICOS','NAOMI','MARIO PINHEIRO']): note='Tratamento do filho excluído do orçamento pela regra vigente; reembolso no Santander não comprovado neste extrato.'
        elif i in [5,23,28]: note={5:'Líquido folha outubro: conciliado com recibo de 30/10.',23:'Férias e abono: conciliado com recibo de 16/10.',28:'Adiantamento salarial: conciliado com /B02 da folha de outubro.'}[i]
        elif 'LUIZ COKE NETO' in desc: note='Transferência entre contas próprias; não é renda adicional. Origem de eventual reembolso no Santander não inferida.'
        else: note='Entrada conservada no fluxo; não é despesa nem renda livre presumida.'
    if i in notes: note=notes[i]
    if i in [2,8,9,15,21,31,34,37,40]: status='provisoria'
    rec={'id':f'EXT-{i:03d}','fonte_id':'ITAU','data':f'2026-10-{accounting}','descricao':desc,'pagina':int(page),'valor_original':value,'valor_pessoal_exato':str(-original if cat!='-' else D('0.00')),'linha':cat if cat!='-' else None,'status':status,'observacao':note}
    if accounting!=day:
        rec['data_impressa']=f'2026-10-{day}'
        rec['observacao']+=' Data impressa de fim de semana/feriado; data contábil pelo bloco do saldo seguinte.'
    if i==2: rec['rateio_status']='aguardando_confirmacao'
    records.append(rec)
balances={'01':'-7488.24','02':'-7811.07','05':'-9936.07','07':'-9986.07','08':'-11235.07','09':'-9612.10','13':'-10839.91','14':'-11258.78','15':'-14797.76','16':'-5710.96','20':'-2183.46','23':'-2475.46','26':'-2619.46','27':'-2577.46','28':'-2535.46','29':'-1628.20','30':'1453.53'}
source={**config['arquivos'][0],'id':'ITAU','nome':'Itaú — extrato outubro','tipo':'extrato','saldo_inicial':'-2084.82','saldo_final':'1453.53','saldos_diarios':{'2026-10-'+k:v for k,v in balances.items()},'observacao_saldos':'PDF exibe saldos históricos sem sinal. Sinais negativos até 29/10 e positivo em 30/10 reconstruídos pelos movimentos e saldo final anterior -2084.82; todos os dias conciliados. Saldo da emissão em 16/11 (-11062.31) não é encerramento de outubro.'}
ledger={'versao':1,'mes_referencia':'2026-10','ciclo_faturas':'2026-11','fontes':[source],'lancamentos':records,'observacoes':[
'PROCESSAMENTO PARCIAL: faltam Mastercard e Visa ciclo novembro. Faturas enviadas ciclo outubro têm hashes idênticos às já contabilizadas em setembro e não foram duplicadas. Zero em categoria sem fonte não significa ausência de gasto.',
'Condomínio EXT-031 de R$ 1.127,81 pode pertencer a setembro já fechado; mantido provisoriamente até confirmação. Total ainda não representa fechamento de outubro.',
'Não foram abatidos créditos de Paloma ou Sonia sem vínculo confirmado. Tratamentos totalizam R$ 6.875,00 no fluxo, fora do orçamento conforme regra vigente.',
source['observacao_saldos'],
'Folha e férias em HOLERITE.md; VA/Alelo pendente e crédito de R$ 720 da Avanade com competência a confirmar. Planilha Excel não alterada nesta etapa.'
]}
write(DATA/'lancamentos.json',ledger)

# Rubricas por posição nas colunas, preservando a página de cada registro.
payroll=[]
for filename in ['2026_10_salario_37002605_20260930__M_70.pdf','2026-10_abono_ferias_37002605_20261016__M_72.pdf','2026-10_abono_ferias.pdf']:
    f=P/'input'/filename; doc=pymupdf.open(f); rub=[]
    for pi,page in enumerate(doc):
        words=page.get_text('words')
        codes=[w for w in words if re.fullmatch(r'(?:[A-Z0-9/]{4})',w[4]) and w[0]<80 and 275<w[1]<570]
        for code in sorted(codes,key=lambda w:w[1]):
            row=sorted([w for w in words if abs(w[1]-code[1])<2],key=lambda w:w[0])
            amount=[w for w in row if w[0]>350 and re.fullmatch(r'[\d.]+,\d{2}',w[4])]
            if not amount: continue
            a=amount[-1]; typ='desconto' if a[0]>450 else 'provento'
            description=' '.join(w[4] for w in row if 75<w[0]<260)
            rub.append({'codigo':code[4],'descricao':description,'tipo':typ,'valor':a[4].replace('.','').replace(',','.'),'pagina':pi+1})
    kind='referencia_setembro' if filename.startswith('2026_10') else ('ferias' if '37002605' in filename else 'folha_outubro')
    expected={'referencia_setembro':('16821.97','13755.96','3066.01'),'ferias':('10708.86','1401.06','9307.80'),'folha_outubro':('25194.11','22228.87','2965.24')}[kind]
    sums=[sum((D(r['valor']) for r in rub if r['tipo']==t),D(0)) for t in ['provento','desconto']]
    assert sums==[D(expected[0]),D(expected[1])],(filename,sums,rub)
    assert sums[0]-sums[1]==D(expected[2])
    payroll.append({'tipo':kind,'competencia':'2026-09' if kind=='referencia_setembro' else '2026-10','pagamento':{'referencia_setembro':'2026-09-30','ferias':'2026-10-16','folha_outubro':'2026-10-30'}[kind],'arquivo':'input/'+filename,'sha256':sha(f),'rubricas':rub,'totais':dict(zip(['proventos','descontos','liquido'],expected))})
config['documentos_complementares']=[{'tipo':p['tipo'],'arquivo':p['arquivo'],'sha256':p['sha256'],'dados':'output/.auditoria/dados/holerite.json'} for p in payroll]
write(P/'periodo.json',config)
net=D('2965.24')+D('5307.33')+D('9307.80')
gross=D('13268.31')+D('900')+D('10708.86')
effective=D('988.07')+D('1565.41')+D('58.90')+D('3600.30')+D('1084.12')
assert net==gross-effective==D('17580.37')
write(DATA/'holerite.json',{'versao':1,'mes_referencia':'2026-10','documentos':payroll,'conferencia':{'folha_liquido':'2965.24','adiantamento':'5307.33','ferias_liquido':'9307.80','liquido_total':'17580.37','bruto_sem_duplicidade':'24877.17','descontos_efetivos':'7296.80','diferenca':'0.00','vinculos_bancarios':{'folha':'EXT-005','adiantamento':'EXT-028','ferias':'EXT-023'}},'beneficios':{'APAE_APDEX_embutido':'900.00','VA_Alelo':None,'credito_Avanade':'720.00','credito_id':'EXT-019','natureza_provavel':'auxilio_creche','competencia_auxilio_creche':'pendente'},'bases_informativas':{'IR_folha':'8996.88','INSS_folha':'16837.93','FGTS_folha':'16837.93','FGTS_mes':'1347.02','IR_ferias':'4747.23'},'mapa_excel':{'aba':'Gastos','coluna':'P — outubro, confirmar rótulos antes de editar','status':'não atualizado; células de receitas/descontos a confirmar no arquivo quando solicitado','valores_conceituais':{'salario_25_dias':'13268.31','ferias_abono_tercos_medias':'10708.86','APAE_APDEX':'900.00','INSS_efetivo':'988.07','IRRF':'1565.41','pensao_total':'4684.42','plano_dental':'58.90','copart_dental':'0.00','copart_medica':'0.00'}},'observacoes':['Recibo nomeado salario 2026_10 é de setembro: somente referência, não receita de outubro.','Provisão INSS férias de 316.94 é devolvida na folha por M389; não somar a INSS efetivo.','Férias/abono são repetidos na folha e compensados por rubricas imp: contar uma vez.']})
parts=['# Holerites — outubro/2026','Conferência documental e bancária válida. VA/Alelo e competência do provável auxílio-creche pendentes.','## Pagamentos conciliados','| Componente | Data | Líquido R$ | Extrato |\n| --- | --- | --- | --- |\n| Adiantamento salarial | 15/10 | 5.307,33 | EXT-028 |\n| Férias e abono | 16/10 | 9.307,80 | EXT-023 |\n| Saldo da folha | 30/10 | 2.965,24 | EXT-005 |\n| **Total** | | **17.580,37** | |','Folha: R$ 25.194,11 − R$ 22.228,87 = R$ 2.965,24. Férias: R$ 10.708,86 − R$ 1.401,06 = R$ 9.307,80.','Folha líquida + adiantamento = R$ 8.272,57; com férias, R$ 17.580,37. Conferência independente: bruto sem repetição de R$ 24.877,17 − descontos efetivos de R$ 7.296,80 = R$ 17.580,37.','O bruto inclui salário de 25 dias (R$ 13.268,31), APAE/APDEX (R$ 900,00) e férias/abono/terços/médias (R$ 10.708,86). As rubricas de férias repetidas na folha são compensadas pelos descontos “imp”. A provisão de INSS de R$ 316,94 do recibo de férias é devolvida na folha; INSS efetivo consolidado: R$ 988,07. Pensão: R$ 3.600,30 + R$ 1.084,12 = R$ 4.684,42. IRRF: R$ 1.565,41. Dental: R$ 58,90.','FGTS de R$ 1.347,02 é informativo. Crédito separado de R$ 720,00 da Avanade em 20/10 é compatível com auxílio-creche; competência pendente. Total de créditos de folha/férias mais esse crédito: R$ 18.300,37, sem VA e sem incluir transferências próprias.','## Documentos e rubricas']
for p in payroll:
    parts += [f"### {p['tipo']} — competência {p['competencia']}",f"Fonte: [{Path(p['arquivo']).name}]({(P/p['arquivo']).as_posix()}); pagamento {p['pagamento']}.",'| Código | Rubrica | Tipo | Valor R$ | Página |\n| --- | --- | --- | --- | --- |\n'+'\n'.join(f"| {r['codigo']} | {r['descricao']} | {r['tipo']} | {br(r['valor'])} | {r['pagina']} |" for r in p['rubricas'])]
parts += ['## Mapa para futura atualização da planilha','Gastos, coluna de outubro: salário R$ 13.268,31; férias/abono R$ 10.708,86; APAE/APDEX R$ 900; INSS R$ 988,07; IR R$ 1.565,41; pensão R$ 4.684,42; dental R$ 58,90. Validar rótulos/células no arquivo antes da escrita. VA pendente; auxílio-creche com competência pendente. Não lançar adiantamento como nova receita ou despesa nem usar o holerite de setembro. Excel não alterado.']
write(OUT/'HOLERITE.md','\n\n'.join(parts))
print('Dados gravados:',len(records),'movimentos;',len(payroll),'recibos; líquido conciliado',net)

# Confirmações do usuário, incorporadas em 16/11/2026.
decisions={'data_confirmacao':'2026-11-16','origem':'respostas de Luiz nesta conversa','VA_alimentacao':'910.82','beneficios':'100.00','auxilio_creche':{'valor':'720.00','natureza':'confirmada_usuario','competencia':'não especificada'},'lancamentos':{
    'EXT-002':{'valor_pessoal_exato':'1219.27','status':'confirmada_usuario','rateio_status':'confirmado_reembolso','credito_vinculado':'EXT-006','observacao':'Luiz confirmou crédito de Paloma EXT-006 de R$ 1.219,26 como reembolso de Magali. Pessoal = 2.438,53 − 1.219,26 = 1.219,27; não dividir novamente.'},
    'EXT-006':{'status':'confirmada_usuario','credito_vinculado':'EXT-002','observacao':'Luiz confirmou reembolso da babá/Magali EXT-002; crédito utilizado uma única vez.'},
    'EXT-007':{'status':'confirmada_usuario','credito_vinculado':'EXT-008','tipo_recebimento':'estorno_do_proprio_debito','observacao':'Luiz confirmou devolução integral do PIX AABB de R$ 130, EXT-008. Não alocar a outra despesa.'},
    'EXT-009':{'status':'confirmada_usuario','linha':'64','rateio_status':'confirmado_manter_integral','observacao':'Luiz confirmou em 16/11/2026: ingresso para a festa de Réveillon na AABB. Categoria Lazer / Viagem confirmada; Luiz confirmou que os R$ 270 ficam integralmente com ele, sem divisão ou reembolso de Paloma.'},
    'EXT-008':{'status':'confirmada_usuario','linha':'64','valor_pessoal_exato':'0.00','credito_vinculado':'EXT-007','observacao':'Ingresso AABB de R$ 130, conforme Luiz; integralmente devolvido por Paloma, vínculo já confirmado. Efeito pessoal zero. Não é refeição.'},
    'EXT-019':{'status':'confirmada_usuario','observacao':'Luiz confirmou: crédito de R$ 720 da Avanade é auxílio-creche. Competência não especificada; não confundir com APAE/APDEX.'},
    'EXT-031':{'status':'excluido_competencia_anterior','linha':None,'valor_pessoal_exato':'0.00','observacao':'Luiz confirmou condomínio de setembro, já incluído no fechamento manual. Mantido no caixa de outubro, sem repetir no orçamento.'},
    'EXT-033':{'status':'confirmada_usuario','observacao':'Luiz confirmou acerto do quadro de setembro de R$ 2.784,06. Recebimento documentado; não abater de despesas de outubro nem alterar fechamento de setembro.'},
    'EXT-034':{'status':'confirmada_usuario','observacao':'Luiz confirmou condomínio de outubro: R$ 1.161,09.'}}}
write(DATA/'confirmacoes_usuario.json',decisions)
for r in records:
    r.update(decisions['lancamentos'].get(r['id'],{}))
ledger['observacoes'][1]='Condomínio de outubro confirmado em R$ 1.161,09. Pagamento de R$ 1.127,81 em 13/10 é de setembro já fechado: excluído do orçamento de outubro, preservado no caixa.'
ledger['observacoes'][2]='Reembolso Magali de R$ 1.219,26 e devolução AABB de R$ 130 confirmados e vinculados uma vez. Acerto de setembro de R$ 2.784,06 confirmado, sem abater outubro. Créditos Sonia permanecem sem vínculo. Tratamentos R$ 6.875,00 no fluxo, fora do orçamento pela regra vigente.'
ledger['observacoes'][4]='Folha e férias em HOLERITE.md. Luiz confirmou alimentação R$ 910,82 + benefícios R$ 100 e auxílio-creche de R$ 720 (competência não especificada). Excel não alterado nesta etapa.'
write(DATA/'lancamentos.json',ledger)
h=read(DATA/'holerite.json')
h['beneficios'].update(VA_Alelo='910.82',outros_beneficios='100.00',total_beneficios_cartao='1010.82',natureza_provavel='auxilio_creche_confirmado_usuario',confirmacao='Luiz, 16/11/2026; crédito de R$ 720 da Avanade é auxílio-creche.')
write(DATA/'holerite.json',h)
report=(OUT/'HOLERITE.md').read_text(encoding='utf-8')
report=report.replace('VA/Alelo e competência do provável auxílio-creche pendentes.','Alimentação R$ 910,82 + benefícios R$ 100,00 confirmados por Luiz em 16/11/2026. Auxílio-creche de R$ 720,00 confirmado; competência não especificada.')
report=report.replace('é compatível com auxílio-creche; competência pendente.','é auxílio-creche, confirmado por Luiz; competência não especificada.')
report=report.replace('VA pendente; auxílio-creche com competência pendente.','Alimentação R$ 910,82 + benefícios R$ 100,00 confirmados; auxílio-creche R$ 720,00 confirmado, competência não especificada.')
report+='\n## Benefícios confirmados\n\nAlimentação: R$ 910,82. Outros benefícios: R$ 100,00. Total no cartão de benefícios: R$ 1.010,82, separado dos depósitos bancários. Auxílio-creche: R$ 720,00, EXT-019. APAE/APDEX: R$ 900,00 já embutidos na folha. A confirmação da natureza do auxílio não esclarece se quita setembro ou outubro; o acompanhamento anterior fica com competência a conciliar.\n'
write(OUT/'HOLERITE.md',report)

# Conferência de Paloma: comparação parcial, não saldo devido.
write(OUT/'RESUMO_PALOMA.md','''# Paloma — outubro/2026

**Comparação parcial: faltam as faturas ciclo novembro. Não representa saldo devido.**

| Gastos totais | Forma | Condição / parcela | Valor total R$ | Valor rateado R$ |
| --- | --- | --- | --- | --- |
| Faxina semanal — comparação | PIX | 4 × R$ 220 para Paloma + R$ 199 SOS Diaristas | 1.079,00 | 539,50 |
| **Total da comparação disponível** | | | **1.079,00** | **539,50** |

A divisão de 50% da faxina acima é apenas comparação, como no quadro anterior; não é confirmação de reembolso. No resumo mensal permanece o débito integral até esclarecer o acerto. Cartões e parcelas de manutenção do ciclo novembro ainda não disponíveis, portanto não entram no total acima. Não somar novamente este quadro às despesas.

## Recebimentos confirmados, fora do acerto atual

- R$ 2.784,06 recebidos em 09/10: acerto do quadro de setembro, confirmado por Luiz. Sem novo abatimento de outubro.
- Magali: R$ 2.438,53 pagos em 30/10, com R$ 1.219,26 recebidos de Paloma em 29/10. Participação líquida de Luiz R$ 1.219,27, já incluída na linha 31; fora de nova cobrança.
- Réveillon AABB: R$ 270 em 29/10, integralmente de Luiz por confirmação; em Lazer / Viagem, fora de qualquer acerto com Paloma.
- AABB: ingresso de R$ 130 em 29/10, integralmente devolvido por Paloma no mesmo dia. Pessoal zero, fora de nova cobrança.

## Pendências

PIX para Paloma de R$ 72 em 23/10 e R$ 1 em 16/10: finalidade não identificada. Não foi identificada provisão de 13º de Bruna; não presumir aporte ou cobrança.

## Snacks e restaurantes — informativo

| Mês | Valor gasto R$ |
| --- | --- |
| out/2026 — apenas extrato, incompleto | 0,00 |

Soma pessoal das linhas **54 + 55 + 53**, sem segundo rateio e fora do acerto. Nenhum valor líquido identificado nessas três linhas do extrato. Os ingressos AABB são Lazer / Viagem; o de R$ 130 foi integralmente devolvido. Faltam cartões; zero parcial não significa ausência de consumo no mês.
''')

spec=importlib.util.spec_from_file_location('mensal',ROOT/'.core/scripts/mensal.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
result=mod.validate(P);mod.render(P,result)
summary=(OUT/'RESUMO_MENSAL.md').read_text(encoding='utf-8')
summary=summary.replace('**Provisório — ver pendências. Total pessoal:', '**PARCIAL — faltam faturas ciclo novembro. Subtotal pessoal disponível:')
summary=summary.replace('Cada linha é o valor a transpor para o mês na planilha.','Valores parciais para conferência; aguardar as faturas antes de transpor o fechamento completo para a planilha.')
write(OUT/'RESUMO_MENSAL.md',summary)
pending=(OUT/'PENDENCIAS.md').read_text(encoding='utf-8')
pending+='''
## Documentos faltantes e confirmações adicionais

- Enviar Mastercard e Visa do ciclo novembro, pela convenção vigente do projeto. Os PDFs de outubro recebidos têm hashes idênticos aos já usados no fechamento de setembro e foram preservados sem reimportação.
- PIX Paloma R$ 72 em 23/10 e R$ 1 em 16/10: finalidade pendente.
- TANKO OURO ADOYI R$ 50 em 07/10; PagSeguro R$ 57,59 em 02/10: finalidade pendente.
- Sonia: créditos de R$ 42 em 27/10 e 28/10, ainda sem vínculo confirmado com saídas. Não abatidos por coincidência.
- Auxílio-creche R$ 720 de 20/10 confirmado como auxílio; competência setembro/outubro não especificada. Não repetir pergunta sobre natureza.
- Reembolsos de tratamentos no Santander: não comprovados pelo extrato Itaú. Transferências próprias de R$ 3.880 e R$ 3.983,02 não comprovam sua composição.
- Faxina: comparação de metade no quadro de Paloma, sem confirmação de acerto; orçamento mantém débitos integrais.

## Já confirmado por Luiz em 16/11/2026

VA alimentação R$ 910,82 + benefícios R$ 100; crédito Avanade R$ 720 como auxílio-creche; acerto de setembro R$ 2.784,06; reembolso Magali R$ 1.219,26; condomínio de setembro R$ 1.127,81 excluído de outubro; condomínio de outubro R$ 1.161,09; devolução do ingresso AABB R$ 130 e ingresso Réveillon AABB R$ 270 integralmente de Luiz, sem divisão. Não solicitar novamente essas confirmações.
'''
write(OUT/'PENDENCIAS.md',pending)
flow=sum((D(r['valor_original']) for r in records),D(0))
write(OUT/'detalhes/CONFERENCIA_DOCUMENTAL.md',f'''# Conferência documental — outubro/2026

44 movimentos bancários, 17 saldos diários conciliados. Saldo inicial **−R$ 2.084,82**, movimento líquido **R$ {br(flow)}**, saldo final **R$ 1.453,53**. Diferença zero.

O PDF omite sinais nos saldos históricos, inclusive visualmente. O saldo inicial foi confrontado com setembro e os sinais foram reconstruídos por cada movimento: negativos até 29/10, positivo em 30/10. Não houve ajuste fictício de transação. Datas impressas 04/10 (Naomi) e 12/10 (Luiz Felipe) conservadas; datas contábeis 05/10 e 13/10 pelos blocos de saldo. Saldo do cabeçalho/posição consolidada de −R$ 11.062,31 refere-se à emissão em 16/11, não ao fim de outubro. Lançamentos futuros de novembro/dezembro excluídos.

As duas faturas ciclo outubro são cópias exatas das fontes de setembro, confirmado por SHA-256. O recibo nomeado salário de outubro é competência 09/26, pagamento em 30/09; não entrou como renda de outubro. O PDF com nome abono_ferias e duas páginas contém a folha de outubro; pensão MG11 está na página 2. O outro recibo de férias contém o pagamento de 16/10. Todas as rubricas e totais foram somados com Decimal e conferidos com os créditos bancários.

Subtotal pessoal disponível após confirmações: **R$ {br(result['total'])}**, sem cartões novos. Não é fechamento final. Caixa de tratamentos R$ 6.875 excluído do orçamento conforme regra; faturas pagas R$ 8.755,58 e condomínio de setembro R$ 1.127,81 não foram novamente contados como despesa.

Auditoria: [lançamentos](../.auditoria/dados/lancamentos.json), [holerites](../.auditoria/dados/holerite.json), [confirmações](../.auditoria/dados/confirmacoes_usuario.json), [duplicidades](../.auditoria/dados/duplicidades.json). Originais preservados; Excel e fechamento de setembro não alterados.
''')
print('Validação e relatórios atualizados; subtotal pessoal',result['total'])

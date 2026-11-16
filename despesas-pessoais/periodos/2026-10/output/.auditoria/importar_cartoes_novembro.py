"""Importa somente as duas faturas recebidas para outubro/ciclo novembro."""
from pathlib import Path
from decimal import Decimal as D
from collections import defaultdict
import json,re,hashlib,importlib.util,unicodedata

P=Path(__file__).resolve().parents[2]; ROOT=P.parents[1]; OUT=P/'output'; DATA=OUT/'.auditoria/dados'; EX=OUT/'.auditoria/extracao'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text((v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2))+'\n',encoding='utf-8')
def money(s):return D(s.replace(' ','').replace('.','').replace(',','.'))
def br(x):return f'{D(x):,.2f}'.replace(',','_').replace('.',',').replace('_','.')
def norm(x):return re.sub(r'[^A-Z0-9]','',unicodedata.normalize('NFKD',x.upper()))
config=read(P/'periodo.json');assert not config.get('fechamento_manual')
assert not read(DATA/'confirmacoes_usuario.json').get('revisao_final_aplicada'), 'Classificações posteriores já aplicadas; preservar dados atuais e usar aplicar_respostas_finais.py.'
ledger=read(DATA/'lancamentos.json')
records=[r for r in ledger['lancamentos'] if r['fonte_id']=='ITAU']
sources=[s for s in ledger['fontes'] if s['id']=='ITAU']
bank_pending=re.split(r'## (?:Documentos faltantes e confirmações adicionais|Confirmações e pendências bancárias preservadas)',(OUT/'PENDENCIAS.md').read_text(encoding='utf-8'))[-1]
bank_pending=bank_pending.split('## Cartões —')[0]
bank_pending='\n'.join(x for x in bank_pending.splitlines() if not x.startswith('- Enviar Mastercard'))

def classify(desc,value,card):
    n=norm(desc)
    if card=='3878':return '56','regra_kb','Cartão de Paloma: uma única metade, incluindo estornos; sem inferir recebimento.'
    rules=[('ITAUSHOP','51'),('ASSTECNICAELE','27'),('SAMSUNGNOITAU','27'),('JIMCOMMAGALI','31'),('HAVANOSASCO','51'),('PANIFICADORA','54'),('AGUANABOCADOCEIRA','54'),('TAGITAU','52'),('BARBEARIA','50'),('BBHOTELS','64'),('BONDINHO','64'),('99FOOD','54'),('IFD','54'),('KEETABR','54'),('BACIODILATTE','54'),('CAASP','41'),('ECOPARQUE','64'),('SY MPLA'.replace(' ',''),'64'),('UBER','52'),('99','52'),('ZUL','52'),('ESTACION','52'),('AMAZONMKTPLC','51'),('MERCADOLIVRE','51'),('APPLECOM','62'),('NETFLIX','63'),('SPOTIFY','61'),('AMAZONPRIMEALUGUEL','64'),('LOTERIAS','65'),('OPENAICHATGPT','novo-openai')]
    if 'ASSOCIACAOATL' in n and abs(value)<=250:return '55','regra_kb','Refeição AABB até R$ 250 conforme regra vigente; parcela literal preservada.'
    for token,line in rules:
        if token in n:
            note='Classificação pelo descritor e regra vigente; valor integral de Luiz.'
            if token=='JIMCOMMAGALI':note='Parcela 03/04 da gestão Bruna/Magali; parte de Paloma já paga, integral de Luiz conforme regra da mesma compra.'
            if token=='OPENAICHATGPT':note='Compra de créditos ChatGPT, não presumida assinatura recorrente. Rubrica OpenAI; IOF real separado.'
            if token=='HAVANOSASCO':note='Parcela final e ajuste da compra para casa já confirmada no ciclo anterior.'
            return line,'regra_kb',note
    inferred=[('FAZENDAREBOUCASREST','53'),('LIMARESTAURANTE','53'),('VIENASHOP','53'),('SANTAFECERVEJARIA','53'),('NEWLIFELANCHES','54'),('CABANALANCHES','54'),('ANGUDOGOMES','53'),('HORTIFRU','39'),('REPUBLICADAFRUTA','54'),('ZONASULDELIV','39'),('BRITUSPARK','52'),('LINKCOMTRIPOAI','58')]
    for token,line in inferred:
        if token in n:return line,'provisoria','Categoria sugerida pelo descritor/contexto; confirmar finalidade e, se aplicável, viagem/rateio.'
    if 'ESTRADAITAPECERICA' in n:return '66','nao_identificado','Descritor já não reconhecido na base. Mantido em Outros, sem repetir pergunta rotineira.'
    return '66','provisoria','Descritor novo: finalidade não confirmada, mantido integralmente em Outros até esclarecimento.'

for sid,suffix,total,due,subtotals in [
    ('MASTERCARD','110800','7658.44','2026-11-15',[('0539','nacional','4062.90'),('1929','nacional','353.68'),('3878','nacional','2974.38'),('1929','internacional','267.48')]),
    ('VISA','110711','844.42','2026-11-01',[('2587','nacional','844.42')])]:
    f=P/'input'/f'Fatura_Itau_20261116-{suffix}.pdf';h=hashlib.sha256(f.read_bytes()).hexdigest()
    src={'id':sid,'nome':sid.title(),'tipo':'cartao','arquivo':'input/'+f.name,'sha256':h,'total_integral':total,'vencimento':due,'subtotais':[{'cartao':c,'tipo':t,'valor':v} for c,t,v in subtotals]}
    if sid=='VISA':src['observacao']='Layout consolidado identifica titular Luiz e cartão principal 2587, sem discriminar finais virtuais por compra. Não atribuir a Paloma.'
    sources.append(src)
    config['arquivos']=[a for a in config['arquivos'] if a['arquivo']!=src['arquivo']]+[{'arquivo':src['arquivo'],'sha256':h}]
    card='2587' if sid=='VISA' else '0539';typ='nacional';counter=0
    sections=[(2,'L'),(2,'R')] if sid=='VISA' else [(2,'L'),(2,'R'),(3,'L'),(3,'R'),(4,'L')]
    for page,side in sections:
        active=sid=='MASTERCARD' or side=='R'
        for line in (EX/f'{suffix}-{page}-{side}.txt').read_text(encoding='utf-8').splitlines():
            if 'Lançamentos: compras' in line:active=True
            if 'Compras parceladas - próximas' in line:break
            title=re.search(r'^(?:\s*)(?:LUIZ COKE NETO|PALOMA PAIXAO COKE) \(final (\d{4})\)',line)
            if title:card=title[1]
            if 'Lançamentos internacionais' in line:typ='internacional'
            m=re.match(r'^\s*(\d\d/\d\d)\s+(.+?)\s+(-? ?[\d.]+,\d{2})\s*$',line)
            if not m or not active:continue
            date,desc,amount=m.groups();value=money(amount)
            if desc=='PAGAMENTO':continue
            parcel=re.search(r'(\d{2}/\d{2})\s*$',desc)
            parcela=parcel[1] if parcel else ''
            if parcel:desc=desc[:parcel.start()].strip()
            desc=re.sub(r'\s+',' ',desc)
            counter+=1;category,status,note=classify(desc,value,card)
            records.append({'id':f'{sid}-{counter:03d}','fonte_id':sid,'cartao':card,'data':date,'descricao':desc,'parcela':parcela,'tipo':typ,'pagina':page,'valor_original':str(value),'valor_pessoal_exato':str(value/2 if card=='3878' else value),'linha':category,'status':status,'observacao':note})
    if sid=='MASTERCARD':
        counter+=1
        records.append({'id':f'{sid}-{counter:03d}','fonte_id':sid,'cartao':'1929','data':'não informada','descricao':'Repasse de IOF das transações internacionais','parcela':'','tipo':'iof','pagina':4,'valor_original':'9.04','valor_pessoal_exato':'9.04','linha':'45','status':'regra_kb','observacao':'IOF efetivo agregado impresso na página 4, sem rateio estimado por compra. PDF não informa data individual do encargo.'})
    selected=[r for r in records if r['fonte_id']==sid]
    assert sum((D(r['valor_original']) for r in selected),D(0))==D(total),(sid,len(selected),sum(D(r['valor_original']) for r in selected))

# Classificações e observações já revisadas pelo usuário no site; nunca importar
# novos débitos SMS nem substituir valores/parcelas da fatura.
site=read(DATA/'site_classificacoes.json');matches=[]
mapping={'delivery':'54','snacks':'54','restaurants':'53','groceries':'39','home':'27','shopping':'51','transport':'52','travel':'64','leisure':'64','other':'66','health':'41'}
for r in records:
    if r['fonte_id']=='ITAU' or r['tipo']=='iof':continue
    n=norm(r['descricao']);value=D(r['valor_original']);candidates=[]
    for e in site['entries']:
        if e['status']!='active' or e['is_test']:continue
        date=e['purchase_date'][8:10]+'/'+e['purchase_date'][5:7]
        if date!=r['data']:continue
        if e['card_last4']!=r['cartao'] and not (r['fonte_id']=='VISA' and e['card_last4'] in ['2587','7396']):continue
        en=norm(e['merchant']);same=n==en or (min(len(n),len(en))>=8 and (n.startswith(en) or en.startswith(n))) or (n.startswith('99FOOD') and en.startswith('99FOOD'))
        if not same:continue
        amount=D(str(e['amount_cents']))/100
        compatible=amount==value
        if r['parcela'] and value>0:compatible=compatible or abs(value*int(r['parcela'].split('/')[1])-amount)<=D('.02')
        if compatible:candidates.append(e)
    if len(candidates)!=1:continue
    e=candidates[0];r['classificacao_site']={'id':e['id'],'categoria':e['category'],'observacao':e['note'],'atualizado_em':e['updated_at'],'valor_sms_centavos':e['amount_cents']}
    matches.append({'lancamento_id':r['id'],'site_id':e['id'],'categoria':e['category'],'observacao':e['note']})
    if not e['needs_review'] and e['category']!='unclassified':
        line=mapping.get(e['category'],r['linha'])
        if e['category']=='restaurants' and 'ASSOCIACAOATL' in n:line='55'
        if 'BARBEARIA' in n and 'cabeleireiro' in e['note'].lower():line='50'
        if 'LOTERIAS' in n:line='65'
        if r['cartao']=='3878':r['categoria_detalhe_site']=e['category']
        else:r['linha']=line
        r['status']='confirmada_usuario'
        r['observacao']+=' Classificação revisada no site: '+e['category']+'.'+(' Observação de Luiz: '+e['note']+'.' if e['note'] else '')+' Valores e parcela preservados conforme PDF.'
    elif e['note']:r['observacao']+=' Observação do site: '+e['note']+'.'

rio_ids=[f'MASTERCARD-{i:03d}' for i in range(27,40)]+['VISA-021']
for r in records:
    if r['id'] in rio_ids:
        r.update(linha='64',status='confirmada_usuario',grupo='Viagem Rio',observacao=r['observacao']+' Luiz confirmou em 16/11 agrupamento dos gastos da viagem de 23–25/10 em Viagem Rio. Valor integral mantido; divisão/recebimento não confirmados.')
    if r.get('cartao'):
        if r['cartao']=='3878' and r['data']=='25/10':r['grupo']='Viagem Rio';r['observacao']+=' Viagem Rio, mantendo uma única metade na linha 56.'
write(DATA/'conferencia_site.json',{'consultado_em':'2026-11-16','project_id':site['project_id'],'vinculos':matches,'viagem_rio_ids':rio_ids,'criterio':'Identidade/descritor + data + cartão compatível + valor ou total parcelado; correspondências ambíguas não aplicadas. SMS não entram como despesa adicional. Viagem por confirmação expressa de Luiz; assinaturas independentes de localização preservadas.'})
config.update(status='provisorio_classificacoes_pendentes',fontes_ausentes=[],observacao_referencia='Outubro pelo extrato contábil e faturas completas do ciclo novembro, recebidas em 16/11. Faturas antigas ciclo outubro preservadas como duplicatas já contabilizadas em setembro.')
ledger['fontes']=sources;ledger['lancamentos']=records
ledger['observacoes'][0]='Documentos completos: Itaú de outubro e faturas Visa/Mastercard ciclo novembro. Incluídas as faturas inteiras, inclusive compras do começo de novembro e parcelas atuais. Faturas antigas de outubro já contabilizadas em setembro não foram duplicadas.'
ledger['observacoes']=[s for s in ledger['observacoes'] if not s.startswith('Cartões: total')]
ledger['observacoes'].append('Cartões: total bruto R$ 8.502,86; cartão Paloma 3878 R$ 2.974,38, única metade de R$ 1.487,19 na linha 56. Sem final 6553 nesta fatura. Valores pessoais dos cartões R$ 7.015,67. Classificações novas e eventual rateio da viagem pendentes, sem inferir reembolso.')
write(P/'periodo.json',config);write(DATA/'lancamentos.json',ledger)
spec=importlib.util.spec_from_file_location('mensal',ROOT/'.core/scripts/mensal.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
result=mod.validate(P);mod.render(P,result)
food=sum((D(r['total']) for r in result['linhas'] if r['linha'] in ['54','55','53']),D(0))
paloma=(OUT/'RESUMO_PALOMA.md').read_text(encoding='utf-8')
start=paloma.index('## Recebimentos confirmados')
tail=paloma[start:].split('## Snacks e restaurantes')[0]
write(OUT/'RESUMO_PALOMA.md',f'''# Paloma — outubro/2026

**Conferência provisória; não representa saldo devido. Cartões ciclo novembro incluídos.**

| Gastos totais | Forma | Condição / parcela | Valor total R$ | Valor rateado R$ |
| --- | --- | --- | --- | --- |
| Faxina semanal — comparação | PIX | 4 × 220 + 199 SOS | 1.079,00 | 539,50 |
| Cartão de Paloma final 3878 | Cartão | Fatura ciclo novembro, líquido de estornos | 2.974,38 | 1.487,19 |
| Manutenção lava e seca antiga — comparação | Cartão | 04/08 | 137,50 | 68,75 |
| Lava e seca nova — comparação | Cartão | 04/14 | 300,04 | 150,02 |
| **Total da comparação** | | | **4.490,92** | **2.245,46** |

Metade do cartão de Paloma confirmada pela regra vigente; inclui todos os gastos e estornos, sem novo rateio. Faxina e manutenção usam comparação de 50% como no quadro anterior, ainda sem confirmação do acerto; no orçamento pessoal permanecem integrais. Gestão Magali 03/04 não é cobrada novamente: parte de Paloma já paga conforme regra. Eventual divisão da viagem ainda não entra no quadro. Não somar este total novamente às despesas.

{tail}
## Snacks e restaurantes — informativo

| Mês | Valor gasto R$ |
| --- | --- |
| out/2026 — provisório | {br(food)} |

Soma pessoal **54 + 55 + 53**, sem novo rateio, fora do acerto. Não inclui linha 56 novamente. Reclassificação de gastos de viagem pode alterar o informativo.
''')
pending=(OUT/'PENDENCIAS.md').read_text(encoding='utf-8')
write(OUT/'PENDENCIAS.md',pending+'\n## Confirmações e pendências bancárias preservadas\n'+bank_pending+'''\n## Cartões — pontos de revisão

- Viagem Rio: agrupamento em Lazer/Viagem confirmado por Luiz. Valores integrais no cartão de Luiz; eventual divisão/reembolso ainda não informado. Cartão de Paloma preserva única metade na linha 56. Assinaturas Apple/Netflix não foram tratadas como gasto da viagem só pela data.
- Site consultado: G3TecAssistencia classificado em Casa (parcela atual R$ 122,50; SMS R$ 245), URIEL GASPAR R$ 30 é Circo Isabela, restaurantes e outras observações incorporados. Não perguntar novamente esses itens.
- AV ROBERT KENNEDY R$ 6 em 11/10 está classificado como Outros no site; R$ 24,80 em 02/11 e SAO JUDAS R$ 24 em 29/10 não encontrados como registros correspondentes revisados. Não extrapolar observação de uma compra para outra.
- TRIPO AI R$ 26,50 em 02/11: provisoriamente Projetos Pessoais; confirmar finalidade. OPENAI R$ 231,94 corresponde a créditos, não assinatura mensal presumida; IOF agregado de R$ 9,04 separado.
''')
details=f'''# Conferência dos cartões — outubro / ciclo novembro

Visa: R$ 844,42, vencimento 01/11/2026. Mastercard: R$ 7.658,44, vencimento 15/11/2026. Totais e subtotais por cartão conciliados com diferença zero. {len(records)-44} registros de cartão, incluindo estornos e IOF real.

Mastercard nacional: Luiz 0539 R$ 4.062,90; Luiz 1929 R$ 353,68; Paloma 3878 R$ 2.974,38. Internacional 1929: R$ 258,44 + IOF R$ 9,04 = R$ 267,48. Visa consolidado identifica titular Luiz e principal 2587; o PDF não separa cartões virtuais, portanto não se inventou essa distinção.

Classificações e observações do site foram consultadas em 16/11; vínculos por lançamento em `.auditoria/dados/conferencia_site.json`. Viagem Rio foi agrupada por confirmação de Luiz, preservando assinatura sem relação com a viagem e regras de titularidade.

Cartões pessoais: R$ 7.015,67. Extrato pessoal: R$ 7.684,71. **Total provisório: R$ {br(result['total'])}.** Participação exata de Paloma: R$ 1.487,19; estornos preservados uma única vez. Nenhum pagamento de fatura foi contado novamente.

Parcelas atuais preservadas. Zara 05/05 e B Linda 02/02 encerram neste ciclo; gestão Magali 03/04 integral de Luiz. A previsão anterior de Mastercard R$ 2.126,67 tinha diferença de R$ 285,46 em relação à lista: a fatura atual cobra Itaú Shop 08/15 de R$ 285,46, sem parcela compensatória inventada. Novas compras e ajustes impedem equiparar previsão ao total atual.

Próximo ciclo: tabela Mastercard soma R$ 2.113,23, igual à próxima fatura impressa; demais R$ 6.036,18. Visa: próxima R$ 96,93, demais R$ 26,93. São previsões de parcelas, não despesas deste mês nem total final da próxima fatura.
'''
write(OUT/'detalhes/CONFERENCIA_CARTOES.md',details)
doc=(OUT/'detalhes/CONFERENCIA_DOCUMENTAL.md').read_text(encoding='utf-8')
doc=re.sub(r'Subtotal pessoal disponível após confirmações:.*?Não é fechamento final\.',f'Total pessoal provisório após inclusão dos cartões: **R$ {br(result["total"])}**. Não é fechamento confirmado.',doc,flags=re.S)
doc+='\nNovas faturas ciclo novembro recebidas em 16/11, extraídas e conciliadas. Ver [conferência dos cartões](CONFERENCIA_CARTOES.md).\n'
write(OUT/'detalhes/CONFERENCIA_DOCUMENTAL.md',doc)
print('VALIDADO',len(records),'registros; TOTAL',result['total'],'ALIMENTACAO',food)
print('Vínculos com site:',len(matches),'Viagem Rio Luiz:',sum(D(r['valor_pessoal_exato']) for r in records if r.get('grupo')=='Viagem Rio' and r.get('cartao')!='3878'))
for r in records:
    if r['fonte_id']!='ITAU' and r['status']=='provisoria':print(r['id'],r['descricao'],r['valor_original'],'linha',r['linha'])

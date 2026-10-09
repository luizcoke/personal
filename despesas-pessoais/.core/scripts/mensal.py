"""Prepare periods, validate normalized records and render the monthly Markdown.
PDF extraction and semantic classification are performed by the agent; this CLI does not guess them.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
from datetime import date
import argparse, calendar, hashlib, json, re, shutil, sys

ROOT=Path(__file__).resolve().parents[2]
D=Decimal
class ValidationError(ValueError):pass

def require(condition,message):
    if not condition:raise ValidationError(message)
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    text=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(text.rstrip()+'\n',encoding='utf-8')
    temporary.replace(path)
def decimal(value):
    require(isinstance(value,str) and re.fullmatch(r'-?\d+(?:\.\d+)?',value),f'Valor monetário deve ser string decimal: {value!r}')
    return D(value)
def cents(value):return value.quantize(D('.01'),rounding=ROUND_HALF_UP)
def br(value,places=2):
    value=cents(value) if places==2 else value
    if places!=2:places=max(places,-value.as_tuple().exponent)
    return f'{value:,.{places}f}'.replace(',','_').replace('.',',').replace('_','.')
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def month(value):
    require(bool(re.fullmatch(r'\d{4}-\d{2}',value)),'Mês deve ser AAAA-MM.')
    date.fromisoformat(value+'-01');return value
def period_path(value,root=ROOT):return Path(root)/'periodos'/month(value)
def local_file(period,relative):
    require(isinstance(relative,str) and not Path(relative).is_absolute(),'Referência deve ser relativa ao período.')
    path=(period/relative).resolve()
    require(path.is_relative_to(period.resolve()),'Referência fora da pasta do período.')
    return path

def prepare(root,reference,cycle,files=()):
    period=period_path(reference,root);month(cycle)
    config_path=period/'periodo.json'
    existing=read(config_path) if config_path.exists() else None
    if existing:require(existing['ciclo_faturas']==cycle,'O período já existe com outro ciclo; revisar sem sobrescrever.')
    incoming=[Path(f).resolve() for f in files]
    seen={f['sha256'] for f in existing.get('arquivos',[])} if existing else set()
    plan=[]
    for source in incoming:
        require(source.is_file() and source.suffix.lower()=='.pdf',f'Entrada deve ser PDF existente: {source}')
        require('_unlocked' not in source.stem.lower(),f'Usar PDF original: {source.name}')
        checksum=digest(source)
        if checksum in seen:continue
        target=period/'input'/source.name
        require(not target.exists() or digest(target)==checksum,f'Outro arquivo já usa o nome {source.name}.')
        require(not any(item[1].name==target.name for item in plan),f'Dois arquivos diferentes com o mesmo nome: {source.name}')
        seen.add(checksum);plan.append((source,target,checksum))
    for rel in ['input','output/detalhes','output/.auditoria/dados','output/.auditoria/extracao']:(period/rel).mkdir(parents=True,exist_ok=True)
    y,m=map(int,reference.split('-'))
    config=existing or {'versao':1,'mes_referencia':reference,'ciclo_faturas':cycle,'extrato_inicio':reference+'-01','extrato_fim':f'{reference}-{calendar.monthrange(y,m)[1]:02}','criterio_cartoes':'faturas_completas','arquivos':[]}
    for source,target,checksum in plan:
        if not target.exists():shutil.copy2(source,target)
        require(digest(target)==checksum,'Falha de integridade na cópia do PDF.')
        config['arquivos'].append({'arquivo':str(target.relative_to(period)).replace('\\','/'),'sha256':checksum})
    write(config_path,config)
    return period,len(plan)

def validate(period,model=None,ledger=None,check_files=True):
    period=Path(period);config=read(period/'periodo.json')
    model=model or read(ROOT/'.core/modelos/planilha.json')
    ledger=ledger or read(period/'output/.auditoria/dados/lancamentos.json')
    require(ledger.get('versao')==1,'Versão de lançamentos não suportada.')
    require(ledger['mes_referencia']==config['mes_referencia'],'Referência do período divergente.')
    require(ledger['ciclo_faturas']==config['ciclo_faturas'],'Ciclo das faturas divergente.')
    valid_lines={r['linha'] for r in model['linhas']}
    require(len(valid_lines)==len(model['linhas']),'Linhas duplicadas no modelo.')
    sources={f['id']:f for f in ledger['fontes']}
    records=ledger['lancamentos'];ids={r['id']:r for r in records}
    require(records and sources,'Faltam fontes ou lançamentos normalizados.')
    require(len(sources)==len(ledger['fontes']),'Fonte duplicada.')
    require(len(ids)==len(records),'ID de lançamento duplicado.')
    manifest={f['arquivo']:f['sha256'] for f in config['arquivos']}
    require(len(manifest)==len(config['arquivos']),'Arquivo duplicado no manifesto.')
    require(len(set(manifest.values()))==len(manifest),'Mesmo PDF registrado mais de uma vez.')
    require(set(manifest)=={f['arquivo'] for f in sources.values()},'Todo PDF importado precisa ter uma única fonte normalizada; fonte extra ou faltante.')
    require(len({f['arquivo'] for f in sources.values()})==len(sources),'PDF repetido em duas fontes.')
    for source in sources.values():
        require(source['tipo'] in ['cartao','extrato'],'Tipo de fonte desconhecido.')
        require(source['sha256']==manifest[source['arquivo']],'Hash da fonte diverge do manifesto.')
        if check_files:
            require(digest(local_file(period,source['arquivo']))==source['sha256'],'PDF original alterado ou fonte errada.')
    used_credits={}
    for r in records:
        require(r['fonte_id'] in sources,f'Fonte ausente em {r["id"]}.')
        source=sources[r['fonte_id']]
        original=decimal(r['valor_original']);personal=decimal(r['valor_pessoal_exato'])
        require(isinstance(r.get('pagina'),int) and r['pagina']>0,f'Página ausente em {r["id"]}.')
        require(bool(r.get('descricao')) and bool(r.get('status')),f'Descrição/status ausente em {r["id"]}.')
        require(r['linha'] is None or r['linha'] in valid_lines,f'Linha não cadastrada em {r["id"]}.')
        if r['linha'] is None:require(personal==0,f'Exclusão com valor pessoal em {r["id"]}.')
        if source['tipo']=='extrato':
            date.fromisoformat(r['data'])
            require(config['extrato_inicio']<=r['data']<=config['extrato_fim'],f'Movimento bancário fora do mês: {r["id"]}.')
            require(personal>=0 and personal<=max(-original,D(0)),f'Participação bancária inválida em {r["id"]}.')
        else:
            require(abs(personal)<=abs(original) and original*personal>=0,f'Participação do cartão inválida em {r["id"]}.')
            if r.get('cartao') in model.get('cartoes_paloma',['3878']):
                require(r['linha']=='56' and personal==original/D(2),'Cartão de Paloma deve ter uma única metade na linha 56.')
            elif r['linha']=='56':raise ValidationError('Linha 56 contém cartão não identificado como de Paloma.')
        if r.get('base_participacao')=='ja_parte_pessoal':
            require(personal==abs(original),'Participação já dividida foi rateada novamente.')
            require(not r.get('credito_vinculado') and not r.get('creditos_aplicados'),'Participação já paga não requer reembolso.')
        credit_id=r.get('credito_vinculado')
        if credit_id:require(credit_id in ids,'Referência a crédito inexistente.')
        if source['tipo']=='extrato' and original<0 and r['linha'] is not None:
            allocations=r.get('creditos_aplicados',[])
            require(not (credit_id and allocations),'Escolher vínculo integral ou alocações explícitas; não os dois.')
            if credit_id:allocations=[{'id':credit_id,'valor':ids[credit_id]['valor_original']}]
            if allocations:
                require(len({a['id'] for a in allocations})==len(allocations),'Crédito repetido na mesma despesa.')
                total_allocated=D(0)
                for allocation in allocations:
                    require(allocation['id'] in ids,'Crédito alocado inexistente.')
                    credit=ids[allocation['id']];amount=decimal(allocation['valor'])
                    require(credit['fonte_id']==r['fonte_id'] and decimal(credit['valor_original'])>0,'Vínculo não aponta para entrada da mesma conta.')
                    require(credit['linha'] is None and decimal(credit['valor_pessoal_exato'])==0,'Crédito vinculado também entra no orçamento.')
                    require(credit.get('tipo_recebimento')!='devolvido','PIX devolvido não pode quitar uma despesa.')
                    require(amount>0,'Alocação de crédito deve ser positiva.')
                    used=used_credits.setdefault(credit['id'],{'valor_utilizado':'0','despesas':[]})
                    accumulated=decimal(used['valor_utilizado'])+amount
                    require(accumulated<=decimal(credit['valor_original']),'Valor do mesmo crédito utilizado mais de uma vez.')
                    used['valor_utilizado']=str(accumulated);used['despesas'].append(r['id'])
                    total_allocated+=amount
                require(-original-personal==total_allocated,'Reembolso não confere com a participação líquida; possível segundo rateio.')
    controls=[]
    for source in sources.values():
        included=[r for r in records if r['fonte_id']==source['id']]
        require(bool(included),'Fonte sem movimentos; revisar a extração.')
        original_sum=sum((decimal(r['valor_original']) for r in included),D(0))
        if source['tipo']=='cartao':
            require(original_sum==decimal(source['total_integral']),f'Total da fatura não fecha: {source["id"]}.')
            expected={(s['cartao'],s['tipo']):decimal(s['valor']) for s in source['subtotais']}
            require(len(expected)==len(source['subtotais']),'Subtotal duplicado na fonte.')
            actual=defaultdict(Decimal)
            for r in included:actual[(r['cartao'],'internacional' if r['tipo'] in ['internacional','iof'] else 'nacional')]+=decimal(r['valor_original'])
            require(dict(actual)==expected,f'Subtotais por cartão não fecham: {source["id"]}.')
            controls.append({'fonte':source['nome'],'controle':'Total integral da fatura','valor':str(original_sum),'diferenca':'0.00'})
        else:
            require(decimal(source['saldo_inicial'])+original_sum==decimal(source['saldo_final']),f'Saldo bancário não fecha: {source["id"]}.')
            if source.get('saldos_diarios'):
                running=decimal(source['saldo_inicial'])
                dates=defaultdict(Decimal)
                for r in included:dates[r['data']]+=decimal(r['valor_original'])
                require(set(dates)<=set(source['saldos_diarios']),'Há dias de movimento sem saldo diário de controle.')
                for day in sorted(source['saldos_diarios']):
                    running+=dates[day]
                    require(running==decimal(source['saldos_diarios'][day]),f'Saldo diário divergente: {day}.')
            controls.append({'fonte':source['nome'],'controle':'Saldo final do extrato','valor':source['saldo_final'],'diferenca':'0.00'})
    grouped=defaultdict(lambda:defaultdict(Decimal))
    for r in records:
        if r['linha'] is not None:grouped[r['linha']][r['fonte_id']]+=decimal(r['valor_pessoal_exato'])
    rows=[]
    for item in model['linhas']:
        values={s:cents(grouped[item['linha']][s]) for s in sources}
        rows.append({**item,'valores':{s:str(v) for s,v in values.items()},'total':str(sum(values.values(),D(0))),'quantidade':sum(r['linha']==item['linha'] for r in records)})
    return {'config':config,'ledger':ledger,'linhas':rows,'fontes':sources,'controles':controls,'total':sum((D(r['total']) for r in rows),D(0)),'creditos_utilizados':used_credits}

def sheet_line(row):
    return row.get('linha_excel',row['linha']) or '—'

def table(headers,rows):
    rows=list(rows)
    if not rows:return 'Nenhum item.'
    def clean(value):return str(value).replace('|','/').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+['| '+' | '.join(clean(x) for x in row)+' |' for row in rows])

def render(period,result,output=None):
    period=Path(period);out=Path(output) if output else period/'output';out.mkdir(parents=True,exist_ok=True)
    data=result['ledger'];records=data['lancamentos'];sources=result['fontes'];rows=result['linhas'];config=result['config']
    uncertain=[r for r in records if r['status'] in ['pendente_extrato','provisoria'] or r.get('rateio_status')=='aguardando_confirmacao']
    status='Provisório — ver pendências' if uncertain else 'Consolidado'
    parts=[f'# {config["mes_referencia"]} — lançamentos para a planilha',f'**{status}. Total pessoal: R$ {br(result["total"])}.**',
           f'Extrato: {config["extrato_inicio"]} a {config["extrato_fim"]}, pela data contábil. Cartões: ciclo {config["ciclo_faturas"]}, {config["criterio_cartoes"].replace("_"," ")}.',
           'Cada linha é o valor a transpor para o mês na planilha. Os 50%/30% são metas dos blocos. `—` indica ausência de lançamento identificado. Não somar novamente relatórios individuais ou o quadro de Paloma.']
    for block in dict.fromkeys(r['bloco'] for r in rows):
        subset=[r for r in rows if r['bloco']==block]
        parts.extend(['## '+block,table(['Linha','Lançamento / item','Categoria','Valor R$'],[[sheet_line(r),r['item'],r['categoria'],(br(D(r['total'])) if r['quantidade'] else '—')+(' ⚠' if any(u['linha']==r['linha'] for u in uncertain) else '')] for r in subset]+[['','**Subtotal**','','**'+br(sum((D(r['total']) for r in subset),D(0)))+'**']])])
    parts.extend(['## Total por fonte',table(['Fonte','Valor pessoal R$'],[[s['nome'],br(sum((D(r['valores'][key]) for r in rows),D(0)))] for key,s in sources.items()]+[['**TOTAL**','**'+br(result['total'])+'**']]),'## Regras e observações do período','\n\n'.join('- '+n for n in data.get('observacoes',[])),
        '## Conciliação dos valores originais',table(['Fonte','Controle','Valor R$','Diferença R$'],[[c['fonte'],c['controle'],br(D(c['valor'])),br(D(c['diferenca']))] for c in result['controles']]),
        '## Documentos originais',table(['Fonte','Documento','Vencimento / período'],[[f['nome'],'['+Path(f['arquivo']).name+']('+local_file(period,f['arquivo']).as_posix()+')',f.get('vencimento',config['mes_referencia'])] for f in sources.values()]),
        '## Movimentos excluídos do orçamento',table(['ID','Data','Descrição','Original R$','Motivo'],[[r['id'],r['data'],r['descricao'],br(D(r['valor_original'])),r.get('observacao','')] for r in records if r['linha'] is None]),
        '## Detalhamento por item','Participações preservam três casas quando necessário. O subtotal é arredondado uma vez por item/fonte.'])
    for item in rows:
        selected=[r for r in records if r['linha']==item['linha']]
        if not selected:continue
        parts.extend([f'### {sheet_line(item)} — {item["item"]} — R$ {br(D(item["total"]))}',table(['ID','Fonte / cartão','Data','Lançamento','Parcela','Original R$','Pessoal exato R$','Página','Observação'],[[r['id'],sources[r['fonte_id']]['nome']+(' / '+r['cartao'] if r.get('cartao') else ''),r['data'],r['descricao'],r.get('parcela',''),br(D(r['valor_original'])),br(D(r['valor_pessoal_exato']),3),r['pagina'],r.get('observacao','')] for r in selected])])
    links=[('PENDENCIAS.md','Pendências'),('RESUMO_PALOMA.md','Conferência para Paloma'),('detalhes/CONFERENCIA_REEMBOLSOS_BABAS.md','Créditos de Paloma por babá')]
    parts.extend(['## Arquivos de apoio','\n'.join('- ['+label+']('+(period/'output'/rel).as_posix()+')' for rel,label in links if rel=='PENDENCIAS.md' or (period/'output'/rel).exists())])
    write(out/'RESUMO_MENSAL.md','\n\n'.join(parts))
    pending=[f'# {config["mes_referencia"]} — pendências de conferência',
        'Categoria, participação e recebimento são decisões distintas. A tabela mensal inclui os valores pessoais atuais; a revisão pode alterá-los.',
        table(['ID','Descrição','Linha','Tipo de dúvida','Valor pessoal R$','Observação'],[[r['id'],r['descricao'],sheet_line(next(item for item in rows if item['linha']==r['linha'])),'Divisão / recebimento' if r.get('rateio_status')=='aguardando_confirmacao' else 'Classificação',br(D(r['valor_pessoal_exato'])),r.get('observacao','')] for r in uncertain]),
        '## Estabelecimentos mantidos em Outros',table(['ID','Descrição','Valor pessoal R$','Decisão'],[[r['id'],r['descricao'],br(D(r['valor_pessoal_exato'])),r.get('observacao','')] for r in records if r['status']=='nao_identificado']),
        '## Próximo período','Consultar [acompanhamentos]('+(ROOT/'.core/conhecimento/ACOMPANHAMENTOS.md').as_posix()+'); previsões não entram nos gastos atuais.']
    write(out/'PENDENCIAS.md','\n\n'.join(pending))
    write(period/'output/.auditoria/dados/conferencia_mensal.json',{'mes_referencia':config['mes_referencia'],'total_pessoal':str(result['total']),'linhas':rows,'controles':result['controles'],'creditos_utilizados':result['creditos_utilizados'],'quantidade_registros':len(records),'pendencias':len(uncertain)})
    return out/'RESUMO_MENSAL.md'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    prep=commands.add_parser('preparar');prep.add_argument('--mes',required=True);prep.add_argument('--ciclo',required=True);prep.add_argument('--arquivos',nargs='*',default=[])
    for name in ['validar','gerar']:
        sub=commands.add_parser(name);sub.add_argument('--mes',required=True)
    args=parser.parse_args()
    try:
        if args.command=='preparar':
            path,count=prepare(ROOT,args.mes,args.ciclo,args.arquivos)
            print(f'Período pronto: {path}; {count} arquivo(s) novo(s).')
        else:
            path=period_path(args.mes);result=validate(path)
            print(f'Conferência válida: {len(result["ledger"]["lancamentos"])} registros, total pessoal R$ {br(result["total"])}.')
            if args.command=='gerar':print(f'Resumo salvo: {render(path,result)}')
        return 0
    except (ValidationError,KeyError,FileNotFoundError,ValueError) as error:
        print(f'Não concluído: {error}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())

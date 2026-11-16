'use client';
import { compareCardNames } from '@/lib/card-order';
import { useCallback, useEffect, useState, type FormEvent } from 'react';
import { Check, Eye, LockKeyhole, Plus, Users } from 'lucide-react';

type Grant={id?:string;name:string;email:string;enabled:boolean;canSummary:boolean;canEntries:boolean;canPeriods:boolean;cards:string[];includeUnknown:boolean;includePix:boolean;linkedAt?:string|null;updatedAt?:string};
type CardOption={last4:string;name:string;brand:string;kind:string};
const empty=():Grant=>({name:'',email:'',enabled:true,canSummary:true,canEntries:false,canPeriods:false,cards:[],includeUnknown:false,includePix:false});
async function request(path:string,options:RequestInit={}):Promise<any>{
  const r=await fetch(path,{...options,headers:{'Content-Type':'application/json',...options.headers}});
  if(!r.headers.get('content-type')?.includes('application/json'))throw new Error('Entre novamente para administrar os acessos.');
  const data=await r.json() as any;if(!r.ok)throw new Error(data.error??'Não foi possível salvar.');return data;
}
function scopeDescription(grant:Grant,available:CardOption[]){
  const cards=grant.cards.map(c=>{const card=available.find(item=>item.last4===c);return card?.name?`${card.name} · final ${c}`:`final ${c}`;});
  if(grant.includePix)cards.push('Pix');
  if(grant.includeUnknown)cards.push('sem cartão identificado');
  return cards.length?cards.join(' · '):'Nenhuma forma de pagamento autorizada';
}
export default function AccessManagement(){
  const [grants,setGrants]=useState<Grant[]>([]);const [cards,setCards]=useState<CardOption[]>([]);
  const [draft,setDraft]=useState<Grant|null>(null);const [busy,setBusy]=useState(false);const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');const [notice,setNotice]=useState('');
  const reload=useCallback(async()=>{
    try{const [people,available]=await Promise.all([request('/api/access'),request('/api/card-registry')]);setGrants(people.grants);setCards(available.cards);}
    catch(e){setGrants([]);setCards([]);setDraft(null);setError((e as Error).message);}finally{setLoading(false);}
  },[]);
  useEffect(()=>{void reload();},[reload]);
  async function save(grant:Grant){
    setBusy(true);setError('');setNotice('');
    try{await request('/api/access',{method:grant.id?'PATCH':'POST',body:JSON.stringify(grant)});setDraft(null);setNotice(grant.enabled?'Permissões salvas. As próximas consultas já usam esta configuração.':'Acesso suspenso. Novas consultas a dados foram bloqueadas.');await reload();}
    catch(e){setError((e as Error).message);}finally{setBusy(false);}
  }
  function submit(e:FormEvent){e.preventDefault();if(draft)void save(draft);}
  function preview(grant:Grant){if(!grant.id)return;sessionStorage.setItem('previewAccessId',grant.id);window.location.assign(grant.canSummary?'/':grant.canEntries?'/lancamentos':grant.canPeriods?'/periodos':'/');}
  const available=[...cards];for(const last4 of draft?.cards??[])if(!available.some(card=>card.last4===last4))available.push({last4,name:'',brand:'unknown',kind:'primary'});available.sort(compareCardNames);
  return <>
    <div className="intro"><div><p className="eyebrow">Você decide o que compartilhar</p><h1>Acessos</h1><p>Escolha páginas, cartões e acesso aos Pix para cada pessoa.</p></div><button className="button primary" disabled={busy} onClick={()=>{setDraft(empty());setError('');setNotice('');}}><Plus size={17}/>Adicionar pessoa</button></div>
    <div className="notice success"><LockKeyhole size={18}/><p><strong>Você é o administrador.</strong> Seu acesso a todos os cartões e páginas permanece completo. Somente você pode editar gastos, conectar iPhones e administrar permissões.</p></div>
    {error&&<p className="notice error" role="alert">{error}</p>}{notice&&<div className="notice success" role="status"><Check size={18}/><p>{notice}</p></div>}
    <div className="access-grid">
      <section className="panel"><h2>Pessoas cadastradas</h2>{loading?<p className="muted">Carregando acessos…</p>:grants.length?grants.map(grant=><article className="access-person" key={grant.id}>
        <div className="row between"><h3>{grant.name}</h3><span className={'badge '+(!grant.enabled?'warn':'')}>{grant.enabled?'Ativo no portal':'Suspenso'}</span></div><p className="small muted access-email">{grant.email}</p>
        <p className="small">{[grant.canSummary?'Visão geral':null,grant.canEntries?'Lançamentos em consulta':null,grant.canPeriods?'Períodos em consulta':null].filter(Boolean).join(' · ')||'Nenhuma página'}</p>
        <p className="small muted">{scopeDescription(grant,cards)}</p><p className="small muted">{grant.linkedAt?'Conta vinculada no primeiro acesso.':'Aguardando o primeiro acesso ao portal.'}</p>
        <div className="row"><button className="button" disabled={busy} onClick={()=>{setDraft({...grant,cards:[...grant.cards]});setError('');setNotice('');}}>Editar permissões</button><button className="button" disabled={busy} onClick={()=>preview(grant)}><Eye size={16}/>Visualizar como</button><button className={'button '+(grant.enabled?'danger':'')} disabled={busy} onClick={()=>void save({...grant,enabled:!grant.enabled})}>{grant.enabled?'Suspender':'Reativar'}</button></div>
      </article>):<div className="empty"><div className="empty-icon"><Users size={24}/></div><h3>Só você tem acesso</h3><p>Cadastre uma pessoa e selecione o que ela poderá consultar.</p></div>}</section>
      {draft?<section className="panel" aria-label="Permissões da pessoa"><h2>{draft.id?'Editar permissões':'Adicionar pessoa'}</h2><form onSubmit={submit}>
        <div className="form-grid"><label className="field full">Nome<input autoFocus required maxLength={80} value={draft.name} onChange={e=>setDraft({...draft,name:e.target.value})}/></label><label className="field full">E-mail da conta ChatGPT<input type="email" required readOnly={Boolean(draft.id)} maxLength={254} value={draft.email} onChange={e=>setDraft({...draft,email:e.target.value})}/><span className="small muted">A pessoa deverá entrar com essa conta. Para trocar de conta, suspenda este acesso e cadastre outro.</span></label></div>
        <fieldset className="permission-group"><legend>Páginas permitidas</legend><label className="permission-option"><input type="checkbox" checked={draft.canSummary} onChange={e=>setDraft({...draft,canSummary:e.target.checked})}/><span><strong>Visão geral</strong><small>Totais de hoje, da semana e do mês, sem os nomes das lojas.</small></span></label><label className="permission-option"><input type="checkbox" checked={draft.canEntries} onChange={e=>setDraft({...draft,canEntries:e.target.checked})}/><span><strong>Lançamentos</strong><small>Data, loja, valor e categoria de cada compra. Somente consulta, sem o SMS original.</small></span></label><label className="permission-option"><input type="checkbox" checked={draft.canPeriods} onChange={e=>setDraft({...draft,canPeriods:e.target.checked})}/><span><strong>Períodos</strong><small>Consultar nomes, datas, horários e totais dos cartões autorizados. Criar e editar continua exclusivo do administrador.</small></span></label></fieldset>
        <fieldset className="permission-group"><legend>Formas de pagamento autorizadas</legend><p className="small muted">A seleção vale para todas as páginas permitidas. Novos cartões ficam bloqueados até você autorizá-los.</p><div className="permission-cards">{available.map(card=><label className="check" key={card.last4}><input type="checkbox" checked={draft.cards.includes(card.last4)} onChange={e=>setDraft({...draft,cards:e.target.checked?[...draft.cards,card.last4]:draft.cards.filter(c=>c!==card.last4)})}/>{card.name?`${card.name} · `:''}Cartão final {card.last4}</label>)}</div>{!available.length&&<p className="small muted">Os cartões aparecem aqui após o primeiro SMS ou a identificação em um lançamento.</p>}<label className="permission-option"><input type="checkbox" checked={draft.includePix} onChange={e=>setDraft({...draft,includePix:e.target.checked})}/><span><strong>Pix</strong><small>Consultar os Pix nas páginas permitidas, sem acesso ao SMS original.</small></span></label><label className="permission-option"><input type="checkbox" checked={draft.includeUnknown} onChange={e=>setDraft({...draft,includeUnknown:e.target.checked})}/><span><strong>Gastos sem cartão identificado</strong><small>Inclui compras cujo SMS não informa a qual cartão pertencem.</small></span></label></fieldset>
        <label className="check"><input type="checkbox" checked={draft.enabled} onChange={e=>setDraft({...draft,enabled:e.target.checked})}/>Acesso ativo</label>
        <div className="permission-preview"><strong className="small">Esta pessoa poderá consultar</strong><p className="small">{draft.enabled?[draft.canSummary?'Visão geral':null,draft.canEntries?'Lançamentos':null,draft.canPeriods?'Períodos':null].filter(Boolean).join(' e ')||'Nenhuma página':'Nenhuma página enquanto o acesso estiver suspenso'}.</p><p className="small muted">{scopeDescription(draft,available)}.</p></div>
        <div className="row"><button className="button primary" disabled={busy}>{busy?'Salvando…':'Salvar permissões'}</button><button type="button" className="button" disabled={busy} onClick={()=>setDraft(null)}>Cancelar</button></div>
      </form></section>:<section className="panel"><h2>Como liberar o primeiro acesso</h2><ol className="access-steps"><li>Cadastre o e-mail e salve as páginas e cartões autorizados.</li><li>Adicione esse mesmo e-mail como <strong>visualizador</strong> no compartilhamento do site pelo ChatGPT.</li><li>Compartilhe o endereço do portal. A pessoa entra com a própria conta e vê somente o que você liberou.</li></ol><p className="small muted">Salvar aqui configura as permissões do portal. Não envia convite nem altera o compartilhamento do site. Depois da primeira liberação, você pode mudar cartões, páginas e suspender o acesso por esta tela.</p><a className="button" href="/" target="_blank" rel="noreferrer">Abrir endereço para compartilhar ↗</a></section>}
    </div>
  </>;
}

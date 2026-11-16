import { env } from 'cloudflare:workers';

export type Access = { id:string; email:string; isOwner:boolean; enabled:boolean; canSummary:boolean; canEntries:boolean; canPeriods:boolean; cards:string[]; includeUnknown:boolean; includePix?:boolean; previewing?:boolean; previewGrantId?:string; previewName?:string };
export type AccessPage = 'summary' | 'entries' | 'setup' | 'access' | 'cards' | 'periods';
export class AccessError extends Error { constructor(message:string, public status=403) { super(message); } }
export function database() { if (!env.DB) throw new Error('Banco de dados indisponível.'); return env.DB; }
export function readCards(value: unknown): string[] {
  try { const parsed=JSON.parse(String(value));return Array.isArray(parsed)&&parsed.length<=32&&parsed.every(c=>typeof c==='string'&&/^\d{4}$/.test(c))?[...new Set<string>(parsed)]:[]; } catch { return []; }
}
export async function resolveAccess(id:string|null, email:string|null):Promise<Access> {
  if(!id||!email)throw new AccessError('Entre com sua conta para continuar.',401);
  const denied:Access={id,email:email.trim().toLowerCase(),isOwner:false,enabled:false,canSummary:false,canEntries:false,canPeriods:false,cards:[],includeUnknown:false};
  const owner=await database().prepare("SELECT value FROM settings WHERE key='owner_id'").first<{value:string}>();
  // This existing site's administrator was provisioned before invitations.
  // Missing configuration must never promote the next visitor to administrator.
  if(owner?.value===id)return {...denied,isOwner:true,enabled:true,canSummary:true,canEntries:true,canPeriods:true};
  let grant=await database().prepare('SELECT * FROM access_grants WHERE user_id=?').bind(id).first<Record<string,any>>();
  if(!grant){
    // Email selects a pending invitation only. Once linked, the stable identity
    // owns the grant even if the account's email changes; it cannot be reclaimed.
    await database().prepare('UPDATE access_grants SET user_id=?,linked_at=? WHERE email=? AND user_id IS NULL AND enabled=1').bind(id,new Date().toISOString(),denied.email).run();
    grant=await database().prepare('SELECT * FROM access_grants WHERE user_id=?').bind(id).first<Record<string,any>>();
  }
  if(!grant||grant.enabled!==1)return denied;
  return {...denied,enabled:true,canSummary:grant.can_summary===1,canEntries:grant.can_entries===1,canPeriods:grant.can_periods===1,cards:readCards(grant.card_last4s),includePix:grant.include_pix===1,includeUnknown:grant.include_unknown===1};
}
export async function resolvePreviewAccess(owner:Access,grantId:string):Promise<Access>{
  if(!owner.isOwner)throw new AccessError('Somente o administrador pode visualizar como outra pessoa.',403);
  if(!/^[a-zA-Z0-9-]{1,100}$/.test(grantId))throw new AccessError('Acesso para visualização inválido.',400);
  const grant=await database().prepare('SELECT * FROM access_grants WHERE id=?').bind(grantId).first<Record<string,any>>();
  if(!grant)throw new AccessError('A pessoa selecionada não foi encontrada.',404);
  return {id:owner.id,email:String(grant.email??''),isOwner:false,enabled:grant.enabled===1,canSummary:grant.can_summary===1,canEntries:grant.can_entries===1,canPeriods:grant.can_periods===1,cards:readCards(grant.card_last4s),includePix:grant.include_pix===1,includeUnknown:grant.include_unknown===1,previewing:true,previewGrantId:grantId,previewName:String(grant.name??grant.email??'Pessoa')};
}
export function permits(access:Access,page:AccessPage) {
  return access.enabled&&(access.isOwner||(page==='summary'?access.canSummary:page==='entries'?access.canEntries:page==='periods'?access.canPeriods:false));
}
export function requirePermission(access:Access,page:AccessPage) {
  if(!permits(access,page))throw new AccessError('Seu acesso não permite abrir esta página. Peça ao administrador para revisar suas permissões.');
}
export function cardScope(access:Access,alias=''):{sql:string;values:string[]} {
  if(access.isOwner)return {sql:'',values:[]};
  const parts:string[]=[];
  if(access.cards.length)parts.push(`${alias}card_last4 IN (${access.cards.map(()=>'?').join(',')})`);
  if(access.includeUnknown)parts.push(`${alias}card_last4 IS NULL`);
  const scopes:string[]=[];
  if(parts.length)scopes.push(`(${alias}source NOT IN ('sms_pix','manual_sms_pix') AND (${parts.join(' OR ')}))`);
  if(access.includePix)scopes.push(`${alias}source IN ('sms_pix','manual_sms_pix')`);
  return {sql:scopes.length?` AND (${scopes.join(' OR ')})`:' AND 0=1',values:access.cards};
}

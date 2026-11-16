import assert from 'node:assert/strict';
import {readdirSync} from 'node:fs';
import {DatabaseSync} from 'node:sqlite';

// The development sign-in exposes one fixed identity. Only this disposable local
// database is used to exercise that same session as an invited viewer.
const base=process.env.TEST_BASE_URL||'http://127.0.0.1:5173';
if(!['localhost','127.0.0.1'].includes(new URL(base).hostname))throw new Error('Local tests only.');
const directory=new URL('../.wrangler/state/v3/d1/miniflare-D1DatabaseObject/',import.meta.url);
const files=readdirSync(directory).filter(n=>/^[a-f0-9]+\.sqlite$/.test(n));assert.equal(files.length,1);
const db=new DatabaseSync(new URL(files[0],directory));
const ownerId=db.prepare("SELECT value FROM settings WHERE key='owner_id'").get().value;
const login=await fetch(base+'/signin-with-chatgpt?return_to=/',{redirect:'manual'});
const cookie=login.headers.getSetCookie().map(c=>c.split(';')[0]).join('; ');assert.ok(cookie);
async function request(path,{method='GET',payload,auth=true,headers={}}={}){
 const response=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(auth?{Cookie:cookie}:{}),...headers},body:payload?JSON.stringify(payload):undefined,redirect:'manual'});
 return {status:response.status,location:response.headers.get('location'),data:response.headers.get('content-type')?.includes('application/json')?await response.json():await response.text()};
}
const now=Date.now();let grantId;const entryIds=[];const email=`viewer-${now}@example.test`;
const date=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const baseline=(await request('/api/summary')).data.totalCents;
const grant={name:'Pessoa de teste',email,enabled:true,canSummary:true,canEntries:false,cards:['7081'],includeUnknown:false};
async function purchase(card,amount,{test=false,excluded=false}={}){
 const message=`Compra aprovada no PERSON BLACK PONTOS ${card?`final ${card}`:'p/ CLIENTE TESTE'} - PANIFICADORA EXEMPLO ${now} valor RS ${amount} em ${date.slice(8)}/${date.slice(5,7)}, as 17h48.`;
 const r=await request('/api/import',{method:'POST',payload:{message,eventId:crypto.randomUUID(),isTest:test}});assert.equal(r.status,201);entryIds.push(r.data.id);
 if(excluded)await request('/api/entries',{method:'PATCH',payload:{id:r.data.id,status:'excluded'}});
 return r.data.id;
}
function configure(fields){
 const allowed=new Set(['enabled','can_summary','can_entries','can_periods','card_last4s','include_unknown','user_id','email']);
 assert.ok(Object.keys(fields).every(k=>allowed.has(k)));
 db.prepare(`UPDATE access_grants SET ${Object.keys(fields).map(k=>k+'=?').join(',')} WHERE id=?`).run(...Object.values(fields),grantId);
}
try{
 assert.equal((await request('/api/access',{auth:false})).status,401);
 assert.equal((await request('/api/access',{method:'POST',headers:{Origin:'https://outside.example'},payload:grant})).status,403);
 for(const invalid of [{...grant,cards:[]},{...grant,cards:['781']},{...grant,canSummary:false},{...grant,enabled:'true'},{...grant,email:'bad'}])assert.equal((await request('/api/access',{method:'POST',payload:invalid})).status,400);
 const created=await request('/api/access',{method:'POST',payload:{...grant,email:email.toUpperCase(),isOwner:true}});assert.equal(created.status,201);grantId=created.data.id;
 assert.equal((await request('/api/access',{method:'POST',payload:grant})).status,409);
 const stored=(await request('/api/access')).data.grants.find(g=>g.id===grantId);assert.equal(stored.email,email);assert.equal(stored.linkedAt,null);assert.deepEqual(stored.cards,['7081']);assert.equal(stored.isOwner,undefined);
 for(const changed of [{...grant,canEntries:true,cards:['7081','7082']},{...grant,enabled:false,canSummary:false,cards:[]},grant]){
  assert.equal((await request('/api/access',{method:'PATCH',payload:{...changed,id:grantId}})).status,200);
  const saved=(await request('/api/access')).data.grants.find(g=>g.id===grantId);assert.equal(saved.enabled,changed.enabled);assert.equal(saved.canEntries,changed.canEntries);assert.deepEqual(saved.cards,changed.cards);
 }
 assert.equal((await request('/api/access',{method:'PATCH',payload:{...grant,id:grantId,email:'another@example.test'}})).status,400);
 const first=await purchase('7081','12,34');db.prepare('UPDATE entries SET note=? WHERE id=?').run('Lanche da escola',first);await purchase('7082','56,78');await purchase(null,'20,00');await purchase('7081','90,00',{test:true});await purchase('7081','80,00',{excluded:true});await purchase('7083','70,00');
 // The owner can preview the selected grant, but the preview loses every owner-only capability.
 const previewHeaders={'X-Preview-Access-Id':grantId};const previewSession=(await request('/api/session',{headers:previewHeaders})).data;
 assert.equal(previewSession.isOwner,false);assert.equal(previewSession.previewing,true);assert.equal(previewSession.previewName,'Pessoa de teste');assert.equal(previewSession.canSummary,true);assert.equal(previewSession.canEntries,false);
 assert.equal((await request('/api/summary',{headers:previewHeaders})).data.totalCents,1234);assert.equal((await request('/api/summary?card=7082',{headers:previewHeaders})).status,403);assert.equal((await request('/api/entries',{headers:previewHeaders})).status,403);assert.equal((await request('/api/access',{headers:previewHeaders})).status,403);
 assert.equal((await request('/api/session',{headers:{'X-Preview-Access-Id':'missing-grant'}})).status,404);
 // Empty-owner configuration does not turn the next visitor into an administrator.
 db.prepare("DELETE FROM settings WHERE key='owner_id'").run();
 assert.equal((await request('/api/session')).data.isOwner,false);assert.equal((await request('/api/summary')).status,403);
 assert.equal(db.prepare("SELECT COUNT(*) AS n FROM settings WHERE key='owner_id'").get().n,0);
 db.prepare("INSERT INTO settings (key,value) VALUES ('owner_id',?)").run('different-local-owner');
 configure({email:'seedy@sites.test'});
 let session=(await request('/api/session')).data;assert.equal(session.isOwner,false);assert.equal(session.enabled,true);assert.equal(session.canSummary,true);assert.equal(session.canEntries,false);
 const linked=db.prepare('SELECT user_id,linked_at FROM access_grants WHERE id=?').get(grantId);assert.equal(linked.user_id,ownerId);assert.ok(linked.linked_at);
 configure({email}); // Matching stable identity continues to work after an email change.
 assert.equal((await request('/api/session')).data.enabled,true);
 const summary=(await request('/api/summary')).data;assert.equal(summary.totalCents,1234);assert.equal(summary.pending,0);
 assert.equal(summary.categories.reduce((s,c)=>s+c.totalCents,0),1234);
 for(const value of ['PANIFICADORA','raw_text','7082','7083','card_last4'])assert.equal(JSON.stringify(summary).includes(value),false);
 assert.equal((await request('/api/summary?card=7082')).status,403);assert.equal((await request('/api/summary?card=unknown')).status,403);
 assert.equal((await request('/api/entries')).status,403);
 assert.deepEqual((await request('/api/cards')).data.cards.map(c=>c.last4),['7081']);
 for(const page of ['/lancamentos','/acessos','/conectar','/periodos'])assert.match((await request(page)).data,/Acesso não autorizado/);
 assert.equal((await request('/')).status,200);
 assert.doesNotMatch((await request('/')).data,/Acesso não autorizado/);
 assert.equal((await request('/resumo')).location,'/');
 // A periods-only viewer lands on the permitted page and loses access on revocation.
 configure({can_summary:0,can_entries:0,can_periods:1});
 assert.equal((await request('/api/session')).data.canPeriods,true);
 assert.equal((await request('/')).location,'/periodos');
 assert.equal((await request('/periodos')).status,200);assert.doesNotMatch((await request('/periodos')).data,/Acesso não autorizado/);
 assert.equal((await request('/api/periods')).status,200);
 assert.equal((await request('/api/periods',{method:'POST',payload:{}})).status,403);
 configure({can_periods:0});assert.equal((await request('/api/periods')).status,403);assert.match((await request('/periodos')).data,/Acesso não autorizado/);
 // Entries-only permission is independent of the summary page.
 configure({can_summary:0,can_entries:1});
 assert.equal((await request('/api/summary')).status,403);assert.equal((await request('/resumo')).location,'/');assert.equal((await request('/')).location,'/lancamentos');
 const entries=(await request('/api/entries')).data.entries;assert.equal(entries.length,1);assert.equal(entries[0].id,first);assert.equal(entries[0].card_last4,'7081');assert.equal(entries[0].note,'Lanche da escola');
 for(const key of ['raw_text','message_hash','event_key','device_id','device_name','review_reason','received_at'])assert.equal(Object.hasOwn(entries[0],key),false);
 assert.equal((await request('/api/entries?card=7082')).status,403);assert.equal((await request('/api/entries?tests=1')).status,403);assert.equal((await request('/api/cards?tests=1')).status,403);
 for(const [path,method,payload] of [['/api/entries','PATCH',{id:first,status:'excluded'}],['/api/import','POST',{message:'Compra R$ 1,00'}],['/api/devices','GET'],['/api/devices','POST',{name:'Tentativa'}],['/api/card-registry','GET'],['/api/card-registry','PUT',{last4:'7081',name:'Tentativa',brand:'visa',kind:'primary',matchRules:[]}],['/api/card-rules/apply','POST',{}],['/api/access','GET'],['/api/access','POST',grant],['/api/access','PATCH',{...grant,id:grantId}]])assert.equal((await request(path,{method,payload})).status,403);
 // A changed card set takes effect on the next query with the same login cookie.
 configure({can_summary:1,card_last4s:JSON.stringify(['7082'])});
 assert.equal((await request('/api/summary')).data.totalCents,5678);assert.equal((await request('/api/entries')).data.entries[0].card_last4,'7082');assert.equal((await request('/api/summary?card=7081')).status,403);
 configure({include_unknown:1});assert.equal((await request('/api/summary')).data.totalCents,7678);assert.equal((await request('/api/summary?card=unknown')).data.totalCents,2000);
 configure({card_last4s:'[]',include_unknown:0});assert.equal((await request('/api/summary')).data.totalCents,0);assert.deepEqual((await request('/api/entries')).data.entries,[]);
 configure({enabled:0});assert.equal((await request('/api/session')).data.enabled,false);assert.equal((await request('/api/summary')).status,403);assert.equal((await request('/api/entries')).status,403);assert.equal((await request('/api/cards')).status,403);assert.match((await request('/')).data,/Acesso não autorizado/);
 // Another identity cannot reclaim a previously linked invitation by email.
 configure({enabled:1,user_id:'another-linked-identity',email:'seedy@sites.test'});assert.equal((await request('/api/session')).data.enabled,false);
 console.log('Acessos: criação/edição, vínculo de conta, páginas, cartões, revogação, projeção de dados e tentativas de acesso direto verificados.');
}finally{
 db.prepare("INSERT INTO settings (key,value) VALUES ('owner_id',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value").run(ownerId);
 if(grantId)db.prepare('DELETE FROM access_grants WHERE id=?').run(grantId);
 for(const id of entryIds)await request('/api/entries',{method:'PATCH',payload:{id,status:'excluded'}});
 assert.equal((await request('/api/summary')).data.totalCents,baseline);
 db.close();
}

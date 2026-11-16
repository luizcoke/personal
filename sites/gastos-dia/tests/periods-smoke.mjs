import assert from 'node:assert/strict';
import {readdirSync} from 'node:fs';
import {DatabaseSync} from 'node:sqlite';
const base=process.env.TEST_BASE_URL||'http://127.0.0.1:5173';
if(!['localhost','127.0.0.1'].includes(new URL(base).hostname))throw new Error('Local tests only.');
const directory=new URL('../.wrangler/state/v3/d1/miniflare-D1DatabaseObject/',import.meta.url);
const files=readdirSync(directory).filter(n=>/^[a-f0-9]+\.sqlite$/.test(n));assert.equal(files.length,1);
const db=new DatabaseSync(new URL(files[0],directory));
const login=await fetch(base+'/signin-with-chatgpt?return_to=/',{redirect:'manual'});
const cookie=login.headers.getSetCookie().map(c=>c.split(';')[0]).join('; ');
async function request(path,{method='GET',payload,auth=true,headers={}}={}){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(auth?{Cookie:cookie}:{}),...headers},body:payload?JSON.stringify(payload):undefined,redirect:'manual'});return {status:r.status,data:r.headers.get('content-type')?.includes('application/json')?await r.json():await r.text()};}
const date=(await request('/api/session')).data.today;
const prefix='period-smoke-'+Date.now();const ids=[],periodIds=[];let previewId;
const period={name:'Teste de horários',startsAt:date+'T13:00',endsAt:date+'T15:00',category:'travel',enabled:true};
async function purchase(time,{test=false,legacy=false,excluded=false}={}){
 const message=`ITAU: Compra aprovada no cartao final 9981, em ${date.slice(8)}/${date.slice(5,7)}/${date.slice(0,4)}${time?' as '+time:''}, no valor de R$ 10,00, em PADARIA ${prefix}-${ids.length}.`;
 const r=await request('/api/import',{method:'POST',payload:{message,isTest:test}});assert.equal(r.status,201,JSON.stringify(r.data));ids.push(r.data.id);
 if(legacy)db.prepare('UPDATE entries SET purchase_time=NULL,time_checked=0 WHERE id=?').run(r.data.id);
 if(excluded)assert.equal((await request('/api/entries',{method:'PATCH',payload:{id:r.data.id,status:'excluded'}})).status,200);
 return r.data.id;
}
async function entries(){const r=await request('/api/entries?card=9981');assert.equal(r.status,200,JSON.stringify(r.data));return r.data.entries;}
async function create(p){const r=await request('/api/periods',{method:'POST',payload:p});if(r.status===201)periodIds.push(r.data.id);return r;}
try{
 assert.equal((await request('/api/periods',{auth:false})).status,401);
 for(const invalid of [{...period,endsAt:period.startsAt},{...period,startsAt:date+'T25:00'},{...period,category:'bad'}])assert.equal((await create(invalid)).status,400);
 const before=await purchase('12:59'),start=await purchase('13:00',{legacy:true}),inside=await purchase('14:00'),end=await purchase('15:00'),after=await purchase('15:01'),unknown=await purchase('');await purchase('14:00',{test:true});await purchase('14:10',{excluded:true});
 const created=await create(period);assert.equal(created.status,201,JSON.stringify(created.data));const id=created.data.id;
 let list=await entries();for(const key of [start,inside,end]){const e=list.find(e=>e.id===key);assert.equal(e.category,'travel');assert.equal(e.base_category,'snacks');}
 for(const key of [before,after,unknown])assert.equal(list.find(e=>e.id===key).category,'snacks');
 assert.equal(list.find(e=>e.id===unknown).needs_review,true);assert.equal(list.find(e=>e.id===start).purchase_time,'13:00');
 let info=(await request('/api/periods')).data.periods.find(p=>p.id===id);assert.equal(info.totalCents,3000);assert.equal(info.entryCount,3);assert.equal(info.missingTimeCount,1);
 const summary=(await request('/api/summary?period=today&card=9981')).data;assert.equal(summary.categories.find(c=>c.id==='travel').totalCents,3000);assert.equal(summary.pending,1);
 const card=(await request('/api/cards?period=today')).data.cards.find(c=>c.last4==='9981');assert.equal(card.foodCents,3000);assert.equal(card.diningCents,3000);assert.equal(card.totalCents,6000);
 const late=await purchase('14:30');assert.equal((await entries()).find(e=>e.id===late).category,'travel');
 assert.equal((await create({...period,name:'Sobreposto'})).status,409);
 assert.equal((await create({...period,startsAt:date+'T15:00',endsAt:date+'T16:00'})).status,409);
 const adjacent=await create({...period,name:'Após',startsAt:date+'T15:01',endsAt:date+'T16:00'});assert.equal(adjacent.status,201);
 // Owner correction makes the missing-time entry count immediately.
 assert.equal((await request('/api/entries',{method:'PATCH',payload:{id:unknown,merchant:'Padaria corrigida',amountCents:1000,category:'snacks',purchaseDate:date,purchaseTime:'14:20'}})).status,200);
 assert.equal((await entries()).find(e=>e.id===unknown).category,'travel');
 assert.equal((await request('/api/entries',{method:'PATCH',payload:{id:unknown,merchant:'Padaria corrigida',amountCents:1000,category:'snacks',purchaseDate:date,purchaseTime:'24:00'}})).status,400);
 assert.equal((await request('/api/periods',{method:'PATCH',payload:{...period,id,enabled:false}})).status,200);
 assert.equal((await entries()).find(e=>e.id===inside).category,'snacks');
 assert.equal((await request('/api/periods',{method:'PATCH',payload:{...period,id,enabled:true,endsAt:date+'T13:00'}})).status,400);
 assert.equal((await request('/api/periods',{method:'PATCH',payload:{...period,id,enabled:true,endsAt:date+'T13:01'}})).status,200);
 list=await entries();assert.equal(list.find(e=>e.id===start).category,'travel');assert.equal(list.find(e=>e.id===inside).category,'snacks');
 // Full-day unknown-time purchases are unambiguous and classify automatically.
 await request('/api/periods',{method:'PATCH',payload:{...period,id,enabled:false}});
 await request('/api/periods',{method:'PATCH',payload:{...period,id:adjacent.data.id,startsAt:date+'T15:01',endsAt:date+'T16:00',enabled:false}});
 await request('/api/entries',{method:'PATCH',payload:{id:unknown,merchant:'Padaria corrigida',amountCents:1000,category:'snacks',purchaseDate:date,purchaseTime:null}});
 assert.equal((await request('/api/periods',{method:'PATCH',payload:{...period,id,startsAt:date+'T00:00',endsAt:date+'T23:59'}})).status,200);
 assert.equal((await entries()).find(e=>e.id===unknown).category,'travel');
 // Viewer scope remains limited; period configuration is owner-only, even in preview.
 for(const cardText of ['final 9982','p/ TESTE SEM CARTAO']){
  const r=await request('/api/import',{method:'POST',payload:{message:`Compra aprovada no PERSON BLACK PONTOS ${cardText} - PADARIA ${prefix}-escopo-${ids.length} valor R$ 17,00 em ${date.slice(8)}/${date.slice(5,7)}/${date.slice(0,4)} as 14h15.`}});assert.equal(r.status,201);ids.push(r.data.id);
 }
 const grant=await request('/api/access',{method:'POST',payload:{name:'Teste período',email:prefix+'@example.test',enabled:true,canSummary:true,canEntries:true,cards:['9981'],includeUnknown:false}});assert.equal(grant.status,201);previewId=grant.data.id;
 const headers={'X-Preview-Access-Id':previewId};
 assert.equal((await request('/api/periods',{headers})).status,403);
 assert.equal((await request('/api/periods',{headers,method:'POST',payload:period})).status,403);
 const permission={id:previewId,name:'Teste período',email:prefix+'@example.test',enabled:true,canSummary:false,canEntries:false,canPeriods:true,cards:['9981'],includeUnknown:false};
 assert.equal((await request('/api/access',{method:'PATCH',payload:permission})).status,200);
 let periodRows=(await request('/api/periods',{headers})).data.periods;assert.equal(periodRows.find(p=>p.id===id).totalCents,7000);assert.equal(periodRows.find(p=>p.id===id).entryCount,7);
 assert.equal((await request('/api/summary',{headers})).status,403);assert.equal((await request('/api/entries',{headers})).status,403);
 assert.equal((await request('/api/periods',{method:'PATCH',headers,payload:{...period,id}})).status,403);
 assert.equal((await request('/api/periods',{method:'POST',headers,payload:period})).status,403);
 // Omission from a legacy editor preserves the explicitly enabled permission.
 const legacy={...permission};delete legacy.canPeriods;
 assert.equal((await request('/api/access',{method:'PATCH',payload:legacy})).status,200);assert.equal((await request('/api/session',{headers})).data.canPeriods,true);
 assert.equal((await request('/api/access',{method:'PATCH',payload:{...permission,includeUnknown:true}})).status,200);
 periodRows=(await request('/api/periods',{headers})).data.periods;assert.equal(periodRows.find(p=>p.id===id).totalCents,8700);
 assert.equal((await request('/api/access',{method:'PATCH',payload:{...permission,canSummary:true,canEntries:true,canPeriods:false}})).status,200);
 assert.equal((await request('/api/periods',{headers})).status,403);
 const viewer=(await request('/api/entries?card=9981',{headers})).data.entries;
 assert.equal(viewer.find(e=>e.id===inside).category,'travel');
 for(const e of viewer)for(const key of ['raw_text','base_category','period_name','period_id'])assert.equal(Object.hasOwn(e,key),false);
 // A purchase from yesterday is classified by purchase time, not today's receipt.
 const previous=new Date(date+'T12:00:00Z');previous.setUTCDate(previous.getUTCDate()-1);const yesterday=previous.toISOString().slice(0,10);
 await request('/api/periods',{method:'PATCH',payload:{...period,id,enabled:false}});
 const overnight=await create({...period,name:'Virada do dia',startsAt:yesterday+'T23:30',endsAt:date+'T00:30'});assert.equal(overnight.status,201);
 for(const [day,time,expected] of [[yesterday,'23:29','snacks'],[yesterday,'23:30','travel'],[date,'00:30','travel'],[date,'00:31','snacks']]){
  const r=await request('/api/import',{method:'POST',payload:{message:`Compra aprovada R$ 10,00 em PADARIA ${prefix}-virada-${ids.length}, dia ${day.slice(8)}/${day.slice(5,7)}/${day.slice(0,4)} as ${time}. Cartao final 9981`}});assert.equal(r.status,201);ids.push(r.data.id);assert.equal(r.data.category,expected);assert.equal((await entries()).find(e=>e.id===r.data.id).category,expected);
 }
 assert.equal((await request('/api/periods',{auth:false,method:'POST',payload:period})).status,401);
 console.log('Períodos: limites inclusivos, recebimento tardio, históricos, horário ausente/corrigido, sobreposição, edição/desativação, totais e permissões verificados.');
}finally{
 for(const id of ids)db.prepare('DELETE FROM entries WHERE id=?').run(id);
 for(const id of periodIds)db.prepare('DELETE FROM spending_periods WHERE id=?').run(id);
 if(previewId)db.prepare('DELETE FROM access_grants WHERE id=?').run(previewId);
 db.close();
}

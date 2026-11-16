import { database, AccessError, cardScope, type Access } from './access';
import { isCategory, parseSMS, validLocalDateTime } from './domain';

type Row = Record<string, any>;
// All times are local wall-clock times in America/Sao_Paulo, at minute precision.
// Unknown times qualify only when the entire purchase date is inside the period.
export const EFFECTIVE_ENTRIES = `(SELECT e.*, COALESCE(p.category,e.category) AS effective_category,
 p.id AS period_id,p.name AS period_name,
 CASE WHEN e.purchase_time IS NULL AND EXISTS (
   SELECT 1 FROM spending_periods q WHERE q.enabled=1
   AND e.purchase_date BETWEEN substr(q.starts_at,1,10) AND substr(q.ends_at,1,10)
   AND NOT (e.purchase_date||'T00:00'>=q.starts_at AND e.purchase_date||'T23:59'<=q.ends_at)
 ) THEN 1 ELSE 0 END AS period_needs_review,
 CASE WHEN p.id IS NOT NULL AND e.review_reason='Escolha a categoria.' THEN 0 ELSE e.needs_review END AS effective_needs_review
 FROM entries e LEFT JOIN spending_periods p ON p.enabled=1
 AND e.purchase_date||'T'||COALESCE(e.purchase_time,'00:00')>=p.starts_at
 AND e.purchase_date||'T'||COALESCE(e.purchase_time,'23:59')<=p.ends_at)`;

export async function spendingPeriods(access:Access) {
 const scope=cardScope(access,'e.');
 const rows=await database().prepare(`SELECT p.*,
  (SELECT COALESCE(SUM(e.amount_cents),0) FROM ${EFFECTIVE_ENTRIES} e WHERE e.period_id=p.id AND e.is_test=0 AND e.status='active'${scope.sql}) AS total_cents,
  (SELECT COUNT(*) FROM ${EFFECTIVE_ENTRIES} e WHERE e.period_id=p.id AND e.is_test=0 AND e.status='active'${scope.sql}) AS entry_count,
  (SELECT COUNT(*) FROM ${EFFECTIVE_ENTRIES} e WHERE e.period_needs_review=1 AND e.purchase_date BETWEEN substr(p.starts_at,1,10) AND substr(p.ends_at,1,10) AND e.is_test=0 AND e.status='active' AND p.enabled=1${scope.sql}) AS missing_time_count
  FROM spending_periods p ORDER BY p.starts_at DESC`).bind(...scope.values,...scope.values,...scope.values).all<Row>();
 return rows.results.map(p=>({id:p.id,name:p.name,startsAt:p.starts_at,endsAt:p.ends_at,category:p.category,enabled:p.enabled===1,totalCents:Number(p.total_cents),entryCount:Number(p.entry_count),missingTimeCount:Number(p.missing_time_count)}));
}

async function recoverTimes(start:string,end:string) {
 // Bounded batches, restricted to the requested dates. Never infer purchase time
 // from arrival time or overwrite a time explicitly edited by the owner.
 for(;;){
  const rows=await database().prepare('SELECT id,raw_text,received_at,purchase_date FROM entries WHERE time_checked=0 AND purchase_date BETWEEN ? AND ? LIMIT 50').bind(start.slice(0,10),end.slice(0,10)).all<Row>();
  if(!rows.results.length)return;
  await database().batch(rows.results.map(row=>{
   const parsed=parseSMS(row.raw_text,new Date(row.received_at));
   return database().prepare('UPDATE entries SET purchase_time=?,time_checked=1 WHERE id=? AND time_checked=0 AND purchase_date=?').bind(parsed.purchaseDate===row.purchase_date?parsed.purchaseTime:null,row.id,row.purchase_date);
  }));
 }
}

export async function saveSpendingPeriod(b:Row,editing:boolean) {
 if(typeof b.name!=='string'||b.name.trim().length<2||b.name.trim().length>80||!validLocalDateTime(b.startsAt)||!validLocalDateTime(b.endsAt)||b.endsAt<=b.startsAt||!isCategory(b.category)||b.category==='unclassified'||typeof b.enabled!=='boolean')throw new AccessError('Preencha nome, categoria, início e fim. O fim precisa ser posterior ao início.',400);
 if(b.startsAt<'2000-01-01T00:00'||b.endsAt>'2100-12-31T23:59')throw new AccessError('Use datas entre 2000 e 2100.',400);
 if(editing&&(typeof b.id!=='string'||!await database().prepare('SELECT id FROM spending_periods WHERE id=?').bind(b.id).first()))throw new AccessError('Período não encontrado.',404);
 const id=editing?b.id:crypto.randomUUID();
 if(!editing){const count=await database().prepare('SELECT COUNT(*) AS n FROM spending_periods').first<{n:number}>();if((count?.n??0)>=100)throw new AccessError('Limite de 100 períodos atingido.',400);}
 if(b.enabled){const conflict=await database().prepare('SELECT name FROM spending_periods WHERE enabled=1 AND id<>? AND starts_at<=? AND ends_at>=? LIMIT 1').bind(id,b.endsAt,b.startsAt).first<Row>();if(conflict)throw new AccessError('Este intervalo coincide com outro período ativo. Ajuste os horários ou desative o outro período.',409);}
 await recoverTimes(b.startsAt,b.endsAt);
 const now=new Date().toISOString();
 try{
  if(editing)await database().prepare('UPDATE spending_periods SET name=?,starts_at=?,ends_at=?,category=?,enabled=?,updated_at=? WHERE id=?').bind(b.name.trim(),b.startsAt,b.endsAt,b.category,Number(b.enabled),now,id).run();
  else await database().prepare('INSERT INTO spending_periods (id,name,starts_at,ends_at,category,enabled,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)').bind(id,b.name.trim(),b.startsAt,b.endsAt,b.category,Number(b.enabled),now,now).run();
 }catch(error){if(String(error).includes('overlapping_spending_period'))throw new AccessError('Este intervalo coincide com outro período ativo.',409);throw error;}
 return {ok:true,id};
}

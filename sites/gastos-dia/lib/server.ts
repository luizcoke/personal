import { EFFECTIVE_ENTRIES, spendingPeriods, saveSpendingPeriod } from './spending-periods';
import { env } from 'cloudflare:workers';
import { CATEGORIES, hash, isCategory, money, normalize, parseSMS, periodRange, todaySP, validDate, validTime } from './domain';
import { AccessError, cardScope, database, readCards, requirePermission, resolveAccess, resolvePreviewAccess, type Access } from './access';

type Row = Record<string, any>;
const db=database;
function json(data: unknown, status = 200) { return Response.json(data, { status, headers: { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer' } }); }
class Problem extends Error { constructor(message: string, public status = 400) { super(message); } }
async function body(req: Request) {
  const text = await req.text();
  if (text.length > 12000) throw new Problem('Mensagem muito grande.', 413);
  try { const b = JSON.parse(text); if (!b || Array.isArray(b) || typeof b !== 'object') throw new Error(); return b; } catch { throw new Problem('Envie um corpo JSON válido.'); }
}
function sameOrigin(req: Request) {
  const origin = req.headers.get('Origin');
  if (origin && origin !== new URL(req.url).origin) throw new Problem('Origem não permitida.', 403);
}
async function identity(req: Request) { const user=await resolveAccess(req.headers.get('oai-authenticated-user-id'),req.headers.get('oai-authenticated-user-email'));const preview=req.headers.get('x-preview-access-id');return preview?resolvePreviewAccess(user,preview):user; }
async function owner(req: Request) { const user = await identity(req); requirePermission(user,'access');return user; }
function entryResponse(row: Row) { return { ...row, base_category: row.effective_category ? row.category : undefined, category: row.effective_category ?? row.category, is_test: Boolean(row.is_test), needs_review: Boolean(row.period_needs_review || (row.effective_needs_review ?? row.needs_review)), review_reason: row.raw_text === undefined ? undefined : [row.period_id ? String(row.review_reason??'').replace('Escolha a categoria.','').trim() : row.review_reason, row.period_needs_review ? 'Informe o horário da compra para conferir o período.' : ''].filter(Boolean).join(' ') }; }
async function receipt(row: Row) {
  if(row.id){const effective=await db().prepare(`SELECT effective_category FROM ${EFFECTIVE_ENTRIES} WHERE id=?`).bind(row.id).first<Row>();if(effective)row={...row,category:effective.effective_category};}
  const cents: number | null = row.amount_cents ?? null;
  return { amount: cents === null ? null : cents / 100, amountFormatted: cents === null ? null : money(cents), paymentMethod: String(row.source ?? '').endsWith('_pix') ? 'pix' : 'card', currency: 'BRL', amountCents: cents, category: row.category, cardLast4: row.card_last4 ?? null };
}
function cardFilter(url: URL, access:Access, alias = '') {
  const value = url.searchParams.get('card') ?? 'all';
  if (!['all', 'unknown', 'pix'].includes(value) && !/^\d{4}$/.test(value)) throw new Problem('Escolha um cartão ou Pix.');
  if(!access.isOwner&&value!=='all'&&(value==='pix'?!access.includePix:value==='unknown'?!access.includeUnknown:!access.cards.includes(value)))throw new Problem('Esta forma de pagamento não está autorizada para sua conta.',403);
  const scope=cardScope(access,alias);
  const pix=`${alias}source IN ('sms_pix','manual_sms_pix')`;
  const selection=value==='all'?'':value==='pix'?` AND ${pix}`:` AND NOT (${pix}) AND ${alias}card_last4 ${value==='unknown'?'IS NULL':'= ?'}`;
  return { value, sql:scope.sql+selection, values:[...scope.values,...(/^\d{4}$/.test(value)?[value]:[])] };
}
function grantResponse(row:Row){return {id:row.id,name:row.name,email:row.email,enabled:row.enabled===1,canSummary:row.can_summary===1,canEntries:row.can_entries===1,canPeriods:row.can_periods===1,cards:readCards(row.card_last4s),includePix:row.include_pix===1,includeUnknown:row.include_unknown===1,linkedAt:row.linked_at,updatedAt:row.updated_at};}
const CARD_BRANDS=['visa','mastercard','elo','amex','hipercard','other','unknown'];
const CARD_KINDS=['primary','virtual','additional','debit','other'];
function readMatchRules(value:unknown):string[]{try{const parsed=JSON.parse(String(value));return Array.isArray(parsed)?parsed.filter(rule=>typeof rule==='string'):[];}catch{return [];}}
function cardProfileInput(b:Row){
  if(typeof b.last4!=='string'||!/^\d{4}$/.test(b.last4))throw new Problem('Informe os quatro últimos dígitos do cartão.');
  if(typeof b.name!=='string'||b.name.trim().length>80)throw new Problem('O nome do cartão deve ter até 80 caracteres.');
  if(typeof b.brand!=='string'||!CARD_BRANDS.includes(b.brand)||typeof b.kind!=='string'||!CARD_KINDS.includes(b.kind))throw new Problem('Escolha uma bandeira e um tipo válidos.');
  const parent=b.kind==='virtual'&&typeof b.parentLast4==='string'&&/^\d{4}$/.test(b.parentLast4)?b.parentLast4:null;
  if(parent===b.last4)throw new Problem('O cartão virtual deve apontar para outro cartão principal.');
  if(!Array.isArray(b.matchRules)||b.matchRules.length>10||b.matchRules.some((rule:unknown)=>typeof rule!=='string'||rule.trim().length<5||rule.trim().length>200))throw new Problem('Cadastre até 10 frases, com 5 a 200 caracteres cada.');
  const matchRules=[...new Map<string,string>(b.matchRules.map((rule:string)=>[normalize(rule),rule.trim()])).values()];
  return {last4:b.last4,name:b.name.trim(),brand:b.brand,kind:b.kind,parent,matchRules};
}
function grantInput(b:Row){
  if(b.includePix===undefined)b={...b,includePix:false};
  if(b.canPeriods===undefined)b={...b,canPeriods:false};
  if(typeof b.name!=='string'||!b.name.trim()||b.name.length>80||typeof b.email!=='string'||b.email.length>254||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(b.email.trim()))throw new Problem('Informe nome e e-mail da conta que terá acesso.');
  if(['enabled','canSummary','canEntries','canPeriods','includePix','includeUnknown'].some(key=>typeof b[key]!=='boolean')||!Array.isArray(b.cards)||b.cards.length>32||b.cards.some((c:unknown)=>typeof c!=='string'||!/^\d{4}$/.test(c)))throw new Problem('Revise as páginas e os cartões autorizados.');
  const cards=[...new Set<string>(b.cards)].sort();
  if(b.enabled&&(!b.canSummary&&!b.canEntries&&!b.canPeriods))throw new Problem('Selecione pelo menos uma página para ativar o acesso.');
  if(b.enabled&&!cards.length&&!b.includeUnknown&&!b.includePix)throw new Problem('Selecione pelo menos um cartão ou Pix para ativar o acesso.');
  return {name:b.name.trim(),email:b.email.trim().toLowerCase(),enabled:Number(b.enabled),canSummary:Number(b.canSummary),canEntries:Number(b.canEntries),canPeriods:Number(b.canPeriods),cards,includePix:Number(b.includePix),includeUnknown:Number(b.includeUnknown)};
}
function selectedPeriod(url: URL) {
  const period = url.searchParams.get('period') ?? 'week';
  if (!['today', 'week', 'month'].includes(period)) throw new Problem('Período inválido.');
  return { period, ...periodRange(period) };
}
async function applyMerchantRule(parsed: ReturnType<typeof parseSMS>) {
  if (parsed.paymentMethod === 'pix' || !parsed.merchant) return;
  const rule = await db().prepare('SELECT category FROM rules WHERE merchant_key=?').bind(normalize(parsed.merchant)).first<Row>();
  if (rule && isCategory(rule.category)) { parsed.category = rule.category; parsed.reasons = parsed.reasons.filter(x => x !== 'Escolha a categoria.'); }
}
async function cardMatch(text:string){
  const rows=await db().prepare('SELECT last4,match_rules FROM card_profiles').all<Row>();const message=normalize(text);const matches=new Set<string>();
  for(const row of rows.results)for(const rule of readMatchRules(row.match_rules))if(message.includes(normalize(rule)))matches.add(row.last4);
  return matches.size===1?{last4:[...matches][0],ambiguous:false}:matches.size>1?{last4:null,ambiguous:true}:{last4:null,ambiguous:false};
}
async function applyCardRule(parsed:ReturnType<typeof parseSMS>,text:string){
  if(parsed.paymentMethod === 'pix' || parsed.cardLast4)return;const match=await cardMatch(text);if(match.last4)parsed.cardLast4=match.last4;else if(match.ambiguous)parsed.reasons.push('Mais de uma regra de cartão corresponde a esta mensagem.');
}
async function ingest(b: Row, deviceId: string | null, source: string, isTest: boolean) {
  if (typeof b.message !== 'string' || !b.message.trim() || b.message.length > 4000) throw new Problem('O campo message deve conter o texto do SMS (até 4.000 caracteres).');
  const text = b.message.trim();
  const now = new Date().toISOString();
  let received = new Date();
  if (b.receivedAt) {
    const date = new Date(b.receivedAt);
    if (isNaN(date.getTime()) || date.getTime() > Date.now() + 300000 || date.getTime() < Date.now() - 366 * 86400000) throw new Problem('receivedAt deve ser uma data ISO válida de até um ano atrás.');
    received = date;
  }
  const parsed = parseSMS(text, received);
  if (parsed.ignored) return json({ status: 'ignored', paymentMethod: parsed.paymentMethod ?? 'card', message: parsed.reasons.join(' ') });
  if (parsed.paymentMethod === 'pix') source += '_pix';
  await applyCardRule(parsed,text);
  const messageHash = await hash(normalize(text));
  const eventId = typeof b.eventId === 'string' && /^[a-zA-Z0-9_-]{1,100}$/.test(b.eventId) ? b.eventId : null;
  // Timestamp-bearing SMS and client event IDs deduplicate indefinitely. Without either,
  // only identical messages arriving within ten minutes are treated as retries.
  const eventKey = await hash(`${deviceId ?? source}:${isTest}:${eventId ?? (parsed.hasMessageTime ? messageHash : messageHash + ':' + Math.floor(Date.now() / 600000))}`);
  const recent = await db().prepare('SELECT * FROM entries WHERE is_test=? AND message_hash=? AND coalesce(device_id,source)=? AND received_at>=? LIMIT 1').bind(Number(isTest), messageHash, deviceId ?? source, new Date(Date.now() - 600000).toISOString()).first<Row>();
  const existing = await db().prepare('SELECT * FROM entries WHERE event_key=?').bind(eventKey).first<Row>();
  const duplicate = existing ?? recent;
  if (duplicate) {
    if(!duplicate.source.endsWith('_pix')&&!duplicate.card_last4&&duplicate.status==='active'){const match=await cardMatch(duplicate.raw_text);if(match.last4){await db().prepare('UPDATE entries SET card_last4=?,updated_at=? WHERE id=? AND card_last4 IS NULL').bind(match.last4,now,duplicate.id).run();duplicate.card_last4=match.last4;}}
    // A parser improvement can recover an untouched failed reading on retry.
    // Preserve the original SMS and never overwrite user edits or exclusions.
    if (duplicate.message_hash === messageHash && duplicate.status === 'active' && duplicate.needs_review === 1 && duplicate.amount_cents === null && duplicate.updated_at === duplicate.received_at) {
      const recovered = parseSMS(duplicate.raw_text, new Date(duplicate.received_at));
      await applyCardRule(recovered,duplicate.raw_text);
      await applyMerchantRule(recovered);
      if (!recovered.ignored && recovered.amountCents !== null && !recovered.reasons.length) {
        const updated = await db().prepare("UPDATE entries SET amount_cents=?,merchant=?,category=?,purchase_date=?,purchase_time=?,time_checked=1,needs_review=0,review_reason='',updated_at=? WHERE id=? AND status='active' AND needs_review=1 AND amount_cents IS NULL AND updated_at=? AND updated_at=received_at").bind(recovered.amountCents, recovered.merchant, recovered.category, recovered.purchaseDate, recovered.purchaseTime, now, duplicate.id, duplicate.updated_at).run();
        if (updated.meta.changes) return json({ status: 'reprocessed', id: duplicate.id, message: 'Lançamento pendente recuperado. A compra foi contada uma única vez.', ...await receipt({ id: duplicate.id, amount_cents: recovered.amountCents, category: recovered.category, card_last4: duplicate.card_last4 }) });
      }
    }
    return json({ status: 'duplicate', message: 'Este SMS já foi recebido. Nenhum gasto foi somado novamente.', id: duplicate.id, ...await receipt(duplicate) });
  }
  await applyMerchantRule(parsed);
  const id = crypto.randomUUID();
  await db().prepare('INSERT OR IGNORE INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at,purchase_time,time_checked) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)').bind(id, deviceId, eventKey, messageHash, text, parsed.amountCents, parsed.merchant, parsed.category, parsed.purchaseDate, parsed.cardLast4, parsed.installments, Number(parsed.reasons.length > 0), parsed.reasons.join(' '), 'active', source, Number(isTest), now, now, parsed.purchaseTime, 1).run();
  const inserted = await db().prepare('SELECT id,amount_cents,category,card_last4,source FROM entries WHERE event_key=?').bind(eventKey).first<Row>();
  if (deviceId) await db().prepare('UPDATE devices SET last_received_at=? WHERE id=?').bind(now, deviceId).run();
  return json({ status: inserted?.id === id ? (parsed.reasons.length ? 'needs_review' : 'received') : 'duplicate', id: inserted?.id, message: inserted?.id !== id ? 'SMS já recebido.' : parsed.reasons.length ? 'SMS recebido. Abra os lançamentos para conferir.' : 'Compra registrada.', ...await receipt(inserted ?? {}) }, 201);
}
export async function handle(req: Request): Promise<Response> {
  try {
    const url = new URL(req.url); const path = url.pathname; const method = req.method;
    if (path === '/api/health' && method === 'GET') return json({ status: 'ok' });
    if (path === '/api/sms' && method === 'POST') {
      const key = req.headers.get('X-Device-Key');
      if (!key || key.length > 200) throw new Problem('Chave do iPhone ausente ou inválida.', 401);
      const device = await db().prepare('SELECT id FROM devices WHERE token_hash=? AND revoked=0').bind(await hash(key)).first<Row>();
      if (!device) throw new Problem('Conexão do iPhone inválida ou revogada.', 401);
      const b = await body(req);
      return await ingest(b, device.id, 'sms', b.isTest === true);
    }
    if (method !== 'GET') sameOrigin(req);
    if (path === '/api/session' && method === 'GET') {
      const user = await identity(req);
      return json({ isOwner:user.isOwner,enabled:user.enabled,canSummary:user.canSummary,canEntries:user.canEntries,canPeriods:user.canPeriods,includePix:user.isOwner||Boolean(user.includePix),today:todaySP(),previewing:Boolean(user.previewing),previewGrantId:user.previewGrantId??null,previewName:user.previewName??null });
    }
    if (path === '/api/summary' && method === 'GET') {
      const user = await identity(req);
      requirePermission(user,'summary');
      const filter = cardFilter(url,user);
      const { period, start, end } = selectedPeriod(url);
      const rows = await db().prepare(`SELECT effective_category AS category,SUM(amount_cents) AS total,COUNT(*) AS count FROM ${EFFECTIVE_ENTRIES} WHERE is_test=0 AND status='active' AND amount_cents IS NOT NULL AND purchase_date BETWEEN ? AND ?` + filter.sql + ' GROUP BY effective_category').bind(start, end, ...filter.values).all<Row>();
      const pending = await db().prepare(`SELECT COUNT(*) AS count, SUM(CASE WHEN amount_cents IS NULL THEN 1 ELSE 0 END) AS missing FROM ${EFFECTIVE_ENTRIES} WHERE is_test=0 AND status='active' AND (effective_needs_review=1 OR period_needs_review=1) AND purchase_date BETWEEN ? AND ?` + filter.sql).bind(start, end, ...filter.values).first<Row>();
      const last = await db().prepare('SELECT MAX(received_at) AS received FROM entries WHERE is_test=0' + (!user.isOwner?" AND status='active'":'') + filter.sql).bind(...filter.values).first<Row>();
      // This response intentionally has no transaction IDs, merchants, card numbers,
      // SMS text, device identities, or purchase-level timestamps.
      return json({ period, start, end, totalCents: rows.results.reduce((s, r) => s + Number(r.total), 0), categories: CATEGORIES.map(c => ({ ...c, totalCents: Number(rows.results.find(r => r.category === c.id)?.total ?? 0) })), pending: Number(pending?.count ?? 0), missingAmounts: Number(pending?.missing ?? 0), updatedAt: last?.received ?? null });
    }
    if (path === '/api/cards' && method === 'GET') {
      const user=await identity(req);
      requirePermission(user,user.canSummary?'summary':'entries');
      if(!user.isOwner&&url.searchParams.get('tests')==='1')throw new Problem('Os testes são exclusivos do administrador.',403);
      const scope=cardScope(user);
      const { start, end } = selectedPeriod(url);
      const isTest = Number(url.searchParams.get('tests') === '1');
      const foodCategories = CATEGORIES.filter(c => c.food).map(c => c.id);
      const rows = await db().prepare(`SELECT CASE WHEN e.source IN ('sms_pix','manual_sms_pix') THEN 'pix' ELSE coalesce(e.card_last4,'unknown') END AS payment_key,e.card_last4 AS last4,p.name,p.brand,p.kind,p.parent_last4,
        SUM(CASE WHEN status='active' AND purchase_date BETWEEN ? AND ? THEN amount_cents ELSE 0 END) AS total,
        SUM(CASE WHEN status='active' AND purchase_date BETWEEN ? AND ? AND effective_category IN (${foodCategories.map(() => '?').join(',')}) THEN amount_cents ELSE 0 END) AS food,
        SUM(CASE WHEN status='active' AND purchase_date BETWEEN ? AND ? AND effective_category IN ('delivery','snacks','restaurants') THEN amount_cents ELSE 0 END) AS dining
        FROM ${EFFECTIVE_ENTRIES} e LEFT JOIN card_profiles p ON p.last4=e.card_last4 WHERE e.is_test=?${!user.isOwner?" AND status='active'":''}${scope.sql} GROUP BY payment_key,e.card_last4,p.name,p.brand,p.kind,p.parent_last4 ORDER BY e.card_last4 IS NULL,e.card_last4`).bind(start, end, start, end, ...foodCategories, start, end, isTest,...scope.values).all<Row>();
      return json({ cards: rows.results.map(r => ({ paymentKey:r.payment_key, last4: r.last4, name:r.name??'', brand:r.brand??'unknown', kind:r.kind??null, parentLast4:r.parent_last4??null, totalCents: Number(r.total ?? 0), foodCents: Number(r.food ?? 0), diningCents: Number(r.dining ?? 0) })) });
    }
    if (path === '/api/entries' && method === 'GET') {
      const user=await identity(req);requirePermission(user,'entries');
      const includeTest = url.searchParams.get('tests') === '1';
      if(includeTest&&!user.isOwner)throw new Problem('Os testes são exclusivos do administrador.',403);
      const filter = cardFilter(url,user,'e.');
      const page=Number(url.searchParams.get('page')??'1');const pageSize=25;
      if(!Number.isSafeInteger(page)||page<1||page>400)throw new Problem('Página inválida.');
      // Viewer rows have a fixed projection: never send raw SMS, ingestion keys,
      // device identities, hashes, review text, excluded entries or test data.
      const fields=user.isOwner?'e.*,d.name AS device_name,c.name AS card_name,c.brand AS card_brand,c.kind AS card_kind,c.parent_last4 AS card_parent_last4':`e.id,e.merchant,e.amount_cents,e.purchase_date,e.purchase_time,e.effective_category AS category,e.note,e.card_last4,e.installments,CASE WHEN e.period_needs_review=1 THEN 1 ELSE e.effective_needs_review END AS needs_review,e.status,CASE WHEN e.source IN ('sms_pix','manual_sms_pix') THEN 'pix' ELSE 'card' END AS payment_method,c.name AS card_name,c.brand AS card_brand,c.kind AS card_kind,c.parent_last4 AS card_parent_last4`;
      const query=(url.searchParams.get('q')??'').trim();
      if(query.length>100)throw new Problem('A busca deve ter até 100 caracteres.');
      const category=url.searchParams.get('category')??'all';
      if(category!=='all'&&!isCategory(category))throw new Problem('Categoria inválida.');
      // Partial matching tolerates one mistyped letter for queries of 3+ characters.
      const letters=[...normalize(query)].map(c=>c.replace(/[\\%_]/g,'\\$&'));
      const patterns=['%'+letters.join('')+'%'];
      if(/^[A-Z0-9]{3,30}$/.test(normalize(query)))for(let i=0;i<letters.length;i++)patterns.push('*'+letters.map((c,j)=>j===i?'[A-Z0-9]':c).join('')+'*');
      let merchantSQL='e.merchant';
      for(const c of 'áàâãäéèêëíìîïóòôõöúùûüçÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ')merchantSQL=`replace(${merchantSQL},'${c}','${normalize(c)}')`;
      const where=` WHERE e.is_test=?${!user.isOwner?" AND e.status='active'":''}${filter.sql}${query?` AND (${patterns.map((_,i)=>i===0?`upper(${merchantSQL}) LIKE ? ESCAPE '\\'`:`upper(${merchantSQL}) GLOB ?`).join(' OR ')})`:''}${category!=='all'?' AND e.effective_category=?':''}`;
      const values=[Number(includeTest),...filter.values,...(query?patterns:[]),...(category!=='all'?[category]:[])];
      const [rows,count]=await Promise.all([
        db().prepare(`SELECT ${fields} FROM ${EFFECTIVE_ENTRIES} e ${user.isOwner?'LEFT JOIN devices d ON d.id=e.device_id':''} LEFT JOIN card_profiles c ON c.last4=e.card_last4${where} ORDER BY e.received_at DESC LIMIT ? OFFSET ?`).bind(...values,pageSize,(page-1)*pageSize).all<Row>(),
        db().prepare(`SELECT COUNT(*) AS total FROM ${EFFECTIVE_ENTRIES} e${where}`).bind(...values).first<Row>(),
      ]);
      const total=Number(count?.total??0);return json({ entries: rows.results.map(entryResponse),page,pageSize,total,totalPages:Math.max(1,Math.ceil(total/pageSize)) });
    }
    if(path==='/api/periods'&&method==='GET'){const user=await identity(req);requirePermission(user,'periods');return json({periods:await spendingPeriods(user)});}
    const admin=await owner(req);

    if(path==='/api/periods'&&(method==='POST'||method==='PATCH'))return json(await saveSpendingPeriod(await body(req),method==='PATCH'),method==='POST'?201:200);
    if(path==='/api/card-registry'&&method==='GET'){
      const rows=await db().prepare("SELECT x.last4,p.name,p.brand,p.kind,p.parent_last4,p.match_rules,p.updated_at FROM (SELECT DISTINCT card_last4 AS last4 FROM entries WHERE card_last4 IS NOT NULL UNION SELECT last4 FROM card_profiles) x LEFT JOIN card_profiles p ON p.last4=x.last4 ORDER BY x.last4").all<Row>();
      return json({cards:rows.results.map(r=>({last4:r.last4,name:r.name??'',brand:r.brand??'unknown',kind:r.kind??'primary',parentLast4:r.parent_last4??null,matchRules:readMatchRules(r.match_rules),configured:Boolean(r.updated_at)}))});
    }
    if(path==='/api/card-registry'&&method==='PUT'){
      const input=cardProfileInput(await body(req));const now=new Date().toISOString();
      await db().prepare('INSERT INTO card_profiles (last4,name,brand,kind,parent_last4,match_rules,updated_at) VALUES (?,?,?,?,?,?,?) ON CONFLICT(last4) DO UPDATE SET name=excluded.name,brand=excluded.brand,kind=excluded.kind,parent_last4=excluded.parent_last4,match_rules=excluded.match_rules,updated_at=excluded.updated_at').bind(input.last4,input.name,input.brand,input.kind,input.parent,JSON.stringify(input.matchRules),now).run();
      return json({ok:true});
    }
    if(path==='/api/card-rules/apply'&&method==='POST'){
      const rows=await db().prepare("SELECT id,raw_text FROM entries WHERE card_last4 IS NULL AND source NOT IN ('sms_pix','manual_sms_pix') AND status='active' AND is_test=0 ORDER BY received_at DESC LIMIT 1000").all<Row>();let updated=0,ambiguous=0;
      for(const row of rows.results){const match=await cardMatch(row.raw_text);if(match.last4){const result=await db().prepare('UPDATE entries SET card_last4=?,updated_at=? WHERE id=? AND card_last4 IS NULL').bind(match.last4,new Date().toISOString(),row.id).run();updated+=Number(result.meta.changes??0);}else if(match.ambiguous)ambiguous++;}
      return json({ok:true,updated,ambiguous,checked:rows.results.length});
    }
    if(path==='/api/access'&&method==='GET'){
      const rows=await db().prepare('SELECT * FROM access_grants ORDER BY created_at DESC').all<Row>();
      return json({grants:rows.results.map(grantResponse)});
    }
    if(path==='/api/access'&&(method==='POST'||method==='PATCH')){
      const b=await body(req);if(method==='PATCH'&&b.includePix===undefined&&typeof b.id==='string'){const current=await db().prepare('SELECT include_pix FROM access_grants WHERE id=?').bind(b.id).first<Row>();b.includePix=current?.include_pix===1;}if(method==='PATCH'&&b.canPeriods===undefined&&typeof b.id==='string'){const current=await db().prepare('SELECT can_periods FROM access_grants WHERE id=?').bind(b.id).first<Row>();b.canPeriods=current?.can_periods===1;}const input=grantInput(b);const now=new Date().toISOString();
      if(input.email===admin.email)throw new Problem('Sua conta de administrador já tem acesso completo.');
      const existingEmail=await db().prepare('SELECT id FROM access_grants WHERE email=?').bind(input.email).first<Row>();
      if(existingEmail&&(method==='POST'||existingEmail.id!==b.id))throw new Problem('Este e-mail já está cadastrado. Edite o acesso existente.',409);
      if(method==='POST'){
        const count=await db().prepare('SELECT COUNT(*) AS n FROM access_grants').first<Row>();
        if(Number(count?.n)>=50)throw new Problem('Limite de 50 pessoas atingido.');
        const id=crypto.randomUUID();
        const result=await db().prepare('INSERT OR IGNORE INTO access_grants (id,email,name,enabled,can_summary,can_entries,can_periods,card_last4s,include_unknown,include_pix,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)').bind(id,input.email,input.name,input.enabled,input.canSummary,input.canEntries,input.canPeriods,JSON.stringify(input.cards),input.includeUnknown,input.includePix,now,now).run();
        if(!result.meta.changes)throw new Problem('Este e-mail já está cadastrado.',409);
        return json({ok:true,id},201);
      }
      if(typeof b.id!=='string')throw new Problem('Acesso inválido.');
      const current=await db().prepare('SELECT email,user_id FROM access_grants WHERE id=?').bind(b.id).first<Row>();
      if(!current)throw new Problem('Pessoa não encontrada.',404);
      if(current.user_id===admin.id)throw new Problem('O acesso do administrador não pode ser alterado.');
      if(current.email!==input.email)throw new Problem('Para outra conta, cadastre um novo acesso.');
      await db().prepare('UPDATE access_grants SET name=?,enabled=?,can_summary=?,can_entries=?,can_periods=?,card_last4s=?,include_unknown=?,include_pix=?,updated_at=? WHERE id=?').bind(input.name,input.enabled,input.canSummary,input.canEntries,input.canPeriods,JSON.stringify(input.cards),input.includeUnknown,input.includePix,now,b.id).run();
      return json({ok:true});
    }
    if (path === '/api/import' && method === 'POST') { const b = await body(req); return await ingest(b, null, 'manual_sms', b.isTest === true); }
    if (path === '/api/entries' && method === 'PATCH') {
      const b = await body(req);
      if (typeof b.id !== 'string') throw new Problem('Lançamento inválido.');
      if (b.status && !['active', 'excluded'].includes(b.status)) throw new Problem('Estado inválido.');
      if (b.status) { await db().prepare('UPDATE entries SET status=?,updated_at=? WHERE id=?').bind(b.status, new Date().toISOString(), b.id).run(); return json({ ok: true }); }
      const changesTime=Object.hasOwn(b,'purchaseTime');
      if(changesTime&&b.purchaseTime!==null&&(typeof b.purchaseTime!=='string'||!validTime(b.purchaseTime)))throw new Problem('Informe um horário válido, como 14:30, ou deixe em branco.');
      const changesCard = Object.hasOwn(b, 'cardLast4');
      if (changesCard && b.cardLast4 !== null) {
        const current = await db().prepare('SELECT source FROM entries WHERE id=?').bind(b.id).first<Row>();
        if (current?.source.endsWith('_pix')) throw new Problem('Pix não deve ser vinculado a um cartão.');
      }
      if (changesCard && b.cardLast4 !== null && (typeof b.cardLast4 !== 'string' || !/^\d{4}$/.test(b.cardLast4))) throw new Problem('Informe apenas os quatro últimos dígitos do cartão, ou deixe em branco.');
      const changesNote = Object.hasOwn(b, 'note');
      if (changesNote && (typeof b.note !== 'string' || b.note.length > 500)) throw new Problem('A observação deve ter até 500 caracteres.');
      if (!Number.isSafeInteger(b.amountCents) || b.amountCents <= 0 || b.amountCents > 100_000_000 || !isCategory(b.category) || b.category === 'unclassified' || typeof b.merchant !== 'string' || !b.merchant.trim() || b.merchant.length > 160 || typeof b.purchaseDate !== 'string' || !validDate(b.purchaseDate) || b.purchaseDate > todaySP()) throw new Problem('Confira valor, estabelecimento, categoria e data.');
      const result = await db().prepare("UPDATE entries SET amount_cents=?,merchant=?,category=?,purchase_date=?,purchase_time=CASE WHEN ? THEN ? ELSE purchase_time END,time_checked=CASE WHEN ? THEN 1 ELSE time_checked END,card_last4=CASE WHEN ? THEN ? ELSE card_last4 END,note=CASE WHEN ? THEN ? ELSE note END,needs_review=0,review_reason='',updated_at=? WHERE id=?").bind(b.amountCents, b.merchant.trim(), b.category, b.purchaseDate, Number(changesTime), b.purchaseTime??null, Number(changesTime), Number(changesCard), b.cardLast4 ?? null, Number(changesNote), changesNote ? b.note.trim() : '', new Date().toISOString(), b.id).run();
      if (!result.meta.changes) throw new Problem('Lançamento não encontrado.', 404);
      if (b.remember === true) await db().prepare('INSERT INTO rules (merchant_key,category) VALUES (?,?) ON CONFLICT(merchant_key) DO UPDATE SET category=excluded.category').bind(normalize(b.merchant), b.category).run();
      return json({ ok: true });
    }
    if (path === '/api/devices' && method === 'GET') {
      const devices = await db().prepare('SELECT id,name,created_at,last_received_at,revoked FROM devices ORDER BY created_at DESC').all();
      return json({ devices: devices.results, serviceReady: Boolean(env.SITE_SERVICE_TOKEN) });
    }
    if (path === '/api/devices' && method === 'POST') {
      const b = await body(req); if (typeof b.name !== 'string' || b.name.trim().length < 2 || b.name.length > 60) throw new Problem('Dê um nome ao iPhone.');
      if (!env.SITE_SERVICE_TOKEN) throw new Problem('A conexão externa ainda não foi configurada.', 503);
      const count = await db().prepare('SELECT COUNT(*) AS n FROM devices WHERE revoked=0').first<Row>();
      if (Number(count?.n) >= 10) throw new Problem('Revogue uma conexão antiga antes de criar outra.');
      const token = [...crypto.getRandomValues(new Uint8Array(32))].map(n => n.toString(16).padStart(2, '0')).join('');
      const id = crypto.randomUUID();
      await db().prepare('INSERT INTO devices (id,name,token_hash,created_at,revoked) VALUES (?,?,?,?,0)').bind(id, b.name.trim(), await hash(token), new Date().toISOString()).run();
      // Provisioning is explicit, owner-only and non-cacheable. Secrets are never
      // bundled into JavaScript or persisted in browser storage.
      return json({ id, endpoint: url.origin + '/api/sms', deviceKey: token, sitesAuthorization: 'Bearer ' + env.SITE_SERVICE_TOKEN }, 201);
    }
    if (path === '/api/devices' && method === 'DELETE') {
      const b = await body(req); if (typeof b.id !== 'string') throw new Problem('Conexão inválida.');
      await db().prepare('UPDATE devices SET revoked=1 WHERE id=?').bind(b.id).run(); return json({ ok: true });
    }
    throw new Problem('Página não encontrada.', 404);
  } catch (error) {
    if (error instanceof Problem || error instanceof AccessError) return json({ error: error.message }, error.status);
    console.error('Request failed', error instanceof Error ? error.name : 'UnknownError');
    return json({ error: 'Não foi possível concluir. Tente novamente; o resumo não confirma recebimento deste envio.' }, 500);
  }
}

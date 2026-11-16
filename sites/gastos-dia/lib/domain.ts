export const CATEGORIES = [
  { id: 'delivery', label: 'Delivery e refeições', food: true },
  { id: 'snacks', label: 'Padaria e snacks', food: true },
  { id: 'restaurants', label: 'Restaurantes', food: true },
  { id: 'groceries', label: 'Mercado e feira', food: true },
  { id: 'travel', label: 'Viagem', food: false },
  { id: 'transport', label: 'Transporte', food: false },
  { id: 'health', label: 'Saúde', food: false },
  { id: 'subscriptions', label: 'Assinaturas e serviços digitais', food: false },
  { id: 'home', label: 'Casa', food: false },
  { id: 'shopping', label: 'Compras', food: false },
  { id: 'leisure', label: 'Lazer', food: false },
  { id: 'other', label: 'Outros', food: false },
  { id: 'unclassified', label: 'A classificar', food: false },
] as const;
export type Category = typeof CATEGORIES[number]['id'];
export const money = (cents: number) => (cents / 100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
export function normalize(value: string) { return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/\s+/g, ' ').trim(); }
export function isCategory(value: unknown): value is Category { return CATEGORIES.some(c => c.id === value); }
export function moneyToCents(value: string): number | null {
  let s = value.trim().replace(/^R\$\s*/i, '').replace(/\s/g, '');
  if (/^\d{1,3}(\.\d{3})*,\d{2}$/.test(s) || /^\d+,\d{2}$/.test(s)) s = s.replace(/\./g, '').replace(',', '.');
  else if (!/^\d+(\.\d{1,2})?$/.test(s)) return null;
  const [whole, fraction = ''] = s.split('.');
  const amount = Number(whole) * 100 + Number(fraction.padEnd(2, '0'));
  return Number.isSafeInteger(amount) && amount > 0 && amount <= 100_000_000 ? amount : null;
}
export function todaySP(now = new Date()): string { return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit' }).format(now); }
export function validDate(value: string) { return /^\d{4}-\d{2}-\d{2}$/.test(value) && !isNaN(Date.parse(value)) && new Date(value + 'T12:00:00Z').toISOString().slice(0, 10) === value; }
export function periodRange(period: string, reference = todaySP()) {
  const date = new Date(reference + 'T12:00:00Z');
  let start = reference;
  if (period === 'month') start = reference.slice(0, 8) + '01';
  else if (period !== 'today') { date.setUTCDate(date.getUTCDate() - (date.getUTCDay() + 6) % 7); start = date.toISOString().slice(0, 10); }
  return { start, end: reference };
}
export function classify(merchant: string): Category {
  const m = normalize(merchant);
  if (/IFOOD|IFD\*|99FOOD|KEE\*/.test(m)) return 'delivery';
  if (/PADARIA|PANIFICADORA|SNACK|OAKBERRY|ROSSINI|CDBALBERICO|CAFECREME|DOCEIRA|CONFEITARIA|BOLOS/.test(m)) return 'snacks';
  if (/RESTAURAN|COCO BAMBU|OUTBACK|PECORINO|PE DE MANGA|CHEIADEMANIAS/.test(m)) return 'restaurants';
  if (/SUPERMERCADO|HIPERMERCADO|CARREFOUR|ASSAI|ATACADAO|HORTIFRUTI/.test(m)) return 'groceries';
  if (/UBER|99APP|99POP|POSTO |SHELL|IPIRANGA|ESTACIONAMENTO/.test(m)) return 'transport';
  if (/DROGARIA|FARMACIA|DROGASIL|DROGA RAIA/.test(m)) return 'health';
  if (/OPENAI|CHATGPT|GITHUB|NETFLIX|SPOTIFY|ONEDRIVE|MICROSOFT/.test(m)) return 'subscriptions';
  return 'unclassified';
}
export type ParsedSMS = { paymentMethod?: 'pix'; ignored: boolean; amountCents: number | null; merchant: string; category: Category; purchaseDate: string; purchaseTime: string | null; cardLast4: string | null; installments: number | null; reasons: string[]; hasMessageTime: boolean };
export function parseSMS(text: string, received = new Date()): ParsedSMS {
  const clean = text.replace(/\s+/g, ' ').trim();
  const n = normalize(clean);
  const fallback = todaySP(received);
  const result: ParsedSMS = { ignored: false, amountCents: null, merchant: '', category: 'unclassified', purchaseDate: fallback, purchaseTime: null, cardLast4: null, installments: null, reasons: [], hasMessageTime: false };
  // Itaú also sends temporary card authorizations and bill reminders from the
  // purchase-alert sender. Neither represents a new final purchase.
  if (/^(?:ITAU(?:CARD)?[:\s-]*)?PRE[- ]?AUTORIZACAO\b/.test(n) || /\bLEMBRAMOS QUE A FATURA\b/.test(n)) { result.ignored = true; result.reasons.push('Pré-autorização ou aviso de fatura: não somar como nova compra.'); return result; }
  if (/COMPRA (?:FOI )?(?:NEGADA|RECUSADA|NAO APROVADA)|CODIGO (?:DE |PARA )?(?:SEGURANCA|VERIFICACAO|ACESSO)|SENHA (?:DE |PARA )?ACESSO|TOKEN|FATURA (?:FECHOU|FECHADA|VENCE|PAGA)|PAGAMENTO (?:DA |DE )?FATURA/.test(n)) { result.ignored = true; result.reasons.push('Mensagem sem nova compra aprovada.'); return result; }
  const pix = /\bPIX\b/.test(n);
  if (pix) {
    result.paymentMethod = 'pix';
    if (/RECEB(?:IDO|IDA|EU|EMOS)|VOCE RECEBEU|CREDITAD/.test(n)) {
      result.ignored = true; result.reasons.push('Pix recebido: entrada não somada como gasto.'); return result;
    }
    if (/AGEND|PENDENTE|PROCESSANDO|EM PROCESSAMENTO|SOLICIT|COBRANCA|LIMITE|CHAVE|CODIGO|CONFIRME|CONFIRMAR|NAO (?:FOI )?(?:REALIZAD|ENVIAD|CONCLUID)|RECUSAD|NEGAD|FALH|CANCELAD|ESTORNO|DEVOL/.test(n)) {
      result.reasons.push('Pix sem saída confirmada ou possível devolução: confira a mensagem.'); return result;
    }
    if (!/PIX (?:FOI )?(?:ENVIADO|REALIZADO|EFETUADO|CONCLUIDO)|VOCE (?:ENVIOU|TRANSFERIU)|(?:ENVIO|TRANSFERENCIA|PAGAMENTO) (?:PIX )?(?:REALIZADO|REALIZADA|EFETUADO|EFETUADA|CONCLUIDO|CONCLUIDA)/.test(n)) {
      result.reasons.push('Não foi possível confirmar a saída do Pix.'); return result;
    }
  }
  if (!pix && !/COMPRA|TRANSACAO|PAGAMENTO APROVADO/.test(n)) { result.reasons.push('Não foi possível confirmar que a mensagem descreve uma compra.'); return result; }
  if (/ESTORNO|CANCELAD|DEVOLUCAO/.test(n)) { result.reasons.push('Possível estorno ou cancelamento: confira a compra original.'); return result; }
  // Some alerts use the letters "RS" instead of the currency symbol. Require
  // whitespace after RS so product identifiers such as RS232 are not amounts.
  const amounts = [...clean.matchAll(/\b(?:R\$\s*|RS\s+)(\d[\d.,]*\d|\d)/gi)];
  if (/US\$|USD|EUR|EURO|GBP|DOLAR/.test(n)) result.reasons.push('Compra em moeda estrangeira: informe o valor final em reais.');
  else if (amounts.length === 1) result.amountCents = moneyToCents(amounts[0][1]);
  else result.reasons.push(amounts.length ? 'Há mais de um valor na mensagem: confirme o valor da compra.' : 'Valor em reais não identificado.');
  if (amounts.length === 1 && result.amountCents === null && !result.reasons.length) result.reasons.push('Formato do valor não reconhecido.');
  const dm = clean.match(/\b(\d{2})\/(\d{2})(?:\/(\d{2,4}))?\b/);
  if (dm) {
    let year = dm[3] ? Number(dm[3].length === 2 ? '20' + dm[3] : dm[3]) : Number(fallback.slice(0, 4));
    let candidate = `${year}-${dm[2]}-${dm[1]}`;
    if (!dm[3] && candidate > fallback && fallback.slice(5, 7) === '01' && dm[2] === '12') candidate = `${--year}-${dm[2]}-${dm[1]}`;
    if (validDate(candidate) && candidate <= fallback) {
      result.purchaseDate = candidate;
      const times = [...clean.matchAll(/\b(\d{2})[:h](\d{2})\b/gi)];
      if (times.length === 1 && validTime(times[0][1] + ':' + times[0][2])) result.purchaseTime = times[0][1] + ':' + times[0][2];
    }
    else result.reasons.push('Data da compra inválida ou futura: confira a data.');
    result.hasMessageTime = /\b\d{2}[:h]\d{2}\b/.test(clean);
  } else result.reasons.push('Data não identificada: usada a data de recebimento.');
  if (pix) {
    const recipient = clean.match(/\bpara\s+(.+?)(?=,|;|\s+(?:CPF|CNPJ|em\s+\d{2}\/|dia\s+\d{2}\/|no valor|valor|via Pix)|$)/i)?.[1];
    result.merchant = recipient?.replace(/[.\s]+$/, '').slice(0,160) ?? '';
    result.reasons.push('Pix enviado: confirme a categoria e se representa um gasto; transferências próprias ou reembolsos podem ser excluídos.');
    if (!result.merchant) result.reasons.push('Destinatário não identificado.');
    return result;
  }
  result.cardLast4 = clean.match(/(?:final|terminad[oa]\s+em|\*{2,})\s*[:*\-]?\s*(\d{4})\b/i)?.[1] ?? null;
  const installments = clean.match(/\b(?:em\s+)?(\d{1,2})\s*(?:x\b|parcelas?\b)/i);
  if (installments) { result.installments = Number(installments[1]); result.reasons.push('Compra parcelada: confirme que o SMS mostra o valor total da compra.'); }
  const merchantMatches = [...clean.matchAll(/\b(?:em|no estabelecimento|estabelecimento:?)\s+([^,;]+?)(?=\s+(?:dia\s+)?\d{2}\/\d{2}|\s+(?:no )?(?:valor|cart[aã]o|cr[eé]dito|d[eé]bito|limite|saldo)\b|[,;]|$)/gi)];
  // Personnalité purchase alerts put the merchant after the card/cardholder
  // description: "Compra aprovada ... - LOJA valor R$ ... em DD/MM, as HHhMM".
  // Cardholder text belongs to the prefix, never to the merchant/category.
  const itauMerchant = clean.match(/\bcompra aprovada\b.*?\s[-–]\s+(.+?)\s+(?:no\s+)?valor\s*:?\s*(?:R\$|RS\s+(?=\d))/i)?.[1];
  const merchant = itauMerchant?.trim() ?? merchantMatches.map(m => m[1].trim()).filter(m => !/^\d|^R\$|^seu |^seu$/i.test(m)).at(-1);
  if (merchant) result.merchant = merchant.replace(/\s*[-.]\s*$/, '').slice(0, 160);
  if (!result.merchant) result.reasons.push('Estabelecimento não identificado.');
  result.category = classify(result.merchant);
  if (result.category === 'unclassified') result.reasons.push('Escolha a categoria.');
  return result;
}
export async function hash(value: string): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
  return [...new Uint8Array(digest)].map(x => x.toString(16).padStart(2, '0')).join('');
}

export function validTime(value: string) { return /^(?:[01]\d|2[0-3]):[0-5]\d$/.test(value); }
export function validLocalDateTime(value: string) { return typeof value === 'string' && value.length === 16 && value[10] === 'T' && validDate(value.slice(0,10)) && validTime(value.slice(11)); }

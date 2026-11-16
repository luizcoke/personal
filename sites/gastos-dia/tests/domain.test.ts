import test from 'node:test';
import assert from 'node:assert/strict';
import { moneyToCents, parseSMS, periodRange, todaySP, classify, validDate, validTime, validLocalDateTime } from '../lib/domain.ts';
const received = new Date('2026-10-10T18:00:00Z');
test('dinheiro usa centavos e rejeita formatos ambíguos',()=>{
  for(const [value,expected] of [['25,90',2590],['1.234,56',123456],['R$ 0,01',1],['1500.50',150050],['1500',150000]] as const)assert.equal(moneyToCents(value),expected);
  for(const value of ['1,234','1.234','-25','NaN','1e3','0','9999999999999'])assert.equal(moneyToCents(value),null);
});
test('captura SMS de aprovação com data e loja',()=>{
 const p=parseSMS('ITAU: Compra aprovada no cartao final 1234, em 10/10 as 14:35, no valor de R$ 12,90, em PADARIA EXEMPLO.',received);
 assert.equal(p.amountCents,1290);assert.equal(p.merchant,'PADARIA EXEMPLO');assert.equal(p.purchaseDate,'2026-10-10');assert.equal(p.cardLast4,'1234');assert.equal(p.category,'snacks');assert.deepEqual(p.reasons,[]);assert.equal(p.hasMessageTime,true);
});
test('aceita separador de milhar e estabelecimento antes da data',()=>{
 const p=parseSMS('ITAU: Compra aprovada! R$ 1.234,56 em IFD*RESTAURANTE EXEMPLO dia 09/10 12:05. Cartao final 4321',received);
 assert.equal(p.amountCents,123456);assert.equal(p.merchant,'IFD*RESTAURANTE EXEMPLO');assert.equal(p.category,'delivery');assert.equal(p.purchaseDate,'2026-10-09');
});

test('Personnalité reconhece loja após o cartão, valor e hora com h',()=>{
 const p=parseSMS('Compra aprovada no seu PERSON BLACK PONTOS final 1234 - PANIFICADORA EXEMPLO valor R$ 24,90 em 08/10, as 19h26.',received);
 assert.equal(p.amountCents,2490);assert.equal(p.merchant,'PANIFICADORA EXEMPLO');assert.equal(p.purchaseDate,'2026-10-08');assert.equal(p.cardLast4,'1234');assert.equal(p.category,'snacks');assert.equal(p.hasMessageTime,true);assert.deepEqual(p.reasons,[]);
});

test('Personnalité separa titular e loja em compra de cartão adicional',()=>{
 const p=parseSMS('Compra aprovada no PERSON BLACK PONTOS p/ CLIENTE EXEMPLO - DL *UberRides valor R$ 17,80 em 08/10/2026 as 11h03.',received);
 assert.equal(p.amountCents,1780);assert.equal(p.merchant,'DL *UberRides');assert.equal(p.purchaseDate,'2026-10-08');assert.equal(p.cardLast4,null);assert.equal(p.category,'transport');assert.equal(p.hasMessageTime,true);assert.deepEqual(p.reasons,[]);
});

test('Personnalité aceita RS com espaço e preserva centavos, loja e categoria',()=>{
 for(const [value,expected] of [['24,90',2490],['1.234,56',123456],['0,01',1]] as const){
  const p=parseSMS(`Compra aprovada no seu PERSON BLACK PONTOS final 1234 - PANIFICADORA EXEMPLO valor RS ${value} em 08/10, as 19h26.`,received);
  assert.equal(p.amountCents,expected);assert.equal(p.merchant,'PANIFICADORA EXEMPLO');assert.equal(p.category,'snacks');assert.equal(p.purchaseDate,'2026-10-08');assert.deepEqual(p.reasons,[]);
 }
});

test('final de cartão preserva zero inicial e não deduz cartão pelo titular',()=>{
 const p=parseSMS('Compra aprovada no seu PERSON BLACK PONTOS final 0123 - PADARIA EXEMPLO valor RS 36,27 em 08/10, as 19h26.',received);
 assert.equal(p.cardLast4,'0123');
 const additional=parseSMS('Compra aprovada no PERSON BLACK PONTOS p/ CLIENTE EXEMPLO - DL *UberRides valor RS 17,80 em 08/10/2026 as 11h03.',received);
 assert.equal(additional.cardLast4,null);
});

test('variante RS não aceita códigos nem mistura múltiplos valores',()=>{
 for(const message of [
  'Compra aprovada valor RS232 em LOJA EXEMPLO dia 08/10 19:26',
  'Compra aprovada valor RS 24,90 limite R$ 1.000,00 em PADARIA dia 08/10 19:26',
  'Compra aprovada valor R$ 24,90 limite RS 1.000,00 em PADARIA dia 08/10 19:26',
  'Compra aprovada USD 20,00 equivalente RS 100,00 em LOJA dia 08/10 19:26',
  'Estorno da compra RS 24,90 em PADARIA dia 08/10 19:26',
 ]) assert.equal(parseSMS(message,received).amountCents,null);
});

test('Personnalité não soma pré-autorização, estorno ou lembrete de fatura',()=>{
 for(const message of [
  'Pre-autorizacao aprovada no seu PERSON BLACK PONTOS final 1234 - DL *UberRides valor R$ 15,50 em 08/10, as 10h49.',
  'Pré-autorização aprovada para compra no cartão final 1234 valor R$ 15,50.',
  'Lembramos que a fatura do seu PERSON BLACK PONTOS esta em debito automatico, o valor total e de R$ 1.234,56 e vence em 15/10',
 ]){const p=parseSMS(message,received);assert.equal(p.ignored,true);assert.equal(p.amountCents,null);}
 const reversal=parseSMS('Confirmamos o estorno da compra no seu PERSON BLACK PONTOS final 1234 - DL *UberRides valor R$ 15,50 em 08/10/2026 as 10h49.',received);
 assert.equal(reversal.ignored,false);assert.equal(reversal.amountCents,null);assert.match(reversal.reasons.join(' '),/estorno/i);
});
test('não conta fatura, compra negada ou código de acesso',()=>{
 for(const message of ['Compra negada de R$ 100,00','Compra nao aprovada de R$ 20,00','Pagamento da fatura R$ 500,00','Codigo de seguranca 123456 para compra'])assert.equal(parseSMS(message,received).ignored,true);
});
test('ambiguidade, moeda estrangeira e estorno não alteram o total',()=>{
 for(const message of ['Compra aprovada US$ 20,00 em OPENAI','Compra aprovada R$ 20,00 limite R$ 1.000,00','Estorno da compra de R$ 20,00','Compra cancelada R$ 30,00','Olá tudo bem R$ 5,00']){const p=parseSMS(message,received);assert.equal(p.amountCents,null);assert.ok(p.reasons.length);}
});
test('sem data ou loja, solicita revisão; parcela mantém total',()=>{
 const p=parseSMS('Compra aprovada R$ 300,00 em 3 parcelas',received);
 assert.equal(p.amountCents,30000);assert.equal(p.installments,3);assert.ok(p.reasons.length>=2);assert.equal(p.purchaseDate,'2026-10-10');
});
test('datas brasileiras e limites de semana em São Paulo',()=>{
 assert.equal(todaySP(new Date('2026-10-11T01:00:00Z')),'2026-10-10');
 assert.deepEqual(periodRange('week','2026-10-11'),{start:'2026-10-05',end:'2026-10-11'});
 assert.deepEqual(periodRange('week','2026-10-12'),{start:'2026-10-12',end:'2026-10-12'});
 assert.deepEqual(periodRange('month','2026-10-10'),{start:'2026-10-01',end:'2026-10-10'});
 assert.equal(validDate('2026-02-30'),false);
 assert.equal(parseSMS('Compra R$ 1,00 em PADARIA dia 31/12 15:00',new Date('2027-01-01T15:00:00Z')).purchaseDate,'2026-12-31');
});
test('classificações não confundem delivery com transporte/restaurante',()=>{
 assert.equal(classify('99Food *Pizza Hut'),'delivery');assert.equal(classify('ROSSINI EVENTOS'),'snacks');assert.equal(classify('OPENAI'),'subscriptions');assert.equal(classify('LOJA DESCONHECIDA'),'unclassified');
});

test('horário da compra preserva HH:mm e HHhmm, sem usar o recebimento',()=>{
 const received=new Date('2026-10-25T18:00:00Z');
 for(const time of ['09:45','09h45'])assert.equal(parseSMS('Compra aprovada R$ 12,90 em PADARIA dia 23/10/2026 as '+time,received).purchaseTime,'09:45');
 for(const time of ['25:10','12:99',''])assert.equal(parseSMS('Compra aprovada R$ 12,90 em PADARIA dia 23/10/2026 '+time,received).purchaseTime,null);
 assert.equal(parseSMS('Compra aprovada R$ 12,90 em PADARIA as 09:45',received).purchaseTime,null);
 assert.equal(parseSMS('Compra aprovada R$ 12,90 em PADARIA dia 23/10/2026 09:45 12:30',received).purchaseTime,null);
 assert.equal(validTime('23:59'),true);assert.equal(validTime('24:00'),false);
 assert.equal(validLocalDateTime('2026-10-23T18:30'),true);
 for(const value of ['2026-02-30T10:00','2026-10-23T25:10','2026-10-23T09:00Z'])assert.equal(validLocalDateTime(value),false);
});

test('Pix enviado extrai valor e destinatário sem inventar cartão ou categoria',()=>{
 const p=parseSMS('Feito. Pix enviado Você enviou R$ 220,00 para PALOMA, CPF XXX.815.502-XX.',received);
 assert.equal(p.paymentMethod,'pix'); assert.equal(p.amountCents,22000); assert.equal(p.merchant,'PALOMA'); assert.equal(p.cardLast4,null); assert.equal(p.category,'unclassified'); assert.ok(p.reasons.length);
 const dated=parseSMS('ITAU: Pix enviado de R$ 1.234,56 para LOJA EXEMPLO em 10/10/2026 as 13:31.',received);
 assert.equal(dated.amountCents,123456); assert.equal(dated.merchant,'LOJA EXEMPLO'); assert.equal(dated.purchaseTime,'13:31'); assert.equal(dated.hasMessageTime,true);
});
test('Pix recebido não é gasto e textos ambíguos não recebem valor',()=>{
 for(const message of ['Pix recebido R$ 20,00 de MARIA','Você recebeu um Pix de R$ 20,00']) assert.equal(parseSMS(message,received).ignored,true);
 for(const message of ['Pix agendado R$ 20,00 para MARIA','Pix não foi enviado R$ 20,00','Pix enviado cancelado R$ 20,00','Confirme seu Pix R$ 20,00','Pix R$ 20,00','Pix enviado R$ 20,00 saldo R$ 500,00','Devolução Pix enviado R$ 20,00']) {
  const p=parseSMS(message,received); assert.equal(p.amountCents,null,message); assert.ok(p.reasons.length,message);
 }
});

-- Reconcilia as compras aprovadas visíveis nas capturas de SMS de 30/09 a 13/10.
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-09-30-1219-3878-1400',NULL,'sms-reconcile-2026-09-30-1219-3878-1400','sms-reconcile-2026-09-30-1219-3878-1400','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - MP *STEFANYPEREIRA valor RS 14,00 em 30/09/2026 as 12h19.',1400,'MP *STEFANYPEREIRA','unclassified','','2026-09-30','3878',NULL,1,'Escolha a categoria.','active','sms_screenshot_reconciliation',0,'2026-09-30T12:19:00-03:00','2026-09-30T12:19:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-09-30' AND amount_cents=1400 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-01-1137-3878-3199',NULL,'sms-reconcile-2026-10-01-1137-3878-3199','sms-reconcile-2026-10-01-1137-3878-3199','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - AMERICANAS SA valor RS 31,99 em 01/10/2026 as 11h37.',3199,'AMERICANAS SA','shopping','','2026-10-01','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-01T11:37:00-03:00','2026-10-01T11:37:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-01' AND amount_cents=3199 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-01-1332-3878-8997',NULL,'sms-reconcile-2026-10-01-1332-3878-8997','sms-reconcile-2026-10-01-1332-3878-8997','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - LOJA DO TED LAPA valor RS 89,97 em 01/10/2026 as 13h32.',8997,'LOJA DO TED LAPA','shopping','','2026-10-01','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-01T13:32:00-03:00','2026-10-01T13:32:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-01' AND amount_cents=8997 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-01-2020-7396-7567',NULL,'sms-reconcile-2026-10-01-2020-7396-7567','sms-reconcile-2026-10-01-2020-7396-7567','Compra aprovada de R$ 75,67 em 99Food Imigrantes, 01/10 as 20:20 no seu Itau final 7396.',7567,'99Food Imigrantes','delivery','','2026-10-01','7396',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-01T20:20:00-03:00','2026-10-01T20:20:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-01' AND amount_cents=7567 AND COALESCE(card_last4,'')='7396' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-02-0948-3878-920',NULL,'sms-reconcile-2026-10-02-0948-3878-920','sms-reconcile-2026-10-02-0948-3878-920','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - 99APP *99App valor RS 9,20 em 02/10/2026 as 09h48.',920,'99APP *99App','transport','','2026-10-02','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-02T09:48:00-03:00','2026-10-02T09:48:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-02' AND amount_cents=920 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-02-1938-3878-45327',NULL,'sms-reconcile-2026-10-02-1938-3878-45327','sms-reconcile-2026-10-02-1938-3878-45327','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - MERCADO VIOLETA valor RS 453,27 em 02/10/2026 as 19h38.',45327,'MERCADO VIOLETA','groceries','','2026-10-02','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-02T19:38:00-03:00','2026-10-02T19:38:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-02' AND amount_cents=45327 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-03-0949-0539-1600',NULL,'sms-reconcile-2026-10-03-0949-0539-1600','sms-reconcile-2026-10-03-0949-0539-1600','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - AUTO POSTO ALBION LTD valor RS 16,00 em 03/10, as 09h49.',1600,'AUTO POSTO ALBION LTD','transport','','2026-10-03','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-03T09:49:00-03:00','2026-10-03T09:49:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-03' AND amount_cents=1600 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-03-1140-0539-800',NULL,'sms-reconcile-2026-10-03-1140-0539-800','sms-reconcile-2026-10-03-1140-0539-800','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - DRT LANCHONETE valor RS 8,00 em 03/10, as 11h40.',800,'DRT LANCHONETE','restaurants','','2026-10-03','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-03T11:40:00-03:00','2026-10-03T11:40:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-03' AND amount_cents=800 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-03-1241-0539-1000',NULL,'sms-reconcile-2026-10-03-1241-0539-1000','sms-reconcile-2026-10-03-1241-0539-1000','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - DRT LANCHONETE valor RS 10,00 em 03/10, as 12h41.',1000,'DRT LANCHONETE','restaurants','','2026-10-03','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-03T12:41:00-03:00','2026-10-03T12:41:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-03' AND amount_cents=1000 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-03-1741-0539-600',NULL,'sms-reconcile-2026-10-03-1741-0539-600','sms-reconcile-2026-10-03-1741-0539-600','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - PRACA PANAMERICANA valor RS 6,00 em 03/10, as 17h41.',600,'PRACA PANAMERICANA','other','','2026-10-03','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-03T17:41:00-03:00','2026-10-03T17:41:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-03' AND amount_cents=600 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-03-1803-0539-9900',NULL,'sms-reconcile-2026-10-03-1803-0539-9900','sms-reconcile-2026-10-03-1803-0539-9900','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - RAIA25 valor RS 99,00 em 03/10, as 18h03.',9900,'RAIA25','health','','2026-10-03','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-03T18:03:00-03:00','2026-10-03T18:03:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-03' AND amount_cents=9900 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-03-1235-2587-1725',NULL,'sms-reconcile-2026-10-03-1235-2587-1725','sms-reconcile-2026-10-03-1235-2587-1725','Compra aprovada de R$ 17,25 em ASSOCIACAO ATLETI, 03/10 as 12:35 no seu Itau final 2587.',1725,'ASSOCIACAO ATLETI','leisure','','2026-10-03','2587',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-03T12:35:00-03:00','2026-10-03T12:35:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-03' AND amount_cents=1725 AND COALESCE(card_last4,'')='2587' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-04-1511-0539-20611',NULL,'sms-reconcile-2026-10-04-1511-0539-20611','sms-reconcile-2026-10-04-1511-0539-20611','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - CheiaDeManiasBarE valor RS 206,11 em 04/10, as 15h11.',20611,'CheiaDeManiasBarE','restaurants','','2026-10-04','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-04T15:11:00-03:00','2026-10-04T15:11:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-04' AND amount_cents=20611 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-04-1548-3878-16178',NULL,'sms-reconcile-2026-10-04-1548-3878-16178','sms-reconcile-2026-10-04-1548-3878-16178','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - POSTO DE SERVICOS PAZ valor RS 161,78 em 04/10/2026 as 15h48.',16178,'POSTO DE SERVICOS PAZ','transport','','2026-10-04','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-04T15:48:00-03:00','2026-10-04T15:48:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-04' AND amount_cents=16178 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-04-1632-0539-3468',NULL,'sms-reconcile-2026-10-04-1632-0539-3468','sms-reconcile-2026-10-04-1632-0539-3468','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - PAO DE ACUCAR-2352 valor RS 34,68 em 04/10, as 16h32.',3468,'PAO DE ACUCAR-2352','groceries','','2026-10-04','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-04T16:32:00-03:00','2026-10-04T16:32:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-04' AND amount_cents=3468 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-05-1222-3878-31497',NULL,'sms-reconcile-2026-10-05-1222-3878-31497','sms-reconcile-2026-10-05-1222-3878-31497','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - RAIA DROGASIL SA valor RS 314,97 em 05/10/2026 as 12h22.',31497,'RAIA DROGASIL SA','health','','2026-10-05','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-05T12:22:00-03:00','2026-10-05T12:22:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-05' AND amount_cents=31497 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-05-2052-1929-3490',NULL,'sms-reconcile-2026-10-05-2052-1929-3490','sms-reconcile-2026-10-05-2052-1929-3490','Compra aprovada no seu PERSON BLACK PONTOS final 1929 - Amazon Digital BR valor RS 34,90 em 05/10, as 20h52.',3490,'Amazon Digital BR','shopping','','2026-10-05','1929',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-05T20:52:00-03:00','2026-10-05T20:52:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-05' AND amount_cents=3490 AND COALESCE(card_last4,'')='1929' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-06-0835-3878-26880',NULL,'sms-reconcile-2026-10-06-0835-3878-26880','sms-reconcile-2026-10-06-0835-3878-26880','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - Sympla*Sympla-0AWT valor RS 268,80 em 06/10/2026 as 08h35.',26880,'Sympla*Sympla-0AWT','leisure','','2026-10-06','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-06T08:35:00-03:00','2026-10-06T08:35:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-06' AND amount_cents=26880 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-06-1306-3878-500',NULL,'sms-reconcile-2026-10-06-1306-3878-500','sms-reconcile-2026-10-06-1306-3878-500','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - LuisDaviDeLira valor RS 5,00 em 06/10/2026 as 13h06.',500,'LuisDaviDeLira','other','','2026-10-06','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-06T13:06:00-03:00','2026-10-06T13:06:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-06' AND amount_cents=500 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-07-1910-1929-52500',NULL,'sms-reconcile-2026-10-07-1910-1929-52500','sms-reconcile-2026-10-07-1910-1929-52500','Compra aprovada no seu PERSON BLACK PONTOS final 1929 - OPENAI *CHATGPT SUBSCR valor RS 525,00 em 07/10, as 19h10.',52500,'OPENAI *CHATGPT SUBSCR','subscriptions','','2026-10-07','1929',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-07T19:10:00-03:00','2026-10-07T19:10:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-07' AND amount_cents=52500 AND COALESCE(card_last4,'')='1929' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-07-2003-7396-4455',NULL,'sms-reconcile-2026-10-07-2003-7396-4455','sms-reconcile-2026-10-07-2003-7396-4455','Compra aprovada de R$ 44,55 em 99Food Hora, 07/10 as 20:03 no seu Itau final 7396.',4455,'99Food Hora','delivery','','2026-10-07','7396',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-07T20:03:00-03:00','2026-10-07T20:03:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-07' AND amount_cents=4455 AND COALESCE(card_last4,'')='7396' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-11-0755-0539-1000',NULL,'sms-reconcile-2026-10-11-0755-0539-1000','sms-reconcile-2026-10-11-0755-0539-1000','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - PANIFICADORA BELLA ALB valor RS 10,00 em 11/10, as 07h55.',1000,'PANIFICADORA BELLA ALB','snacks','','2026-10-11','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-11T07:55:00-03:00','2026-10-11T07:55:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-11' AND amount_cents=1000 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-11-1227-0539-19741',NULL,'sms-reconcile-2026-10-11-1227-0539-19741','sms-reconcile-2026-10-11-1227-0539-19741','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - ASSOCIACAO ATLETICA B valor RS 197,41 em 11/10, as 12h27.',19741,'ASSOCIACAO ATLETICA B','leisure','','2026-10-11','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-11T12:27:00-03:00','2026-10-11T12:27:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-11' AND amount_cents=19741 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-11-1443-0539-1800',NULL,'sms-reconcile-2026-10-11-1443-0539-1800','sms-reconcile-2026-10-11-1443-0539-1800','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - AGUA NA BOCA DOCEIRA L valor RS 18,00 em 11/10, as 14h43.',1800,'AGUA NA BOCA DOCEIRA L','snacks','','2026-10-11','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-11T14:43:00-03:00','2026-10-11T14:43:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-11' AND amount_cents=1800 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-11-1731-0539-600',NULL,'sms-reconcile-2026-10-11-1731-0539-600','sms-reconcile-2026-10-11-1731-0539-600','Compra aprovada no seu PERSON BLACK PONTOS final 0539 - AV ROBERT KENNEDY valor RS 6,00 em 11/10, as 17h31.',600,'AV ROBERT KENNEDY','other','','2026-10-11','0539',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-11T17:31:00-03:00','2026-10-11T17:31:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-11' AND amount_cents=600 AND COALESCE(card_last4,'')='0539' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-11-1810-3878-2468',NULL,'sms-reconcile-2026-10-11-1810-3878-2468','sms-reconcile-2026-10-11-1810-3878-2468','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - RAIA24 valor RS 24,68 em 11/10/2026 as 18h10.',2468,'RAIA24','health','','2026-10-11','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-11T18:10:00-03:00','2026-10-11T18:10:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-11' AND amount_cents=2468 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
INSERT INTO entries (id,device_id,event_key,message_hash,raw_text,amount_cents,merchant,category,note,purchase_date,card_last4,installments,needs_review,review_reason,status,source,is_test,received_at,updated_at)
SELECT 'sms-reconcile-2026-10-12-0905-3878-31999',NULL,'sms-reconcile-2026-10-12-0905-3878-31999','sms-reconcile-2026-10-12-0905-3878-31999','Compra aprovada no PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE - Wellhub Isabela Paixao valor RS 319,99 em 12/10/2026 as 09h05.',31999,'Wellhub Isabela Paixao','subscriptions','','2026-10-12','3878',NULL,0,'','active','sms_screenshot_reconciliation',0,'2026-10-12T09:05:00-03:00','2026-10-12T09:05:00-03:00'
WHERE NOT EXISTS (SELECT 1 FROM entries WHERE purchase_date='2026-10-12' AND amount_cents=31999 AND COALESCE(card_last4,'')='3878' AND status='active' AND is_test=0);
--> statement-breakpoint
-- Remove somente repetições exatas do mesmo SMS; compras diferentes com o mesmo valor são preservadas.
DELETE FROM entries
WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY message_hash,is_test ORDER BY received_at,id) AS duplicate_number
    FROM entries
    WHERE status='active'
  ) WHERE duplicate_number > 1
);

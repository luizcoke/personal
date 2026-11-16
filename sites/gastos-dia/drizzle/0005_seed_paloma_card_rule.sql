-- Inicializa a regra confirmada para o cartão adicional da Paloma.
UPDATE `card_profiles`
SET `match_rules` = '["PERSON BLACK PONTOS p/ PALOMA PAIXAO COKE"]',
    `updated_at` = CURRENT_TIMESTAMP
WHERE `last4` = '3878'
  AND (`match_rules` = '[]' OR `match_rules` IS NULL);
--> statement-breakpoint
UPDATE `entries`
SET `card_last4` = '3878',
    `updated_at` = CURRENT_TIMESTAMP
WHERE `card_last4` IS NULL
  AND `status` = 'active'
  AND `is_test` = 0
  AND UPPER(`raw_text`) LIKE '%PERSON BLACK PONTOS P/ PALOMA PAIXAO COKE%';

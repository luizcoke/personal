import { sqliteTable, text, integer, index } from 'drizzle-orm/sqlite-core';

export const settings = sqliteTable('settings', {
  key: text('key').primaryKey(), value: text('value').notNull(),
});
export const devices = sqliteTable('devices', {
  id: text('id').primaryKey(), name: text('name').notNull(),
  tokenHash: text('token_hash').notNull().unique(),
  createdAt: text('created_at').notNull(), lastReceivedAt: text('last_received_at'),
  revoked: integer('revoked').notNull().default(0),
});
export const entries = sqliteTable('entries', {
  id: text('id').primaryKey(), deviceId: text('device_id'),
  eventKey: text('event_key').notNull().unique(), messageHash: text('message_hash').notNull(),
  rawText: text('raw_text').notNull(), amountCents: integer('amount_cents'),
  merchant: text('merchant').notNull(), category: text('category').notNull(),
  note: text('note').notNull().default(''),
  purchaseDate: text('purchase_date').notNull(), purchaseTime: text('purchase_time'), timeChecked: integer('time_checked').notNull().default(0), cardLast4: text('card_last4'),
  installments: integer('installments'), needsReview: integer('needs_review').notNull().default(1),
  reviewReason: text('review_reason').notNull(), status: text('status').notNull().default('active'),
  source: text('source').notNull(), isTest: integer('is_test').notNull().default(0),
  receivedAt: text('received_at').notNull(), updatedAt: text('updated_at').notNull(),
}, (t) => [index('entries_period').on(t.purchaseDate, t.isTest, t.status), index('entries_dedupe').on(t.deviceId, t.messageHash, t.receivedAt)]);
export const rules = sqliteTable('rules', {
  merchantKey: text('merchant_key').primaryKey(), category: text('category').notNull(),
});

export const cardProfiles = sqliteTable('card_profiles', {
  last4: text('last4').primaryKey(), name: text('name').notNull().default(''),
  brand: text('brand').notNull().default('unknown'), kind: text('kind').notNull().default('primary'),
  parentLast4: text('parent_last4'), matchRules: text('match_rules').notNull().default('[]'),
  updatedAt: text('updated_at').notNull(),
});

export const accessGrants = sqliteTable('access_grants', {
  id: text('id').primaryKey(), email: text('email').notNull().unique(),
  userId: text('user_id').unique(), name: text('name').notNull(),
  enabled: integer('enabled').notNull().default(1),
  canSummary: integer('can_summary').notNull().default(0),
  canEntries: integer('can_entries').notNull().default(0),
  canPeriods: integer('can_periods').notNull().default(0),
  cardLast4s: text('card_last4s').notNull().default('[]'),
  includePix: integer('include_pix').notNull().default(0),
  includeUnknown: integer('include_unknown').notNull().default(0),
  createdAt: text('created_at').notNull(), updatedAt: text('updated_at').notNull(),
  linkedAt: text('linked_at'),
});

export const spendingPeriods = sqliteTable('spending_periods', {
  id: text('id').primaryKey(), name: text('name').notNull(),
  startsAt: text('starts_at').notNull(), endsAt: text('ends_at').notNull(),
  category: text('category').notNull(), enabled: integer('enabled').notNull().default(1),
  createdAt: text('created_at').notNull(), updatedAt: text('updated_at').notNull(),
}, (t) => [index('spending_periods_range').on(t.enabled, t.startsAt, t.endsAt)]);

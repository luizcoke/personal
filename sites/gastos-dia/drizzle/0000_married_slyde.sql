CREATE TABLE `devices` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`token_hash` text NOT NULL,
	`created_at` text NOT NULL,
	`last_received_at` text,
	`revoked` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `devices_token_hash_unique` ON `devices` (`token_hash`);--> statement-breakpoint
CREATE TABLE `entries` (
	`id` text PRIMARY KEY NOT NULL,
	`device_id` text,
	`event_key` text NOT NULL,
	`message_hash` text NOT NULL,
	`raw_text` text NOT NULL,
	`amount_cents` integer,
	`merchant` text NOT NULL,
	`category` text NOT NULL,
	`purchase_date` text NOT NULL,
	`card_last4` text,
	`installments` integer,
	`needs_review` integer DEFAULT 1 NOT NULL,
	`review_reason` text NOT NULL,
	`status` text DEFAULT 'active' NOT NULL,
	`source` text NOT NULL,
	`is_test` integer DEFAULT 0 NOT NULL,
	`received_at` text NOT NULL,
	`updated_at` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `entries_event_key_unique` ON `entries` (`event_key`);--> statement-breakpoint
CREATE INDEX `entries_period` ON `entries` (`purchase_date`,`is_test`,`status`);--> statement-breakpoint
CREATE INDEX `entries_dedupe` ON `entries` (`device_id`,`message_hash`,`received_at`);--> statement-breakpoint
CREATE TABLE `rules` (
	`merchant_key` text PRIMARY KEY NOT NULL,
	`category` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `settings` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL
);

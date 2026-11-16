CREATE TABLE `access_grants` (
	`id` text PRIMARY KEY NOT NULL,
	`email` text NOT NULL,
	`user_id` text,
	`name` text NOT NULL,
	`enabled` integer DEFAULT 1 NOT NULL,
	`can_summary` integer DEFAULT 0 NOT NULL,
	`can_entries` integer DEFAULT 0 NOT NULL,
	`card_last4s` text DEFAULT '[]' NOT NULL,
	`include_unknown` integer DEFAULT 0 NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text NOT NULL,
	`linked_at` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `access_grants_email_unique` ON `access_grants` (`email`);--> statement-breakpoint
CREATE UNIQUE INDEX `access_grants_user_id_unique` ON `access_grants` (`user_id`);
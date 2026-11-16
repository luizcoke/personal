CREATE TABLE `card_profiles` (
	`last4` text PRIMARY KEY NOT NULL,
	`name` text DEFAULT '' NOT NULL,
	`brand` text DEFAULT 'unknown' NOT NULL,
	`kind` text DEFAULT 'primary' NOT NULL,
	`parent_last4` text,
	`updated_at` text NOT NULL
);

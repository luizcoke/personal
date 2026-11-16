CREATE TABLE `spending_periods` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`starts_at` text NOT NULL,
	`ends_at` text NOT NULL,
	`category` text NOT NULL,
	`enabled` integer DEFAULT 1 NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `spending_periods_range` ON `spending_periods` (`enabled`,`starts_at`,`ends_at`);--> statement-breakpoint
ALTER TABLE `entries` ADD `purchase_time` text;--> statement-breakpoint
ALTER TABLE `entries` ADD `time_checked` integer DEFAULT 0 NOT NULL;
--> statement-breakpoint
CREATE TRIGGER spending_periods_no_overlap_insert BEFORE INSERT ON spending_periods
WHEN NEW.enabled=1 AND EXISTS (SELECT 1 FROM spending_periods WHERE enabled=1 AND starts_at<=NEW.ends_at AND ends_at>=NEW.starts_at)
BEGIN SELECT RAISE(ABORT, 'overlapping_spending_period'); END;
--> statement-breakpoint
CREATE TRIGGER spending_periods_no_overlap_update BEFORE UPDATE ON spending_periods
WHEN NEW.enabled=1 AND EXISTS (SELECT 1 FROM spending_periods WHERE enabled=1 AND id<>NEW.id AND starts_at<=NEW.ends_at AND ends_at>=NEW.starts_at)
BEGIN SELECT RAISE(ABORT, 'overlapping_spending_period'); END;

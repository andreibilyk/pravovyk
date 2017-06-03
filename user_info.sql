BEGIN TRANSACTION;
CREATE TABLE `user_info` (
	`name`	TEXT,
	`hobby`	TEXT,
	`age`	INTEGER,
	`gender`	INTEGER,
	`music_genre`	TEXT
);
COMMIT;

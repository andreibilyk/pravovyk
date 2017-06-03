BEGIN TRANSACTION;
CREATE TABLE `user_interac` (
	`question`	TEXT,
	`answers`	TEXT,
	`branch`	TEXT,
	`category`	TEXT,
	`subcategory`	TEXT,
	`user_answer`	TEXT
);
INSERT INTO `user_interac` VALUES ('Оберіть сферу','Сімейне право,Трудове право,Право споживача,Поліція,Договори,ЖКГ',NULL,NULL,NULL,NULL);
INSERT INTO `user_interac` VALUES ('Який напрямок Вас цікавить із сімейного права?','Аліменти,Права батьків після розлучення,Усиновлення,Розлучення,Поділ майна,Заповіт,Спадок','family_law',NULL,NULL,'Сімейне право');
INSERT INTO `user_interac` VALUES ('Який напрямок Вас цікавить із трудового права?','Трудовий договір,Звільнення,Відпустка,Відрядження,Лікарняний,Праця неповнолітніх','work_law',NULL,NULL,'Трудове право');
INSERT INTO `user_interac` VALUES ('Який напрямок Вас цікавить із прав споживача?','Захист прав споживача,Купівля товарів в Інтернеті','consumer_law
',NULL,NULL,'Право споживача');
INSERT INTO `user_interac` VALUES ('Який напрямок Вас цікавить у сфері поліції?','Права поліцейських,ДТП,Складання протоколу,Обшук людини','police_law',NULL,NULL,'Поліція');
INSERT INTO `user_interac` VALUES ('Що із договорів цікавить Вас?','Don''t know,Don''t know','treaty_law',NULL,NULL,'Договори');
INSERT INTO `user_interac` VALUES ('Який напрямок Вас цікавить із прав ЖКГ?','Don''t know,Don''t know','zhek_law',NULL,NULL,'ЖКГ');
INSERT INTO `user_interac` VALUES ('Оберіть перелік питань,пов''язаних з аліментами','Розмір аліментів,Заборгованість по аліментам','family_law','aliments
',NULL,'Аліменти');
INSERT INTO `user_interac` VALUES ('Оберіть перелік питань,пов''язаних з правами батьків після розлучення','З ким залишається дитина після розлучення?,Не дають батькам дітей','family_law','rights of divorced parents',NULL,'Права батьків після розлучення');
INSERT INTO `user_interac` VALUES ('Що із усиновлення цікавить Вас?','Що треба, щоб усиновити дитину?,Як всиновити?','family_law',NULL,NULL,'Усиновлення');
COMMIT;

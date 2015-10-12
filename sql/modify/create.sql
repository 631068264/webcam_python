CREATE TABLE `role` (
	`id` BIGINT (20) NOT NULL COMMENT '角色识别码 0:管理员,1:普通用户',
	`name` VARCHAR (32) NOT NULL COMMENT '角色名称',
	PRIMARY KEY (`id`)
) ENGINE = INNODB DEFAULT CHARSET = utf8 COMMENT = '角色表';
INSERT INTO `role` VALUES ('0', '管理员');
INSERT INTO `role` VALUES ('1', '普通用户');

CREATE TABLE `account` (
	`id` BIGINT (20) NOT NULL,
	`username` VARCHAR (64) NOT NULL UNIQUE COMMENT '昵称',
	`password` VARCHAR (64) NOT NULL COMMENT '密码',
	`name` VARCHAR (32) DEFAULT NULL COMMENT '姓名',
	`device` VARCHAR (128) NOT NULL DEFAULT '0' COMMENT '设备识别码',
	`role_id` BIGINT (20) NOT NULL DEFAULT '1' COMMENT '角色',
	`status` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: normal, 1: deleted',
	PRIMARY KEY (`id`),
	FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE = INNODB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 COMMENT = '账号表';
INSERT INTO `account` VALUES ('150328239', 'admin', 'c3e01e2715dd95ee3e97475276b2f74b', null, 'd1cc4dfcd4145a0a2ecd44cb3', '1', '0');

CREATE TABLE `task` (
	`id` BIGINT (20) NOT NULL,
	`name` VARCHAR (64) NOT NULL DEFAULT 'Default' COMMENT '用户自定义任务名',
	`src` VARCHAR (200) DEFAULT NULL COMMENT '资源——url',
	`thumbnail` VARCHAR (200) DEFAULT NULL COMMENT '缩略图——url',
	`create_time` datetime DEFAULT NULL COMMENT '任务创建时间 按日期算',
	`duration` BIGINT (20) DEFAULT NULL COMMENT '持续时间',
	`interval` BIGINT (20) DEFAULT NULL COMMENT '时间间隔',
	`size` BIGINT (20) DEFAULT NULL COMMENT '资源大小',
	`account_id` BIGINT (20) NOT NULL COMMENT '用户id',
	`status` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: normal, 1: deleted',
	PRIMARY KEY (`id`),
	FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) ENGINE = INNODB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8 COMMENT = '任务表';

INSERT INTO `task` VALUES ('1', 'Default', null, null, '2015-10-12 22:21:29', '3', '2', null, '150328239', '0');
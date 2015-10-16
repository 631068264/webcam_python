CREATE TABLE `role` (
	`id` BIGINT (20) NOT NULL COMMENT '角色识别码 0:管理员,1:普通用户',
	`name` VARCHAR (32) NOT NULL COMMENT '角色名称',
	PRIMARY KEY (`id`)
) COMMENT = '角色表';

INSERT INTO `role`
VALUES
	('0', '管理员');

INSERT INTO `role`
VALUES
	('1', '普通用户');

CREATE TABLE `account` (
	`id` BIGINT (20) NOT NULL AUTO_INCREMENT,
	`username` VARCHAR (64) NOT NULL UNIQUE COMMENT '昵称',
	`password` VARCHAR (64) NOT NULL COMMENT '密码',
	`name` VARCHAR (32) DEFAULT NULL COMMENT '姓名',
	`size` BIGINT (20) NOT NULL DEFAULT '0' COMMENT '用户资源总大小',
	`device_num` BIGINT (3) NOT NULL DEFAULT '0' COMMENT '设备个数',
	`role_id` BIGINT (20) NOT NULL DEFAULT '1' COMMENT '角色',
	`status` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: normal, 1: deleted',
	PRIMARY KEY (`id`),
	FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) AUTO_INCREMENT = 18620749654 COMMENT = '账号表';
INSERT INTO `account` VALUES ('18620749654', 'admin', '20966d46a6446a610bce72e00eccd954', null, '0', '0', '1', '0');

CREATE TABLE `device` (
	`id` VARCHAR (50) NOT NULL UNIQUE COMMENT '设备ID',
	`name` VARCHAR (64) NOT NULL COMMENT '设备名',
	`status` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: normal, 1: deleted',
	`account_id` BIGINT (20) NOT NULL COMMENT '账号ID',
	FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) COMMENT = '设备表';

CREATE TABLE `task` (
	`id` BIGINT (20) NOT NULL AUTO_INCREMENT COMMENT '任务ID',
	`create_time` datetime DEFAULT NULL COMMENT '任务创建时间',
	`duration` BIGINT (20) DEFAULT NULL COMMENT '持续时间',
	`interval` BIGINT (20) DEFAULT NULL COMMENT '时间间隔',
	`now` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: 非即时, 1: 即时',
	`status` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: normal, 1: deleted',
	`account_id` BIGINT (20) NOT NULL COMMENT '账号ID',
	PRIMARY KEY (`id`),
	FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) COMMENT = '任务表';

CREATE TABLE `src` (
	`id` BIGINT (20) NOT NULL AUTO_INCREMENT COMMENT '资源ID',
	`create_time` datetime DEFAULT NULL COMMENT '资源创建时间,即任务完成时间',
	`src_path` VARCHAR (200) DEFAULT NULL COMMENT '资源——url',
	`thumbnail` VARCHAR (200) DEFAULT NULL COMMENT '缩略图——url',
	`size` BIGINT (20) DEFAULT NULL COMMENT '资源大小',
	`status` TINYINT (4) NOT NULL DEFAULT '0' COMMENT '0: normal, 1: deleted',
	`device_id` BIGINT (20) NOT NULL COMMENT '设备ID',
	`account_id` BIGINT (20) NOT NULL COMMENT '账号ID',
	PRIMARY KEY (`id`),
	FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) COMMENT = '资源表';
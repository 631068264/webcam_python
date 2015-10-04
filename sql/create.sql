/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50096
Source Host           : localhost:3306
Source Database       : webcap

Target Server Type    : MYSQL
Target Server Version : 50096
File Encoding         : 65001

Date: 2015-10-04 11:52:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
`id`  bigint(20) NOT NULL ,
`nick`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '昵称' ,
`password`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码' ,
`name`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '姓名' ,
`device`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '设备识别码' ,
`role_id`  bigint(20) NOT NULL DEFAULT 1 COMMENT '角色' ,
`status`  tinyint(4) NOT NULL DEFAULT 0 COMMENT '0: normal, 1: deleted' ,
PRIMARY KEY (`id`),
FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
UNIQUE INDEX `nick` USING BTREE (`nick`),
INDEX `role_id` USING BTREE (`role_id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
COMMENT='账号表; InnoDB free: 9216 kB; (`role_id`) REFER `webcap/role`(`id`)'

;

-- ----------------------------
-- Records of account
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
`id`  bigint(20) NOT NULL COMMENT '角色识别码 0:管理员,1:普通用户' ,
`name`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '角色名称' ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
COMMENT='角色表'

;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
`id`  bigint(20) NOT NULL ,
`name`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'Default' COMMENT '用户自定义任务名' ,
`src`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '资源——url' ,
`thumbnail`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '缩略图——url' ,
`create_time`  datetime NULL DEFAULT NULL COMMENT '任务创建时间 按日期算' ,
`duration`  datetime NULL DEFAULT NULL COMMENT '持续时间' ,
`interval`  datetime NULL DEFAULT NULL COMMENT '时间间隔' ,
`size`  bigint(20) NULL DEFAULT NULL COMMENT '资源大小' ,
`account_id`  bigint(20) NOT NULL COMMENT '用户id' ,
`status`  tinyint(4) NOT NULL DEFAULT 0 COMMENT '0: normal, 1: deleted' ,
PRIMARY KEY (`id`),
FOREIGN KEY (`account_id`) REFERENCES `account` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `account_id` USING BTREE (`account_id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
COMMENT='任务表; InnoDB free: 9216 kB; (`account_id`) REFER `webcap/account`(`id`)'

;

-- ----------------------------
-- Records of task
-- ----------------------------
BEGIN;
COMMIT;

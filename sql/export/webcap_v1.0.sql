/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50096
Source Host           : localhost:3306
Source Database       : webcap

Target Server Type    : MYSQL
Target Server Version : 50096
File Encoding         : 65001

Date: 2015-11-09 02:14:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` bigint(20) NOT NULL auto_increment,
  `username` varchar(64) NOT NULL COMMENT '昵称',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `name` varchar(32) default NULL COMMENT '姓名',
  `size` bigint(20) NOT NULL default '0' COMMENT '用户资源总大小',
  `device_num` bigint(3) NOT NULL default '0' COMMENT '设备个数',
  `role_id` bigint(20) NOT NULL default '1' COMMENT '角色',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18620749655 DEFAULT CHARSET=utf8 COMMENT='账号表';

-- ----------------------------
-- Records of account
-- ----------------------------
INSERT INTO `account` VALUES ('18620749654', 'admin', '20966d46a6446a610bce72e00eccd954', null, '329293', '1', '1', '0');

-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `id` varchar(50) NOT NULL COMMENT '设备ID',
  `name` varchar(64) NOT NULL COMMENT '设备名',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  `account_id` bigint(20) NOT NULL COMMENT '账号ID',
  UNIQUE KEY `id` (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `device_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='设备表';

-- ----------------------------
-- Records of device
-- ----------------------------
INSERT INTO `device` VALUES ('0d0b0e608af645a0590d0c425', '1234', '0', '18620749654');
INSERT INTO `device` VALUES ('94327938850f768e47de4df4a', '797', '1', '18620749654');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` bigint(20) NOT NULL COMMENT '角色识别码 0:管理员,1:普通用户',
  `name` varchar(32) NOT NULL COMMENT '角色名称',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色表';

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('0', '管理员');
INSERT INTO `role` VALUES ('1', '普通用户');

-- ----------------------------
-- Table structure for src
-- ----------------------------
DROP TABLE IF EXISTS `src`;
CREATE TABLE `src` (
  `id` bigint(20) NOT NULL auto_increment COMMENT '资源ID',
  `create_time` datetime default NULL COMMENT '资源创建时间,即任务完成时间',
  `src_path` varchar(200) default NULL COMMENT '资源——url',
  `thumbnail` varchar(200) default NULL COMMENT '缩略图——url',
  `size` bigint(20) default NULL COMMENT '资源大小',
  `type` tinyint(4) NOT NULL default '0' COMMENT '资源类型0: 图片, 1: 视频',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  `device_id` varchar(50) NOT NULL COMMENT '设备ID',
  `account_id` bigint(20) NOT NULL COMMENT '账号ID',
  PRIMARY KEY  (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `src_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='资源表';

-- ----------------------------
-- Records of src
-- ----------------------------
INSERT INTO `src` VALUES ('7', '2015-11-04 23:25:23', '/static/download/0d0b0e608af645a0590d0c425\\05431759bb8947de988f621beba2db8d.jpg', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '2386', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('8', '2015-11-08 18:09:37', '/static/download/0d0b0e608af645a0590d0c425\\15.jpg', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '7841', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('9', '2015-11-09 00:01:04', '/static/download/0d0b0e608af645a0590d0c425\\641094b2e71f4f06baccbf5cc75a81ad.mp4', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '289818', '1', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('10', '2015-11-09 00:39:37', '/static/download/0d0b0e608af645a0590d0c425\\2b3fa486e34843e18998e01faca9ecf9.mp4', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '48', '1', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('11', '2015-11-09 01:19:11', '/static/download/0d0b0e608af645a0590d0c425\\444ab227646541b39d01931990c38eb0.jpg', '/static/download/0d0b0e608af645a0590d0c425\\4f8e225ba7534f9f98aa583b95eab512.jpg', '14027', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('12', '2015-11-09 01:20:10', '/static/download/0d0b0e608af645a0590d0c425\\e8b3498d448d4ebdb612d0eedc0fde52.mp4', '/static/download/0d0b0e608af645a0590d0c425\\bc8baa6dc60748eba97a8d4551a0f586.jpg', '48', '1', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('13', '2015-11-09 02:06:00', '/static/download/0d0b0e608af645a0590d0c425\\1220625cebe649b3a20bb8798f90a802.mp4', '/static/download/0d0b0e608af645a0590d0c425\\d16922a842594a0eb8ce25b60b880fc4.jpg', '48', '1', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('14', '2015-11-09 02:13:16', '/static/download/0d0b0e608af645a0590d0c425\\bb66e72d868348a89e4985386f70cdd7.jpg', '/static/download/0d0b0e608af645a0590d0c425\\1ace39fa692d493c98cd2686b17d9d77.jpg', '15077', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` bigint(20) NOT NULL auto_increment COMMENT '任务ID',
  `create_time` datetime default NULL COMMENT '任务创建时间',
  `execute_time` datetime default NULL COMMENT '任务执行时间',
  `finish_time` datetime default NULL COMMENT '任务完成时间',
  `duration` bigint(20) default NULL COMMENT '持续时间',
  `interval` bigint(20) default NULL COMMENT '时间间隔',
  `now` tinyint(4) NOT NULL default '0' COMMENT '是否立即执行0: 非即时, 1: 即时',
  `type` tinyint(4) NOT NULL default '0' COMMENT '资源类型0: 图片, 1: 视频',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted,2:finished',
  `device_id` varchar(50) NOT NULL COMMENT '设备ID',
  `account_id` bigint(20) NOT NULL COMMENT '账号ID',
  PRIMARY KEY  (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COMMENT='任务表';

-- ----------------------------
-- Records of task
-- ----------------------------
INSERT INTO `task` VALUES ('15', '2015-11-04 00:00:00', '2015-11-04 23:25:14', '2015-11-04 23:25:23', '6', '5', '1', '0', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('16', '2015-11-07 00:00:00', '1970-01-01 15:12:00', null, '6', '5', '0', '1', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('17', '2015-11-09 00:00:00', '1970-01-01 02:06:00', '2015-11-09 02:06:00', '6', '5', '0', '1', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('18', '2015-11-09 00:00:00', '2015-11-08 18:09:37', '2015-11-08 18:09:37', null, null, '1', '0', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('19', '2015-11-09 00:00:00', '2015-11-09 00:01:04', '2015-11-09 00:01:04', '10', null, '1', '1', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('20', '2015-11-09 00:00:00', '2015-11-09 00:39:37', '2015-11-09 00:39:37', '9', null, '1', '1', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('21', '2015-11-09 00:00:00', '2015-11-09 01:04:25', null, null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('22', '2015-11-09 00:00:00', '2015-11-09 01:19:11', '2015-11-09 01:19:11', null, null, '1', '0', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('23', '2015-11-09 00:00:00', '2015-11-09 01:20:10', '2015-11-09 01:20:10', '6', null, '1', '1', '2', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('24', '2015-11-09 00:00:00', '2015-11-09 02:09:57', null, null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('25', '2015-11-09 00:00:00', '2015-11-09 02:10:18', null, null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('26', '2015-11-09 00:00:00', '2015-11-09 02:10:52', null, null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('27', '2015-11-09 00:00:00', '2015-11-09 02:12:41', null, null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('28', '2015-11-09 00:00:00', '2015-11-09 02:13:08', '2015-11-09 02:13:16', null, null, '1', '0', '2', '0d0b0e608af645a0590d0c425', '18620749654');

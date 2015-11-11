/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50096
Source Host           : localhost:3306
Source Database       : webcap

Target Server Type    : MYSQL
Target Server Version : 50096
File Encoding         : 65001

Date: 2015-11-12 00:45:23
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` char(32) NOT NULL,
  `username` varchar(64) NOT NULL COMMENT '用户名',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `name` varchar(32) default NULL COMMENT '姓名',
  `size` bigint(20) NOT NULL default '0' COMMENT '用户资源总大小',
  `device_num` bigint(3) NOT NULL default '0' COMMENT '设备个数',
  `role_id` bigint(20) NOT NULL default '1' COMMENT '角色',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='账号表';

-- ----------------------------
-- Records of account
-- ----------------------------
INSERT INTO `account` VALUES ('1245202f9d684ed289540e78f23e8830', 'admin1', 'd8391e64f711e839fea07348b9cab217', null, '0', '0', '0', '0');
INSERT INTO `account` VALUES ('edfea2daabed4af5a0a449882bfff58f', 'admin', '20966d46a6446a610bce72e00eccd954', null, '344406', '1', '1', '0');

-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `id` varchar(50) NOT NULL default '' COMMENT '设备ID',
  `name` varchar(64) NOT NULL COMMENT '设备名',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  `account_id` char(32) NOT NULL COMMENT '账号ID',
  PRIMARY KEY  (`id`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='设备表';

-- ----------------------------
-- Records of device
-- ----------------------------
INSERT INTO `device` VALUES ('0d0b0e608af645a0590d0c425', '1234', '0', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `device` VALUES ('94327938850f768e47de4df4a', '797', '1', 'edfea2daabed4af5a0a449882bfff58f');

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
  `id` char(32) NOT NULL COMMENT '资源ID',
  `create_time` datetime default NULL COMMENT '资源创建时间,即任务完成时间',
  `src_path` varchar(200) default NULL COMMENT '资源——url',
  `thumbnail` varchar(200) default NULL COMMENT '缩略图——url',
  `size` bigint(20) default NULL COMMENT '资源大小',
  `type` tinyint(4) NOT NULL default '0' COMMENT '资源类型0: 图片, 1: 视频',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  `device_id` varchar(50) NOT NULL COMMENT '设备ID',
  `account_id` char(32) NOT NULL COMMENT '账号ID',
  PRIMARY KEY  (`id`),
  KEY `device_id` (`device_id`,`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源表';

-- ----------------------------
-- Records of src
-- ----------------------------
INSERT INTO `src` VALUES ('2d89f73b7ede49deab45fd918868af49', '2015-11-09 01:20:10', '/static/download/0d0b0e608af645a0590d0c425\\e8b3498d448d4ebdb612d0eedc0fde52.mp4', '/static/download/0d0b0e608af645a0590d0c425\\bc8baa6dc60748eba97a8d4551a0f586.jpg', '48', '1', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('4cc8be68c8c14aad855aceba9eb518d3', '2015-11-09 01:19:11', '/static/download/0d0b0e608af645a0590d0c425\\444ab227646541b39d01931990c38eb0.jpg', '/static/download/0d0b0e608af645a0590d0c425\\4f8e225ba7534f9f98aa583b95eab512.jpg', '14027', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('5a46b6bbd0cd4ed9b3e4152775d6a649', '2015-11-09 00:01:04', '/static/download/0d0b0e608af645a0590d0c425\\641094b2e71f4f06baccbf5cc75a81ad.mp4', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '289818', '1', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('6f50dc8bf917430ab88247fa3952c615', '2015-11-04 23:25:23', '/static/download/0d0b0e608af645a0590d0c425\\05431759bb8947de988f621beba2db8d.jpg', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '2386', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('93ea4033bb18416fbe36f0eef6627a05', '2015-11-09 02:06:00', '/static/download/0d0b0e608af645a0590d0c425\\1220625cebe649b3a20bb8798f90a802.mp4', '/static/download/0d0b0e608af645a0590d0c425\\d16922a842594a0eb8ce25b60b880fc4.jpg', '48', '1', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('ca62e43ca3b1442e834bc2b1cf6cb216', '2015-11-12 00:11:38', '/static/download/0d0b0e608af645a0590d0c425\\b7fd14d51a49486a8a2fce00774758b3.jpg', '/static/download/0d0b0e608af645a0590d0c425\\4cb57eea95fb417d9488c5c11e4ace28.jpg', '15113', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('cc353c3ce1664f52b926c825c10e1b41', '2015-11-09 02:13:16', '/static/download/0d0b0e608af645a0590d0c425\\bb66e72d868348a89e4985386f70cdd7.jpg', '/static/download/0d0b0e608af645a0590d0c425\\1ace39fa692d493c98cd2686b17d9d77.jpg', '15077', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `src` VALUES ('e9594ee856b9463382c39b56f2b247bc', '2015-11-08 18:09:37', '/static/download/0d0b0e608af645a0590d0c425\\15.jpg', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '7841', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `src` VALUES ('f0557687141f422993a9e1eb73e11275', '2015-11-09 00:39:37', '/static/download/0d0b0e608af645a0590d0c425\\2b3fa486e34843e18998e01faca9ecf9.mp4', '/static/download/0d0b0e608af645a0590d0c425\\13.jpg', '48', '1', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` char(32) NOT NULL COMMENT '任务ID',
  `create_time` date default NULL COMMENT '任务创建时间',
  `execute_time` datetime default NULL COMMENT '任务执行时间',
  `finish_time` datetime default NULL COMMENT '任务完成时间',
  `duration` bigint(20) default NULL COMMENT '持续时间',
  `now` tinyint(4) NOT NULL default '0' COMMENT '是否立即执行0: 非即时, 1: 即时',
  `type` tinyint(4) NOT NULL default '0' COMMENT '资源类型0: 图片, 1: 视频',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted,2:finished',
  `device_id` varchar(50) NOT NULL COMMENT '设备ID',
  `account_id` char(32) NOT NULL COMMENT '账号ID',
  PRIMARY KEY  (`id`),
  KEY `device_id` (`device_id`,`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务表';

-- ----------------------------
-- Records of task
-- ----------------------------
INSERT INTO `task` VALUES ('0212d1950967485b8a7fc30fe5153d3f', '2015-11-09', '1970-01-01 01:04:25', null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', '18620749654');
INSERT INTO `task` VALUES ('0c600a5b7c6c46bb948b0cd89bf61f55', '2015-11-09', '1970-01-01 01:19:11', '1970-01-01 01:19:11', null, '1', '0', '1', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('10e1bcbca9c94d189cb79057439c3783', '2015-11-13', '1970-01-01 08:00:00', null, null, '0', '0', '1', '94327938850f768e47de4df4a', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('166f225bb57c45249c471c2c7e16903c', '2015-11-14', '1970-01-01 08:00:00', null, null, '0', '0', '1', '94327938850f768e47de4df4a', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('231bc64f928846fda7fa5c4bfee6b4d8', '2015-11-15', '1970-01-01 08:00:00', null, null, '0', '0', '1', '94327938850f768e47de4df4a', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('25734660248c4e618f59a0a2611556eb', '2015-11-07', '1970-01-01 15:12:00', null, '6', '5', '1', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('3164f620b4884fccb73f71c6e6325a4f', '2015-11-12', '2015-11-12 00:09:41', '2015-11-12 00:11:38', null, '1', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('34a3093d1da548428baa942631ee03e6', '2015-11-16', '1970-01-01 08:00:00', null, null, '0', '0', '1', '94327938850f768e47de4df4a', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('3a95d312262e46a8a45d08e93322cad0', '2015-11-09', '1970-01-01 02:10:18', null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('55844ab6401b4c38adccc230ed40dca6', '2015-11-09', '1970-01-01 02:06:00', '1970-01-01 02:06:00', '6', '0', '1', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('592f7bd3abbe41da9bbc3b6920720234', '2015-11-09', '1970-01-01 02:10:52', null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('5f9875862da64bdfa25c66e676fd23a4', '2015-11-09', '1970-01-01 00:39:37', '1970-01-01 00:39:37', '9', '1', '1', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('68ebf75ef17b43d1b5cddb32b19ff54c', '2015-11-09', '1970-01-01 02:12:41', null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('778285c455a94cd2b43f450e3a22df29', '2015-11-11', '2015-11-11 23:32:52', null, null, '1', '0', '1', '94327938850f768e47de4df4a', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('91db5991443b41ebbdd5eba0d50250f1', '2015-11-04', '1970-01-01 23:25:14', '1970-01-01 23:25:23', '6', '1', '0', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('cc29ddf7aece4b0689627480fb8af374', '2015-11-09', '1970-01-01 18:09:37', '1970-01-01 18:09:37', null, '1', '0', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('d971cacbfc614a5cb4424f0bf73dc0d8', '2015-11-09', '1970-01-01 01:20:10', '1970-01-01 01:20:10', '6', '1', '1', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('ecc301fedcc847d0b84fe00b75297c5b', '2015-11-09', '1970-01-01 00:01:04', '1970-01-01 00:01:04', '10', '1', '1', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('fcee6818e11c4621b8e100115d4c799e', '2015-11-09', '1970-01-01 02:13:08', '1970-01-01 02:13:16', null, '1', '0', '2', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');
INSERT INTO `task` VALUES ('fd1d5fc95b4a407d93c2f6e11974269d', '2015-11-09', '1970-01-01 02:09:57', null, null, '1', '0', '0', '0d0b0e608af645a0590d0c425', 'edfea2daabed4af5a0a449882bfff58f');

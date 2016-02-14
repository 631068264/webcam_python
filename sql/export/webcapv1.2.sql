/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50096
Source Host           : localhost:3306
Source Database       : webcap

Target Server Type    : MYSQL
Target Server Version : 50096
File Encoding         : 65001

Date: 2016-02-14 10:47:41
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
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS `device`;
CREATE TABLE `device` (
  `id` varchar(50) NOT NULL default '' COMMENT '设备ID',
  `name` varchar(64) NOT NULL COMMENT '设备名',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted',
  `account_id` char(32) NOT NULL COMMENT '账号ID',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY  (`id`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='设备表';

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
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` char(32) NOT NULL COMMENT '任务ID',
  `create_time` date default NULL COMMENT '任务创建时间',
  `execute_time` datetime default NULL COMMENT '任务执行时间',
  `finish_time` datetime default NULL COMMENT '任务完成时间',
  `duration` bigint(20) default NULL COMMENT '持续时间',
  `cycle` tinyint(4) NOT NULL default '0' COMMENT '是否循环任务',
  `now` tinyint(4) NOT NULL default '0' COMMENT '是否立即执行0: 非即时, 1: 即时',
  `type` tinyint(4) NOT NULL default '0' COMMENT '资源类型0: 图片, 1: 视频',
  `status` tinyint(4) NOT NULL default '0' COMMENT '0: normal, 1: deleted,2:finished',
  `device_id` varchar(50) NOT NULL COMMENT '设备ID',
  `account_id` char(32) NOT NULL COMMENT '账号ID',
  PRIMARY KEY  (`id`),
  KEY `device_id` (`device_id`,`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务表';

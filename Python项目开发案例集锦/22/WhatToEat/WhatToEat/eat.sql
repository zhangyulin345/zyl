/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 80012
Source Host           : localhost:3306
Source Database       : eat

Target Server Type    : MYSQL
Target Server Version : 80012
File Encoding         : 65001

Date: 2019-01-28 13:20:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'mr', 'pbkdf2:sha256:50000$TkExX9Jm$d63477853a17dcaedcd52be4b6213ebb74b61a12456762ac19d6b7dfb559aa57');

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('9de4a4f0b761');

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `order_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_category_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES ('1', '东北菜', '2018-11-19 17:35:33', '1');
INSERT INTO `category` VALUES ('2', '川菜', '2018-11-19 17:41:20', '2');
INSERT INTO `category` VALUES ('3', '湘菜', '2018-11-19 17:47:45', '3');

-- ----------------------------
-- Table structure for food
-- ----------------------------
DROP TABLE IF EXISTS `food`;
CREATE TABLE `food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `cate_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cate_id` (`cate_id`),
  KEY `ix_food_addtime` (`addtime`),
  CONSTRAINT `food_ibfk_1` FOREIGN KEY (`cate_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of food
-- ----------------------------
INSERT INTO `food` VALUES ('3', '第三鲜', '2018-11-28 16:42:50', '1');
INSERT INTO `food` VALUES ('4', '土豆炖粉条', '2018-11-28 16:42:58', '1');
INSERT INTO `food` VALUES ('5', '翠花酸菜', '2018-11-28 16:43:11', '1');
INSERT INTO `food` VALUES ('6', '水煮鱼', '2018-11-28 17:52:56', '2');
INSERT INTO `food` VALUES ('7', '麻婆豆腐', '2018-11-28 17:53:20', '2');
INSERT INTO `food` VALUES ('8', '四川火锅', '2018-11-28 17:53:28', '2');
INSERT INTO `food` VALUES ('9', '回锅肉', '2018-11-28 17:54:04', '2');
INSERT INTO `food` VALUES ('10', '毛血旺', '2018-11-28 17:54:23', '2');
INSERT INTO `food` VALUES ('11', '口水鸡', '2018-11-28 17:54:38', '2');
INSERT INTO `food` VALUES ('12', '剁椒鱼头', '2018-12-03 18:03:37', '3');
INSERT INTO `food` VALUES ('13', '锅包肉', '2018-12-04 10:57:39', '2');
INSERT INTO `food` VALUES ('14', '麻辣烫', '2018-12-04 10:57:55', '2');
INSERT INTO `food` VALUES ('25', '干锅茶树菇', '2018-12-11 13:19:09', '3');
INSERT INTO `food` VALUES ('26', '东安子鸡', '2018-12-11 13:25:52', '3');
INSERT INTO `food` VALUES ('27', '猪肉炖粉条', '2018-12-21 13:22:26', '1');
INSERT INTO `food` VALUES ('28', '锅包肉', '2018-12-21 13:22:57', '1');

-- ----------------------------
-- Table structure for record
-- ----------------------------
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `food` varchar(255) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_record_addtime` (`addtime`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of record
-- ----------------------------
INSERT INTO `record` VALUES ('10', '8', '水煮鱼', '1', '2018-12-23 10:12:57');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(50) DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('8', 'oVAL60CQxQ1sxIE-r4AT21p-3_eg', '冯春龙', null, 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGibzXbuZbwxEcKQBbOEVQGHmsC1HsLRc1Qk5jLSQf2ichmQr1kshDtFOnzgb3cvNjUpK7HX2OX5cw/132', '2018-12-17 16:43:43');

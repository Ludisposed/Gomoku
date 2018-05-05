/*
* @Author: Li Qin
* @Date:   2018-05-06 00:24:59
* @Last Modified by:   Li Qin
* @Last Modified time: 2018-05-06 00:35:44
*/
DROP DATABASE IF EXISTS `gomoku`;
CREATE DATABASE `gomoku`;
USE `gomoku`;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(20)  NOT NULL COMMENT "user's name",
  `games_win` varchar(200) DEFAULT NULL COMMENT "games' id user win",
  `games_lose` varchar(200) DEFAULT NULL COMMENT "games' id user lose",
  `game_current` varchar(20) DEFAULT NULL COMMENT 'game user is playing currently',
  `value_1` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `value_2` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `value_3` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for `game`
-- ----------------------------
DROP TABLE IF EXISTS `game`;
CREATE TABLE `game` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT "id",
  `order_black` varchar(200) DEFAULT NULL COMMENT "order of how black side place pieces",
  `order_white` varchar(200) DEFAULT NULL COMMENT "order of how white side place pieces",
  `result` int DEFAULT NULL COMMENT 'winner is black=1/white=-1/win-win=0/still continue=-2',
  `value_1` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `value_2` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `value_3` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of game
-- ----------------------------
-- Adminer 4.8.1 MySQL 8.1.0 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `Nodes`;
CREATE TABLE `Nodes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `id_node` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_name` text NOT NULL,
  `neighbors` json NOT NULL,
  `id_floor` tinyint NOT NULL,
  `Extra` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2023-08-31 19:31:18
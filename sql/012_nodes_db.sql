SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `Nodes`;
CREATE TABLE `Nodes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `id_node` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_name` text NOT NULL,
  `neighbors` json NOT NULL,
  `id_floor` tinyint NOT NULL,
  `status` tinyint NOT NULL,
  `Extra` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

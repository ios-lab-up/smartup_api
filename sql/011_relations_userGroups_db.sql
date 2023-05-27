SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `RelationUserGroup`;

CREATE TABLE `RelationUserGroup` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `groupID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `userID` (`userID`),
  KEY `groupID` (`groupID`),
  CONSTRAINT `RelationUserGroup_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `User` (`ID`),
  CONSTRAINT `RelationUserGroup_ibfk_2` FOREIGN KEY (`groupID`) REFERENCES `Group` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
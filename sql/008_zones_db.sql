SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Zones`;

CREATE TABLE
    `Zones` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` date DEFAULT NULL,
        `LastUpdate` timestamp NULL DEFAULT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
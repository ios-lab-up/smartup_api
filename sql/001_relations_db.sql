SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8;

DROP TABLE IF EXISTS `RelationGroupSchedule`;

CREATE TABLE
    `RelationGroupSchedule` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `GroupID` int(11) NOT NULL,
        `ScheduleID` int(11) NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `GroupID` (`GroupID`),
        KEY `ScheduleID` (`ScheduleID`),
        CONSTRAINT `RelationGroupSchedule_ibfk_1` FOREIGN KEY (`GroupID`) REFERENCES `Group` (`ID`),
        CONSTRAINT `RelationGroupSchedule_ibfk_2` FOREIGN KEY (`ScheduleID`) REFERENCES `Schedule` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;
SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Schedule`;

CREATE TABLE
    `Schedule` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `ClassroomID` int(11) NOT NULL,
        `Day` text NOT NULL,
        `StartTime` time NOT NULL,
        `EndTime` time NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` date NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `ClassroomID` (`ClassroomID`),
        CONSTRAINT `Schedule_ibfk_6` FOREIGN KEY (`ClassroomID`) REFERENCES `Classroom` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;
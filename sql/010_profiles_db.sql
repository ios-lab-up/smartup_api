SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Profile`;

CREATE TABLE
    `Profile` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` time NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;

INSERT INTO
    `Profile` (
        `ID`,
        `Name`,
        `Status`,
        `CreationDate`,
        `LastUpdate`
    )
VALUES (
        1,
        'Administrador',
        1,
        '20:07:43',
        '2023-03-17 20:07:43'
    ), (
        2,
        'Maestro',
        1,
        '20:07:59',
        '2023-03-17 20:07:59'
    ), (
        3,
        'Estudiante',
        1,
        '20:08:18',
        '2023-03-17 20:08:18'
    );

DROP TABLE IF EXISTS `User`;

CREATE TABLE
    `User` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `UserID` text NOT NULL,
        `Password` text NOT NULL,
        `Name` text NOT NULL,
        `LastName` text NOT NULL,
        `Email` text NOT NULL,
        `ProfileID` int(11) NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` date NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        `Options` int(11) NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `ProfileID` (`ProfileID`),
        CONSTRAINT `User_ibfk_1` FOREIGN KEY (`ProfileID`) REFERENCES `Profile` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
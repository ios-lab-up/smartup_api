SET NAMES utf8;

DROP TABLE IF EXISTS `Profile`;

CREATE TABLE
    `Profile` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` time NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

DROP TABLE IF EXISTS `User`;

CREATE TABLE
    `User` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `UserID` text,
        `Password` text,
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
        'Super Usuario',
        1,
        '23:27:38',
        '2023-03-19 23:27:38'
    ), (
        2,
        'Administrador',
        1,
        '23:28:01',
        '2023-03-19 23:28:01'
    ), (
        3,
        'Estudiante',
        1,
        '23:28:34',
        '2023-03-19 23:28:34'
    ), (
        4,
        'Visitante',
        1,
        '23:28:47',
        '2023-03-19 23:28:47'
    ), (
        5,
        'Maestro',
        1,
        '23:29:10',
        '2023-03-19 23:29:10'
    );

INSERT INTO
    `User` (
        `ID`,
        `UserID`,
        `Password`,
        `Name`,
        `LastName`,
        `Email`,
        `ProfileID`,
        `Status`,
        `CreationDate`,
        `LastUpdate`,
        `Options`
    )
VALUES (
        1,
        '0',
        '12345',
        'SMARTUP-ADMIN',
        'Null',
        'Null',
        1,
        1,
        '2023-03-20',
        '2023-03-20 00:21:32',
        0
    );
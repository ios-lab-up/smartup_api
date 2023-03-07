DROP TABLE IF EXISTS `Classroom`;

CREATE TABLE
    `Classroom` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` text NOT NULL,
        `Options` int(11) NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` date NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;
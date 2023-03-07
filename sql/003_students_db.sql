SET NAMES utf8;

DROP TABLE IF EXISTS `Student`;

CREATE TABLE
    `Student` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `StudentID` text NOT NULL,
        `Password` text NOT NULL,
        `Name` text NOT NULL,
        `LastName` text NOT NULL,
        `Email` text NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` date NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        `Options` int(11) NOT NULL,
        PRIMARY KEY (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;
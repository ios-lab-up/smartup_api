DROP TABLE IF EXISTS `Group`;

CREATE TABLE
    `Group` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Subject` int(11) NOT NULL,
        `ClassNumber` int(11) NOT NULL,
        `Group` text NOT NULL,
        `Teacher` int(11) NOT NULL,
        `Language` text NOT NULL,
        `Students` text,
        `Modality` text NOT NULL,
        `Description` text,
        `StartDate` date DEFAULT NULL,
        `EndDate` date DEFAULT NULL,
        `Options` int(11) NOT NULL,
        `Status` tinyint(4) NOT NULL,
        `CreationDate` date NOT NULL,
        `LastUpdate` timestamp NOT NULL,
        PRIMARY KEY (`ID`),
        KEY `Teacher` (`Teacher`),
        KEY `Subject` (`Subject`),
        CONSTRAINT `Group_ibfk_1` FOREIGN KEY (`Teacher`) REFERENCES `Teacher` (`ID`),
        CONSTRAINT `Group_ibfk_2` FOREIGN KEY (`Subject`) REFERENCES `Subject` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = latin1;
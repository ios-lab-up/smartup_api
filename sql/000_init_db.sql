-- Adminer 4.8.1 MySQL 5.7.39 dump

SET NAMES utf8;

SET time_zone = '+00:00';

SET foreign_key_checks = 0;

SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

set character_set_client = 'utf8';

set character_set_connection = 'utf8';

set character_set_database = 'utf8';

set character_set_results = 'utf8';

set character_set_server = 'utf8';

DROP TABLE IF EXISTS `App`;

CREATE TABLE
    `App` (
        `ID` int(11) NOT NULL AUTO_INCREMENT,
        `Name` varchar(255) NOT NULL,
        `Key` varchar(255) NOT NULL,
        `Admin` int(11) DEFAULT NULL,
        PRIMARY KEY (`ID`),
        KEY `Admin` (`Admin`),
        CONSTRAINT `App_ibfk_1` FOREIGN KEY (`Admin`) REFERENCES `User` (`ID`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO
    `App` (`ID`, `Name`, `Key`, `Admin`)
VALUES (
        1,
        'SmartUP',
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOjEsImV4cCI6NTUxNjAyMzUzNn0.uIrYEN-JJZ2KsGMTtRhJvwb2z8W2WJMIMbWg9Ve--yM',
        1
    );
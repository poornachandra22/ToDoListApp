CREATE DATABASE `todolist`;
CREATE TABLE `tasks` (
  `idtasks` int(11) NOT NULL AUTO_INCREMENT,
  `taskscontent` varchar(255) NOT NULL,
  PRIMARY KEY (`idtasks`)
);
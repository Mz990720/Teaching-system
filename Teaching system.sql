/*******************************************************************************
   TeachSystem Database - Version 0.1
   Script: Teaching system.sql
   Description: Creates and populates the TeachSystem database.
   DB Server: MySQL
********************************************************************************/

/*******************************************************************************
   Previous Setting
********************************************************************************/
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

/*******************************************************************************
   Drop database
********************************************************************************/
DROP DATABASE IF EXISTS TeachSystem;

/*******************************************************************************
   Create database
********************************************************************************/
CREATE DATABASE TeachSystem;

USE TeachSystem;

/*******************************************************************************
   Create Tables
********************************************************************************/
CREATE TABLE `Student`( 
    `StudentId` VARCHAR(10) NOT NULL,
    `LoginPassword` VARCHAR(120) NOT NULL,
    `UserName` VARCHAR(20) NOT NULL,
    `RealName` VARCHAR(20) NOT NULL,
    `SexId` INT NOT NULL,
    `College` VARCHAR(20) NOT NULL,
    `Phone` VARCHAR(11) NOT NULL,
    `Email` VARCHAR(60) NOT NULL,
    `Description` VARCHAR(512) ,
    `CourseNumber` INT NOT NULL,
    `CourseID` VARCHAR(140) NOT NULL,
    CONSTRAINT `PK_StudentId` PRIMARY KEY (`StudentId`)
);

INSERT INTO `Student` (`studentId`, `LoginPassword`, `UserName`, `RealName`, `SexId`, `college`,`Phone`, `Email`, `Description`,`CourseNumber`,`CourseID`) VALUES ('3170101010', 'pbkdf2:sha256:50000$LQL9X8i9$af463c266d44ef644b60704c96ed7138eb762b99d0eb91a197830203c2d610c3','Zhang', 'ZhangSan',1,'computer science','13112345678','123456@qq.com','good!',2,'0101001 0101002 ');
INSERT INTO `Student` (`studentId`, `LoginPassword`, `UserName`, `RealName`, `SexId`, `college`,`Phone`, `Email`, `Description`,`CourseNumber`,`CourseID`) VALUES ('3170101001', 'pbkdf2:sha256:50000$LQL9X8i9$af463c266d44ef644b60704c96ed7138eb762b99d0eb91a197830203c2d610c3','Li', 'Lisi',0,'computer science','13112345677','1234567@qq.com','very good!',3,'0101001 0101002 0101003 ');


CREATE TABLE `Teacher`( 
    `TeacherId` VARCHAR(11) NOT NULL,
    `LoginPassword` VARCHAR(120) NOT NULL,
    `UserName` VARCHAR(20) NOT NULL,
    `RealName` VARCHAR(20) NOT NULL,
    `SexId` INT NOT NULL,
    `College` VARCHAR(20) NOT NULL,
    `Phone` VARCHAR(11) NOT NULL,
    `Email` VARCHAR(60) NOT NULL,
    `Description` VARCHAR(512) ,
    `CourseNumber` INT NOT NULL,

    CONSTRAINT `PK_TeacherId` PRIMARY KEY (`TeacherId`)
);
INSERT INTO `Teacher` (`TeacherId`, `LoginPassword`, `UserName`, `RealName`, `SexId`, `college`,`Phone`, `Email`, `Description`,`CourseNumber`) VALUES ('20170101010', 'pbkdf2:sha256:50000$LQL9X8i9$af463c266d44ef644b60704c96ed7138eb762b99d0eb91a197830203c2d610c3','Joker', 'LiSi',0,'computer science','15959038291','123@qq.com','not good!',1);
INSERT INTO `Teacher` (`TeacherId`, `LoginPassword`, `UserName`, `RealName`, `SexId`, `college`,`Phone`, `Email`, `Description`,`CourseNumber`) VALUES ('20180201001', 'pbkdf2:sha256:50000$LQL9X8i9$af463c266d44ef644b60704c96ed7138eb762b99d0eb91a197830203c2d610c3','Laoda', 'Lousir',1,'computer science','15959038292','1234@qq.com','very good!',1);
INSERT INTO `Teacher` (`TeacherId`, `LoginPassword`, `UserName`, `RealName`, `SexId`, `college`,`Phone`, `Email`, `Description`,`CourseNumber`) VALUES ('20180201002', 'pbkdf2:sha256:50000$LQL9X8i9$af463c266d44ef644b60704c96ed7138eb762b99d0eb91a197830203c2d610c3','Lu', 'Luxiqun',1,'computer science','15959038292','1234@qq.com','good!',1);


CREATE TABLE `Visitor`( 
   	`UserName` VARCHAR(20) NOT NULL,
   	`LoginPassword` VARCHAR(120) NOT NULL,
   	`Phone` VARCHAR(11) NOT NULL,
   	`Email`  VARCHAR(60) NOT NULL,
   	`CourseRecord` VARCHAR(140) NOT NULL,
    PRIMARY KEY (`UserName`)
);


CREATE TABLE `Course`(
    `CourseID` VARCHAR(7) NOT NULL,
    `CourseName` VARCHAR(20) NOT NULL,
    `TeacherId` VARCHAR(11) NOT NULL,
    `CoursewareAddress` VARCHAR(100),
	`HomeworkNumber` INT NOT NULL,
	`StudentsNumber` INT NOT NULL,
	`CourseTime` INT NOT NULL, 
	`TestTime` VARCHAR(11) NOT NULL,
	`Information` VARCHAR(512), 
    PRIMARY KEY (`CourseId`)
);
INSERT INTO `Course`(`CourseID`,`CourseName`,`TeacherID`,`CoursewareAddress`,`HomeworkNumber`,`StudentsNumber`,`CourseTime`,`TestTime`,`Information`)VALUES('0101001','数据结构','20170101010','./data/coursesource/20170101010/0101001',1,50,16,'2019.12.29','计算机学院的必修课：关于数据结构和算法。');
INSERT INTO `Course`(`CourseID`,`CourseName`,`TeacherID`,`CoursewareAddress`,`HomeworkNumber`,`StudentsNumber`,`CourseTime`,`TestTime`,`Information`)VALUES('0101002','计组','20180201001','./data/coursesource/20180201001/0101002',1,40,16,'2020.1.10','计算机学院的必修课：关于计算机系统原理');
INSERT INTO `Course`(`CourseID`,`CourseName`,`TeacherID`,`CoursewareAddress`,`HomeworkNumber`,`StudentsNumber`,`CourseTime`,`TestTime`,`Information`)VALUES('0101003','计算理论','20180201002','./data/coursesource/20180201002/0101003',1,30,16,'2020.1.11','计算机学院的必修课：关于计算机网络知识');
INSERT INTO `Course`(`CourseID`,`CourseName`,`TeacherID`,`CoursewareAddress`,`HomeworkNumber`,`StudentsNumber`,`CourseTime`,`TestTime`,`Information`)VALUES('0101004','计网','20170101010','./data/coursesource/20170101010/0101003',1,50,16,'2020.1.11','计算机学院的必修课：关于计算机网络知识');
INSERT INTO `Course`(`CourseID`,`CourseName`,`TeacherID`,`CoursewareAddress`,`HomeworkNumber`,`StudentsNumber`,`CourseTime`,`TestTime`,`Information`)VALUES('0101005','操作系统','20170101010','./data/coursesource/20170101010/0101004',1,50,16,'2020.1.11','计算机学院的必修课：关于计算机操作系统');


CREATE TABLE `Homework`( 
    `CourseId` VARCHAR(7) NOT NULL,
	`TeacherId` VARCHAR(11) NOT NULL,
    `HomeworkNumber` INT NOT NULL,
    `TaskAddress` VARCHAR(100) ,
    `StudentAddress` VARCHAR(100),
    `Description` VARCHAR(512) ,
    `Deadline` DATETIME NOT NULL,
    `Score` INT NOT NULL,
    `Submitnumber` INT NOT NULL,
    PRIMARY KEY (`CourseId`,`TeacherId`,`HomeworkNumber`)
);
INSERT INTO `Homework` (`CourseId` ,`TeacherId`,`HomeworkNumber`,`TaskAddress`,`StudentAddress`,`Description`,`Deadline`,`Score`,`Submitnumber`)VALUES('0101001','20170101010',1,'./data/coursesource/20170101010/0101001/teacher-homework','./data/coursesource/20170101010/0101001/student-homework','NP problem','2019-12-31 00:00:00',50,0);
INSERT INTO `Homework` (`CourseId` ,`TeacherId`,`HomeworkNumber`,`TaskAddress`,`StudentAddress`,`Description`,`Deadline`,`Score`,`Submitnumber`)VALUES('0101002','20180201001',1,'./data/coursesource/20180201001/0101002/teacher-homework','./data/coursesource/20180201001/0101002/student-homework','Virtual Memory','2020-1-1 00:00:00',100,0);
INSERT INTO `Homework` (`CourseId` ,`TeacherId`,`HomeworkNumber`,`TaskAddress`,`StudentAddress`,`Description`,`Deadline`,`Score`,`Submitnumber`)VALUES('0101003','20180201002',1,'./data/coursesource/20180201002/0101003/teacher-homework','./data/coursesource/20180201002/0101003/student-homework','Physical Layer','2020-1-2 00:00:00',100,0);

CREATE TABLE `Thecode`( 
    `Id` INT NOT NULL,
	  `Realcode` VARCHAR(11) NOT NULL,
    `Format` INT NOT NULL,
    PRIMARY KEY (`Id`)
);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(1,'uwv6',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(2,'k4p8',2);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(3,'7364',2);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(4,'zppk',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(5,'qnmx',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(6,'5809',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(7,'LXFC',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(8,'FLNK',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(9,'MGNU',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(10,'VYIL',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(11,'Q3NB',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(12,'2REU',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(13,'7YQI',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(14,'CLF8',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(15,'ADZ7',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(16,'QDNI',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(17,'74M3',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(18,'FURA',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(19,'VI60',1);
INSERT INTO `Thecode`(`Id`,`Realcode`,`Format`)VALUES(20,'S45D',1);

CREATE TABLE `Board_Public`(
     `Title` VARCHAR(50)  NULL,
     `UserName` VARCHAR(20) NOT NULL , 
     `Content`  VARCHAR(100) NOT NULL, /*发言的内容*/
     `Number` INT NOT NULL  /*发言的序号*/
);
INSERT INTO `Board_Public` () VALUES('留言板','李强','请问如何查看作业','1');
INSERT INTO `Board_Public` () VALUES('留言板','张婷','同问','2');

CREATE TABLE `Board_CourseName`( 
     `Title` VARCHAR(50) NOT NULL, 
     `UserName` VARCHAR(20) NOT NULL ,
     `Content`  VARCHAR(100) NOT NULL, 
     `Number` INT NOT NULL,
     `Type`  INT NOT NULL /*一个课程有多个留言板，一次用0,1,2表示*/
);
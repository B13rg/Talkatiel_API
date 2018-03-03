/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.5.57 : Database - talkatiel
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`talkatiel` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `talkatiel`;

/*Table structure for table `posts` */

DROP TABLE IF EXISTS `posts`;

CREATE TABLE `posts` (
  `postID` double NOT NULL AUTO_INCREMENT,
  `title` varchar(70) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `postDate` datetime DEFAULT NULL,
  `upvotes` double DEFAULT NULL,
  `downvotes` double DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `parentPost` double DEFAULT NULL,
  `userID` double DEFAULT NULL,
  PRIMARY KEY (`postID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `postsarchive` */

DROP TABLE IF EXISTS `postsarchive`;

CREATE TABLE `postsarchive` (
  `postID` double NOT NULL,
  `title` varchar(70) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `postDate` datetime DEFAULT NULL,
  `upvotes` double DEFAULT NULL,
  `downvotes` double DEFAULT NULL,
  `parentPost` double DEFAULT NULL,
  `userID` double DEFAULT NULL,
  `moveDate` datetime DEFAULT NULL,
  PRIMARY KEY (`postID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `reports` */

DROP TABLE IF EXISTS `reports`;

CREATE TABLE `reports` (
  `reportID` double NOT NULL AUTO_INCREMENT,
  `postID` double DEFAULT NULL,
  `userID` double DEFAULT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`reportID`),
  KEY `PostReference` (`postID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `ID` double NOT NULL,
  `phonenumber` varchar(16) DEFAULT NULL,
  `deviceID` double DEFAULT NULL,
  `points` double DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

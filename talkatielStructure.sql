/*Table structure for table `posts` */

CREATE TABLE `posts` (
  `postID` double PRIMARY KEY,
  `title` varchar(70) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `postDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `upvotes` double DEFAULT NULL,
  `downvotes` double DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `parentPost` double DEFAULT NULL,
  `userID` double DEFAULT NULL
);

/*Table structure for table `postsarchive` */

CREATE TABLE `postsarchive` (
  `postID` double PRIMARY KEY,
  `title` varchar(70) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `postDate` datetime DEFAULT NULL,
  `upvotes` double DEFAULT NULL,
  `downvotes` double DEFAULT NULL,
  `parentPost` double DEFAULT NULL,
  `userID` double DEFAULT NULL,
  `moveDate` datetime DEFAULT CURRENT_TIMESTAMP
);

/*Table structure for table `reports` */

CREATE TABLE `reports` (
  `reportID` double,
  `postID` double DEFAULT NULL,
  `userID` double DEFAULT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`reportID`)
);

/*Table structure for table `users` */

CREATE TABLE `users` (
  `ID` double NOT NULL,
  `phonenumber` varchar(16) DEFAULT NULL,
  `deviceID` double DEFAULT NULL,
  `points` double DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
);
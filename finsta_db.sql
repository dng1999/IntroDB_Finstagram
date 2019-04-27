-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Apr 19, 2019 at 11:44 PM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `finsta`
--

-- --------------------------------------------------------

--
-- Table structure for table `Belong`
--

CREATE TABLE `Belong` (
  `groupName` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `groupOwner` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `CloseFriendGroup`
--

CREATE TABLE `CloseFriendGroup` (
  `groupName` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `groupOwner` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Comment`
--

CREATE TABLE `Comment` (
  `commentID`int(11) NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photoID` int(11) NOT NULL,
  `commentText` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Follow`
--

CREATE TABLE `Follow` (
  `followerUsername` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `followeeUsername` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `acceptedfollow` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Liked`
--

CREATE TABLE `Liked` (
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photoID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Person`
--

CREATE TABLE `Person` (
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` char(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fname` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lname` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(2048) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bio` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `isPrivate` tinyint(1) DEFAULT NULL,
  `displayTimestamp` tinyint(1) DEFAULT '0',
  `displayTagged` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Photo`
--

CREATE TABLE `Photo` (
  `photoID` int(11) NOT NULL,
  `photoOwner` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `filePath` varchar(2048) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `caption` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `allFollowers` tinyint(1) DEFAULT NULL,
  `groupName` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `groupOwner` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Share`
--

CREATE TABLE `Share` (
  `groupName` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `groupOwner` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photoID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Tag`
--

CREATE TABLE `Tag` (
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photoID` int(11) NOT NULL,
  `acceptedTag` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Belong`
--
ALTER TABLE `Belong`
  ADD PRIMARY KEY (`groupName`,`groupOwner`,`username`),
  ADD KEY `belong_ibfk_2` (`username`);

--
-- Indexes for table `CloseFriendGroup`
--
ALTER TABLE `CloseFriendGroup`
  ADD PRIMARY KEY (`groupName`,`groupOwner`),
  ADD KEY `closefriendgroup_ibfk_1` (`groupOwner`);

--
-- Indexes for table `Comment`
--
ALTER TABLE `Comment`
  ADD PRIMARY KEY (`commentID`),
  ADD KEY `comment_ibfk_1` (`photoID`),
  ADD KEY `comment_ibfk_2` (`username`);

--
-- Indexes for table `Follow`
--
ALTER TABLE `Follow`
  ADD PRIMARY KEY (`followerUsername`,`followeeUsername`),
  ADD KEY `follow_ibfk_2` (`followeeUsername`);

--
-- Indexes for table `Liked`
--
ALTER TABLE `Liked`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `liked_ibfk_2` (`photoID`);

--
-- Indexes for table `Person`
--
ALTER TABLE `Person`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `Photo`
--
ALTER TABLE `Photo`
  ADD PRIMARY KEY (`photoID`),
  ADD KEY `cf_group` (`groupName`,`groupOwner`),
  ADD KEY `photo_ibfk_1` (`photoOwner`);

--
-- Indexes for table `Share`
--
ALTER TABLE `Share`
  ADD PRIMARY KEY (`groupName`,`groupOwner`,`photoID`),
  ADD KEY `share_ibfk_2` (`photoID`);

--
-- Indexes for table `Tag`
--
ALTER TABLE `Tag`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `tag_ibfk_2` (`photoID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Photo`
--
ALTER TABLE `Photo`
  MODIFY `photoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


-- AUTO_INCREMENT for table `Comment`
--
ALTER TABLE `Comment`
  MODIFY `commentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


--
-- Constraints for dumped tables
--

--
-- Constraints for table `Belong`
--
ALTER TABLE `Belong`
  ADD CONSTRAINT `belong_ibfk_1` FOREIGN KEY (`groupName`,`groupOwner`) REFERENCES `CloseFriendGroup` (`groupName`, `groupOwner`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `belong_ibfk_2` FOREIGN KEY (`username`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `CloseFriendGroup`
--
ALTER TABLE `CloseFriendGroup`
  ADD CONSTRAINT `closefriendgroup_ibfk_1` FOREIGN KEY (`groupOwner`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Comment`
--
ALTER TABLE `Comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`username`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Follow`
--
ALTER TABLE `Follow`
  ADD CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`followerUsername`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`followeeUsername`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Liked`
--
ALTER TABLE `Liked`
  ADD CONSTRAINT `liked_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `liked_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Photo`
--
ALTER TABLE `Photo`
  ADD CONSTRAINT `cf_group` FOREIGN KEY (`groupName`,`groupOwner`) REFERENCES `CloseFriendGroup` (`groupName`, `groupOwner`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `photo_ibfk_1` FOREIGN KEY (`photoOwner`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Share`
--
ALTER TABLE `Share`
  ADD CONSTRAINT `share_ibfk_1` FOREIGN KEY (`groupName`,`groupOwner`) REFERENCES `CloseFriendGroup` (`groupName`, `groupOwner`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `share_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Tag`
--
ALTER TABLE `Tag`
  ADD CONSTRAINT `tag_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tag_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`) ON DELETE CASCADE ON UPDATE CASCADE;

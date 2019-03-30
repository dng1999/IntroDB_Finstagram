-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 30, 2019 at 01:34 AM
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

--
-- Dumping data for table `Person`
--

INSERT INTO `Person` (`username`, `password`, `fname`, `lname`, `avatar`, `bio`, `isPrivate`, `displayTimestamp`, `displayTagged`) VALUES
('rainymood', 'b7e57fa71a8e6dfba720495031f1fb442fd7bf60bb620e93e91fadab8d5e2ef2', 'Tomoyo', 'Naka', NULL, NULL, NULL, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `Photo`
--

CREATE TABLE `Photo` (
  `photoID` int(11) NOT NULL,
  `photoOwner` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `filePath` varchar(2048) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `caption` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `allFollowers` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `Photo`
--

INSERT INTO `Photo` (`photoID`, `photoOwner`, `timestamp`, `filePath`, `caption`, `allFollowers`) VALUES
(1, NULL, '2019-03-29 23:32:43', 'rabbit.png', NULL, NULL);

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
  `acceptedTag` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Belong`
--
ALTER TABLE `Belong`
  ADD PRIMARY KEY (`groupName`,`groupOwner`,`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `CloseFriendGroup`
--
ALTER TABLE `CloseFriendGroup`
  ADD PRIMARY KEY (`groupName`,`groupOwner`),
  ADD KEY `groupOwner` (`groupOwner`);

--
-- Indexes for table `Comment`
--
ALTER TABLE `Comment`
  ADD PRIMARY KEY (`photoID`,`username`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `Follow`
--
ALTER TABLE `Follow`
  ADD PRIMARY KEY (`followerUsername`,`followeeUsername`),
  ADD KEY `followeeUsername` (`followeeUsername`);

--
-- Indexes for table `Liked`
--
ALTER TABLE `Liked`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

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
  ADD KEY `photoOwner` (`photoOwner`);

--
-- Indexes for table `Share`
--
ALTER TABLE `Share`
  ADD PRIMARY KEY (`groupName`,`groupOwner`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Tag`
--
ALTER TABLE `Tag`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Photo`
--
ALTER TABLE `Photo`
  MODIFY `photoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Belong`
--
ALTER TABLE `Belong`
  ADD CONSTRAINT `belong_ibfk_1` FOREIGN KEY (`groupName`,`groupOwner`) REFERENCES `CloseFriendGroup` (`groupName`, `groupOwner`),
  ADD CONSTRAINT `belong_ibfk_2` FOREIGN KEY (`username`) REFERENCES `Person` (`username`);

--
-- Constraints for table `CloseFriendGroup`
--
ALTER TABLE `CloseFriendGroup`
  ADD CONSTRAINT `closefriendgroup_ibfk_1` FOREIGN KEY (`groupOwner`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Comment`
--
ALTER TABLE `Comment`
  ADD CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`),
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`username`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Follow`
--
ALTER TABLE `Follow`
  ADD CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`followerUsername`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`followeeUsername`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Liked`
--
ALTER TABLE `Liked`
  ADD CONSTRAINT `liked_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `liked_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Photo`
--
ALTER TABLE `Photo`
  ADD CONSTRAINT `photo_ibfk_1` FOREIGN KEY (`photoOwner`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Share`
--
ALTER TABLE `Share`
  ADD CONSTRAINT `share_ibfk_1` FOREIGN KEY (`groupName`,`groupOwner`) REFERENCES `CloseFriendGroup` (`groupName`, `groupOwner`),
  ADD CONSTRAINT `share_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Tag`
--
ALTER TABLE `Tag`
  ADD CONSTRAINT `tag_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `tag_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

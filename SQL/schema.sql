-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 16, 2014 at 03:25 PM
-- Server version: 5.5.35
-- PHP Version: 5.4.4-14+deb7u7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `doorKarma`
--
DROP DATABASE `doorKarma`;
CREATE DATABASE `doorKarma` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `doorKarma`;

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
CREATE TABLE IF NOT EXISTS `events` (
  `eventNumber` int(11) NOT NULL AUTO_INCREMENT,
  `rFrom` varchar(64) NOT NULL,
  `rFill` varchar(64) DEFAULT NULL,
  `tSubmit` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tFill` timestamp NULL DEFAULT NULL,
  `platSubType` varchar(255) NOT NULL,
  `platSubVer` varchar(255) NOT NULL,
  `platSubUUID` varchar(255) NOT NULL,
  `platFillType` varchar(255) DEFAULT NULL,
  `platFillVer` varchar(255) DEFAULT NULL,
  `platFillUUID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`eventNumber`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 01, 2024 at 06:08 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `oefhz`
--

-- --------------------------------------------------------

--
-- Table structure for table `fts_app_role`
--

CREATE TABLE `fts_app_role` (
  `id` bigint(20) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fts_app_role`
--

INSERT INTO `fts_app_role` (`id`, `role_name`, `description`, `status`) VALUES
(1, 'ADMIN', 'admin', 1),
(2, 'GMS', 'gms', 1),
(3, 'DAKGHAR', 'dak', 1),
(4, 'HOS', 'hos', 1),
(5, 'GO', 'go', 1),
(6, 'CO', 'co', 1),
(7, 'DO', 'do', 1),
(8, 'GM', 'gm', 1); 

-- --------------------------------------------------------

--
-- Table structure for table `fts_app_user`
--

CREATE TABLE `fts_app_user` (
  `id` bigint(20) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fts_app_user`
--

INSERT INTO `fts_app_user` (`id`, `username`, `email`, `password`, `created`, `updated`, `status`) VALUES
(1, 'admin', 'admin@admin.com', 'pbkdf2_sha256$600000$t96IGSt5SlPKFVqY4CSNYJ$H9DF2PQtSq82x/ybiBCp6fm3ruGJi6pmFmRxPhpmQp8=', '2024-05-08 18:15:28.000000', '2024-05-08 18:15:28.000000', 1),
(2, 'dakghar', NULL, 'pbkdf2_sha256$600000$09waHuFA0Hkx0Tgy8Fqy2d$k6rvNuRrshrTgZ0oPOMXPofKr8hzTlCBfSkoVChWpt8=', '2024-05-08 15:38:55.302982', '2024-05-08 15:38:55.302982', 1),
(3, 'gms', NULL, 'pbkdf2_sha256$600000$vMSYJf5rK4g5Bez97nS6FV$ZtvQ3EQGK953oiBHm/LbBNgnzhuZNPIZJFUpR8nFQqQ=', '2024-05-08 17:41:36.144957', '2024-05-08 17:41:36.144957', 1),
(4, 'user1', NULL, 'pbkdf2_sha256$600000$ZGnqrl055mpImOyNMbIbbf$6R9i2PzX39OA3dG61M9lb3UedeKTzgrMxP+d8NLgGc0=', '2024-05-08 17:44:13.009062', '2024-05-08 17:44:13.009062', 1),
(5, 'user2', NULL, 'pbkdf2_sha256$600000$IuGuU348kbphccMcEclrwm$LVORZA4iXQ5rDrLN4U3rebLgSGeHEzsa0UwgkboX/Bc=', '2024-05-08 17:44:43.774196', '2024-05-23 11:15:58.979402', 1),
(6, 'user3', NULL, 'pbkdf2_sha256$600000$h08yf1Ey5eFT0pCboVmsb0$gFlFrL+ZgvJLaROwzsRXtWpJ/GD2QaD4cI8lUG/vTXA=', '2024-05-08 17:45:06.113681', '2024-05-08 17:45:06.113681', 1),
(7, 'user4', NULL, 'pbkdf2_sha256$600000$YG2nw3TAh7meisC3LhmU8R$TM896mdP2wnXUv/ng8+OW8x6ORo+ypxibWmpWAn4aZg=', '2024-05-08 17:45:32.601148', '2024-05-08 17:45:32.601148', 1),
(8, 'gm', NULL, 'pbkdf2_sha256$600000$XJf2CUHKuAf0W1KdzUAP3l$D9jq5dVvXIg9kKLxxUQoT94Fscesvpo1dgMtEwFjfYE=', '2024-05-10 17:24:43.853589', '2024-05-10 17:24:43.853589', 1),
(9, 'user5', NULL, 'pbkdf2_sha256$600000$bYntKFzcfkOuHBL6JSvoMr$gTH7+NlPg3+Sf5Oed/HFyJvFgQLr9GUcSINJPbNp6MU=', '2024-05-11 19:16:20.146209', '2024-05-11 19:16:20.146209', 1),
(16, 'admin12', NULL, 'pbkdf2_sha256$600000$0424xwqyrKHWMA9LdGrEvA$0VO2o4Oo7xmuV3zDSrMxaJSRPayoS2E7+djIZ6tXREQ=', '2024-05-22 10:29:42.005405', '2024-05-22 10:29:42.005405', 1);

-- --------------------------------------------------------

--
-- Table structure for table `fts_app_userdetail`
--

CREATE TABLE `fts_app_userdetail` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fts_app_userdetail`
--

INSERT INTO `fts_app_userdetail` (`id`, `email`, `full_name`, `created`, `updated`, `status`, `user_id`, `phone`) VALUES
(1, 'admin@admin.com', 'Algobasket1', '2024-05-08 19:22:53.000000', '2024-05-08 19:22:53.000000', 1, 1, '1'),
(2, NULL, 'Name Dakghar', '2024-05-08 15:38:55.304486', '2024-05-08 15:38:55.304486', 1, 2, '1'),
(3, NULL, 'Name GMS', '2024-05-08 17:41:36.147011', '2024-05-08 17:41:36.147011', 1, 3, '1'),
(4, NULL, 'Laxman Sharma', '2024-05-08 17:44:13.010567', '2024-05-23 13:01:16.807099', 1, 4, '8888888888'),
(5, NULL, 'Rahul Bhatia', '2024-05-08 17:44:43.775203', '2024-05-23 11:28:56.209019', 1, 5, '8888888888'),
(6, NULL, 'Sachin Ten', '2024-05-08 17:45:06.114682', '2024-05-23 15:07:47.219131', 1, 6, '8888888888'),
(7, NULL, 'Tanmay', '2024-05-08 17:45:32.602209', '2024-05-08 17:45:32.602209', 1, 7, '1'),
(8, NULL, 'Lavit', '2024-05-10 17:24:43.854587', '2024-05-10 17:24:43.854587', 1, 8, '1'),
(9, NULL, 'Krish', '2024-05-11 19:16:20.147715', '2024-05-11 19:16:20.147715', 1, 9, '1'),
(14, NULL, 'Algobasket2', '2024-05-22 10:29:42.007407', '2024-05-22 10:29:42.007407', 1, 16, '08800580884');

-- --------------------------------------------------------

--
-- Table structure for table `fts_app_userrolemap`
--

CREATE TABLE `fts_app_userrolemap` (
  `id` bigint(20) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `role_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fts_app_userrolemap`
--

INSERT INTO `fts_app_userrolemap` (`id`, `status`, `role_id`, `user_id`) VALUES
(1, 1, 1, 1),
(2, 1, 3, 2),
(3, 1, 2, 3),
(4, 1, 4, 4),
(5, 1, 5, 5),
(6, 1, 6, 6),
(7, 1, 7, 7),
(8, 1, 8, 8),
(9, 1, 4, 9),
(14, 1, 1, 16);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fts_app_role`
--
ALTER TABLE `fts_app_role`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fts_app_user`
--
ALTER TABLE `fts_app_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `fts_app_userdetail`
--
ALTER TABLE `fts_app_userdetail`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fts_app_userdetail_user_id_9ffc4649_fk_fts_app_user_id` (`user_id`);

--
-- Indexes for table `fts_app_userrolemap`
--
ALTER TABLE `fts_app_userrolemap`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fts_app_userrolemap_role_id_1dffc6d3_fk_fts_app_role_id` (`role_id`),
  ADD KEY `fts_app_userrolemap_user_id_83aeac7f_fk_fts_app_user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fts_app_role`
--
ALTER TABLE `fts_app_role`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `fts_app_user`
--
ALTER TABLE `fts_app_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `fts_app_userdetail`
--
ALTER TABLE `fts_app_userdetail`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `fts_app_userrolemap`
--
ALTER TABLE `fts_app_userrolemap`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fts_app_userdetail`
--
ALTER TABLE `fts_app_userdetail`
  ADD CONSTRAINT `fts_app_userdetail_user_id_9ffc4649_fk_fts_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `fts_app_user` (`id`);

--
-- Constraints for table `fts_app_userrolemap`
--
ALTER TABLE `fts_app_userrolemap`
  ADD CONSTRAINT `fts_app_userrolemap_role_id_1dffc6d3_fk_fts_app_role_id` FOREIGN KEY (`role_id`) REFERENCES `fts_app_role` (`id`),
  ADD CONSTRAINT `fts_app_userrolemap_user_id_83aeac7f_fk_fts_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `fts_app_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

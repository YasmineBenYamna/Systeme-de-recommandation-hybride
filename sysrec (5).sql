-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 07 mai 2025 à 13:24
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `sysrec`
--

-- --------------------------------------------------------

--
-- Structure de la table `achats`
--

CREATE TABLE `achats` (
  `id_achat` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_produit` int(11) DEFAULT NULL,
  `quantite` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `achats`
--

INSERT INTO `achats` (`id_achat`, `id_user`, `id_produit`, `quantite`) VALUES
(1, 2, 35, 1),
(2, 1, 18, 1);

-- --------------------------------------------------------

--
-- Structure de la table `notes`
--

CREATE TABLE `notes` (
  `id_user` int(11) NOT NULL,
  `id_produit` int(11) NOT NULL,
  `note` int(11) DEFAULT NULL CHECK (`note` >= 1 and `note` <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `notes`
--

INSERT INTO `notes` (`id_user`, `id_produit`, `note`) VALUES
(1, 17, 1),
(1, 23, 2),
(1, 25, 4),
(1, 28, 1),
(1, 29, 4),
(1, 30, 3),
(1, 31, 1),
(1, 32, 2),
(1, 35, 4),
(1, 36, 1),
(2, 17, 5),
(2, 25, 2),
(2, 28, 5),
(2, 29, 2),
(2, 30, 1),
(2, 31, 4),
(2, 32, 4),
(3, 24, 5),
(3, 25, 2),
(3, 28, 4),
(3, 29, 5),
(3, 30, 4),
(3, 31, 2),
(3, 32, 5),
(3, 36, 4);

-- --------------------------------------------------------

--
-- Structure de la table `produit`
--

CREATE TABLE `produit` (
  `id_produit` int(11) NOT NULL,
  `description` text NOT NULL,
  `prix` decimal(10,2) NOT NULL,
  `top1` int(11) DEFAULT NULL,
  `top2` int(11) DEFAULT NULL,
  `top3` int(11) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `nomproduit` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `produit`
--

INSERT INTO `produit` (`id_produit`, `description`, `prix`, `top1`, `top2`, `top3`, `image_url`, `nomproduit`) VALUES
(17, 'Ordinateur portable 15 pouces avec processeur Intel Core i7, 16 Go de RAM, SSD 512 Go.', 899.99, 18, 33, 27, 'pc1.jpeg', 'Dell Inspiron 15 Pro'),
(18, 'Ordinateur de bureau pour gaming, carte graphique RTX 3060, 32 Go RAM.', 1299.00, 17, 33, 27, 'pc2.jpeg', 'HP Omen Gamer X'),
(19, 'PC portable d’entrée de gamme, idéal pour les étudiants.', 429.00, 30, 20, 33, 'pc3.jpeg', 'HP Pavilion Student 14'),
(20, 'Mini PC compact pour usage bureautique.', 349.99, 30, 19, 21, 'pc4.jpg', 'Lenovo ThinkCentre Nano'),
(21, 'PC tout-en-un avec écran 24 pouces Full HD.', 749.00, 22, 20, 19, 'pc5.jpeg', 'Dell Inspiron All-in-One 24'),
(22, 'Caméra numérique 24 MP avec zoom optique 20x.', 599.90, 32, 25, 21, 'camera1.jpg', 'Sony CyberShot Zoom X20'),
(23, 'Caméra reflex avec capteur haute résolution et écran orientable.', 949.00, 32, 25, 30, 'camera2.jpeg', 'Canon EOS 250D'),
(24, 'Caméra de surveillance IP Wi-Fi avec vision nocturne.', 89.99, 35, 32, 26, 'camera3.jpg', 'Xiaomi Mi Home Security'),
(25, 'Reflex numérique avec objectif 18-55mm.', 899.00, 23, 22, 17, 'camera4.jpg', 'Canon EOS 2000D'),
(26, 'Caméra de tableau de bord pour voiture avec détection de mouvement.', 79.00, 35, 32, 24, 'camera5.jpg', 'Xiaomi Dash Cam Pro'),
(27, 'Smartphone Android avec écran AMOLED 6.5\", 128 Go de stockage.', 499.99, 17, 30, 23, 'phone1.jpg', 'Samsung Galaxy A72'),
(28, 'iPhone 13 avec puce A15 Bionic, 256 Go.', 899.99, 17, 27, 18, 'phone2.jpg', 'Apple iPhone 13 256Go'),
(29, 'Smartphone 5G avec batterie 5000mAh, double SIM.', 379.90, 31, 36, 32, 'phone3.jpg', 'Xiaomi Redmi Note 12 Pro'),
(30, 'Téléphone compact avec écran 5.4\", idéal pour une main.', 329.90, 20, 19, 27, 'phone4.jpg', 'Apple iPhone 13 Mini'),
(31, 'Smartphone reconditionné, garanti 12 mois.', 199.00, 36, 32, 29, 'phone5.jpg', 'Apple iPhone SE - Reconditionné'),
(32, 'Smartphone avec triple caméra et capteur principal 108 MP.', 649.99, 23, 22, 35, 'phone6.jpg', 'Xiaomi Redmi Note 11 Pro'),
(33, 'Ordinateur portable 17 pouces pour graphisme et montage vidéo.', 1399.99, 17, 19, 21, 'pc6.jpg', 'HP Envy Creator 17'),
(34, 'Smartphone incassable avec coque renforcée, parfait pour le chantier.', 299.00, 31, 36, 32, 'phone7.jpg', 'DOOGEE S96 Pro'),
(35, 'Caméra pour vloggers avec stabilisation intégrée.', 499.00, 32, 24, 26, 'camera6.jpg', 'Sony ZV-E10 Vlogger'),
(36, 'Smartphone de la série Pro avec charge rapide.', 599.00, 31, 32, 29, 'phone8.jpg', 'Apple iPhone 12 Pro');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `adresse` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id_user`, `login`, `password`, `adresse`) VALUES
(1, 'usf', 'mdp1', 'alice@example.com'),
(2, 'Bojb', 'mdp2', 'bob@example.com'),
(3, 'Cha', 'mdp3', 'charlie@example.com');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `achats`
--
ALTER TABLE `achats`
  ADD PRIMARY KEY (`id_achat`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_produit` (`id_produit`);

--
-- Index pour la table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id_user`,`id_produit`),
  ADD KEY `id_produit` (`id_produit`);

--
-- Index pour la table `produit`
--
ALTER TABLE `produit`
  ADD PRIMARY KEY (`id_produit`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `login` (`login`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `achats`
--
ALTER TABLE `achats`
  MODIFY `id_achat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `produit`
--
ALTER TABLE `produit`
  MODIFY `id_produit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `achats`
--
ALTER TABLE `achats`
  ADD CONSTRAINT `achats_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`),
  ADD CONSTRAINT `achats_ibfk_2` FOREIGN KEY (`id_produit`) REFERENCES `produit` (`id_produit`);

--
-- Contraintes pour la table `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE CASCADE,
  ADD CONSTRAINT `notes_ibfk_2` FOREIGN KEY (`id_produit`) REFERENCES `produit` (`id_produit`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

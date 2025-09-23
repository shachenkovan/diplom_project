-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: diplom_project
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `passwrd` varchar(255) NOT NULL,
  `fio` varchar(150) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT ' ',
  `email` varchar(100) DEFAULT NULL,
  `role_id` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (34,'admin','scrypt:32768:8:1$w8NRVetd8Q8GamSh$aa53409c3c46341a3a7c1fbc15a5b3e763c49792d421d9f8ee46c5259c2fbc8ca9479041e1390361f0982da9c2f546d861f171c249fcf3083d4ebb805d0533c7','Иванов Иван Иванович','2003-03-03','89063206733','admin@domain.com',1,'2025-05-04 12:24:10','2025-09-19 11:01:46'),(35,'e_morozova','scrypt:32768:8:1$GP3X8F8Zz7n50K4X$f2c00fdbefc5b8ec29ed4d858823df5a5f45db5e243ba911cd0296f65d7b36e13866d0b0119c8ec3618e266027d15a8a32441d8945cc0699ce582cad80fa0c71','Морозова Екатерина Викторовна','1961-06-03','89201245768','morozova1@mail.com',2,'2025-05-04 13:31:56','2025-09-22 11:37:34'),(36,'moderator','scrypt:32768:8:1$9hNvYU2rgowqbmCR$6fd052d1693143bd4954beb03109bb75dfd2edef1cf85b026db7f1f5f136bf297d6800ae986739eb4f1513ca2183919429ce0cce7c6117e4bc7c5d0b1ed06ebe','Петров Петр Петрович','2001-02-01','89265453908','moderator@domain.com',3,'2025-05-04 13:35:09','2025-05-04 13:35:09'),(37,'sidorovv','scrypt:32768:8:1$HXU4z3V8WlgulrM5$3ba1ee695181aa6db4777fc37760200409704c0219a7b665241b746b3b716e20593f2af8eba29c03105d13524989b3f9b57720beba4edf903c4355f684af2647','Сидоров Георгий Максимович',NULL,NULL,'sid1988@mail.com',2,'2025-05-05 14:17:15','2025-05-05 14:17:15');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-23 11:37:28

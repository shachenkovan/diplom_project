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
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(10000) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `published` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (41,'Поздравляем с днём рождения!','Сегодня день рождения у наших коллег:\r\n— Анна Петрова (отдел кадров)\r\n— Илья Смирнов (ИТ-отдел)\r\nЖелаем здоровья, вдохновения и отличного настроения! ?','2025-05-04 13:57:44',1),(42,'Новый порядок подачи заявок на отпуск','С 1 июня заявки на отпуск будут приниматься исключительно через портал.\r\nДля подачи заявки необходимо перейти в раздел \"Запросить отпуск\" и выбрать желаемый период. Подтверждение придёт после одобрения руководства.','2025-05-04 13:58:52',1),(43,'Субботник на территории предприятия','Дорогие коллеги!\r\n11 мая в 10:00 состоится весенний субботник. Приглашаем всех желающих принять участие в благоустройстве территории.\r\nИнвентарь будет выдан на месте. После работ — чай и угощения!','2025-05-04 13:59:07',1),(44,'Напоминание о прохождении инструктажа','До 10 мая всем сотрудникам необходимо пройти ежегодный инструктаж по технике безопасности.\r\nИнструктаж доступен в разделе \"Техника безопасности\" на портале. После прохождения не забудьте подтвердить это у вашего руководителя.','2025-05-04 13:59:19',1),(45,'Внимание! Плановое отключение электроэнергии','Уважаемые сотрудники!\r\n5 мая с 10:00 до 13:00 в связи с техническими работами будет произведено плановое отключение электроэнергии в корпусах Б и В. Просим сохранить все данные и завершить работу оборудования заранее.\r\nСпасибо за понимание!','2025-05-04 13:59:36',1);
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
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

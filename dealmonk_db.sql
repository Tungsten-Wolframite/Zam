-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: dealmonk_db
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'super user'),(2,'super_user_group'),(3,'vkm_user');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,1,41),(42,1,42),(43,1,43),(44,1,44),(45,1,45),(46,1,46),(47,1,47),(48,1,48),(49,1,49),(50,1,50),(51,1,51),(52,1,52),(53,1,53),(54,1,54),(55,1,55),(56,1,56),(57,1,57),(58,1,58),(59,1,59),(60,1,60),(61,2,1),(62,2,2),(63,2,3),(64,2,4),(65,2,5),(66,2,6),(67,2,7),(68,2,8),(69,2,9),(70,2,10),(71,2,11),(72,2,12),(73,2,13),(74,2,14),(75,2,15),(76,2,16),(77,2,17),(78,2,18),(79,2,19),(80,2,20),(81,2,21),(82,2,22),(83,2,23),(84,2,24),(85,2,25),(86,2,26),(87,2,27),(88,2,28),(89,2,29),(90,2,30),(91,2,31),(92,2,32),(93,2,33),(94,2,34),(95,2,35),(96,2,36),(97,2,37),(98,2,38),(99,2,39),(100,2,40),(101,2,41),(102,2,42),(103,2,43),(104,2,44),(105,2,45),(106,2,46),(107,2,47),(108,2,48),(109,2,49),(110,2,50),(111,2,51),(112,2,52),(113,2,53),(114,2,54),(115,2,55),(116,2,56),(117,2,57),(118,2,58),(119,2,59),(120,2,60),(121,3,1),(122,3,2),(123,3,3),(124,3,4),(125,3,5),(126,3,6),(127,3,7),(128,3,8),(129,3,9),(130,3,10),(131,3,11),(132,3,12),(133,3,13),(134,3,14),(135,3,15),(136,3,16),(137,3,17),(138,3,18),(139,3,19),(140,3,20),(141,3,21),(142,3,22),(143,3,23),(144,3,24),(145,3,25),(146,3,26),(147,3,27),(148,3,28),(149,3,29),(150,3,30),(151,3,31),(152,3,32),(153,3,33),(154,3,34),(155,3,35),(156,3,36),(157,3,37),(158,3,38),(159,3,39),(160,3,40),(161,3,41),(162,3,42),(163,3,43),(164,3,44),(165,3,45),(166,3,46),(167,3,47),(168,3,48),(169,3,49),(170,3,50),(171,3,51),(172,3,52),(173,3,53),(174,3,54),(175,3,55),(176,3,56),(177,3,57),(178,3,58),(179,3,59),(180,3,60);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add user',7,'add_restaurantadmin'),(20,'Can change user',7,'change_restaurantadmin'),(21,'Can delete user',7,'delete_restaurantadmin'),(22,'Can add user',8,'add_consumer'),(23,'Can change user',8,'change_consumer'),(24,'Can delete user',8,'delete_consumer'),(25,'Can add consumer payment credentials',9,'add_consumerpaymentcredentials'),(26,'Can change consumer payment credentials',9,'change_consumerpaymentcredentials'),(27,'Can delete consumer payment credentials',9,'delete_consumerpaymentcredentials'),(28,'Can add restaurant',10,'add_restaurant'),(29,'Can change restaurant',10,'change_restaurant'),(30,'Can delete restaurant',10,'delete_restaurant'),(31,'Can add restaurant branch',11,'add_restaurantbranch'),(32,'Can change restaurant branch',11,'change_restaurantbranch'),(33,'Can delete restaurant branch',11,'delete_restaurantbranch'),(34,'Can add area fact table',12,'add_areafacttable'),(35,'Can change area fact table',12,'change_areafacttable'),(36,'Can delete area fact table',12,'delete_areafacttable'),(37,'Can add restaurant rating',13,'add_restaurantrating'),(38,'Can change restaurant rating',13,'change_restaurantrating'),(39,'Can delete restaurant rating',13,'delete_restaurantrating'),(40,'Can add restaurant offer',14,'add_restaurantoffer'),(41,'Can change restaurant offer',14,'change_restaurantoffer'),(42,'Can delete restaurant offer',14,'delete_restaurantoffer'),(43,'Can add restaurant booking',15,'add_restaurantbooking'),(44,'Can change restaurant booking',15,'change_restaurantbooking'),(45,'Can delete restaurant booking',15,'delete_restaurantbooking'),(46,'Can add invoice',16,'add_invoice'),(47,'Can change invoice',16,'change_invoice'),(48,'Can delete invoice',16,'delete_invoice'),(49,'Can add offer_map',17,'add_offer_map'),(50,'Can change offer_map',17,'change_offer_map'),(51,'Can delete offer_map',17,'delete_offer_map'),(52,'Can add cuisine fact table',18,'add_cuisinefacttable'),(53,'Can change cuisine fact table',18,'change_cuisinefacttable'),(54,'Can delete cuisine fact table',18,'delete_cuisinefacttable'),(55,'Can add cuisine restaurent map',19,'add_cuisinerestaurentmap'),(56,'Can change cuisine restaurent map',19,'change_cuisinerestaurentmap'),(57,'Can delete cuisine restaurent map',19,'delete_cuisinerestaurentmap'),(58,'Can add cuisine restaurent branch map',20,'add_cuisinerestaurentbranchmap'),(59,'Can change cuisine restaurent branch map',20,'change_cuisinerestaurentbranchmap'),(60,'Can delete cuisine restaurent branch map',20,'delete_cuisinerestaurentbranchmap');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$4SZrmWP7EqKB$f4GufSU4aqScZepEXHrIj1Dccb1cZJOc0f/lEoPyEDI=','2015-09-04 10:29:05',1,'admin','','','',1,1,'2015-08-28 11:35:59'),(2,'pbkdf2_sha256$20000$DLEyjs4A7jbg$JqM5bqrJ1gSVHZE/TzoFqZOOy4cYM9mZhCZKCCprVCs=','2015-09-03 14:10:45',0,'v@gmail.com','vikram','chandel','',1,1,'2015-08-28 11:42:06'),(3,'admin',NULL,0,'vkas@gmail.com','Vikas','Padhy','vkas@gmail.com',0,1,'2015-08-28 14:55:30'),(4,'admin',NULL,0,'deal@gmail.com','Manoj','Bawane','deal@gmail.com',0,1,'2015-08-28 14:57:29'),(5,'admin',NULL,0,'akshay@gmail.com','Akshay','Maldhure','akshay@gmail.com',0,1,'2015-08-28 14:58:34'),(6,'admin',NULL,0,'Pranali@gmail.com','Pranali','Khatode','Pranali@gmail.com',0,1,'2015-08-28 15:00:00'),(7,'pbkdf2_sha256$20000$8nBWmQ5ctPKB$6Yakw9sJ/EhCxVbS/jnz6TyQx69/mbUGAtJcMb0rF7A=',NULL,0,'demoa@demo.com','','','',0,1,'2015-08-28 15:22:49'),(8,'pbkdf2_sha256$20000$0zw6s3YUBH79$66bIErTgQD0YZ7gsr1XbC2qZU4iwtM+v326AJhpch9Q=','2015-08-28 16:09:40',0,'kasturi@gmail.com','kasturi','panse','',1,1,'2015-08-28 16:09:08'),(9,'pbkdf2_sha256$20000$gXzwfJ6Ra1qS$d2dvRoz88n/5Sj2d1qqGhLkUoev/4FLoz5+vMsJ9pQ4=','2015-08-30 12:33:08',0,'mikesawant@gmail.com','Mike','Sawant','',1,1,'2015-08-30 09:14:06'),(10,'pbkdf2_sha256$20000$MvhUt47hxegE$9kg6svNfYQHHgCMoQBDK+kF7WDDDiSm+B+xCg3xnbPc=','2015-09-01 07:17:23',0,'sdf@gmail.com','fds','dsf','',1,1,'2015-08-31 15:14:29'),(11,'pbkdf2_sha256$20000$s9SKBdGBS8Oq$XD+s3haWPby3oYd23KD5JZsFUM1KrggmX61H0zL/opk=',NULL,0,'nilgud@gmail.com','nilesh','g','',1,1,'2015-08-31 15:17:16'),(12,'pbkdf2_sha256$20000$Wth1Eywi8zKa$DPDb0wc1UrMa7C/OSOkCpSuUQJeAtURuiooC1mI9Eio=','2015-08-31 15:19:08',0,'dalone@gmail.com','darshana','alone','',1,1,'2015-08-31 15:18:56'),(13,'pbkdf2_sha256$20000$IO9GmamtQCuy$6Vg7XXBucymD+mAaJV/M2/rNkYBYKQ7fN/vziQVgAQk=',NULL,0,'kasturi.panse@tungstenbigdata.','Kasturi','Panse','',1,1,'2015-09-02 13:46:16'),(14,'pbkdf2_sha256$20000$U33CLZgOuOC0$/c1qw5D9JQppQA5OTS/nls/KFDxM81JVUvT0IzQ2o4U=','2015-09-02 13:47:28',0,'samir@gmail.com','Samir','Mohan','',1,1,'2015-09-02 13:47:09'),(15,'pbkdf2_sha256$20000$AvreitYTF39p$MOGORoPTGYu6NI2JLN8B5Lq4DeQni5jKBISBiEFmR94=','2015-09-02 14:15:23',0,'kgudhe@gmail.com','kirti','gudhe','',1,1,'2015-09-02 13:48:30'),(16,'pbkdf2_sha256$20000$IKwjBSadmPSq$lTjP53s/RsNM3LR4rerL7mxi/d/OORzo27M60ckMGNo=','2015-09-02 14:14:43',0,'A@gmail.com','A','B','',1,1,'2015-09-02 14:14:26'),(17,'pbkdf2_sha256$20000$a5vJ2u4qBWRw$AIliB9vrPSQtgUejcz36FvQQnd8unM3eq1fQnwXWXKE=','2015-09-02 14:25:52',0,'dilip@gmail.com','Dilip','Shah','',1,1,'2015-09-02 14:25:05'),(18,'pbkdf2_sha256$20000$vtD6lxmOHj0o$NMsP7QevlKUYzCbkcKWV7jqI9dnZLGqDFcZG/pGTU6g=','2015-09-02 15:32:21',0,'shivani@gmail.com','Shivani','Sawant','',1,1,'2015-09-02 15:31:35'),(19,'pbkdf2_sha256$20000$dQ58aD7D10iw$/v+/zqWyDZb0YK2v9NL8d1kkSXo6oO5+DrGIM4mVFR4=',NULL,0,'abhi@gmail.com','Abhi','shek','',1,1,'2015-09-03 04:56:02'),(20,'pbkdf2_sha256$20000$bczxO6k2BzpP$mcMJC9PytY3UU8M25WenvztWYgYm84bxrvlHkDOfh5E=','2015-09-03 14:16:15',1,'admin@admin.com','admin','admin','admin@admin.com',1,1,'2015-09-03 09:37:47'),(21,'pbkdf2_sha256$20000$O8osDaMjpp18$udq9jPdEmmjB8jWE7vgiCbPkIwZ1qxRNjV/XVAK5C5M=','2015-09-03 11:12:32',0,'mohan@gmail.com','mohan','lal','',1,1,'2015-09-03 11:11:52'),(22,'pbkdf2_sha256$20000$XTWHGa8h7r0u$gMWNwHkvYegYLiLzqn/ll3kaNa2pPBmfmM17P00rPag=',NULL,0,'sc@gmail.com','Shubhangi','Chaudhari','',1,1,'2015-09-03 11:16:21'),(23,'pbkdf2_sha256$20000$tdFAo93Pmlip$DCIte6jahOtz3mx1fgqTkWIt8WA8LpoMGrzb04q4lP8=',NULL,0,'z@gmail.com','z','y','',1,1,'2015-09-03 12:00:18'),(24,'pbkdf2_sha256$20000$Hqku5a4GFVrL$QgruQxslo8co6U57T/H6nYlkRA/JAIgIANrxE/bwWDo=',NULL,0,'asfa@as.com','a','kumar','',1,1,'2015-09-03 12:03:02'),(25,'pbkdf2_sha256$20000$FIoSmef5me7e$X8gRGMWVqYaiVqbRNVJ5BXL0gecYXeQUXI3Kpke3A1Y=',NULL,0,'e@gmail.com','e','e','',1,1,'2015-09-03 12:17:51'),(26,'pbkdf2_sha256$20000$jJ3bLLec6fLr$4J3jUSxGIFV9FEjCxsf35u0i4DDNUYSFQBi7pGnvrFo=','2015-09-03 13:43:42',0,'vikas.d.padhy@gmail.com','Bipin','Das','',1,1,'2015-09-03 12:42:33'),(27,'pbkdf2_sha256$20000$c49rIM47N0SJ$yah7c7GAU6oJh85HWrjfCsrZdvaQ5+Zo6UCaDv8U5OI=',NULL,0,'dev@dm.com','Dev','Vyas','',1,1,'2015-09-03 12:47:11'),(28,'pbkdf2_sha256$20000$7iGMmmQJboW5$oaEHrFSy2LB44jXIDZnezw9FgGT6/+vLNjc1P3fS/nE=',NULL,0,'lopa@dm.com','Lopa','Gawas','',1,1,'2015-09-03 12:47:44'),(30,'pbkdf2_sha256$20000$26d8SLaGPhaK$Yof8n4jL5FJD46GnLD8v7y+mP/VqfD+5z812bC0fFU8=',NULL,0,'swapnil.kadu@tungstenbigdata.c','Swapnil','Kadu','',1,1,'2015-09-03 13:48:06'),(31,'pbkdf2_sha256$20000$6HCfl7riAidK$Ag0MUsIiBjJpmQ6erpxHWjIAlkIm114Rz4OuUwi2uU0=','2015-09-03 14:17:28',0,'saza@dm.com','Saza','Maaf','',1,1,'2015-09-03 14:16:51');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,20,1),(2,20,2),(3,20,3);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,20,1),(2,20,2),(3,20,3),(4,20,4),(5,20,5),(6,20,6),(7,20,7),(8,20,8),(9,20,9),(10,20,10),(11,20,11),(12,20,12),(13,20,13),(14,20,14),(15,20,15),(16,20,16),(17,20,17),(18,20,18),(19,20,19),(20,20,20),(21,20,21),(22,20,22),(23,20,23),(24,20,24),(25,20,25),(26,20,26),(27,20,27),(28,20,28),(29,20,29),(30,20,30),(31,20,31),(32,20,32),(33,20,33),(34,20,34),(35,20,35),(36,20,36),(37,20,37),(38,20,38),(39,20,39),(40,20,40),(41,20,41),(42,20,42),(43,20,43),(44,20,44),(45,20,45),(46,20,46),(47,20,47),(48,20,48),(49,20,49),(50,20,50),(51,20,51),(52,20,52),(53,20,53),(54,20,54),(55,20,55),(56,20,56),(57,20,57),(58,20,58),(59,20,59),(60,20,60);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_areafacttable`
--

DROP TABLE IF EXISTS `dealmonkapp_areafacttable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_areafacttable` (
  `fact_id` int(11) NOT NULL AUTO_INCREMENT,
  `fact_city` varchar(45) NOT NULL,
  `fact_state` varchar(45) NOT NULL,
  PRIMARY KEY (`fact_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_areafacttable`
--

LOCK TABLES `dealmonkapp_areafacttable` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_areafacttable` DISABLE KEYS */;
INSERT INTO `dealmonkapp_areafacttable` VALUES (1,'Pune','Maharashtra'),(2,'Mumbai','Maharashtra'),(3,'New Delhi','Delhi'),(4,'Bengaluru','Karnatka'),(5,'Hyderabad','Telangana'),(6,'Jaipur','Rajasthan'),(7,'Kolkata','WB'),(8,'chennai','Tamilnadu'),(9,'Bhopal','MP'),(10,'Sagar','MP');
/*!40000 ALTER TABLE `dealmonkapp_areafacttable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_consumer`
--

DROP TABLE IF EXISTS `dealmonkapp_consumer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_consumer` (
  `user_ptr_id` int(11) NOT NULL,
  `consumer_id` int(11) NOT NULL AUTO_INCREMENT,
  `consumer_email` varchar(45) NOT NULL,
  `consumer_contactno` varchar(45) DEFAULT NULL,
  `consumer_first_name` varchar(45) NOT NULL,
  `consumer_last_name` varchar(45) NOT NULL,
  `sign_up_via` varchar(10) DEFAULT NULL,
  `sign_up_source` varchar(10) DEFAULT NULL,
  `apns_token` varchar(10) DEFAULT NULL,
  `consumer_image` varchar(255) NOT NULL,
  `consumer_city` varchar(45) DEFAULT NULL,
  `consumer_state` varchar(45) DEFAULT NULL,
  `consumer_country` varchar(45) DEFAULT NULL,
  `consumer_gender` varchar(1) DEFAULT NULL,
  `consumer_age` int(11) DEFAULT NULL,
  `consumer_location` varchar(45) DEFAULT NULL,
  `consumer_feedback` varchar(200) DEFAULT NULL,
  `consumer_brownypoint` int(11) DEFAULT NULL,
  `is_consumer_email_alert` varchar(1) DEFAULT NULL,
  `is_consumer_sms_alert` varchar(1) DEFAULT NULL,
  `consumer_create_by` varchar(45) DEFAULT NULL,
  `consumer_create_date` datetime DEFAULT NULL,
  `consumer_update_by` varchar(45) DEFAULT NULL,
  `consumer_update_date` datetime DEFAULT NULL,
  `consumer_status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`consumer_id`),
  UNIQUE KEY `user_ptr_id` (`user_ptr_id`),
  CONSTRAINT `dealmonkapp_consume_user_ptr_id_43c1d596c79830bb_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_consumer`
--

LOCK TABLES `dealmonkapp_consumer` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_consumer` DISABLE KEYS */;
INSERT INTO `dealmonkapp_consumer` VALUES (7,1,'demoa@demo.com','8976567854','demoa','demo','DMAPP','DMAPP','','images/uploaded_image2015-08-28_152249_050123.png',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `dealmonkapp_consumer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_consumerpaymentcredentials`
--

DROP TABLE IF EXISTS `dealmonkapp_consumerpaymentcredentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_consumerpaymentcredentials` (
  `consumer_payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `consumer_payment_bankname` varchar(45) NOT NULL,
  `consumer_payment_cardno` varchar(45) NOT NULL,
  `consumer_payment_cardtype` varchar(45) NOT NULL,
  `consumer_payment_cvv` varchar(45) NOT NULL,
  `consumer_payment_expdate` date NOT NULL,
  `consumer_payment_datetime` datetime NOT NULL,
  `consumer_payment_create_by` varchar(45) NOT NULL,
  `consumer_payment_create_date` datetime NOT NULL,
  `consumer_payment_update_date` datetime NOT NULL,
  `consumer_payment_update_by` varchar(45) NOT NULL,
  `consumer_payment_status` varchar(1) NOT NULL,
  `consumer_id_id` int(11) NOT NULL,
  PRIMARY KEY (`consumer_payment_id`),
  KEY `D8f5d02ade3416ff07f946e9b48ed5f6` (`consumer_id_id`),
  CONSTRAINT `D8f5d02ade3416ff07f946e9b48ed5f6` FOREIGN KEY (`consumer_id_id`) REFERENCES `dealmonkapp_consumer` (`consumer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_consumerpaymentcredentials`
--

LOCK TABLES `dealmonkapp_consumerpaymentcredentials` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_consumerpaymentcredentials` DISABLE KEYS */;
/*!40000 ALTER TABLE `dealmonkapp_consumerpaymentcredentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_cuisinefacttable`
--

DROP TABLE IF EXISTS `dealmonkapp_cuisinefacttable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_cuisinefacttable` (
  `fact_id` int(11) NOT NULL AUTO_INCREMENT,
  `fact_cuisine` varchar(70) NOT NULL,
  `fact_cuisine_create_date` datetime DEFAULT NULL,
  `fact_cuisine_create_by` varchar(45) NOT NULL,
  `fact_cuisine_update_date` datetime DEFAULT NULL,
  `fact_cuisine_update_by` varchar(45) NOT NULL,
  PRIMARY KEY (`fact_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_cuisinefacttable`
--

LOCK TABLES `dealmonkapp_cuisinefacttable` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_cuisinefacttable` DISABLE KEYS */;
INSERT INTO `dealmonkapp_cuisinefacttable` VALUES (1,'Indian','2015-09-02 13:56:05','Admin','2015-09-02 13:55:28','Admin'),(2,'Chinese','2015-09-02 13:56:24','Admin','2015-09-02 13:56:15','Admin'),(3,'North Indian','2015-09-02 13:56:50','Admin','2015-09-02 13:56:33','Admin'),(4,'South Indian','2015-09-02 13:57:26','Admin','2015-09-02 13:57:20','Admin'),(5,'West Indian','2015-09-02 14:12:05','Admin','2015-09-02 14:11:58','Admin');
/*!40000 ALTER TABLE `dealmonkapp_cuisinefacttable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_cuisinerestaurentbranchmap`
--






DROP TABLE IF EXISTS `dealmonkapp_cuisinerestaurentbranchmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_cuisinerestaurentbranchmap` (
  `cuisine_rest_branch_id` int(11) NOT NULL AUTO_INCREMENT,
  `cuisine_rest_branch_create_date` datetime DEFAULT NULL,
  `cuisine_rest_branch_create_by` varchar(45) NOT NULL,
  `cuisine_rest_branch_update_date` datetime DEFAULT NULL,
  `cuisine_rest_branch_update_by` varchar(45) NOT NULL,
  `cuisine_id_id` int(11) DEFAULT NULL,
  `restaurant_branch_id_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cuisine_rest_branch_id`),
  KEY `fcea6cc0af4ef880ab0add766cb97d84` (`cuisine_id_id`),
  KEY `dealmonkapp_cuisinerestaurentbranchmap_368dc34f` (`restaurant_branch_id_id`),
  CONSTRAINT `D282debf7fd90358f314a66c81ea6382` FOREIGN KEY (`restaurant_branch_id_id`) REFERENCES `dealmonkapp_restaurantbranch` (`restaurant_branch_id`),
  CONSTRAINT `fcea6cc0af4ef880ab0add766cb97d84` FOREIGN KEY (`cuisine_id_id`) REFERENCES `dealmonkapp_cuisinefacttable` (`fact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_cuisinerestaurentbranchmap`
--

LOCK TABLES `dealmonkapp_cuisinerestaurentbranchmap` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_cuisinerestaurentbranchmap` DISABLE KEYS */;
/*!40000 ALTER TABLE `dealmonkapp_cuisinerestaurentbranchmap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_cuisinerestaurentmap`
--

DROP TABLE IF EXISTS `dealmonkapp_cuisinerestaurentmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_cuisinerestaurentmap` (
  `cuisine_rest_id` int(11) NOT NULL AUTO_INCREMENT,
  `cuisine_rest_create_date` datetime DEFAULT NULL,
  `cuisine_rest_create_by` varchar(45) NOT NULL,
  `cuisine_rest_update_date` datetime DEFAULT NULL,
  `cuisine_rest_update_by` varchar(45) NOT NULL,
  `cuisine_id_id` int(11) DEFAULT NULL,
  `restaurant_id_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cuisine_rest_id`),
  KEY `ddeca4988bbb80f5dc5f5973361571fa` (`cuisine_id_id`),
  KEY `D274b43ea7c197c08689a13d195bb7bd` (`restaurant_id_id`),
  CONSTRAINT `D274b43ea7c197c08689a13d195bb7bd` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`),
  CONSTRAINT `ddeca4988bbb80f5dc5f5973361571fa` FOREIGN KEY (`cuisine_id_id`) REFERENCES `dealmonkapp_cuisinefacttable` (`fact_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_cuisinerestaurentmap`
--

LOCK TABLES `dealmonkapp_cuisinerestaurentmap` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_cuisinerestaurentmap` DISABLE KEYS */;
INSERT INTO `dealmonkapp_cuisinerestaurentmap` VALUES (1,NULL,'samir@gmail.com','2015-09-02 14:02:13','samir@gmail.com',1,8),(2,NULL,'samir@gmail.com','2015-09-02 14:02:13','samir@gmail.com',2,8),(3,NULL,'samir@gmail.com','2015-09-02 14:02:13','samir@gmail.com',3,8),(4,NULL,'shivani@gmail.com','2015-09-02 15:35:46','shivani@gmail.com',1,9),(5,NULL,'vikas.d.padhy@gmail.com','2015-09-03 12:55:10','vikas.d.padhy@gmail.com',3,10),(6,NULL,'vikas.d.padhy@gmail.com','2015-09-03 12:55:10','vikas.d.padhy@gmail.com',4,10),(7,NULL,'vikas.d.padhy@gmail.com','2015-09-03 12:55:10','vikas.d.padhy@gmail.com',5,10),(8,NULL,'saza@dm.com','2015-09-03 14:20:41','saza@dm.com',3,11),(9,NULL,'saza@dm.com','2015-09-03 14:20:41','saza@dm.com',4,11),(10,NULL,'saza@dm.com','2015-09-03 14:20:41','saza@dm.com',5,11),(11,NULL,'saza@dm.com','2015-09-03 14:20:56','saza@dm.com',3,12),(12,NULL,'saza@dm.com','2015-09-03 14:20:56','saza@dm.com',4,12),(13,NULL,'saza@dm.com','2015-09-03 14:20:56','saza@dm.com',5,12);
/*!40000 ALTER TABLE `dealmonkapp_cuisinerestaurentmap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_invoice`
--

DROP TABLE IF EXISTS `dealmonkapp_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_invoice` (
  `invoice_id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice_datetime` datetime NOT NULL,
  `invoice_amount` int(11) NOT NULL,
  `restaurant_offer_amount` int(11) NOT NULL,
  `invoice_create_datetime` datetime NOT NULL,
  `invoice_create_by` varchar(45) NOT NULL,
  `invoice_update_date` datetime NOT NULL,
  `invoice_update_by` varchar(45) NOT NULL,
  `invoice_status` varchar(1) NOT NULL,
  `consumer_id_id` int(11) NOT NULL,
  `restaurant_booking_id_id` int(11) NOT NULL,
  `restaurant_id_id` int(11) NOT NULL,
  PRIMARY KEY (`invoice_id`),
  KEY `eaf4b55538cc34be5e3971224c0c2bc3` (`consumer_id_id`),
  KEY `dealmonkapp_invoice_674dca3c` (`restaurant_booking_id_id`),
  KEY `dealmonkapp_invoice_7b4e8351` (`restaurant_id_id`),
  CONSTRAINT `cf1b4c78dd3569f8add746c90df4673e` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`),
  CONSTRAINT `D45cc19d4995134d8063232ce5255f90` FOREIGN KEY (`restaurant_booking_id_id`) REFERENCES `dealmonkapp_restaurantbooking` (`restaurant_booking_id`),
  CONSTRAINT `eaf4b55538cc34be5e3971224c0c2bc3` FOREIGN KEY (`consumer_id_id`) REFERENCES `dealmonkapp_consumer` (`consumer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_invoice`
--

LOCK TABLES `dealmonkapp_invoice` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `dealmonkapp_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_offer_map`
--

DROP TABLE IF EXISTS `dealmonkapp_offer_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_offer_map` (
  `offer_map_id` int(11) NOT NULL AUTO_INCREMENT,
  `offer_map_time_from` time DEFAULT NULL,
  `offer_map_time_to` time DEFAULT NULL,
  `offer_map_date` date DEFAULT NULL,
  `offer_map_creation_date` datetime DEFAULT NULL,
  `offer_map_created_by` varchar(45) NOT NULL,
  `offer_map_update_date` datetime DEFAULT NULL,
  `offer_map_update_by` varchar(45) NOT NULL,
  `offer_map_status` varchar(1) NOT NULL,
  `restaurant_id_id` int(11) DEFAULT NULL,
  `restaurant_offer_id_id` int(11) NOT NULL,
  PRIMARY KEY (`offer_map_id`),
  KEY `dealmonkapp_offer_map_7b4e8351` (`restaurant_id_id`),
  KEY `dealmonkapp_offer_map_07bff703` (`restaurant_offer_id_id`),
  CONSTRAINT `D19eee9ebcb038dd026459a9a0cc508c` FOREIGN KEY (`restaurant_offer_id_id`) REFERENCES `dealmonkapp_restaurantoffer` (`restaurant_offer_id`),
  CONSTRAINT `D49c98ddf8207fef629c6e809b5e80c4` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_offer_map`
--

LOCK TABLES `dealmonkapp_offer_map` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_offer_map` DISABLE KEYS */;
INSERT INTO `dealmonkapp_offer_map` VALUES (2,'16:00:00','23:00:00','2015-08-30','2015-08-28 15:29:29','admin','2015-08-28 15:29:29','admin','1',4,2),(3,'18:00:00','21:00:00','2015-08-30','2015-08-28 15:30:15','admin','2015-08-28 15:30:15','admin','1',3,4),(4,'18:00:00','23:30:00','2015-08-30','2015-08-28 15:30:57','admin','2015-08-28 15:30:57','admin','1',5,6),(41,'12:00:00','22:00:00','2015-08-30','2015-08-30 11:45:26','admin','2015-08-30 11:45:26','admin','1',6,9),(62,'22:30:00','00:00:00','2015-08-30','2015-08-30 12:34:41','mikesawant@gmail.com','2015-08-30 12:34:41','mikesawant@gmail.com','1',6,11),(63,'10:30:00','23:30:00','2015-09-02','2015-08-30 12:34:41','mikesawant@gmail.com','2015-08-30 12:34:41','mikesawant@gmail.com','1',6,11),(135,'11:00:00','14:00:00','2015-09-02','2015-09-02 15:43:14','shivani@gmail.com','2015-09-02 15:43:14','shivani@gmail.com','1',9,12),(136,'07:30:00','12:00:00','2015-09-01','2015-09-02 15:43:29','v@gmail.com','2015-09-02 15:43:29','v@gmail.com','1',1,1);
/*!40000 ALTER TABLE `dealmonkapp_offer_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_restaurant`
--

DROP TABLE IF EXISTS `dealmonkapp_restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_restaurant` (
  `restaurant_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_name` varchar(45) NOT NULL,
  `restaurant_owner_firstname` varchar(45) DEFAULT NULL,
  `restaurant_owner_lastname` varchar(45) DEFAULT NULL,
  `restaurant_owner_contact` varchar(45) DEFAULT NULL,
  `restaurant_owner_email` varchar(45) DEFAULT NULL,
  `restaurant_image` varchar(100) NOT NULL,
  `restaurant_contactno` varchar(45) NOT NULL,
  `restaurant_addr1` varchar(45) NOT NULL,
  `restaurant_addr2` varchar(45) NOT NULL,
  `restaurant_area` varchar(45) NOT NULL,
  `restaurant_city` varchar(45) NOT NULL,
  `restaurant_state` varchar(45) NOT NULL,
  `restaurant_zipcode` varchar(45) NOT NULL,
  `restaurant_description` varchar(45) NOT NULL,
  `restaurant_opentime_day` time DEFAULT NULL,
  `restaurant_closetime_day` time DEFAULT NULL,
  `restaurant_opentime_eve` time DEFAULT NULL,
  `restaurant_closetime_eve` time DEFAULT NULL,
  `restaurant_create_date` date DEFAULT NULL,
  `restaurant_create_by` varchar(45) NOT NULL,
  `restaurant_update_date` date DEFAULT NULL,
  `restaurant_update_by` varchar(45) NOT NULL,
  `restaurant_status` varchar(1) NOT NULL,
  `restaurant_has_branch` int(11) NOT NULL,
  `restaurant_cuisine_type` varchar(45) DEFAULT NULL,
  `restaurant_admin_id_id` int(10) NOT NULL,
  `restaurant_lat` varchar(45) DEFAULT NULL,
  `restaurant_lon` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`),
  KEY `dealmonkapp_restaurant_279564bf` (`restaurant_admin_id_id`),
  CONSTRAINT `D85da53cd89504bfabb30f6bf6a35cea` FOREIGN KEY (`restaurant_admin_id_id`) REFERENCES `dealmonkapp_restaurantadmin`(`restaurant_admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_restaurant`
--

LOCK TABLES `dealmonkapp_restaurant` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_restaurant` DISABLE KEYS */;
INSERT INTO `dealmonkapp_restaurant` VALUES (1,'Padhy Khau Restaurant ','Vikas sir','Padhy','9175103645','vikas.padhy@tungstenbigdata.com','default_icon_restaurant.png','9876543210','Kothrud','Kothrud','kothrud','Pune','Maharashtra','411038','Close to IT Hub & Classic Look','03:00:00','03:00:00','14:25:19','14:25:22','2015-08-28','v@gmail.com','2015-08-28','v@gmail.com','1',0,'Indian',1,'18.505915','73.795035'),(2,'Della Cuisines','Bhudevi','Deshpande','9595903117','bhudevi.deshpande@tungstenbigdata.com','default_icon_restaurant.png','020 22002200','Premlok Society','Kothrud','Kothrud Depo','Pune','Maharashtra','411029','Close to IT Hub & Classic Look','14:35:53','14:35:54','14:35:55','14:35:57',NULL,'admin','2015-08-28','admin','1',0,'Italian',2,'18.445819','73.815336'),(3,'Nolera Food Fiesta','Ankita','Lahoti','9923540175','ankita.lahoti@tungstenbigdata.com','restaurant/Modern-Home-in-New-Canaan-Connecticut-Living-Room-Interior.jpg','020 11003322','C-12, F. C. Road','Behind Fitness Hall','Shivaji Nagar','Pune','Maharashtra','411004','Placed in a well surrounded area','14:42:24','14:42:25','14:42:26','14:42:27',NULL,'admin','2015-08-28','admin','1',0,'Punjabi',3,'18.530822','73.847465'),(4,'Lunch-n-Dinner','Kumar','Roy','8877887788','kumar.roy@tungstenbigdata.com','restaurant/Awesome-Living-Room-Interior-HD-1080p-HDWallWide.jpg','020 65566556','23, B Block','Opp. Sane Building','Koregaon Park','Pune','Maharashtra','411007','Rich Area and bliss surroundings','14:46:41','14:46:42','14:46:43','14:46:44',NULL,'admin','2015-08-28','admin','1',0,'Continental',4,'18.536208','73.893975'),(5,'Sunny-n-Sandy','Diwakar','Garg','9565956585','diwakar.garg@tungstenbigdata.com','restaurant/Interior-living-room-small-spaces-design-ideas.jpg','020 99669966','JK park','Below R Mart','Hadapsar','Pune','Maharashtra','411011','Close to IT Hub & Classic Look','14:53:36','14:53:37','14:53:38','14:53:39',NULL,'admin','2015-08-28','admin','1',0,'Mediterrenean',5,'18.508920','73.926026'),(6,'Sirji Da Dhaba','Chaman','Patil','9988998899','vbn@qwe.vom','restaurant/Awesome-Living-Room-Interior-HD-1080p-HDWallWide_wxc7vev.jpg','3322332233','Near Tirangaa Hotel','Paud Phata, Kothrud','Paud Phata','Pune','Maharashtra','411038','Good Food Good People','09:30:00','12:00:00','02:30:00','11:00:00',NULL,'mikesawant@gmail.com','2015-08-30','mikesawant@gmail.com','1',0,'Punjabi',7,'18.507399','73.807650'),(7,'abc Dhawa','','','','','restaurant/Lighthouse_pQ97vBg.jpg','9876543211','1 modibaug','R','modibaug','Pune','Maharashtra','411001','nothing',NULL,NULL,NULL,NULL,NULL,'dalone@gmail.com','2015-08-31','dalone@gmail.com','1',0,NULL,10,'18.5108224','73.79020919999999'),(8,'Vikings Plateau 57','','','','','restaurant/20.jpg','1212112121','Saudamini Commercial Complex','','','Pune','Maharashtra','','Awesome Food Awesome People','09:00:00','14:00:00','15:30:00','22:00:00',NULL,'samir@gmail.com','2015-09-02','samir@gmail.com','1',0,NULL,12,'',''),(9,'Food Funtastica','','','','','restaurant/28.jpg','9988998898','Road No. 10, Banjara Hills','','Anandnagar','Pune','Maharashtra','411038','','09:30:00','14:00:00','15:30:00','22:00:00',NULL,'shivani@gmail.com','2015-09-02','shivani@gmail.com','1',0,NULL,16,'18.510836899999997','73.7895822'),(10,'Razor Shack 69','','','','','restaurant/11.jpg','1245481245','Bank of India, Paud Road, Kothrud','','Kothrud','Pune','Maharashtra','411038','Paradise for Spicy Food Lovers !!!','10:00:00','13:00:00','14:30:00','22:30:00',NULL,'vikas.d.padhy@gmail.com','2015-09-03','vikas.d.padhy@gmail.com','1',0,NULL,23,'18.509431880552793','73.8140058517456'),(11,'Razor Shack 69','','','','','restaurant/12.jpg','1245481245','Bank of India, Paud Road, Kothrud','','Kothrud','Pune','Maharashtra','411038','Paradise for Spicy Food Lovers !!!','10:00:00','13:00:00','14:30:00','22:30:00',NULL,'saza@dm.com','2015-09-03','saza@dm.com','1',0,NULL,27,'18.509263672924703','73.81409168243408'),(12,'Razor Shack 69','','','','','restaurant/12_DS5oE9V.jpg','1245481245','Bank of India, Paud Road, Kothrud','','Kothrud','Pune','Maharashtra','411038','Paradise for Spicy Food Lovers !!!','10:00:00','13:00:00','14:30:00','22:30:00',NULL,'saza@dm.com','2015-09-03','saza@dm.com','1',0,NULL,27,'18.509263672924703','73.81409168243408');
/*!40000 ALTER TABLE `dealmonkapp_restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_restaurantadmin`
--

DROP TABLE IF EXISTS `dealmonkapp_restaurantadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_restaurantadmin` (
  `user_ptr_id` int(11) NOT NULL,
  `restaurant_admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_admin_first_name` varchar(45) NOT NULL,
  `restaurant_admin_last_name` varchar(45) NOT NULL,
  `restaurant_admin_email` varchar(45) NOT NULL,
  `restaurant_admin_contactno` varchar(45) NOT NULL,
  `is_restaurant_admin_email_alert_on` varchar(1) NOT NULL,
  `is_restaurant_admin_sms_alert_on` varchar(1) NOT NULL,
  `restaurant_admin_create_date` datetime NOT NULL,
  `restaurant_admin_create_by` varchar(45) DEFAULT NULL,
  `restaurant_admin_update_date` datetime NOT NULL,
  `restaurant_admin_update_by` varchar(45) DEFAULT NULL,
  `restaurant_admin_status` varchar(1) NOT NULL,
  `restaurant_admin_has_restaurant` int(11) NOT NULL,
  PRIMARY KEY (`restaurant_admin_id`),
  UNIQUE KEY `user_ptr_id` (`user_ptr_id`),
  CONSTRAINT `dealmonkapp_restaur_user_ptr_id_2f73c1b7b14d37f0_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_restaurantadmin`
--

LOCK TABLES `dealmonkapp_restaurantadmin` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_restaurantadmin` DISABLE KEYS */;
INSERT INTO `dealmonkapp_restaurantadmin` VALUES (2,1,'vikram','chandel','v@gmail.com','9876543210','1','1','2015-08-28 11:42:06',NULL,'2015-08-28 11:42:06',NULL,'1',1),(3,2,'Vikas','Padhy','vkas@gmail.com','9175103645','1','1','2015-08-28 14:57:26','admin','2015-08-28 14:55:30','admin','1',0),(4,3,'Manoj','Bawane','deal@gmail.com','9988774411','1','1','2015-08-28 14:58:34','admin','2015-08-28 14:57:29','admin','1',0),(5,4,'Akshay','Maldhure','akshay@gmail.com','8928513850','1','1','2015-08-28 14:59:57','admin','2015-08-28 14:58:34','admin','1',0),(6,5,'Pranali','Khatode','Pranali@gmail.com','7878787878','1','1','2015-08-28 15:01:00','admin','2015-08-28 15:00:00','admin','1',0),(8,6,'kasturi','panse','kasturi@gmail.com','7507542642','1','1','2015-08-28 16:09:08',NULL,'2015-08-28 16:09:08',NULL,'1',0),(9,7,'Mike','Sawant','mikesawant@gmail.com','9175103645','1','1','2015-08-30 09:14:06',NULL,'2015-08-30 09:14:06',NULL,'1',1),(10,8,'fds','dsf','sdf@gmail.com','9876543210','1','1','2015-08-31 15:14:29',NULL,'2015-08-31 15:14:29',NULL,'1',0),(11,9,'nilesh','g','nilgud@gmail.com','1234567899','1','1','2015-08-31 15:17:16',NULL,'2015-08-31 15:17:16',NULL,'1',0),(12,10,'darshana','alone','dalone@gmail.com','1234543322','1','1','2015-08-31 15:18:56',NULL,'2015-08-31 15:18:56',NULL,'1',1),(13,11,'Kasturi','Panse','kasturi.panse@tungstenbigdata.com','7507542642','1','1','2015-09-02 13:46:16',NULL,'2015-09-02 13:46:16',NULL,'1',0),(14,12,'Samir','Mohan','samir@gmail.com','9923540175','1','1','2015-09-02 13:47:09',NULL,'2015-09-02 13:47:09',NULL,'1',1),(15,13,'kirti','gudhe','kgudhe@gmail.com','9766846756','1','1','2015-09-02 13:48:30',NULL,'2015-09-02 13:48:30',NULL,'1',0),(16,14,'A','B','A@gmail.com','9876543210','1','1','2015-09-02 14:14:26',NULL,'2015-09-02 14:14:26',NULL,'1',0),(17,15,'Dilip','Shah','dilip@gmail.com','7845784571','1','1','2015-09-02 14:25:05',NULL,'2015-09-02 14:25:05',NULL,'1',0),(18,16,'Shivani','Sawant','shivani@gmail.com','1245124512','1','1','2015-09-02 15:31:35',NULL,'2015-09-02 15:31:35',NULL,'1',1),(19,17,'Abhi','shek','abhi@gmail.com','9876543210','1','1','2015-09-03 04:56:02',NULL,'2015-09-03 04:56:02',NULL,'1',0),(21,18,'mohan','lal','mohan@gmail.com','9876543210','1','1','2015-09-03 11:11:52',NULL,'2015-09-03 11:11:52',NULL,'1',0),(22,19,'Shubhangi','Chaudhari','sc@gmail.com','4749030987','1','1','2015-09-03 11:16:21',NULL,'2015-09-03 11:16:21',NULL,'1',0),(23,20,'z','y','z@gmail.com','9876543210','1','1','2015-09-03 12:00:18',NULL,'2015-09-03 12:00:18',NULL,'1',0),(24,21,'a','kumar','asfa@as.com','9876543210','1','1','2015-09-03 12:03:02',NULL,'2015-09-03 12:03:02',NULL,'1',0),(25,22,'e','e','e@gmail.com','9876543210','1','1','2015-09-03 12:17:51',NULL,'2015-09-03 12:17:51',NULL,'1',0),(26,23,'Bipin','Das','vikas.d.padhy@gmail.com','9923540175','1','1','2015-09-03 12:42:33',NULL,'2015-09-03 12:42:33',NULL,'1',1),(27,24,'Dev','Vyas','dev@dm.com','4512451245','1','1','2015-09-03 12:47:11',NULL,'2015-09-03 12:47:11',NULL,'1',0),(28,25,'Lopa','Gawas','lopa@dm.com','7845784578','1','1','2015-09-03 12:47:44',NULL,'2015-09-03 12:47:44',NULL,'1',0),(30,26,'Swapnil','Kadu','swapnil.kadu@tungstenbigdata.com','9966996699','1','1','2015-09-03 13:48:06',NULL,'2015-09-03 13:48:06',NULL,'1',0),(31,27,'Saza','Maaf','saza@dm.com','1212121212','1','1','2015-09-03 14:16:51',NULL,'2015-09-03 14:16:51',NULL,'1',1);
/*!40000 ALTER TABLE `dealmonkapp_restaurantadmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_restaurantbooking`
--

DROP TABLE IF EXISTS `dealmonkapp_restaurantbooking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_restaurantbooking` (
  `restaurant_booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_booking_date` date NOT NULL,
  `restaurant_booking_time_from` time NOT NULL,
  `consumer_coupon_code` varchar(45) NOT NULL,
  `restaurant_booking_covers` int(11) NOT NULL,
  `restaurant_booking_status` varchar(45) NOT NULL,
  `restaurant_booking_create_date` datetime DEFAULT NULL,
  `restaurant_booking_create_by` varchar(45) NOT NULL,
  `restaurant_booking_update_date` datetime DEFAULT NULL,
  `restaurant_booking_update_by` varchar(45) NOT NULL,
  `restaurant_checkin_status` int(11) NOT NULL,
  `consumer_id_id` int(11) NOT NULL,
  `restaurant_branch_id_id` int(11) DEFAULT NULL,
  `restaurant_id_id` int(11) DEFAULT NULL,
  `restaurant_offer_id_id` int(11) NOT NULL,
  `restaurant_booking_time_to` time NOT NULL,
  PRIMARY KEY (`restaurant_booking_id`),
  KEY `D94fa061936044eee9d201aaeb6ab14e` (`consumer_id_id`),
  KEY `dealmonkapp_restaurantbooking_368dc34f` (`restaurant_branch_id_id`),
  KEY `dealmonkapp_restaurantbooking_7b4e8351` (`restaurant_id_id`),
  KEY `dealmonkapp_restaurantbooking_07bff703` (`restaurant_offer_id_id`),
  CONSTRAINT `D09b29fc52a15f61e5ed9d175c07337c` FOREIGN KEY (`restaurant_offer_id_id`) REFERENCES `dealmonkapp_restaurantoffer` (`restaurant_offer_id`),
  CONSTRAINT `D0d81410f98ea9a64afcc0f281dbcc2a` FOREIGN KEY (`restaurant_branch_id_id`) REFERENCES `dealmonkapp_restaurantbranch` (`restaurant_branch_id`),
  CONSTRAINT `d891cb832823537bc650891891180656` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`),
  CONSTRAINT `D94fa061936044eee9d201aaeb6ab14e` FOREIGN KEY (`consumer_id_id`) REFERENCES `dealmonkapp_consumer` (`consumer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_restaurantbooking`
--

LOCK TABLES `dealmonkapp_restaurantbooking` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_restaurantbooking` DISABLE KEYS */;
INSERT INTO `dealmonkapp_restaurantbooking` VALUES (1,'2015-08-30','12:00:00','DM2923',2,'Confirmed','2015-08-30 00:00:00','demoa@demo.com','2015-08-30 11:53:59','demoa@demo.com',0,1,NULL,NULL,6,9,'22:00:00'),(3,'2015-08-30','16:00:00','DM5158',2,'Confirmed','2015-08-30 00:00:00','demoa@demo.com','2015-08-30 12:04:50','demoa@demo.com',0,1,NULL,3,NULL,2,'23:00:00');
/*!40000 ALTER TABLE `dealmonkapp_restaurantbooking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_restaurantbranch`
--

DROP TABLE IF EXISTS `dealmonkapp_restaurantbranch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_restaurantbranch` (
  `restaurant_branch_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_branch_name` varchar(45) NOT NULL,
  `restaurant_branch_contact` varchar(45) NOT NULL,
  `restaurant_branch_address1` varchar(45) NOT NULL,
  `restaurant_branch_address2` varchar(45) NOT NULL,
  `restaurant_branch_area` varchar(45) NOT NULL,
  `restaurant_branch_city` varchar(45) NOT NULL,
  `restaurant_branch_state` varchar(45) NOT NULL,
  `restaurant_branch_pincode` varchar(6) NOT NULL,
  `restaurant_branch_lat` varchar(45) NOT NULL,
  `restaurant_branch_lon` varchar(45) NOT NULL,
  `restaurant_branch_opentime_day` time DEFAULT NULL,
  `restaurant_branch_closetime_day` time DEFAULT NULL,
  `restaurant_branch_opentime_eve` time DEFAULT NULL,
  `restaurant_branch_closetime_eve` time DEFAULT NULL,
  `restaurant_branch_cuisine_type` varchar(45) DEFAULT NULL,
  `restaurant_branch_create_date` datetime DEFAULT NULL,
  `restaurant_branch_create_by` varchar(45) NOT NULL,
  `restaurant_branch_update_date` datetime DEFAULT NULL,
  `restaurant_branch_update_by` varchar(45) NOT NULL,
  `restaurant_branch_status` varchar(1) NOT NULL,
  `restaurant_admin_id_id` int(11) NOT NULL,
  `restaurant_id_id` int(11) NOT NULL,
  PRIMARY KEY (`restaurant_branch_id`),
  KEY `ab97b0e2b383794f474c0c88d2a0f7f6` (`restaurant_admin_id_id`),
  KEY `D39cf23db975a759c76384d57d45ab74` (`restaurant_id_id`),
  CONSTRAINT `ab97b0e2b383794f474c0c88d2a0f7f6` FOREIGN KEY (`restaurant_admin_id_id`) REFERENCES `dealmonkapp_restaurantadmin` (`restaurant_admin_id`),
  CONSTRAINT `D39cf23db975a759c76384d57d45ab74` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_restaurantbranch`
--

LOCK TABLES `dealmonkapp_restaurantbranch` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_restaurantbranch` DISABLE KEYS */;
INSERT INTO `dealmonkapp_restaurantbranch` VALUES (1,'Khau Food Gallery','020 1221112','Kalka Nagar','Behind FR Mall','Deccan','Pune','Maharashtra','411005','18.517557','73.841660','15:05:28','15:05:29','15:05:30','15:05:31','Indian','2015-08-28 15:02:13','admin','2015-08-28 15:02:13','admin','1',1,1),(2,'Ginger Food Mall','020 56565656','JP Chowk','Near FSD Showroom','Bavdhan','Pune','Maharashtra','411040','18.515604','73.781905','15:07:54','15:07:56','15:08:01','15:08:02','Punjabi','2015-08-28 15:05:46','admin','2015-08-28 15:05:46','admin','1',2,2),(3,'Seasen Bliss Restaurant','020 25552555','Opp. GSK Gate 1','Erandwana','Nal Stop','Pune','Maharashtra','411005','18.509258','73.831628','15:13:37','15:13:39','15:13:40','15:13:43','Continental','2015-08-28 15:09:05','admin','2015-08-28 15:09:05','admin','1',4,4);
/*!40000 ALTER TABLE `dealmonkapp_restaurantbranch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_restaurantoffer`
--

DROP TABLE IF EXISTS `dealmonkapp_restaurantoffer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_restaurantoffer` (
  `restaurant_offer_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_offer_detail` varchar(45) NOT NULL,
  `restaurant_offer_creation_date` datetime DEFAULT NULL,
  `restaurant_offer_created_by` varchar(45) NOT NULL,
  `restaurant_offer_update_date` datetime DEFAULT NULL,
  `restaurant_offer_update_by` varchar(45) NOT NULL,
  `restaurant_offer_status` varchar(1) NOT NULL,
  `restaurant_id_id` int(11) NOT NULL,
  PRIMARY KEY (`restaurant_offer_id`),
  KEY `D03bd44ac1c5e9dcbeb97e7239cca692` (`restaurant_id_id`),
  CONSTRAINT `D03bd44ac1c5e9dcbeb97e7239cca692` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_restaurantoffer`
--

LOCK TABLES `dealmonkapp_restaurantoffer` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_restaurantoffer` DISABLE KEYS */;
INSERT INTO `dealmonkapp_restaurantoffer` VALUES (1,'10% discount','2015-09-02 11:47:36','v@gmail.com','2015-09-02 11:47:36','v@gmail.com','1',1),(2,'15% discount','2015-08-28 11:47:59','v@gmail.com','2015-08-28 11:47:59','v@gmail.com','1',1),(3,'25% Discount','2015-08-30 15:15:33','','2015-08-30 15:15:33','','1',2),(4,'20% Discount','2015-08-30 15:16:15','','2015-08-30 15:16:15','','1',3),(5,'10% Discount','2015-08-30 15:18:25','','2015-08-30 15:18:25','','1',4),(6,'305% Discount','2015-08-30 15:18:40','','2015-08-30 15:18:40','','1',5),(7,'35% Off','2015-08-30 09:08:56','v@gmail.com','2015-08-30 09:08:56','v@gmail.com','1',1),(9,'50% Off for Lunch for 2','2015-08-30 11:44:50','','2015-08-30 11:44:50','','1',6),(10,'25% discount','2015-08-30 12:22:41','v@gmail.com','2015-08-30 12:22:41','v@gmail.com','1',1),(11,'25% Off','2015-09-02 12:33:29','mikesawant@gmail.com','2015-09-02 12:33:29','mikesawant@gmail.com','1',6),(12,'45% Discount','2015-09-02 15:37:58','shivani@gmail.com','2015-09-02 15:37:58','shivani@gmail.com','1',9),(13,'35% Discount','2015-09-02 15:44:01','shivani@gmail.com','2015-09-02 15:44:01','shivani@gmail.com','1',9),(15,'35% Discount','2015-09-03 12:57:13','vikas.d.padhy@gmail.com','2015-09-03 12:57:13','vikas.d.padhy@gmail.com','1',10),(17,'30% off','2015-09-03 14:26:29','v@gmail.com','2015-09-03 14:26:29','v@gmail.com','1',1);
/*!40000 ALTER TABLE `dealmonkapp_restaurantoffer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dealmonkapp_restaurantrating`
--

DROP TABLE IF EXISTS `dealmonkapp_restaurantrating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealmonkapp_restaurantrating` (
  `restaurant_rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurant_rating` int(11) NOT NULL,
  `restaurant_feedback` varchar(45) NOT NULL,
  `restaurant_issues` varchar(45) NOT NULL,
  `restaurant_rating_create_by` varchar(45) NOT NULL,
  `restaurant_rating_create_date` datetime NOT NULL,
  `restaurant_update_by` varchar(45) NOT NULL,
  `restaurant_update_date` datetime NOT NULL,
  `consumer_id_id` int(11) NOT NULL,
  `restaurant_branch_id_id` int(11) NOT NULL,
  `restaurant_id_id` int(11) NOT NULL,
  PRIMARY KEY (`restaurant_rating_id`),
  KEY `c80f718f5f84a7a8983cb756e9e17687` (`consumer_id_id`),
  KEY `cbaa84b405ce5ccbe5a1ef1e026a8b1b` (`restaurant_branch_id_id`),
  KEY `c13309d94e49af6d33834770bbf04712` (`restaurant_id_id`),
  CONSTRAINT `c13309d94e49af6d33834770bbf04712` FOREIGN KEY (`restaurant_id_id`) REFERENCES `dealmonkapp_restaurant` (`restaurant_id`),
  CONSTRAINT `c80f718f5f84a7a8983cb756e9e17687` FOREIGN KEY (`consumer_id_id`) REFERENCES `dealmonkapp_consumer` (`consumer_id`),
  CONSTRAINT `cbaa84b405ce5ccbe5a1ef1e026a8b1b` FOREIGN KEY (`restaurant_branch_id_id`) REFERENCES `dealmonkapp_restaurantbranch` (`restaurant_branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealmonkapp_restaurantrating`
--

LOCK TABLES `dealmonkapp_restaurantrating` WRITE;
/*!40000 ALTER TABLE `dealmonkapp_restaurantrating` DISABLE KEYS */;
/*!40000 ALTER TABLE `dealmonkapp_restaurantrating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2015-08-28 14:31:51','1','1',2,'Changed restaurant_owner_firstname, restaurant_owner_lastname, restaurant_owner_contact, restaurant_owner_email, restaurant_state, restaurant_zipcode, restaurant_description, restaurant_opentime_day, restaurant_closetime_day, restaurant_opentime_eve, restaurant_closetime_eve, restaurant_cuisine_type, restaurant_lat and restaurant_lon.',10,1),(2,'2015-08-28 14:38:04','2','2',1,'',10,1),(3,'2015-08-28 14:43:58','3','3',1,'',10,1),(4,'2015-08-28 14:48:09','4','4',1,'',10,1),(5,'2015-08-28 14:55:18','5','5',1,'',10,1),(6,'2015-08-28 14:57:26','2','2',1,'',7,1),(7,'2015-08-28 14:58:34','3','3',1,'',7,1),(8,'2015-08-28 14:59:57','4','4',1,'',7,1),(9,'2015-08-28 15:01:00','5','5',1,'',7,1),(10,'2015-08-28 15:01:15','2','2',2,'Changed restaurant_admin_id.',10,1),(11,'2015-08-28 15:01:27','3','3',2,'Changed restaurant_admin_id.',10,1),(12,'2015-08-28 15:01:40','4','4',2,'Changed restaurant_admin_id.',10,1),(13,'2015-08-28 15:01:54','5','5',2,'Changed restaurant_admin_id.',10,1),(14,'2015-08-28 15:05:45','1','1',1,'',11,1),(15,'2015-08-28 15:08:26','2','2',1,'',11,1),(16,'2015-08-28 15:09:05','1','1',2,'Changed restaurant_branch_cuisine_type.',11,1),(17,'2015-08-28 15:14:02','3','3',1,'',11,1),(18,'2015-08-28 15:15:31','2','DMRO00000002',2,'Changed restaurant_offer_detail.',14,1),(19,'2015-08-28 15:16:04','3','DMRO00000003',1,'',14,1),(20,'2015-08-28 15:16:12','2','DMRO00000002',2,'Changed restaurant_id.',14,1),(21,'2015-08-28 15:17:11','4','DMRO00000004',1,'',14,1),(22,'2015-08-28 15:17:54','2','DMRO00000002',2,'Changed restaurant_id.',14,1),(23,'2015-08-28 15:18:04','3','DMRO00000003',2,'Changed restaurant_id.',14,1),(24,'2015-08-28 15:18:15','4','DMRO00000004',2,'No fields changed.',14,1),(25,'2015-08-28 15:18:19','4','DMRO00000004',2,'No fields changed.',14,1),(26,'2015-08-28 15:18:23','3','DMRO00000003',2,'No fields changed.',14,1),(27,'2015-08-28 15:18:40','5','DMRO00000005',1,'',14,1),(28,'2015-08-28 15:18:56','6','DMRO00000006',1,'',14,1),(29,'2015-08-28 15:29:29','1','DMI00000001',1,'',17,1),(30,'2015-08-28 15:30:14','2','DMI00000002',1,'',17,1),(31,'2015-08-28 15:30:57','3','DMI00000003',1,'',17,1),(32,'2015-08-28 15:31:27','4','DMI00000004',1,'',17,1),(33,'2015-08-30 09:06:01','4','DMI00000004',2,'Changed offer_map_date.',17,1),(34,'2015-08-30 09:06:10','3','DMI00000003',2,'Changed offer_map_date.',17,1),(35,'2015-08-30 09:06:20','2','DMI00000002',2,'Changed restaurant_id and offer_map_date.',17,1),(36,'2015-08-30 09:06:26','4','DMI00000004',2,'No fields changed.',17,1),(37,'2015-08-30 09:06:58','6','DMRO00000006',2,'Changed restaurant_offer_creation_date and restaurant_offer_update_date.',14,1),(38,'2015-08-30 09:07:07','5','DMRO00000005',2,'Changed restaurant_offer_creation_date and restaurant_offer_update_date.',14,1),(39,'2015-08-30 09:07:18','6','DMRO00000006',2,'No fields changed.',14,1),(40,'2015-08-30 09:07:27','4','DMRO00000004',2,'Changed restaurant_offer_creation_date and restaurant_offer_update_date.',14,1),(41,'2015-08-30 09:07:37','3','DMRO00000003',2,'Changed restaurant_offer_creation_date and restaurant_offer_update_date.',14,1),(42,'2015-08-30 11:34:10','6','6',2,'Changed restaurant_addr1, restaurant_addr2, restaurant_cuisine_type, restaurant_lat and restaurant_lon.',10,1),(43,'2015-08-30 11:43:07','6','6',2,'Changed restaurant_addr1, restaurant_addr2, restaurant_area and restaurant_lon.',10,1),(44,'2015-08-30 11:43:21','6','6',2,'Changed restaurant_lat.',10,1),(45,'2015-08-30 11:44:50','7','DMRO00000007',2,'No fields changed.',14,1),(46,'2015-08-30 11:45:19','9','DMRO00000009',1,'',14,1),(47,'2015-08-30 11:46:14','41','DMI00000041',1,'',17,1),(48,'2015-08-30 12:02:56','2','DMBK00000002',3,'',15,1),(49,'2015-08-31 15:22:47','1','FT00000001',1,'',12,1),(50,'2015-09-02 05:55:38','131','DMI00000131',2,'Changed offer_map_date.',17,1),(51,'2015-09-02 05:55:55','63','DMI00000063',2,'Changed offer_map_time_from and offer_map_date.',17,1),(52,'2015-09-02 05:56:28','1','DMRO00000001',2,'Changed restaurant_offer_creation_date and restaurant_offer_update_date.',14,1),(53,'2015-09-02 05:56:36','11','DMRO00000011',2,'Changed restaurant_offer_creation_date and restaurant_offer_update_date.',14,1),(54,'2015-09-02 13:56:15','1','1',1,'',18,1),(55,'2015-09-02 13:56:28','2','2',1,'',18,1),(56,'2015-09-02 13:56:55','3','3',1,'',18,1),(57,'2015-09-02 13:57:20','3','3',2,'Changed fact_cuisine.',18,1),(58,'2015-09-02 13:57:30','4','4',1,'',18,1),(59,'2015-09-02 13:58:48','1','FT00000001',2,'No fields changed.',12,1),(60,'2015-09-02 14:03:53','2','FT00000002',1,'',12,1),(61,'2015-09-02 14:04:30','3','FT00000003',1,'',12,1),(62,'2015-09-02 14:04:47','3','FT00000003',2,'Changed fact_city and fact_state.',12,1),(63,'2015-09-02 14:08:01','4','FT00000004',1,'',12,1),(64,'2015-09-02 14:08:51','5','FT00000005',1,'',12,1),(65,'2015-09-02 14:09:50','6','FT00000006',1,'',12,1),(66,'2015-09-02 14:10:04','7','FT00000007',1,'',12,1),(67,'2015-09-02 14:10:32','8','FT00000008',1,'',12,1),(68,'2015-09-02 14:10:46','9','FT00000009',1,'',12,1),(69,'2015-09-02 14:11:11','10','FT00000010',1,'',12,1),(70,'2015-09-02 14:12:10','5','5',1,'',18,1),(71,'2015-09-03 09:36:04','1','super user',1,'',3,1),(72,'2015-09-03 09:36:28','2','super_user_group',1,'',3,1),(73,'2015-09-03 09:36:57','3','vkm_user',1,'',3,1),(74,'2015-09-03 09:37:47','20','admin@admin.com',1,'',4,1),(75,'2015-09-03 09:39:02','20','admin@admin.com',2,'Changed first_name, last_name, email, is_staff, is_superuser, groups, user_permissions and last_login.',4,1),(76,'2015-09-03 12:58:37','14','DMRO00000014',3,'',14,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(12,'dealmonkapp','areafacttable'),(8,'dealmonkapp','consumer'),(9,'dealmonkapp','consumerpaymentcredentials'),(18,'dealmonkapp','cuisinefacttable'),(20,'dealmonkapp','cuisinerestaurentbranchmap'),(19,'dealmonkapp','cuisinerestaurentmap'),(16,'dealmonkapp','invoice'),(17,'dealmonkapp','offer_map'),(10,'dealmonkapp','restaurant'),(7,'dealmonkapp','restaurantadmin'),(15,'dealmonkapp','restaurantbooking'),(11,'dealmonkapp','restaurantbranch'),(14,'dealmonkapp','restaurantoffer'),(13,'dealmonkapp','restaurantrating'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-08-28 11:35:11'),(2,'auth','0001_initial','2015-08-28 11:35:14'),(3,'admin','0001_initial','2015-08-28 11:35:15'),(4,'contenttypes','0002_remove_content_type_name','2015-08-28 11:35:15'),(5,'auth','0002_alter_permission_name_max_length','2015-08-28 11:35:16'),(6,'auth','0003_alter_user_email_max_length','2015-08-28 11:35:16'),(7,'auth','0004_alter_user_username_opts','2015-08-28 11:35:16'),(8,'auth','0005_alter_user_last_login_null','2015-08-28 11:35:16'),(9,'auth','0006_require_contenttypes_0002','2015-08-28 11:35:16'),(10,'dealmonkapp','0001_initial','2015-08-28 11:35:28'),(11,'sessions','0001_initial','2015-08-28 11:35:29'),(12,'dealmonkapp','0002_auto_20150828_1146','2015-08-28 11:46:05'),(13,'dealmonkapp','0003_auto_20150828_1229','2015-08-28 12:29:08'),(14,'dealmonkapp','0004_auto_20150828_1349','2015-08-28 13:49:28'),(15,'dealmonkapp','0005_auto_20150830_0729','2015-08-30 07:30:21'),(16,'dealmonkapp','0006_auto_20150830_0948','2015-08-30 09:48:14'),(17,'dealmonkapp','0007_auto_20150902_1334','2015-09-02 13:34:25');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('93270qbtuf91lxhbei82ju110xqu62fw','M2ZmZjY0MTgyOTY3ZDk2NWYzMjY3NjU0YjIyMjcwYmRjODgxMjhhZDp7ImxvZ2luX3N0YXR1cyI6dHJ1ZSwiX2F1dGhfdXNlcl9pZCI6IjIiLCJsb2dpbl91c2VyIjoidkBnbWFpbC5jb20iLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImZ1bGxfbmFtZSI6InZpa3JhbSBjaGFuZGVsIiwib3duZXJpZCI6MiwiX2F1dGhfdXNlcl9oYXNoIjoiZjRhNzA0Zjk4NzY3ZGYzZGNjYTcxYjA1NTJlMmM2NTE2YjQ5MDA3NiJ9','2015-09-13 15:19:57'),('ah6qlzubw89trkm4pjbhbq7zlqjwj1ez','MTc2MGI2YjI0YmMxMmIzNGI3ODNjZWM4NGZiYWZmMmFiMTdkYTY1Yjp7Il9hdXRoX3VzZXJfaGFzaCI6IjJkNThhYWE0ODZlMjNiNWUwYjY0MTE3Njc0NzcyOGZkMDIyYzM0MTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2015-09-18 10:29:05'),('crqvezhydoepdb5ghciavk3es0xuta32','MTc2MGI2YjI0YmMxMmIzNGI3ODNjZWM4NGZiYWZmMmFiMTdkYTY1Yjp7Il9hdXRoX3VzZXJfaGFzaCI6IjJkNThhYWE0ODZlMjNiNWUwYjY0MTE3Njc0NzcyOGZkMDIyYzM0MTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2015-09-16 15:26:08'),('iuk7yfoxvb0e5crs8ik7kzkelp8znfc8','M2ZmZjY0MTgyOTY3ZDk2NWYzMjY3NjU0YjIyMjcwYmRjODgxMjhhZDp7ImxvZ2luX3N0YXR1cyI6dHJ1ZSwiX2F1dGhfdXNlcl9pZCI6IjIiLCJsb2dpbl91c2VyIjoidkBnbWFpbC5jb20iLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImZ1bGxfbmFtZSI6InZpa3JhbSBjaGFuZGVsIiwib3duZXJpZCI6MiwiX2F1dGhfdXNlcl9oYXNoIjoiZjRhNzA0Zjk4NzY3ZGYzZGNjYTcxYjA1NTJlMmM2NTE2YjQ5MDA3NiJ9','2015-09-12 05:18:50'),('p0tltkt3g5ex172rfx8f87wk4bfhq1zs','ZTE4YTk2ZjgzZjBkMWQxODExOWE3NTkzM2VkMTQ5NDhmODg5NjVjMDp7ImxvZ2luX3N0YXR1cyI6dHJ1ZSwiX2F1dGhfdXNlcl9pZCI6IjIwIiwibG9naW5fdXNlciI6ImFkbWluQGFkbWluLmNvbSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiZnVsbF9uYW1lIjoiYWRtaW4gYWRtaW4iLCJvd25lcmlkIjoyMCwiX2F1dGhfdXNlcl9oYXNoIjoiMDY3N2U4MTM4ZDZlYzIzMmU2NzVjYzg4NzMxZDJiNTY4NmMzN2YxNCJ9','2015-09-17 11:15:13'),('yb9568ky5bcwlkdwhjliivmwc6v1prgj','MTc2MGI2YjI0YmMxMmIzNGI3ODNjZWM4NGZiYWZmMmFiMTdkYTY1Yjp7Il9hdXRoX3VzZXJfaGFzaCI6IjJkNThhYWE0ODZlMjNiNWUwYjY0MTE3Njc0NzcyOGZkMDIyYzM0MTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2015-09-17 09:35:01');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-04 16:11:47

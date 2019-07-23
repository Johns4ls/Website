-- MySQL dump 10.16  Distrib 10.1.23-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	10.1.23-MariaDB-9+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tTemporary`
--

DROP TABLE IF EXISTS `tTemporary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tTemporary` (
  `tempID` int(11) NOT NULL AUTO_INCREMENT,
  `WithdrawDeposit` varchar(255) DEFAULT NULL,
  `Company` varchar(255) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Amount` float DEFAULT NULL,
  UNIQUE KEY `PersonID` (`tempID`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tTemporary`
--

LOCK TABLES `tTemporary` WRITE;
/*!40000 ALTER TABLE `tTemporary` DISABLE KEYS */;
INSERT INTO `tTemporary` VALUES (19,'Withdraw','Five Below','2018-09-28',-8.09),(20,'Withdraw','Kroger','2018-10-16',-90.98),(21,'Withdraw','Amazon','2018-10-20',-38.95),(22,'Withdraw','Amazon','2018-11-07',-152.82);
/*!40000 ALTER TABLE `tTemporary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tTransaction`
--

DROP TABLE IF EXISTS `tTransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tTransaction` (
  `TransID` int(6) NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `WithdrawDeposit` varchar(50) NOT NULL,
  `Company` varchar(50) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Amount` float NOT NULL,
  `Comments` mediumtext,
  `Receipt` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`TransID`)
) ENGINE=InnoDB AUTO_INCREMENT=254 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tTransaction`
--

LOCK TABLES `tTransaction` WRITE;
/*!40000 ALTER TABLE `tTransaction` DISABLE KEYS */;
INSERT INTO `tTransaction` VALUES (2,'Initial Transfer','Dad Deposited money to keep account open','Deposit','Guardian','2017-09-01',50,'This was the initial creation of the checking account',''),(3,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2017-09-15',735,'',''),(4,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2017-09-29',735,'',''),(5,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2017-10-02',-20,'',''),(6,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2017-10-02',-3.45,'Utility Service Fee',''),(7,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2017-10-02',-101.5,'',''),(8,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Amazon','2017-10-03',-64.99,'',''),(9,'Medication','','Withdraw','Bethesda North Apothecary','2017-10-04',-22.14,'','15283788351134864722884078117097.jpg'),(10,'Groceries','Monthly groceries','Withdraw','Kroger','2017-10-04',-31.66,'','2018-04-18_16.48.15.jpg'),(11,'Groceries','Monthly groceries','Withdraw','Kroger','2017-10-17',-37.16,'','2018-04-18_16.42.47.jpg'),(12,'Medication','','Withdraw','Kroger','2017-10-19',-70,'','15283788963457662708337893468894.jpg'),(13,'Underpads ','McKesson UPHV3036 StayDry Ultra Underpads, 30\" x 36\" (Pack of 100)','Withdraw','Amazon','2017-10-26',-41.28,'',''),(14,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2017-10-30',-92.73,'',''),(15,'Medication','','Withdraw','Bethesda North Apothecary','2017-10-30',-22.25,'',''),(16,'Housing','Monthly House Payment','Withdraw','US Bank','2017-10-30',-200,'',''),(17,'TV','32\" TV','Withdraw','Wal-Mart','2017-10-31',-168.67,'','15283797084963752569610399610079.jpg'),(18,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2017-11-01',735,'',''),(19,'Gas','Gas for Andrew\'s Van','Withdraw','Shell Oil','2017-11-01',-20,'',''),(20,'Wipes','Huggies One & Done Scented Baby Wipes, Hypoallergenic, 3 Refill Packs, 648 Count','Withdraw','Amazon','2017-11-06',-15.62,'',''),(21,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Amazon','2017-11-06',-90.9,'',''),(22,'Medication','','Withdraw','Bethesda North Apothecary','2017-11-10',-21.7,'','15283787619042539690592007769984.jpg'),(23,'Groceries','','Withdraw','Kroger','2017-11-13',-71.61,'','2018-04-18_16.40.48.jpg'),(24,'Underpads ','McKesson UPHV3036 StayDry Ultra Underpads, 30\" x 36\" (Pack of 100)','Withdraw','Amazon','2017-11-16',-41.01,'',''),(25,'Medication','','Withdraw','Bethesda North Apothecary','2017-11-24',-25,'',''),(26,'Medication','Ear infection medication','Withdraw','Kroger Pharmacy','2017-11-16',-25,'',''),(27,'Medication','','Withdraw','Bethesda North Apothecary','2017-11-24',-22.25,'','15283789579735164459814598683824.jpg'),(28,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2017-11-24',-101.5,'',''),(29,'Groceries','Monthly groceries','Withdraw','Meijer','2017-11-24',-55.74,'',''),(30,'Groceries','Monthly groceries','Withdraw','Amazon','2017-11-29',-48.49,'We started using Prime Now for groceries',''),(31,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2017-12-01',735,'',''),(32,'Groceries','Stool Softeners to help regulate GI system','Withdraw','Amazon','2017-12-01',-17.41,'',''),(33,'Music','Monthly music from amazon','Withdraw','Amazon','2017-12-01',-8.53,'',''),(34,'Housing','Monthly House Payment','Withdraw','US Bank','2017-12-07',-200,'',''),(35,'Clothing','','Withdraw','Target','2017-12-08',-21.86,'',''),(36,'Clothing','','Withdraw','Target','2017-12-11',-13.87,'',''),(37,'Clothing','','Withdraw','Target','2017-12-11',-12.8,'',''),(38,'Clothing','','Withdraw','Target','2017-12-11',-10.66,'',''),(39,'Clothing','','Withdraw','Target','2017-12-11',-10.66,'',''),(40,'Clothing','','Withdraw','Target','2017-12-11',-8.53,'',''),(41,'Clothing','','Withdraw','Target','2017-12-11',-8,'',''),(42,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','NorthShore Care Supply','2017-12-11',-90.9,'',''),(43,'t-shirt','New t-shirt','Withdraw','Hot-Topic','2017-12-11',-4.99,'',''),(44,'Clothing','Socks','Withdraw','Amazon','2017-12-11',-13.87,'',''),(45,'Groceries','Monthly groceries','Withdraw','Kroger','2017-12-15',-65.61,'','2018-04-18_16.47.20.jpg'),(46,'Clothing','','Withdraw','Hot-Topic','2017-12-18',-45.69,'',''),(47,'Medication','','Withdraw','Bethesda North Apothecary','2017-12-18',-20.65,'','15283789980297873116678300292387.jpg'),(48,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2017-12-18',-101.5,'',''),(49,'Newport Aquarium','Aquarium Pass','Withdraw','Newport Aquarium','2017-12-18',-53.18,'',''),(50,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2017-12-18',-10,'',''),(51,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-01-01',750,'',''),(52,'Housing','Monthly House Payment','Withdraw','US Bank','2017-12-29',-200,'',''),(53,'Underpads ','McKesson UPHV3036 StayDry Ultra Underpads, 30\" x 36\" (Pack of 100)','Withdraw','Amazon','2018-01-03',-42.14,'',''),(54,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','NorthShore Care Supply','2018-01-11',-90.9,'',''),(55,'Medication','','Withdraw','Bethesda North Apothecary','2018-01-16',-10,'',''),(56,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-01-26',-101.5,'',''),(57,'Groceries','Monthly groceries','Withdraw','Shipt','2018-01-29',-120.31,'',''),(58,'Groceries','Balance differential for adding an item','Withdraw','Shipt','2018-01-29',-2.53,'',''),(59,'Groceries','Added tip for Delivery','Withdraw','Shipt','2018-01-29',-5,'',''),(60,'Housing','Monthly House Payment','Withdraw','US Bank','2018-01-29',-200,'',''),(61,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-01-31',-20,'',''),(62,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-01-31',-10,'',''),(63,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-02-01',750,'',''),(64,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','NorthShore Care Supply','2018-02-14',-90.9,'',''),(65,'Head pillow','','Withdraw','Amazon','2018-02-15',-16,'When he is lethargic, it helps him keep an open airway to breathe',''),(66,'Medication','','Withdraw','Bethesda North Apothecary','2018-02-16',-17.1,'','15283786817641200491062980742650.jpg'),(67,'Medication','','Withdraw','Kroger','2018-02-20',-11.49,'',''),(68,'Medication','','Withdraw','Bethesda North Apothecary','2018-02-26',-24.45,'',''),(69,'Wipes','Huggies One & Done Scented Baby Wipes, Hypoallergenic, 3 Refill Packs, 648 Count','Withdraw','Amazon','2018-02-26',-15.62,'',''),(70,'Groceries','Monthly groceries','Withdraw','Shipt','2018-02-27',-124.31,'',''),(71,'Groceries','Balance differential for adding an item','Withdraw','Shipt','2018-02-27',-7.69,'',''),(72,'Groceries','Added tip for Delivery','Withdraw','Shipt','2018-02-27',-5,'',''),(73,'Housing','Monthly House Payment','Withdraw','US Bank','2018-02-27',-200,'',''),(74,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-02-27',-100,'',''),(75,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-02-27',-10,'',''),(76,'Doctor Visit ','Remaining Balance paid for doctors visit','Withdraw','Trihealth','2018-03-07',-10,'',''),(77,'Doctor Visit','','Withdraw','Children\'s Hospital','2018-03-08',-145.32,'',''),(78,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','NorthShore Care Supply','2018-03-09',-97.04,'',''),(79,'Underpads ','McKesson UPHV3036 StayDry Ultra Underpads, 30\" x 36\" (Pack of 100)','Withdraw','Amazon','2018-03-09',-40.03,'',''),(80,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-03-01',750,'',''),(81,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-02-27',-10,'',''),(83,'Groceries','Monthly groceries','Withdraw','Shipt','2018-03-20',-122.73,'',''),(84,'Groceries','Added tip for Delivery','Withdraw','Shipt','2018-03-20',-10,'',''),(91,'Dinner','Bought a Box Meal at KFC','Withdraw','KFC','2018-03-26',-5.05,'','15283783728871378199768523727710.jpg'),(92,'Medication','','Withdraw','Bethesda North Apothecary','2018-03-26',-22.25,'','15283786211468797526220660517344.jpg'),(93,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-03-27',-100,'',''),(94,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-03-27',-20,'',''),(95,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-03-27',-10,'',''),(120,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-03-30',750,'',''),(122,'Dinner','Mashed Potatoes and Gravy','Withdraw','KFC','2018-03-29',-3.99,'',''),(124,'Groceries','Added tip for Delivery','Withdraw','Shipt','2018-04-12',-5,'',''),(125,'Groceries','Monthly Groceries','Withdraw','Shipt','2018-04-11',-73.92,'',''),(126,'Groceries','Balance differential for adding an item','Withdraw','Shipt','2018-04-11',-3.45,'',''),(127,'Groceries','Monthly Groceries','Withdraw','Shipt','2018-04-16',-48.1,'',''),(128,'Medical and Comfort Supplies','Pillows and Probiotic','Withdraw','Target','2018-04-17',-64.51,'','15283795825401443417988250182681.jpg'),(129,'Wipes','Huggies One & Done Scented Baby Wipes, Hypoallergenic, 3 Refill Packs, 648 Count','Withdraw','Amazon','2018-04-03',-15.62,'',''),(130,'Medical Supplies','pulse oximeter to monitor heart rate and oxygen saturation levels','Withdraw','Amazon','2018-04-12',-19.8,'',''),(131,'Medical Supplies','Littman Stethoscope to monitor lung congestion and function ','Withdraw','Amazon','2018-04-12',-92.25,'',''),(132,'Medical Supplies','sterilizing medical supplies ','Withdraw','Amazon','2018-04-13',-130.77,'disposable gloves, hand sanitizer and dispenser, thermometer and covers, Lysol wipes and lysol additive detergent',''),(133,'Medical Supplies','Lysol Wipes','Withdraw','Amazon','2018-04-14',-10.66,'Amazon separated the transactions',''),(134,'Medical Supplies','tyolenol to help with fevers','Withdraw','Amazon','2018-04-16',-16.48,'',''),(135,'Medication','','Withdraw','Kroger','2018-04-16',-45,'','15283795450507119315291402428519.jpg'),(136,'Drink','Bug juice','Withdraw','Thorntons','2018-03-29',-2.11,'',''),(148,'Dinner','','Withdraw','KFC','2018-04-26',-3.99,'','15283794493853369093510796307749.jpg'),(149,'Housing','Monthly House Payment','Withdraw','US Bank','2018-03-30',-200,'',''),(150,'Groceries','Added tip for Delivery','Withdraw','Shipt','2018-04-17',-5,'',''),(151,'Medication','','Withdraw','Bethesda North Apothecary','2018-04-26',-33.14,'','15283794979038254155864630653707.jpg'),(152,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-04-28',-97.04,'',''),(153,'dietary supplement','ensure enlive shakes 12 ct','Withdraw','Walgreens','2018-04-28',-16.99,'',''),(154,'Medication','Albuterol for the nebulizer','Withdraw','Kroger','2018-04-28',-45,'','15283793974796710690488152116094.jpg'),(155,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-04-30',-200,'',''),(156,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-04-30',-20,'',''),(157,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-04-30',-20,'',''),(158,'Housing','Monthly House Payment','Withdraw','US Bank','2018-04-30',-200,'',''),(159,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-05-01',750,'',''),(160,'Oral Care','Toothette Oral Care Plus Untreated Single Use Swabs, (Pack of 20)','Withdraw','Amazon','2018-05-04',-16.07,'',''),(161,'Medication','','Withdraw','Kroger','2018-05-11',-70.53,'','15283793510688458391910884613892.jpg'),(162,'Aquarium pass','season pass for the acquarium ','Withdraw','Newport Aquarium','2018-05-11',-21.49,'',''),(163,'Medication','','Withdraw','Kroger','2018-05-19',-45,'',''),(164,'shelves','new shelves to hold diapers','Withdraw','Lowe\'s','2018-05-17',-290.7,'','2018-05-21 17.30.32.jpg'),(165,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-05-26',-97.04,'',''),(166,'Groceries','','Withdraw','Kroger','2018-05-28',-114.39,'','15283791250496067417806316556455.jpg'),(167,'Groceries','Pediasure ','Withdraw','Amazon','2018-05-12',-43.96,'',''),(168,'Pedialyte','','Withdraw','Walgreens','2018-05-26',-41.17,'',''),(169,'Food Grinder And Wipes','KitchenAid KFC3516WH 3.5 Cup Mini Food Processor, White and  HUGGIES One and Done Refreshing Baby Wipes, Refill Pack (3-Pack, 648 Sheets Total), Scented, Alcohol-free, Hypoallergenic','Withdraw','Amazon','2018-05-26',-40.63,'',''),(171,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-05-31',-100,'',''),(172,'Housing','Monthly House Payment','Withdraw','US Bank','2018-05-31',-200,'',''),(175,'Medication','','Withdraw','Bethesda North Apothecary','2018-05-25',-35,'','15283792548724882932164977538881.jpg'),(176,'Underpads ','McKesson UPHV3036 StayDry Ultra Underpads, 30\" x 36\" (Pack of 100)','Withdraw','Amazon','2018-05-26',-49.27,'',''),(177,'Groceries','Florastor probiotic','Withdraw','Walgreens','2018-05-28',-23.48,'',''),(178,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-06-01',750,'',''),(179,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-06-01',-10,'',''),(180,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-06-01',-10,'',''),(181,'Groceries','Miralax & Pedialyte','Withdraw','Amazon','2018-06-07',-49.48,'MiraLAX Powder Laxative, 45 Doses, 26.9 Ounce, Pedialyte AdvancedCare+ Electrolyte Drink with 33% More Electrolytes and has PreActiv Prebiotics, Berry Frost, 1 Liter, 4 Count',''),(182,'Groceries','PediaSure Grow & Gain Nutrition Shake For Kids, Chocolate, 8 fl oz (Pack of 24)','Withdraw','Amazon','2018-06-07',-36.98,'',''),(183,'Medication','Nebulizer treatment','Withdraw','Kroger','2018-06-06',-45,'',''),(184,'Groceries','','Withdraw','Meijer','2018-06-04',-36.13,'','15283803398719132188671582215862.jpg'),(185,'Pedialyte','','Withdraw','Walgreens','2018-06-05',-7.23,'',''),(186,'Groceries','','Withdraw','Walgreens','2018-06-10',-30.47,'','15299737803272956618363978525355.jpg'),(187,'Medication','','Withdraw','Bethesda North Apothecary','2018-06-11',-28.91,'','15299736628548833684794140939738.jpg'),(188,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-06-22',-97.04,'',''),(189,'Medication','','Withdraw','Kroger','2018-06-20',-56.01,'','15299735470977338211971266618905.jpg'),(190,'Medication','','Withdraw','Bethesda North Apothecary','2018-06-25',-25,'','1529973511615668382999157168853.jpg'),(191,'Medication','Florastor probiotic','Withdraw','Walgreens','2018-06-20',-43.28,'','15299736168438489466759032435995.jpg'),(192,'Wipes','','Withdraw','Amazon','2018-06-22',-16,'',''),(193,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-06-29',750,'',''),(194,'Housing','Monthly House Payment','Withdraw','US Bank','2018-06-29',-200,'',''),(195,'Gas','Gas for the handicapped van','Withdraw','Thorntons','2018-06-26',-20.09,'',''),(196,'Groceries','Monthly Groceries','Withdraw','Shipt','2018-07-12',-121.18,'',''),(197,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-07-24',-10,'',''),(198,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-07-24',-50,'',''),(199,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-07-24',-10,'',''),(200,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-07-26',-104.55,'',''),(201,'Medication','','Withdraw','Bethesda North Apothecary','2018-07-12',-20,'','20180904_181612.jpg'),(202,'Housing','Monthly House Payment','Withdraw','US Bank','2018-07-30',-200,'',''),(203,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-08-01',750,'',''),(204,'Medication','','Withdraw','Kroger','2018-08-10',-50,'','20180904_181519.jpg'),(205,'Groceries','','Withdraw','Walgreens','2018-08-10',-35.11,'','20180904_181446.jpg'),(206,'Medication','','Withdraw','Bethesda North Apothecary','2018-08-08',-20,'',''),(207,'Food','','Withdraw','McDonald\'s','2018-08-05',-7.26,'','20180904_181625.jpg'),(208,'Groceries','','Withdraw','Walgreens','2018-08-01',-12.74,'','20180904_181455.jpg'),(209,'Medication','','Withdraw','Kroger','2018-07-19',-44.48,'','20180904_181635.jpg'),(210,'Medication','','Withdraw','Kroger','2018-07-08',-42.76,'','20180904_181511.jpg'),(211,'Gas','Gas for the handicapped van','Withdraw','United Dairy Farmers','2018-08-15',-10,'',''),(212,'Groceries','','Withdraw','Kroger','2018-08-15',-90.96,'',''),(213,'Medication','Ativan','Withdraw','Kroger','2018-08-18',-1.72,'','20180904_181528.jpg'),(214,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-08-26',-104.55,'',''),(215,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-08-29',-10,'',''),(216,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-08-29',-10,'',''),(217,'Housing','Monthly House Payment','Withdraw','US Bank','2018-08-29',-200,'',''),(218,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-08-29',-50,'',''),(219,'Gas','Gas for the handicapped van','Withdraw','Thorntons','2018-08-22',-29.07,'',''),(220,'Medication','','Withdraw','Bethesda North Apothecary','2018-08-27',-37.8,'',''),(221,'Food','Dinner','Withdraw','KFC','2018-08-30',-9.04,'',''),(222,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-08-31',750,'',''),(223,'Groceries','Groceries','Withdraw','Kroger','2018-09-04',-114.09,'','0904181512.jpg'),(224,'Groceries','Carnation (40 ct)','Withdraw','Amazon','2018-08-15',-23.77,'',''),(225,'Underpads','McKesson Underpads','Withdraw','Amazon','2018-08-05',-30,'',''),(226,'Wipes','Wipes (Huggies)','Withdraw','Amazon','2018-08-05',-16,'',''),(227,'Medication','Ibuprofen, Florastor, and Zyrtec','Withdraw','Amazon','2018-07-13',-86.4,'',''),(228,'Groceries','Pudding, Carnation (powder), and Carnation bottle)','Withdraw','Amazon','2018-07-05',-67.42,'',''),(229,'Dinner','','Withdraw','KFC','2018-09-08',-8.99,'',''),(230,'Dinner','','Withdraw','KFC','2018-09-14',-3.99,'',''),(231,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-09-19',-100,'',''),(232,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-09-19',-15,'',''),(233,'Doctor Visit','Done with Check','Withdraw','Trihealth','2018-09-12',-20,'',''),(234,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Amazon','2018-09-25',-79.13,'',''),(235,'Housing','Monthly House Payment','Withdraw','US Bank','2018-09-28',-200,'',''),(236,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-09-29',750,'',''),(237,'Blanket','YnM Weighted Blanket (15 lbs, 48\'\'x72\'\', Twin Size) | Gravity 2.0 Heavy Blanket | 100% Cotton Material with Glass Beads | Great Sleep Therapy for People with Anxiety, Autism, ADHD, Insomnia or Stress','Withdraw','Amazon','2018-09-09',-69.9,'',''),(239,'Wipes','HUGGIES One & Done Scented Baby Wipes, Hypoallergenic, 3 Refill Packs, 648 Count Total and Florastor Probiotic','Withdraw','Amazon','2018-09-09',-75.82,'',''),(240,'School Supplies','Hynes Eagle Printed Kids School Backpack Cool Children Bookbag Shark, AmazonBasics AAA Performance Alkaline Batteries (20-Pack)','Withdraw','Amazon','2018-09-15',-34.45,'',''),(241,'Dinner','','Withdraw','KFC','2018-09-30',-9.04,'',''),(242,'Groceries','Carnation Breakfast Essentials, Desitin Paste','Withdraw','Amazon','2018-10-04',-61.89,'',''),(243,'Medical','Medline Ultrasoft Dry Baby Wipes, Gerber Organic 2nd Foods Baby Food','Withdraw','Amazon','2018-10-14',-43.9,'',''),(244,'Medical','','Withdraw','Meijer','2018-10-14',-25.59,'',''),(245,'Clermont County Water','Monthly Water Bill Payment','Withdraw','Clermont County Utilities','2018-10-17',-10,'',''),(246,'Duke Energy','Monthly Electric Bill','Withdraw','Duke Energy','2018-10-17',-100,'',''),(247,'Trash Removal','Monthly Payment for Waste Disposal','Withdraw','Rumpke','2018-10-17',-10,'',''),(248,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-10-20',-88.54,'',''),(249,'Housing','Monthly House Payment','Withdraw','US Bank','2018-10-30',-200,'',''),(250,'Medication','','Withdraw','CW Botanicals','2018-10-22',-123.08,'',''),(251,'SSI Check Deposit','Monthly Social Security Deposit','Deposit','SSI','2018-11-01',750,'',''),(252,'Groceries','Monthly Groceries','Withdraw','Shipt','2018-11-07',-62.29,'',''),(253,'Diapers','Tranquility All Night Through Adult Disposable Briefs','Withdraw','Northshore Care Supply','2018-11-13',-88.54,'','');
/*!40000 ALTER TABLE `tTransaction` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-19  4:00:02

/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 8.2.0 : Database - nas_sys
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`nas_sys` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `nas_sys`;

/*Table structure for table `bgm` */

DROP TABLE IF EXISTS `bgm`;

CREATE TABLE `bgm` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bgm` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `path` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `bgm` */

insert  into `bgm`(`id`,`bgm`,`path`,`time`) values (1,'东京漂移','get_small_say/back/djpy.mp3','2024-05-12 06:03:04'),(2,'风之谷','get_small_say/back/fzg.mp3','2024-05-18 13:59:54'),(3,'撒哈拉','get_small_say/back/sahara.mp3','2024-05-22 10:29:20');

/*Table structure for table `books` */

DROP TABLE IF EXISTS `books`;

CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `path` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `book_id` int DEFAULT NULL,
  `get_step` int DEFAULT NULL COMMENT ' 0 未下载，1 下载完成 2 转换完成 ,3 下载失败 4 转换失败 ,5 加背景成功 6 加背景失败',
  `time` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `dir` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `task_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `man_uuid` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `page` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89867 DEFAULT CHARSET=latin1;

/*Data for the table `books` */


/*Table structure for table `small_say` */

DROP TABLE IF EXISTS `small_say`;

CREATE TABLE `small_say` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `link` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `last_updated` datetime DEFAULT NULL,
  `background_music` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `download_progress` int DEFAULT NULL,
  `conversion_progress` int DEFAULT NULL,
  `data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `data2` int DEFAULT NULL,
  `data3` double DEFAULT NULL,
  `conversion_max` int DEFAULT NULL,
  `download_max` int DEFAULT NULL,
  `data4` datetime DEFAULT NULL,
  `time` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `add_back_progress` int DEFAULT NULL,
  `add_back_max` int DEFAULT NULL,
  `voice` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `background_music_id` int DEFAULT NULL,
  `voice_id` int DEFAULT NULL,
  `userid` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

/*Data for the table `small_say` */



/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text COLLATE utf8mb4_unicode_ci,
  `pass` text COLLATE utf8mb4_unicode_ci,
  `logo` longtext COLLATE utf8mb4_unicode_ci,
  `token` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user` */



/*Table structure for table `voice` */

DROP TABLE IF EXISTS `voice`;

CREATE TABLE `voice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `msg` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `voice` */

insert  into `voice`(`id`,`name`,`value`,`msg`,`time`) values (1,'小小','zh-CN-XiaoxiaoNeural',NULL,'2024-05-12 06:07:41'),(2,'小艺','zh-CN-XiaoyiNeural',NULL,'2024-05-12 06:07:43'),(3,'云间','zh-CN-YunjianNeural',NULL,'2024-05-12 06:07:45'),(4,'云溪','zh-CN-YunxiNeural',NULL,'2024-05-12 06:07:46'),(5,'云霞','zh-CN-YunxiaNeural',NULL,'2024-05-12 06:07:48'),(6,'云阳','zh-CN-YunyangNeural',NULL,'2024-05-12 06:07:49'),(7,'辽宁-小贝','zh-CN-liaoning-XiaobeiNeural',NULL,'2024-05-12 06:07:51'),(8,'山西-小妮','zh-CN-shaanxi-XiaoniNeural',NULL,'2024-05-12 06:07:52'),(9,'云间和','zh-CN-YunJheNeural',NULL,'2024-05-12 06:07:53');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

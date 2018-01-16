
CREATE DATABASE IF NOT EXISTS osint;
GRANT USAGE ON *.* TO 'osintuser'@localhost IDENTIFIED BY 'password';
GRANT  SELECT, INSERT, UPDATE ON osint.* TO 'osintuser'@localhost;
FLUSH PRIVILEGES;
USE osint;

DROP TABLE IF EXISTS `tweet_media_urls`;
CREATE TABLE `tweet_media_urls` (
  `tweet_id` bigint(20) unsigned NOT NULL,
  `media_url` varchar(140) NOT NULL,
  KEY `tweet_id` (`tweet_id`),
  KEY `media_url` (`media_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `tweet_tags`;
CREATE TABLE `tweet_tags` (
  `tweet_id` bigint(20) unsigned NOT NULL,
  `tag` varchar(100) NOT NULL,
  KEY `tweet_id` (`tweet_id`),
  KEY `tag` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `tweet_urls`;
CREATE TABLE `tweet_urls` (
  `tweet_id` bigint(20) unsigned NOT NULL,
  `url` varchar(140) NOT NULL,
  KEY `tweet_id` (`tweet_id`),
  KEY `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `tweets`;
CREATE TABLE `tweets` (
  `tweet_id` bigint(20) unsigned NOT NULL,
  `tweet_text` varchar(160) NOT NULL,
  `created_at` datetime NOT NULL,
  `screen_name` char(20) NOT NULL,
  `lang` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`tweet_id`),
  KEY `created_at` (`created_at`),
  KEY `screen_name` (`screen_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

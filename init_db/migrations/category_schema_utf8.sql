Table	Create Table
product_category	CREATE TABLE `product_category` (\n  `category_id` int NOT NULL AUTO_INCREMENT,\n  `category_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,\n  `isactive` tinyint(1) NOT NULL,\n  PRIMARY KEY (`category_id`),\n  UNIQUE KEY `category_name_unique` (`category_name`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci

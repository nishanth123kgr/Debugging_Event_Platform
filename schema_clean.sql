-- Clean database schema for debugging platform

-- Table structure for table `q1`
CREATE TABLE `q1` (
  `id` varchar(50) NOT NULL,
  `submitted_time` longtext NOT NULL,
  `time_taken` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `q2`
CREATE TABLE `q2` (
  `id` varchar(50) NOT NULL,
  `submitted_time` longtext NOT NULL,
  `time_taken` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `q3`
CREATE TABLE `q3` (
  `id` varchar(50) NOT NULL,
  `submitted_time` longtext NOT NULL,
  `time_taken` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `q4`
CREATE TABLE `q4` (
  `id` varchar(50) NOT NULL,
  `submitted_time` longtext NOT NULL,
  `time_taken` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `q5`
CREATE TABLE `q5` (
  `id` varchar(50) NOT NULL,
  `submitted_time` longtext NOT NULL,
  `time_taken` longtext NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `users`
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `lang` varchar(8) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `q1_status` int(11) NOT NULL DEFAULT 0,
  `q2_status` int(11) NOT NULL DEFAULT 0,
  `q3_status` int(11) NOT NULL DEFAULT 0,
  `q4_status` int(11) NOT NULL DEFAULT 0,
  `q5_status` int(11) NOT NULL DEFAULT 0,
  `total_score` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

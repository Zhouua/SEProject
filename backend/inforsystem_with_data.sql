/*
 Navicat Premium Dump SQL

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80400 (8.4.0)
 Source Host           : localhost:3306
 Source Schema         : inforsystem

 Target Server Type    : MySQL
 Target Server Version : 80400 (8.4.0)
 File Encoding         : 65001

 Date: 05/06/2025 16:03:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for administrator
-- ----------------------------
DROP TABLE IF EXISTS `administrator`;
CREATE TABLE `administrator`  (
  `user_id` int NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  CONSTRAINT `administrator_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrator
-- ----------------------------
INSERT INTO `administrator` VALUES (1);

-- ----------------------------
-- Table structure for application
-- ----------------------------
DROP TABLE IF EXISTS `application`;
CREATE TABLE `application`  (
  `app_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `admin_id` int NULL DEFAULT NULL,
  `sec_id` int NOT NULL,
  `reason` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `teacher_id` int NOT NULL,
  `suggestion` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `final` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`app_id`) USING BTREE,
  INDEX `idx_application_section`(`sec_id` ASC) USING BTREE,
  INDEX `teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `application_ibfk_1` FOREIGN KEY (`sec_id`) REFERENCES `section` (`sec_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `application_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `application_ibfk_3` FOREIGN KEY (`admin_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of application
-- ----------------------------
INSERT INTO `application` VALUES (1, 1, 502, 'test', 7, '不行', 1);
INSERT INTO `application` VALUES (2, 1, 701, '我希望不上这节课', 7, '不行', 0);
INSERT INTO `application` VALUES (3, 1, 101, 'fuck you', 2, 'fuck you!', 1);
INSERT INTO `application` VALUES (4, 1, 101, 'fuck you', 2, 'shit!', 0);
INSERT INTO `application` VALUES (5, NULL, 101, 'fuck you', 2, NULL, 0);
INSERT INTO `application` VALUES (6, NULL, 101, 'fuck yoo', 2, NULL, 0);
INSERT INTO `application` VALUES (7, NULL, 101, 'fuck', 2, NULL, NULL);
INSERT INTO `application` VALUES (8, NULL, 401, 'fuckx', 3, NULL, 0);
INSERT INTO `application` VALUES (9, NULL, 1001, 'cnm', 5, NULL, NULL);

-- ----------------------------
-- Table structure for classroom
-- ----------------------------
DROP TABLE IF EXISTS `classroom`;
CREATE TABLE `classroom`  (
  `campus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `room_number` int NOT NULL,
  `capacity` int NOT NULL,
  `classroom_id` int NOT NULL AUTO_INCREMENT,
  `building` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`classroom_id`) USING BTREE,
  UNIQUE INDEX `classroom_id`(`classroom_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of classroom
-- ----------------------------
INSERT INTO `classroom` VALUES ('Main Campus', 101, 190, 1, 'Building A', 'Lecture Hall');
INSERT INTO `classroom` VALUES ('Main Campus', 102, 280, 2, 'Building A', 'Standard Classroom');
INSERT INTO `classroom` VALUES ('Main Campus', 201, 230, 3, 'Building B', 'Lab');
INSERT INTO `classroom` VALUES ('Main Campus', 202, 240, 4, 'Building B', 'Small Classroom');
INSERT INTO `classroom` VALUES ('Science Campus', 301, 200, 5, 'Building C', 'Lecture Hall');
INSERT INTO `classroom` VALUES ('Science Campus', 302, 114514, 6, 'Building C', 'Standard Classroom');
INSERT INTO `classroom` VALUES ('Science Campus', 401, 225, 7, 'Building D', 'Lab');
INSERT INTO `classroom` VALUES ('Downtown Campus', 501, 300, 8, 'Building E', 'Lecture Hall');
INSERT INTO `classroom` VALUES ('Downtown Campus', 502, 180, 9, 'Building E', 'Standard Classroom');
INSERT INTO `classroom` VALUES ('Main Campus', 103, 190, 10, 'Building A', 'Standard Classroom');
INSERT INTO `classroom` VALUES ('Science Campus', 303, 140, 11, 'Building C', 'Small Classroom');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dept_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `credits` int NOT NULL,
  `course_introduction` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `capacity` int NOT NULL,
  `required_room_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `grade_year` int NOT NULL DEFAULT 1,
  `period` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`course_id`) USING BTREE,
  UNIQUE INDEX `course_id`(`course_id` ASC) USING BTREE,
  INDEX `dept_name`(`dept_name` ASC) USING BTREE,
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (1, 'Introduction to Programming', 'Computer Science', 3, 'Basics of programming using Python.', 100, 'Lecture Hall', 1, 4);
INSERT INTO `course` VALUES (2, 'Data Structures', 'Computer Science', 4, 'Fundamental data structures.', 80, 'Lecture Hall', 2, 4);
INSERT INTO `course` VALUES (3, 'Algorithms', 'Computer Science', 4, 'Design and analysis of algorithms.', 70, 'Standard Classroom', 3, 4);
INSERT INTO `course` VALUES (4, 'Operating Systems', 'Computer Science', 3, 'Concepts of modern operating systems.', 60, 'Standard Classroom', 3, 3);
INSERT INTO `course` VALUES (5, 'Database Systems', 'Computer Science', 3, 'Introduction to database design and SQL.', 90, 'Lab', 2, 4);
INSERT INTO `course` VALUES (6, 'Circuit Theory', 'Electrical Engineering', 4, 'Fundamentals of electrical circuits.', 70, 'Lecture Hall', 1, 4);
INSERT INTO `course` VALUES (7, 'Digital Logic Design', 'Electrical Engineering', 3, 'Design of digital circuits.', 60, 'Lab', 2, 4);
INSERT INTO `course` VALUES (8, 'Signals and Systems', 'Electrical Engineering', 4, 'Analysis of signals and linear systems.', 50, 'Standard Classroom', 3, 4);
INSERT INTO `course` VALUES (9, 'Calculus I', 'Mathematics', 4, 'Differential calculus.', 120, 'Lecture Hall', 1, 5);
INSERT INTO `course` VALUES (10, 'Linear Algebra', 'Mathematics', 3, 'Vectors, matrices, and linear transformations.', 100, 'Lecture Hall', 1, 3);
INSERT INTO `course` VALUES (11, 'Probability and Statistics', 'Mathematics', 3, 'Introduction to probability and statistics.', 90, 'Standard Classroom', 2, 3);
INSERT INTO `course` VALUES (12, 'Classical Mechanics', 'Physics', 4, 'Newtonian mechanics and conservation laws.', 60, 'Lecture Hall', 1, 4);
INSERT INTO `course` VALUES (13, 'Electromagnetism', 'Physics', 4, 'Electric and magnetic fields.', 50, 'Standard Classroom', 2, 4);
INSERT INTO `course` VALUES (14, 'Quantum Mechanics I', 'Physics', 3, 'Introduction to quantum physics.', 40, 'Small Classroom', 3, 3);
INSERT INTO `course` VALUES (15, 'Principles of Management', 'Business Administration', 3, 'Basic management theories.', 100, 'Lecture Hall', 1, 3);
INSERT INTO `course` VALUES (16, 'Marketing Fundamentals', 'Business Administration', 3, 'Introduction to marketing concepts.', 90, 'Lecture Hall', 2, 3);
INSERT INTO `course` VALUES (17, 'Financial Accounting', 'Business Administration', 3, 'Basics of financial accounting.', 80, 'Standard Classroom', 2, 3);
INSERT INTO `course` VALUES (18, 'Intro to AI', 'Computer Science', 3, 'Basic concepts of Artificial Intelligence.', 50, 'Lab', 4, 3);
INSERT INTO `course` VALUES (19, 'Microeconomics', 'Business Administration', 3, 'Principles of microeconomics.', 70, 'Standard Classroom', 1, 3);
INSERT INTO `course` VALUES (20, 'Thermodynamics', 'Physics', 3, 'Principles of heat and energy transfer.', 40, 'Small Classroom', 2, 3);

-- ----------------------------
-- Table structure for curriculum
-- ----------------------------
DROP TABLE IF EXISTS `curriculum`;
CREATE TABLE `curriculum`  (
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  INDEX `course_id`(`course_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `curriculum_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `curriculum_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of curriculum
-- ----------------------------

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department`  (
  `dept_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `campus` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`dept_name`) USING BTREE,
  UNIQUE INDEX `dept_name`(`dept_name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES ('Business Administration', 'Downtown Campus');
INSERT INTO `department` VALUES ('Computer Science', 'Main Campus');
INSERT INTO `department` VALUES ('Electrical Engineering', 'Main Campus');
INSERT INTO `department` VALUES ('Mathematics', 'Science Campus');
INSERT INTO `department` VALUES ('Physics', 'Science Campus');

-- ----------------------------
-- Table structure for grade
-- ----------------------------
DROP TABLE IF EXISTS `grade`;
CREATE TABLE `grade`  (
  `takes_id` int NOT NULL,
  `grade` int NOT NULL,
  `proportion` decimal(3, 2) NULL DEFAULT NULL,
  `type` enum('attending','homework','test') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `grade_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`grade_id`) USING BTREE,
  UNIQUE INDEX `grade_id`(`grade_id` ASC) USING BTREE,
  INDEX `idx_grade_take`(`takes_id` ASC) USING BTREE,
  CONSTRAINT `grade_ibfk_1` FOREIGN KEY (`takes_id`) REFERENCES `takes` (`takes_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `chk_grade_range` CHECK (`grade` between 0 and 100),
  CONSTRAINT `chk_proportion_range` CHECK (`proportion` between 0 and 1)
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of grade
-- ----------------------------
INSERT INTO `grade` VALUES (1, 85, 0.20, 'homework', 1);
INSERT INTO `grade` VALUES (1, 90, 0.30, 'test', 2);
INSERT INTO `grade` VALUES (1, 78, 0.50, 'attending', 3);
INSERT INTO `grade` VALUES (2, 92, 0.20, 'homework', 4);
INSERT INTO `grade` VALUES (2, 88, 0.30, 'test', 5);
INSERT INTO `grade` VALUES (2, 95, 0.50, 'attending', 6);
INSERT INTO `grade` VALUES (3, 70, 0.25, 'homework', 7);
INSERT INTO `grade` VALUES (3, 75, 0.25, 'test', 8);
INSERT INTO `grade` VALUES (3, 80, 0.50, 'attending', 9);
INSERT INTO `grade` VALUES (4, 80, 0.30, 'homework', 10);
INSERT INTO `grade` VALUES (4, 85, 0.40, 'test', 11);
INSERT INTO `grade` VALUES (4, 90, 0.30, 'attending', 12);
INSERT INTO `grade` VALUES (5, 95, 0.20, 'homework', 13);
INSERT INTO `grade` VALUES (5, 89, 0.40, 'test', 14);
INSERT INTO `grade` VALUES (5, 92, 0.40, 'attending', 15);
INSERT INTO `grade` VALUES (6, 60, 0.10, 'homework', 16);
INSERT INTO `grade` VALUES (6, 70, 0.60, 'test', 17);
INSERT INTO `grade` VALUES (6, 75, 0.30, 'attending', 18);
INSERT INTO `grade` VALUES (7, 88, 0.20, 'homework', 19);
INSERT INTO `grade` VALUES (7, 91, 0.40, 'test', 20);
INSERT INTO `grade` VALUES (7, 85, 0.40, 'attending', 21);
INSERT INTO `grade` VALUES (8, 76, 0.25, 'homework', 22);
INSERT INTO `grade` VALUES (8, 82, 0.25, 'test', 23);
INSERT INTO `grade` VALUES (8, 79, 0.50, 'attending', 24);
INSERT INTO `grade` VALUES (9, 93, 0.30, 'homework', 25);
INSERT INTO `grade` VALUES (9, 87, 0.40, 'test', 26);
INSERT INTO `grade` VALUES (9, 90, 0.30, 'attending', 27);
INSERT INTO `grade` VALUES (10, 81, 0.20, 'homework', 28);
INSERT INTO `grade` VALUES (10, 84, 0.40, 'test', 29);
INSERT INTO `grade` VALUES (10, 88, 0.40, 'attending', 30);

-- ----------------------------
-- Table structure for grade_change
-- ----------------------------
DROP TABLE IF EXISTS `grade_change`;
CREATE TABLE `grade_change`  (
  `takes_id` int NOT NULL,
  `teacher_id` int NOT NULL,
  `result` tinyint(1) NULL DEFAULT NULL,
  `new_grade` int NOT NULL,
  `apply_time` datetime NOT NULL,
  `check_time` datetime NULL DEFAULT NULL,
  `grade_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `grade_change_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`grade_change_id`) USING BTREE,
  UNIQUE INDEX `grade_change_id`(`grade_change_id` ASC) USING BTREE,
  INDEX `teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_grade_change_search`(`takes_id` ASC, `check_time` ASC) USING BTREE,
  CONSTRAINT `grade_change_ibfk_1` FOREIGN KEY (`takes_id`) REFERENCES `takes` (`takes_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `grade_change_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of grade_change
-- ----------------------------
INSERT INTO `grade_change` VALUES (1, 2, NULL, 92, '2024-12-20 10:00:00', NULL, 'Final Grade Correction', 1);
INSERT INTO `grade_change` VALUES (3, 2, 1, 80, '2025-01-10 09:00:00', '2025-01-11 14:00:00', 'Test Regrade', 2);
INSERT INTO `grade_change` VALUES (5, 4, 0, 90, '2024-12-15 11:30:00', '2024-12-16 10:00:00', 'Homework Appeal', 3);

-- ----------------------------
-- Table structure for homework_correction
-- ----------------------------
DROP TABLE IF EXISTS `homework_correction`;
CREATE TABLE `homework_correction`  (
  `student_id` int NOT NULL,
  `homework_id` int NOT NULL,
  `score` int NOT NULL,
  `feedback` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`student_id`, `homework_id`) USING BTREE,
  INDEX `homework_correction_ibfk_1`(`homework_id` ASC) USING BTREE,
  CONSTRAINT `homework_correction_ibfk_1` FOREIGN KEY (`homework_id`) REFERENCES `homework_information` (`homework_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `homework_correction_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `record_check_score` CHECK ((`score` >= 0) and (`score` <= 100))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of homework_correction
-- ----------------------------

-- ----------------------------
-- Table structure for homework_information
-- ----------------------------
DROP TABLE IF EXISTS `homework_information`;
CREATE TABLE `homework_information`  (
  `homework_id` int NOT NULL AUTO_INCREMENT,
  `sec_id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `deadline` datetime NOT NULL,
  `proportion` double NOT NULL,
  `committed` tinyint(1) NOT NULL DEFAULT 0,
  `files` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`homework_id`) USING BTREE,
  INDEX `homework_information_ibfk_1`(`sec_id` ASC) USING BTREE,
  CONSTRAINT `homework_information_ibfk_1` FOREIGN KEY (`sec_id`) REFERENCES `section` (`sec_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `check_proportion` CHECK ((`proportion` >= 0) and (`proportion` <= 1))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of homework_information
-- ----------------------------

-- ----------------------------
-- Table structure for homework_record
-- ----------------------------
DROP TABLE IF EXISTS `homework_record`;
CREATE TABLE `homework_record`  (
  `student_id` int NOT NULL,
  `homework_id` int NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `files` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`student_id`, `homework_id`) USING BTREE,
  INDEX `homework_record_ibfk_1`(`homework_id` ASC) USING BTREE,
  CONSTRAINT `homework_record_ibfk_1` FOREIGN KEY (`homework_id`) REFERENCES `homework_information` (`homework_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `homework_record_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of homework_record
-- ----------------------------

-- ----------------------------
-- Table structure for personal_information
-- ----------------------------
DROP TABLE IF EXISTS `personal_information`;
CREATE TABLE `personal_information`  (
  `personal_infor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `picture` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`personal_infor_id`) USING BTREE,
  UNIQUE INDEX `personal_infor_id`(`personal_infor_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of personal_information
-- ----------------------------
INSERT INTO `personal_information` VALUES (1, 'Alice Wonderland', '555-0101', 'alice.jpg');
INSERT INTO `personal_information` VALUES (2, 'Bob The Builder', '555-0102', 'bob.jpg');
INSERT INTO `personal_information` VALUES (3, 'Charles Xavier', '555-0103', 'charles.jpg');
INSERT INTO `personal_information` VALUES (4, 'Diana Prince', '555-0104', 'diana.jpg');
INSERT INTO `personal_information` VALUES (5, 'Edward Scissorhands', '555-0105', 'edward.jpg');
INSERT INTO `personal_information` VALUES (6, 'Fiona Gallagher', '555-0106', 'fiona.jpg');
INSERT INTO `personal_information` VALUES (7, 'Gregory House', '555-0107', 'gregory.jpg');
INSERT INTO `personal_information` VALUES (8, 'Harry Potter', '555-0108', 'harry.jpg');
INSERT INTO `personal_information` VALUES (9, 'Irene Adler', '555-0109', 'irene.jpg');
INSERT INTO `personal_information` VALUES (10, 'John Doe', '555-0110', 'john.jpg');
INSERT INTO `personal_information` VALUES (11, 'Jane Smith', '555-0111', 'jane.jpg');
INSERT INTO `personal_information` VALUES (12, 'Admin User', '555-0000', 'admin.jpg');
INSERT INTO `personal_information` VALUES (13, 'Prof. Alan Turing', '555-0201', 'turing.jpg');
INSERT INTO `personal_information` VALUES (14, 'Prof. Marie Curie', '555-0202', 'curie.jpg');
INSERT INTO `personal_information` VALUES (15, 'Prof. Isaac Newton', '555-0203', 'newton.jpg');
INSERT INTO `personal_information` VALUES (16, 'Prof. Ada Lovelace', '555-0204', 'lovelace.jpg');
INSERT INTO `personal_information` VALUES (17, 'Prof. Peter Parker', '555-0205', 'parker.jpg');
INSERT INTO `personal_information` VALUES (18, 'Michael Scott', '555-0206', 'scott.jpg');
INSERT INTO `personal_information` VALUES (19, 'Student Alpha', '555-0301', 's_alpha.jpg');
INSERT INTO `personal_information` VALUES (20, 'Student Beta', '555-0302', 's_beta.jpg');
INSERT INTO `personal_information` VALUES (21, 'Student Gamma', '555-0303', 's_gamma.jpg');
INSERT INTO `personal_information` VALUES (22, 'Student Delta', '555-0304', 's_delta.jpg');
INSERT INTO `personal_information` VALUES (23, 'Student Epsilon', '555-0305', 's_epsilon.jpg');
INSERT INTO `personal_information` VALUES (24, 'Student Zeta', '555-0306', 's_zeta.jpg');
INSERT INTO `personal_information` VALUES (25, 'Student Eta', '555-0307', 's_eta.jpg');
INSERT INTO `personal_information` VALUES (26, 'Student Theta', '555-0308', 's_theta.jpg');
INSERT INTO `personal_information` VALUES (27, 'Student Iota', '555-0309', 's_iota.jpg');
INSERT INTO `personal_information` VALUES (28, 'Student Kappa', '555-0310', 's_kappa.jpg');
INSERT INTO `personal_information` VALUES (29, 'Student Lambda', '555-0311', 's_lambda.jpg');
INSERT INTO `personal_information` VALUES (30, 'Student Mu', '555-0312', 's_mu.jpg');

-- ----------------------------
-- Table structure for section
-- ----------------------------
DROP TABLE IF EXISTS `section`;
CREATE TABLE `section`  (
  `course_id` int NOT NULL,
  `sec_id` int NOT NULL AUTO_INCREMENT,
  `semester` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `year` int NOT NULL,
  `remain_capacity` int NULL DEFAULT NULL,
  `classroom_id` int NULL DEFAULT NULL,
  `time_slot_ids` json NULL,
  `teacher_id` int NOT NULL,
  PRIMARY KEY (`sec_id`) USING BTREE,
  UNIQUE INDEX `sec_id`(`sec_id` ASC) USING BTREE,
  INDEX `classroom_id`(`classroom_id` ASC) USING BTREE,
  INDEX `teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_section_course`(`course_id` ASC) USING BTREE,
  INDEX `idx_section_search`(`semester` ASC, `year` ASC) USING BTREE,
  CONSTRAINT `section_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `section_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `section_ibfk_3` FOREIGN KEY (`classroom_id`) REFERENCES `classroom` (`classroom_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `section_ibfk_4` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1002 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of section
-- ----------------------------
INSERT INTO `section` VALUES (1, 2, 'Spring', 2026, NULL, 1, '[1, 2, 3, 4]', 2);
INSERT INTO `section` VALUES (1, 101, 'Fall', 2024, NULL, 1, '[1, 2, 3, 4]', 2);
INSERT INTO `section` VALUES (1, 102, 'Fall', 2024, NULL, 1, '[5, 6, 7, 8]', 5);
INSERT INTO `section` VALUES (2, 201, 'Fall', 2024, NULL, 1, '[9, 10, 11, 12]', 2);
INSERT INTO `section` VALUES (5, 301, 'Fall', 2024, NULL, 3, '[1, 2, 3, 4]', 8);
INSERT INTO `section` VALUES (6, 401, 'Fall', 2024, NULL, 1, '[13, 14, 15, 16]', 3);
INSERT INTO `section` VALUES (9, 501, 'Fall', 2024, NULL, 5, '[1, 2, 3, 4, 5]', 4);
INSERT INTO `section` VALUES (9, 502, 'Spring', 2025, NULL, 5, '[9, 10, 11, 12, 13]', 7);
INSERT INTO `section` VALUES (10, 601, 'Fall', 2024, NULL, 5, '[6, 7, 8]', 4);
INSERT INTO `section` VALUES (11, 701, 'Spring', 2025, NULL, 6, '[1, 2, 3]', 7);
INSERT INTO `section` VALUES (12, 801, 'Fall', 2024, NULL, 5, '[17, 18, 19, 20]', 6);
INSERT INTO `section` VALUES (15, 901, 'Fall', 2024, NULL, 8, '[1, 2, 3]', 10);
INSERT INTO `section` VALUES (18, 1001, 'Spring', 2025, NULL, 3, '[9, 10, 11]', 5);

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `user_id` int NOT NULL,
  `dept_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tot_cred` int NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  INDEX `dept_name`(`dept_name` ASC) USING BTREE,
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `student_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (11, 'Computer Science', 12);
INSERT INTO `student` VALUES (12, 'Computer Science', 24);
INSERT INTO `student` VALUES (13, 'Electrical Engineering', 9);
INSERT INTO `student` VALUES (14, 'Electrical Engineering', 21);
INSERT INTO `student` VALUES (15, 'Mathematics', 15);
INSERT INTO `student` VALUES (16, 'Mathematics', 30);
INSERT INTO `student` VALUES (17, 'Physics', 6);
INSERT INTO `student` VALUES (18, 'Physics', 18);
INSERT INTO `student` VALUES (19, 'Business Administration', 12);
INSERT INTO `student` VALUES (20, 'Business Administration', 27);
INSERT INTO `student` VALUES (21, 'Computer Science', 0);
INSERT INTO `student` VALUES (22, 'Electrical Engineering', 3);
INSERT INTO `student` VALUES (23, 'Mathematics', 36);
INSERT INTO `student` VALUES (24, 'Physics', 9);
INSERT INTO `student` VALUES (25, 'Business Administration', 45);
INSERT INTO `student` VALUES (26, 'Computer Science', 12);
INSERT INTO `student` VALUES (27, 'Electrical Engineering', 24);
INSERT INTO `student` VALUES (28, 'Mathematics', 9);
INSERT INTO `student` VALUES (29, 'Physics', 21);
INSERT INTO `student` VALUES (30, 'Business Administration', 15);

-- ----------------------------
-- Table structure for takes
-- ----------------------------
DROP TABLE IF EXISTS `takes`;
CREATE TABLE `takes`  (
  `student_id` int NOT NULL,
  `takes_id` int NOT NULL AUTO_INCREMENT,
  `sec_id` int NOT NULL,
  PRIMARY KEY (`takes_id`) USING BTREE,
  UNIQUE INDEX `takes_id`(`takes_id` ASC) USING BTREE,
  INDEX `sec_id`(`sec_id` ASC) USING BTREE,
  INDEX `idx_takes_student`(`student_id` ASC) USING BTREE,
  CONSTRAINT `takes_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `takes_ibfk_2` FOREIGN KEY (`sec_id`) REFERENCES `section` (`sec_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `takes_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `student` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of takes
-- ----------------------------
INSERT INTO `takes` VALUES (11, 1, 101);
INSERT INTO `takes` VALUES (12, 2, 101);
INSERT INTO `takes` VALUES (11, 3, 201);
INSERT INTO `takes` VALUES (13, 4, 401);
INSERT INTO `takes` VALUES (15, 5, 501);
INSERT INTO `takes` VALUES (16, 6, 501);
INSERT INTO `takes` VALUES (11, 7, 301);
INSERT INTO `takes` VALUES (12, 8, 201);
INSERT INTO `takes` VALUES (14, 9, 401);
INSERT INTO `takes` VALUES (17, 10, 801);
INSERT INTO `takes` VALUES (19, 11, 901);
INSERT INTO `takes` VALUES (20, 12, 901);
INSERT INTO `takes` VALUES (21, 13, 102);
INSERT INTO `takes` VALUES (22, 14, 401);
INSERT INTO `takes` VALUES (23, 15, 502);
INSERT INTO `takes` VALUES (24, 16, 801);
INSERT INTO `takes` VALUES (25, 17, 901);
INSERT INTO `takes` VALUES (26, 18, 101);
INSERT INTO `takes` VALUES (27, 19, 401);
INSERT INTO `takes` VALUES (28, 20, 601);
INSERT INTO `takes` VALUES (11, 21, 601);
INSERT INTO `takes` VALUES (15, 22, 601);
INSERT INTO `takes` VALUES (21, 23, 701);
INSERT INTO `takes` VALUES (23, 24, 701);
INSERT INTO `takes` VALUES (26, 25, 1001);
INSERT INTO `takes` VALUES (5, 26, 1001);
INSERT INTO `takes` VALUES (29, 27, 1001);
INSERT INTO `takes` VALUES (13, 28, 201);
INSERT INTO `takes` VALUES (14, 29, 101);
INSERT INTO `takes` VALUES (16, 30, 301);
INSERT INTO `takes` VALUES (18, 31, 801);

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `user_id` int NOT NULL,
  `dept_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `salary` int NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  INDEX `dept_name`(`dept_name` ASC) USING BTREE,
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `teacher_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES (2, 'Computer Science', 70000);
INSERT INTO `teacher` VALUES (3, 'Electrical Engineering', 72000);
INSERT INTO `teacher` VALUES (4, 'Mathematics', 68000);
INSERT INTO `teacher` VALUES (5, 'Computer Science', 80000);
INSERT INTO `teacher` VALUES (6, 'Physics', 75000);
INSERT INTO `teacher` VALUES (7, 'Mathematics', 82000);
INSERT INTO `teacher` VALUES (8, 'Computer Science', 73000);
INSERT INTO `teacher` VALUES (9, 'Physics', 69000);
INSERT INTO `teacher` VALUES (10, 'Business Administration', 71000);

-- ----------------------------
-- Table structure for time_slot
-- ----------------------------
DROP TABLE IF EXISTS `time_slot`;
CREATE TABLE `time_slot`  (
  `time_slot_id` int NOT NULL AUTO_INCREMENT,
  `day` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`time_slot_id`) USING BTREE,
  UNIQUE INDEX `time_slot_id`(`time_slot_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of time_slot
-- ----------------------------
INSERT INTO `time_slot` VALUES (1, 1, '08:00:00', '08:50:00');
INSERT INTO `time_slot` VALUES (2, 1, '09:00:00', '09:50:00');
INSERT INTO `time_slot` VALUES (3, 1, '10:00:00', '10:50:00');
INSERT INTO `time_slot` VALUES (4, 1, '11:00:00', '11:50:00');
INSERT INTO `time_slot` VALUES (5, 1, '13:00:00', '13:50:00');
INSERT INTO `time_slot` VALUES (6, 1, '14:00:00', '14:50:00');
INSERT INTO `time_slot` VALUES (7, 1, '15:00:00', '15:50:00');
INSERT INTO `time_slot` VALUES (8, 1, '16:00:00', '16:50:00');
INSERT INTO `time_slot` VALUES (9, 2, '08:00:00', '08:50:00');
INSERT INTO `time_slot` VALUES (10, 2, '09:00:00', '09:50:00');
INSERT INTO `time_slot` VALUES (11, 2, '10:00:00', '10:50:00');
INSERT INTO `time_slot` VALUES (12, 2, '11:00:00', '11:50:00');
INSERT INTO `time_slot` VALUES (13, 2, '13:00:00', '13:50:00');
INSERT INTO `time_slot` VALUES (14, 2, '14:00:00', '14:50:00');
INSERT INTO `time_slot` VALUES (15, 2, '15:00:00', '15:50:00');
INSERT INTO `time_slot` VALUES (16, 2, '16:00:00', '16:50:00');
INSERT INTO `time_slot` VALUES (17, 3, '08:00:00', '08:50:00');
INSERT INTO `time_slot` VALUES (18, 3, '09:00:00', '09:50:00');
INSERT INTO `time_slot` VALUES (19, 3, '10:00:00', '10:50:00');
INSERT INTO `time_slot` VALUES (20, 3, '11:00:00', '11:50:00');
INSERT INTO `time_slot` VALUES (21, 3, '13:00:00', '13:50:00');
INSERT INTO `time_slot` VALUES (22, 3, '14:00:00', '14:50:00');
INSERT INTO `time_slot` VALUES (23, 3, '15:00:00', '15:50:00');
INSERT INTO `time_slot` VALUES (24, 3, '16:00:00', '16:50:00');
INSERT INTO `time_slot` VALUES (25, 4, '08:00:00', '08:50:00');
INSERT INTO `time_slot` VALUES (26, 4, '09:00:00', '09:50:00');
INSERT INTO `time_slot` VALUES (27, 4, '10:00:00', '10:50:00');
INSERT INTO `time_slot` VALUES (28, 4, '11:00:00', '11:50:00');
INSERT INTO `time_slot` VALUES (29, 4, '13:00:00', '13:50:00');
INSERT INTO `time_slot` VALUES (30, 4, '14:00:00', '14:50:00');
INSERT INTO `time_slot` VALUES (31, 4, '15:00:00', '15:50:00');
INSERT INTO `time_slot` VALUES (32, 4, '16:00:00', '16:50:00');
INSERT INTO `time_slot` VALUES (33, 5, '08:00:00', '08:50:00');
INSERT INTO `time_slot` VALUES (34, 5, '09:00:00', '09:50:00');
INSERT INTO `time_slot` VALUES (35, 5, '10:00:00', '10:50:00');
INSERT INTO `time_slot` VALUES (36, 5, '11:00:00', '11:50:00');
INSERT INTO `time_slot` VALUES (37, 5, '13:00:00', '13:50:00');
INSERT INTO `time_slot` VALUES (38, 5, '14:00:00', '14:50:00');
INSERT INTO `time_slot` VALUES (39, 5, '15:00:00', '15:50:00');
INSERT INTO `time_slot` VALUES (40, 5, '16:00:00', '16:50:00');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `account_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `personal_infor_id` int NOT NULL,
  `type` enum('student','teacher','administrator') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `personal_infor_id`(`personal_infor_id` ASC) USING BTREE,
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`personal_infor_id`) REFERENCES `personal_information` (`personal_infor_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin01', 'hashed_password_admin01', 12, 'administrator');
INSERT INTO `user` VALUES (2, 'teacher001', 'hashed_password_t001', 1, 'teacher');
INSERT INTO `user` VALUES (3, 'teacher002', 'hashed_password_t002', 2, 'teacher');
INSERT INTO `user` VALUES (4, 'teacher003', 'hashed_password_t003', 3, 'teacher');
INSERT INTO `user` VALUES (5, 'teacher004', 'hashed_password_t004', 13, 'teacher');
INSERT INTO `user` VALUES (6, 'teacher005', 'hashed_password_t005', 14, 'teacher');
INSERT INTO `user` VALUES (7, 'teacher006', 'hashed_password_t006', 15, 'teacher');
INSERT INTO `user` VALUES (8, 'teacher007', 'hashed_password_t007', 16, 'teacher');
INSERT INTO `user` VALUES (9, 'teacher008', 'hashed_password_t008', 17, 'teacher');
INSERT INTO `user` VALUES (10, 'teacher009', 'hashed_password_t009', 18, 'teacher');
INSERT INTO `user` VALUES (11, 'student001', 'hashed_password_s001', 4, 'student');
INSERT INTO `user` VALUES (12, 'student002', 'hashed_password_s002', 5, 'student');
INSERT INTO `user` VALUES (13, 'student003', 'hashed_password_s003', 6, 'student');
INSERT INTO `user` VALUES (14, 'student004', 'hashed_password_s004', 7, 'student');
INSERT INTO `user` VALUES (15, 'student005', 'hashed_password_s005', 8, 'student');
INSERT INTO `user` VALUES (16, 'student006', 'hashed_password_s006', 9, 'student');
INSERT INTO `user` VALUES (17, 'student007', 'hashed_password_s007', 10, 'student');
INSERT INTO `user` VALUES (18, 'student008', 'hashed_password_s008', 11, 'student');
INSERT INTO `user` VALUES (19, 'student009', 'hashed_password_s009', 19, 'student');
INSERT INTO `user` VALUES (20, 'student010', 'hashed_password_s010', 20, 'student');
INSERT INTO `user` VALUES (21, 'student011', 'hashed_password_s011', 21, 'student');
INSERT INTO `user` VALUES (22, 'student012', 'hashed_password_s012', 22, 'student');
INSERT INTO `user` VALUES (23, 'student013', 'hashed_password_s013', 23, 'student');
INSERT INTO `user` VALUES (24, 'student014', 'hashed_password_s014', 24, 'student');
INSERT INTO `user` VALUES (25, 'student015', 'hashed_password_s015', 25, 'student');
INSERT INTO `user` VALUES (26, 'student016', 'hashed_password_s016', 26, 'student');
INSERT INTO `user` VALUES (27, 'student017', 'hashed_password_s017', 27, 'student');
INSERT INTO `user` VALUES (28, 'student018', 'hashed_password_s018', 28, 'student');
INSERT INTO `user` VALUES (29, 'student019', 'hashed_password_s019', 29, 'student');
INSERT INTO `user` VALUES (30, 'student020', 'hashed_password_s020', 30, 'student');

SET FOREIGN_KEY_CHECKS = 1;

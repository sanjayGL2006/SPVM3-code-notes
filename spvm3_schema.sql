-- =============================================================================
-- SPVM3 TECH SOLUTION — MYSQL DATABASE SCHEMATIC & SEED DATA
-- =============================================================================
-- Author: Sanjay G L (Founder & Lead Director, SPVM3 Tech Solution)
-- Description: Complete MySQL database setup script for SPVM3 Tech Solution,
--              including students, 21 course subjects, certificates, progress tracking,
--              automated trigger views, and seed data.
-- =============================================================================

-- 1. DATABASE CREATION
CREATE DATABASE IF NOT EXISTS `spvm3_db`
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `spvm3_db`;

-- -----------------------------------------------------------------------------
-- 2. DROP EXISTING TABLES (If resetting schema)
-- -----------------------------------------------------------------------------
DROP VIEW IF EXISTS `v_issued_certificates`;
DROP VIEW IF EXISTS `v_student_overview`;
DROP TABLE IF EXISTS `certificates`;
DROP TABLE IF EXISTS `student_progress`;
DROP TABLE IF EXISTS `courses`;
DROP TABLE IF EXISTS `students`;
DROP TABLE IF EXISTS `visitors`;

-- -----------------------------------------------------------------------------
-- 3. STUDENTS TABLE (User registrations & leads)
-- -----------------------------------------------------------------------------
CREATE TABLE `students` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `full_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `welcome_email_sent` TINYINT(1) DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_student_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 4. COURSES / SUBJECTS TABLE (21 Master CS Modules)
-- -----------------------------------------------------------------------------
CREATE TABLE `courses` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `subject_code` VARCHAR(50) NOT NULL UNIQUE,
    `course_title` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(255) NOT NULL,
    `category` VARCHAR(100) NOT NULL,
    `course_hours` INT DEFAULT 40,
    `icon` VARCHAR(10) DEFAULT '📘',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_subject_code` (`subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 5. CERTIFICATES TABLE (ISO-Certified Certificates Issued)
-- -----------------------------------------------------------------------------
CREATE TABLE `certificates` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `cert_id` VARCHAR(100) NOT NULL UNIQUE,
    `student_name` VARCHAR(150) NOT NULL,
    `student_email` VARCHAR(150) NOT NULL,
    `subject_code` VARCHAR(50) NOT NULL,
    `course_title` VARCHAR(255) NOT NULL,
    `course_hours` VARCHAR(50) DEFAULT '40 Hours',
    `verification_hash` VARCHAR(255) DEFAULT NULL,
    `email_sent` TINYINT(1) DEFAULT 0,
    `issued_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_email`) REFERENCES `students`(`email`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`subject_code`) REFERENCES `courses`(`subject_code`) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX `idx_cert_id` (`cert_id`),
    INDEX `idx_student_email_cert` (`student_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 6. STUDENT PROGRESS TRACKING TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE `student_progress` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_email` VARCHAR(150) NOT NULL,
    `subject_code` VARCHAR(50) NOT NULL,
    `completion_percentage` DECIMAL(5,2) DEFAULT 0.00,
    `modules_completed` INT DEFAULT 0,
    `last_accessed` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `student_course_unique` (`student_email`, `subject_code`),
    FOREIGN KEY (`student_email`) REFERENCES `students`(`email`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`subject_code`) REFERENCES `courses`(`subject_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 7. VISITORS TABLE (Platform Analytics & Leads)
-- -----------------------------------------------------------------------------
CREATE TABLE `visitors` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `welcome_email_sent` TINYINT(1) DEFAULT 0,
    `visited_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 8. ANALYTICS & VERIFICATION VIEWS
-- -----------------------------------------------------------------------------

-- Certificate Verification View
CREATE VIEW `v_issued_certificates` AS
SELECT 
    c.`cert_id`,
    c.`student_name`,
    c.`student_email`,
    c.`course_title`,
    c.`course_hours`,
    c.`issued_at`,
    c.`email_sent`,
    co.`category`,
    co.`icon`
FROM `certificates` c
JOIN `courses` co ON c.`subject_code` = co.`subject_code`;

-- Student Activity Overview View
CREATE VIEW `v_student_overview` AS
SELECT 
    s.`id` AS student_id,
    s.`full_name`,
    s.`email`,
    COUNT(DISTINCT p.`subject_code`) AS courses_enrolled,
    AVG(p.`completion_percentage`) AS avg_completion_pct,
    COUNT(DISTINCT c.`cert_id`) AS total_certificates_earned
FROM `students` s
LEFT JOIN `student_progress` p ON s.`email` = p.`student_email`
LEFT JOIN `certificates` c ON s.`email` = c.`student_email`
GROUP BY s.`id`, s.`full_name`, s.`email`;

-- -----------------------------------------------------------------------------
-- 9. SEED DATA (21 Master Computer Science Modules)
-- -----------------------------------------------------------------------------
INSERT INTO `courses` (`subject_code`, `course_title`, `file_path`, `category`, `course_hours`, `icon`) VALUES
('ai-systems', 'AI Systems & LLM Agents Notes', 'ai-systems-notes.html', 'Artificial Intelligence', 55, '🤖'),
('blockchain', 'Blockchain & Cryptography Notes', 'blockchain-notes.html', 'Systems & Security', 45, '⛓️'),
('dsa', 'Data Structures & Algorithms (DSA)', 'data-structures-notes.html', 'Core Computer Science', 60, '🧩'),
('html-css', 'HTML & CSS Complete Notes', 'HTML-CSS-Complete-Notes.html', 'Web Development', 35, '🌐'),
('javascript', 'JavaScript A–Z Master Notes', 'js-notes.html', 'Web Development', 50, '⚡'),
('react-js', 'React.js Reference Notes', 'react-notes.html', 'Frontend Development', 45, '⚛️'),
('react-manual', 'React Field Manual', 'react-field-manual.html', 'Frontend Development', 40, '📘'),
('electron-js', 'Electron.js Desktop App Notes', 'electron-js-notes.html', 'Desktop Development', 35, '💻'),
('php', 'PHP Complete Notes', 'php-notes.html', 'Backend Development', 40, '🐘'),
('python', 'Python A–Z Master Notes', 'python_notes.html', 'Programming Languages', 65, '🐍'),
('c-prog', 'C Programming Complete Notes', 'C-Programming-Complete-Notes.html', 'Programming Languages', 50, '🔤'),
('cpp', 'C++ Interactive Notes', 'cpp-notes.html', 'Programming Languages', 55, '⚡'),
('java', 'Java Brewed Complete Notes', 'java-notes.html', 'Programming Languages', 60, '☕'),
('dbms-sql', 'DBMS & SQL Complete Reference', 'DBMS-and-SQL-Complete-Reference.html', 'Databases', 50, '🗄️'),
('os', 'Operating Systems Notes', 'operating-systems-complete-notes.html', 'Core Computer Science', 50, '🖥️'),
('comp-fund', 'Fundamentals of Computers Notes', 'fundamentals-of-computers-notes.html', 'Core Computer Science', 30, '🕹️'),
('software-testing', 'Software Testing & QA Notes', 'software-testing-notes.html', 'Software Engineering', 40, '🧪'),
('git', 'Git & Version Control Guide', 'git-clone-guide.html', 'DevOps & Tools', 25, '🌿'),
('docker', 'Docker Interactive Guide', 'docker-notes.html', 'DevOps & Cloud', 40, '🐳'),
('kubernetes', 'Kubernetes A to Z Guide', 'kubernetes-a-to-z-guide.html', 'DevOps & Cloud', 50, '☸️'),
('deep-learning', 'Deep Learning & AI Notes', 'deep-learning-notes.html', 'Artificial Intelligence', 65, '🧠');

-- -----------------------------------------------------------------------------
-- 10. SEED SAMPLE DEMO DATA (Admin & Verified Certificate)
-- -----------------------------------------------------------------------------
INSERT INTO `students` (`full_name`, `email`, `welcome_email_sent`) VALUES
('Sanjay G L', 'spvm3techsolution@gmail.com', 1),
('Demo Student', 'student@example.com', 1);

INSERT INTO `certificates` (`cert_id`, `student_name`, `student_email`, `subject_code`, `course_title`, `course_hours`, `verification_hash`, `email_sent`) VALUES
('SPVM3-CERT-2026-PYTHON01', 'Sanjay G L', 'spvm3techsolution@gmail.com', 'python', 'Python A–Z Master Notes', '65 Hours', 'HASH-SPVM3-PY-9921', 1),
('SPVM3-CERT-2026-DBMS02', 'Demo Student', 'student@example.com', 'dbms-sql', 'DBMS & SQL Complete Reference', '50 Hours', 'HASH-SPVM3-SQL-4481', 1);

INSERT INTO `student_progress` (`student_email`, `subject_code`, `completion_percentage`, `modules_completed`) VALUES
('spvm3techsolution@gmail.com', 'python', 100.00, 10),
('spvm3techsolution@gmail.com', 'ai-systems', 85.50, 8),
('student@example.com', 'dbms-sql', 90.00, 9);

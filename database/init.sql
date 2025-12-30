-- ==================== 学生信息数据库初始化脚本 ====================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE student_db;

-- 删除已存在的表
DROP TABLE IF EXISTS students;

-- 创建学生信息表
CREATE TABLE students (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(50) NOT NULL COMMENT '学生姓名',
    student_id VARCHAR(20) NOT NULL UNIQUE COMMENT '学号（唯一）',
    class_name VARCHAR(50) NOT NULL COMMENT '班级',
    college VARCHAR(100) NOT NULL COMMENT '学院',
    major VARCHAR(100) NOT NULL COMMENT '专业',
    grade VARCHAR(10) NOT NULL COMMENT '年级',
    gender ENUM('男', '女') NOT NULL COMMENT '性别',
    phone VARCHAR(20) COMMENT '手机号',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_student_id (student_id),
    INDEX idx_college (college),
    INDEX idx_class_name (class_name),
    INDEX idx_grade (grade)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学生信息表';

-- 插入示例数据
INSERT INTO students (name, student_id, class_name, college, major, grade, gender, phone) VALUES
('张三', '2024001', '计算机1班', '计算机学院', '计算机科学与技术', '2024级', '男', '13800138001'),
('李四', '2024002', '计算机1班', '计算机学院', '计算机科学与技术', '2024级', '男', '13800138002'),
('王五', '2024003', '计算机1班', '计算机学院', '计算机科学与技术', '2024级', '女', '13800138003'),
('赵六', '2023001', '软件工程1班', '软件学院', '软件工程', '2023级', '男', '13800138004'),
('钱七', '2023002', '软件工程1班', '软件学院', '软件工程', '2023级', '女', '13800138005'),
('孙八', '2022001', '数据科学1班', '数据科学学院', '数据科学', '2022级', '男', '13800138006'),
('周九', '2022002', '数据科学1班', '数据科学学院', '数据科学', '2022级', '女', '13800138007'),
('吴十', '2021001', '人工智能1班', '人工智能学院', '人工智能', '2021级', '男', '13800138008'),
('郑十一', '2021002', '人工智能1班', '人工智能学院', '人工智能', '2021级', '女', '13800138009'),
('王十二', '2024004', '计算机2班', '计算机学院', '计算机科学与技术', '2024级', '男', '13800138010');

-- 查看表结构
DESCRIBE students;

-- 查看插入的数据
SELECT * FROM students ORDER BY student_id;

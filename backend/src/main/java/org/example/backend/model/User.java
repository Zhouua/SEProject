package org.example.backend.model;

// 用户类
public class User {
    private int user_id; // 用户ID
    private String account; // 账号
    private String password; // 密码
    private int person_info_id; // 个人信息ID
    private enum type {Student, Teacher, Admin}; // 用户类型（学生、教师、管理员）
}

package org.example.backend.model;


// 学生类
public class Student {
    private int user_id; // 用户ID
    private String dept_name; // 专业
    private int tot_cred; // 总学分

    public Student() {
        // 默认构造函数
    }
    // 构造函数
    public Student(int id, String sampleCurriculum, String computerScience, int i) {
        user_id = id;
        dept_name = sampleCurriculum;
        tot_cred = i;
    }

    public int getId() {
        return user_id;
    }
    public String getPersonalCurriculum() {
        return "";
    }
}

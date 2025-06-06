package org.example.backend.model;

// 课程类
public class Course {
    private int course_id; // 课程ID
    private String title; // 课程名称
    private String dept_name; // 所属专业
    private int credit; // 学分
    private String course_info; // 课程信息
    private int capacity; // 课程容量

    public Course(int courseId, String title, String deptName, int credit, String courseInfo, int capacity) {
        this.course_id = courseId;
        this.title = title;
        this.dept_name = deptName;
        this.credit = credit;
        this.course_info = courseInfo;
        this.capacity = capacity;
    }

    public int getCourseId() { return course_id; }
    public void setCourseId(int id) { this.course_id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDeptName() { return dept_name; }
    public void setDeptName(String deptName) { this.dept_name = deptName; }

    public int getCredit() { return credit; }
    public void setCredit(int credits) { this.credit = credit; }

    public String getCourseInfo() { return course_info; }
    public void setCourseInfo(String courseInfo) { this.course_info = courseInfo; }

    public int getCapacity() { return capacity; }
    public void setCapacity(int capacity) { this.capacity = capacity;}
}

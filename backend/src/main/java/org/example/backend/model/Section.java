package org.example.backend.model;

import java.sql.Time;
import java.time.Year;

// section类
public class Section {
    private int course_id; // 课程ID
    private int sec_id; // 课程节ID
    private String semester; // 学期
    private Year year; // 年份
    private int classroom_id; // 教室ID
    private String time_slot_ids; // 上课时间段
    private int teacher_id; // 教师ID
    private int remain_capacity; // 剩余容量

    public int getSec_id() {
        return sec_id;
    }
    public void setSec_id(int sec_id) { this.sec_id = sec_id; }

    public int getCourse_id(){ return course_id; }

    public void setCourse_id(int course_id){ this.course_id = course_id; }

    public String getSemester(){ return semester; }
    public void setSemester(String semester){ this.semester = semester; }

    public Year getYear(){ return year; }
    public void setYear(Year year){ this.year = year; }

    public int getClassroom_id(){ return classroom_id; }
    public void setClassroom_id(int classroom_id){ this.classroom_id = classroom_id; }

    public String getTime_slot_id(){ return time_slot_ids; }
    public void setTime_slot_id(String time_slot_ids){ this.time_slot_ids = time_slot_ids; }

    public int getTeacher_id(){ return teacher_id; }
    public void setTeacher_id(int teacher_id){ this.teacher_id = teacher_id; }

    public int getRemain_capacity(){ return remain_capacity; }
    public void setRemain_capacity(int remain_capacity){ this.remain_capacity = remain_capacity; }
}

package org.example.backend.model;

import org.springframework.cglib.core.Local;

import java.sql.Time;
import java.time.LocalTime;

public class Timeslot {
    int time_slot_id; // 时间段ID
    int day; // 周几
    LocalTime start_time; // 开始时间
    LocalTime end_time; // 结束时间

    // 添加格式化描述方法
    public String getFormattedDescription() {
        String dayName = getDayName(day);
        return dayName + " 第" + start_time + "-" + end_time + "节";
    }

    // 根据day值获取星期几名称
    public String getDayName(int day) {
        switch (day) {
            case 1: return "周一";
            case 2: return "周二";
            case 3: return "周三";
            case 4: return "周四";
            case 5: return "周五";
            case 6: return "周六";
            case 7: return "周日";
            default: return "未知";
        }
    }

    public int getTime_slot_id() {
        return time_slot_id;
    }
    public void setTime_slot_id(int time_slot_id) {
        this.time_slot_id = time_slot_id;
    }
    public int getDay() {
        return day;
    }
    public void setDay(int day) {
        this.day = day;
    }
    public LocalTime getStart_time() {
        return start_time;
    }
    public void setStart_time(LocalTime start_time) {
        this.start_time = start_time;
    }
    public LocalTime getEnd_time() {
        return end_time;
    }
    public void setEnd_time(LocalTime end_time) {
        this.end_time = end_time;
    }

    @Override
    public String toString() {
        return "Timeslot{" +
                "time_slot_id=" + time_slot_id +
                ", day=" + day +
                ", start_time=" + start_time +
                ", end_time=" + end_time +
                '}';
    }
}

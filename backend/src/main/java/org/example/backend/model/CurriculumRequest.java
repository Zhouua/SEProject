package org.example.backend.model;

import java.util.List;

public class CurriculumRequest {
    private int userId; // user_id的培养方案
    private List<Integer> courseIds; // 课程ID数组

    public int getUserId() {
        return userId;
    }

    public List<Integer> getCourseIds() {
        return courseIds;
    }
}


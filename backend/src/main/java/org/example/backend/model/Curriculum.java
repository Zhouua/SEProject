package org.example.backend.model;

public class Curriculum {
    private int user_id;
    private int course_id;

    public Curriculum(int user_id, int course_id) {
        this.user_id = user_id;
        this.course_id = course_id;
    }

    public int getUserId() {
        return user_id;
    }

    public int getCourseId() {
        return course_id;
    }
}

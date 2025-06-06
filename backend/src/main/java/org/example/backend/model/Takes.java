package org.example.backend.model;

public class Takes {
    private int take_id;
    private int student_id;
    private int sec_id;

    public int getSec_id() {
        return sec_id;
    }

    public void setSec_id(int sec_id) {
        this.sec_id = sec_id;
    }

    public int getStudent_id() {
        return student_id;
    }

    public void setStudent_id(int student_id) {
        this.student_id = student_id;
    }

    public void setTake_id(int take_id) {
        this.take_id = take_id;
    }

    public int getTake_id() {
        return take_id;
    }
}

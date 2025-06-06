package org.example.backend.controller;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.example.backend.service.AdminService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/admin")
public class AdminController {
    @Autowired
    private AdminService adminService;

    //设置选课时间
    @PutMapping("/SelectionTime")
    public ResponseEntity<String> setSelectionTime(@RequestBody SelectionTime selectionTime) {
        try {
            String result = adminService.setSelectionTime(selectionTime);
            if (!result.equals("设置成功")) {
                return ResponseEntity.status(400).body(result);
            }
            return ResponseEntity.ok("设置成功");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(e.getMessage());
        }
    }

    //学生查询
    @GetMapping("/HelpSelect/students")
    public ResponseEntity<List<Student_>> studentSearch(
            @RequestParam(required = false) String studentId,
            @RequestParam(required = false) String studentName
    ) {
        try {
            List<Student_> students = adminService.searchStudent(studentId,studentName);
            if (students.isEmpty()) {
                return ResponseEntity.status(404).body(null);
            }
            return ResponseEntity.ok(students);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(null);
        }
    }

    //课程查询
    @GetMapping("/HelpSelect/courses")
    public ResponseEntity<List<Section_>> courseSearch(
            @RequestParam(required = false) String courseYear,
            @RequestParam(required = false) String courseSemester,
            @RequestParam(required = false) String courseName,
            @RequestParam(required = false) String courseInstructor
    ) {
        try {
            List<Section_> courses = adminService.searchCourse(courseYear,courseSemester,courseName,courseInstructor);
            if (courses.isEmpty()) {
                return ResponseEntity.status(404).body(null);
            }
            return ResponseEntity.ok(courses);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(null);
        }
    }

    //进行选课
    @PostMapping("/HelpSelect")
    public ResponseEntity<String> helpSelect(@RequestBody takes_ take_info) {
        try {
            String result = adminService.helpSelect(take_info.getStudent_id(),take_info.getSection_id());
            if (!result.equals("选课成功")) {
                return ResponseEntity.status(400).body(result);
            }
            return ResponseEntity.ok("选课成功");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(e.getMessage());
        }
    }

    public static class SelectionTime {
        @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm")
        private LocalDateTime primaryStart;
        @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm")
        private LocalDateTime primaryEnd;
        @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm")
        private LocalDateTime supplementaryStart;
        @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm")
        private LocalDateTime supplementaryEnd;

        public LocalDateTime getPrimaryStart() {return primaryStart;}
        public LocalDateTime getPrimaryEnd() {return primaryEnd;}
        public LocalDateTime getSupplementaryStart() {return supplementaryStart;}
        public LocalDateTime getSupplementaryEnd() {return supplementaryEnd;}
    }

    public static class Student_ {
        private String student_id;
        private String student_name;
        private String dept_name;

        public String getStudent_id() {return student_id;}
        public String getDept_name() {return dept_name;}
        public String getStudent_name() {return student_name;}
        public void setStudent_id(String student_id) {this.student_id = student_id;}
        public void setDept_name(String dept_name) {this.dept_name = dept_name;}
        public void setStudent_name(String student_name) {this.student_name = student_name;}
    }

    public static class Section_ {
        private String courseId;
        private String name;
        private String instructor;
        private String credit;
        private String time;
        private String place;
        private String sectionId;
        private String capacity;

        public String getCourseId() {return courseId;}
        public String getName() {return name;}
        public String getInstructor() {return instructor;}
        public String getCredit() {return credit;}
        public String getTime() {return time;}
        public String getPlace() {return place;}
        public String getSectionId() {return sectionId;}
        public String getCapacity() {return capacity;}

        public void setCourseId(String courseId) {this.courseId = courseId;}
        public void setName(String name) {this.name = name;}
        public void setInstructor(String instructor) {this.instructor = instructor;}
        public void setCredit(String credit) {this.credit = credit;}
        public void setTime(String time) {this.time = time;}
        public void setPlace(String place) {this.place = place;}
        public void setSectionId(String sectionId) {this.sectionId = sectionId;}
        public void setCapacity(String capacity) {this.capacity = capacity;}
    }

    public static class takes_ {
        @JsonProperty("studentId")
        private String student_id;
        @JsonProperty("sectionId")
        private String section_id;

        public String getStudent_id() {return student_id;}
        public String getSection_id() {return section_id;}
        public void setStudent_id(String student_id) {this.student_id = student_id;}
        public void setSection_id(String section_id) {this.section_id = section_id;}
    }
}

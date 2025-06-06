package org.example.backend.controller;

import java.util.List;
import java.util.Map;

import org.example.backend.service.TeacherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;

@RestController
@RequestMapping("/teacher")
public class TeacherController {

    @Autowired
    private TeacherService teacherService;

    @GetMapping("/{user_id}/CourseResultT")
    public ResponseEntity<List<Section_>> courseSearch(
            @PathVariable("user_id") String teacherId,
            @RequestParam(required = false) String courseName,
            @RequestParam String courseYear,
            @RequestParam String courseSemester
    ) {
        try {
            if (teacherId == null || teacherId.trim().isEmpty()
            ) {
                return ResponseEntity.badRequest().body(null);
            }
            List<Section_> courses = teacherService.selectCourseResult(Integer.parseInt(teacherId), courseName, courseYear, courseSemester);
            return ResponseEntity.ok(courses);
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body(null);
        }
        catch (RuntimeException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    /**
     * 获取教师的周课表数据。
     * @param teacherId 教师ID。
     * @param year 学年。
     * @param semester 学期。
     * @return 包含课表数据的 TimetableResponse。
     */
    @GetMapping("/{user_id}/timetable")
    public ResponseEntity<TimetableResponse> getTeacherTimetable(
            @PathVariable("user_id") String teacherId,
            @RequestParam String year,
            @RequestParam String semester) {
        try {
            if (teacherId == null || teacherId.trim().isEmpty() ||
                    year == null || year.trim().isEmpty() ||
                    semester == null || semester.trim().isEmpty()) {
                return ResponseEntity.badRequest().build();
            }
            TimetableResponse timetable = teacherService.getTeacherTimetable(Integer.parseInt(teacherId), year, semester);
            return ResponseEntity.ok(timetable);
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    // Section_ DTO (用于选课结果列表)
    public static class Section_ {
        // ... (保持不变)
        private String courseId;    // 课程ID
        private String name;        // 课程名称
        private String year;        // 学年
        private String semester;    // 学期
        private String time;        // 上课时间 (列表视图用)
        private String place;       // 上课地点
        private String instructor;  // 授课教师
        private String credit;      // 学分
        private int takes;          // 选课人数

        public String getCourseId() { return courseId; }
        public void setCourseId(String courseId) { this.courseId = courseId; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getYear() { return year; }
        public void setYear(String year) { this.year = year; }
        public String getSemester() { return semester; }
        public void setSemester(String semester) { this.semester = semester; }
        public String getTime() { return time; }
        public void setTime(String time) { this.time = time; }
        public String getPlace() { return place; }
        public void setPlace(String place) { this.place = place; }
        public String getInstructor() { return instructor; }
        public void setInstructor(String instructor) { this.instructor = instructor; }
        public String getCredit() { return credit; }
        public void setCredit(String credit) { this.credit = credit; }
        public int getTakes() { return takes; }
        public void setTakes(int takes) { this.takes = takes; }
    }

    // --- 新增用于周课表的 DTO ---
    /**
     * 代表课表中的一个课程安排条目。
     */
    public static class TimetableEntry {
        private String courseName;  // 课程名称
        private String location;    // 上课地点
        private String period;      // 时间段描述，例如 "第1-2节"
        private int studentCount;
        // private String dayOfWeek; // 星期几 (可以从Map的key获取，或者也在这里存一份)

        public TimetableEntry(String courseName, String location, String period, int studentCount) {
            this.courseName = courseName;
            this.location = location;
            this.period = period;
            this.studentCount = studentCount;
        }

        public String getCourseName() { return courseName; }
        public void setCourseName(String courseName) { this.courseName = courseName; }
        public String getLocation() { return location; }
        public void setLocation(String location) { this.location = location; }
        public String getPeriod() { return period; }
        public void setPeriod(String period) { this.period = period; }
        public int getStudentCount() { return studentCount; } // Getter for studentCount
        public void setStudentCount(int studentCount) { this.studentCount = studentCount; } // Setter for studentCount
    }

    /**
     * 用于封装整个周课表的响应数据。
     */
    public static class TimetableResponse {
        private String teacherId;
        private String year;
        private String semester;
        private Map<String, List<TimetableEntry>> timetable; // key: 星期几 (如 "周一"), value: 当天课程列表
        private String errorMessage; // 用于传递错误信息

        public String getTeacherId() { return teacherId; }
        public void setTeacherId(int teacherId) { this.teacherId = Integer.toString(teacherId);  }
        public String getYear() { return year; }
        public void setYear(String year) { this.year = year; }
        public String getSemester() { return semester; }
        public void setSemester(String semester) { this.semester = semester; }
        public Map<String, List<TimetableEntry>> getTimetable() { return timetable; }
        public void setTimetable(Map<String, List<TimetableEntry>> timetable) { this.timetable = timetable; }
        public String getErrorMessage() { return errorMessage; }
        public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
    }
}
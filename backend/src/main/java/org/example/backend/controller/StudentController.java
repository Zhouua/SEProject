package org.example.backend.controller;

import org.example.backend.mapper.*;
import org.example.backend.model.*;
import org.example.backend.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.sql.SQLException;
import java.time.Year;
import java.util.*;

// 负责前后端交互，接受前端请求，调用service层，接收 service 层返回的数据，最后返回具体的页面和数据到客户端
@CrossOrigin(origins = "http://localhost:5173")
@RestController
@RequestMapping("/student")
public class StudentController {
    @Autowired
    private StudentService studentService;// 学生服务层

    // zza
    @GetMapping("/getCourseStatus")
    public Integer getCourseStatus(@RequestParam Integer userId,
                                   @RequestParam Integer courseId) throws SQLException {

            // 根据 userId 和 courseId 查询数据库判断是否已添加培养方案
            boolean isEnrolled = studentService.courseInCurriculum(userId, courseId);
            return isEnrolled ? 1 : 0;
    }

    // zza
    @GetMapping("/getAllCourses")
    public ResponseEntity<List<Course>> getAllCourses() {
        System.out.println("获取所有课程信息");
        // 获取所有课程信息
        try {
            CourseMapper courseMapper= new CourseMapper();
            List<Course> courses = courseMapper.getAllCourses();
            return ResponseEntity.ok(courses);
        } catch (SQLException e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(null);
        }
    }

    // szx
    static public class SecInfo{
        public int sec_id;
        public String title;
        public  String semester;
        public String time;
        public String timeIds;
        public String dept_name;
        public String teacher;
        public int capacity;
        public int left_capacity;
        public boolean is_selected;
        public SecInfo(){}
    };
    @GetMapping("/{user_id}/getSections")
    public ResponseEntity<List<SecInfo>> getAllsections(@PathVariable int user_id) {
        System.out.println("获取所有教学班信息");
        // 获取所有课程信息
        try {
            CourseMapper courseMapper = new CourseMapper();
            SectionMapper sectionMapper = new SectionMapper();
            TakesMapper takesMapper = new TakesMapper();
            TimeslotMapper timeslotMapper = new TimeslotMapper();
            TeacherMapper teacherMapper = new TeacherMapper();
            List<SecInfo> secInfos = new ArrayList<>();
            List<Section> sections = sectionMapper.selectAll();
            for (Section section : sections) {
                if(!section.getYear().equals(Year.now())) continue;
                Course course =courseMapper.getCourseById(section.getCourse_id());
                String time = timeslotMapper.getTimeinStr(section.getTime_slot_id());
                SecInfo secInfo = new SecInfo();
                secInfo.sec_id=section.getSec_id();
                secInfo.title = course.getTitle();
                secInfo.semester = section.getSemester();
                secInfo.time =time;
                secInfo.timeIds = section.getTime_slot_id();
                secInfo.dept_name= course.getDeptName();
                secInfo.teacher=teacherMapper.getTeacherNameById(section.getTeacher_id());
                secInfo.capacity = course.getCapacity();
                secInfo.left_capacity =section.getRemain_capacity();
                secInfo.is_selected = takesMapper.selectTakes(user_id, section.getSec_id());
                //System.out.println("教学班ID："+secInfo.sec_id+" 课程名称："+secInfo.title+"课程学期："+secInfo.semester+" 课程时间："+secInfo.time+" 上课教室："+secInfo.dept_name+" 上课教师："+secInfo.teacher+" 课程容量："+secInfo.capacity+" 已选人数："+secInfo.left_capacity+" "+(secInfo.is_selected?"已选课程":"未选课程"));
                secInfos.add(secInfo);
            }
            return ResponseEntity.ok(secInfos);
        } catch (SQLException e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(null);
        }
    }

    // szx
    @GetMapping("/{user_id}/getSelectionTime")
    public Map<String, String> getSelectionTime() throws IOException {
        String filePath = "selectionTime.txt";
        List<String> lines = new ArrayList<>();

        // 按行读取四个时间
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null && lines.size() < 4) {
                lines.add(line.trim());
            }
        }

        if (lines.size() < 4) {
            throw new IOException("selectionTime.txt格式错误，行数不足4行");
        }
        Map<String, String> result = new HashMap<>();
        result.put("PRIMARY_SELECTION_START", lines.get(0));System.out.println(lines.get(0));
        result.put("PRIMARY_SELECTION_END", lines.get(1));System.out.println(lines.get(1));
        result.put("SUPPLEMENTARY_SELECTION_START", lines.get(2));System.out.println(lines.get(2));
        result.put("SUPPLEMENTARY_SELECTION_END", lines.get(3));System.out.println(lines.get(3));
        return result;
    }

    // zza
    @PostMapping("removePersonalCurriculum")
    public ResponseEntity<String> removePersonalCurriculum(@RequestBody CurriculumRequest request) {
        // @RequestBody注解用来绑定通过http请求中application/json类型上传的数据
        try {
            int userId = request.getUserId();
            System.out.println("学生 ID：" + userId);
            for (Integer courseId : request.getCourseIds()) {
                System.out.println("选中课程 ID：" + courseId);
                Curriculum curriculum = new Curriculum(userId, courseId);
                // 调用 service 层，将数据写入数据库
                String result = studentService.removePersonalCurriculum(curriculum);
                if (!result.equals("删除成功")) {
                    return ResponseEntity.status(400).body(result); // 返回错误信息
                }
            }
            return ResponseEntity.ok("已从培养方案中删除课程");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(e.getMessage());
        }
    }

    // zza
    @PostMapping("/setPersonalCurriculum")
    public ResponseEntity<String> setPersonalCurriculum(@RequestBody CurriculumRequest request) {
        // @RequestBody注解用来绑定通过http请求中application/json类型上传的数据
        try {
            int userId = request.getUserId();
            System.out.println("学生 ID：" + userId);
            for (Integer courseId : request.getCourseIds()) {
                System.out.println("选中课程 ID：" + courseId);
                Curriculum curriculum = new Curriculum(userId, courseId);
                // 调用 service 层，将数据写入数据库
                String result = studentService.setPersonalCurriculum(curriculum);
                if (!result.equals("添加成功")) {
                    return ResponseEntity.status(400).body(result); // 返回错误信息
                }
            }
            return ResponseEntity.ok("已添加课程进入培养方案");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body(e.getMessage());
        }
    }

    // szx
    @GetMapping("/{user_id}/chooseCourse/{sec_id}")
    public ResponseEntity<String> chooseCourse(@PathVariable int user_id, @PathVariable int sec_id) {
        // 通过网页表单提交的json信息，学生选课
        // 返回选课结果的状态码
        System.out.println("选择课程：" + user_id+", 学生信息：" + sec_id);
        String result = studentService.chooseCourse(user_id, sec_id);
        System.out.println(result);
        if(result.equals("选课成功")) { return ResponseEntity.ok("选课成功"); }
        else return ResponseEntity.status(500).body(result);
    }

    // szx
    @GetMapping("/{user_id}/dropCourse/{sec_id}")
    public ResponseEntity<String> dropCourse(@PathVariable int user_id, @PathVariable int sec_id) {
        // 通过网页表单提交的json信息，学生退课
        // 返回退课结果的状态码
        System.out.println("退选课程：" + sec_id+", 学生信息：" + user_id);
        String result = studentService.dropCourse(user_id, sec_id);
        if(result.equals("退课成功")) { return ResponseEntity.ok("退课成功"); }
        else return ResponseEntity.status(500).body(result);
    }

    // lmt
    @GetMapping("/{user_id}/CourseResultS")
    public ResponseEntity<List<Section_>> courseSearch(
            @PathVariable("user_id") String studentId,
            @RequestParam(defaultValue = "") String courseYear,
            @RequestParam(defaultValue = "") String courseSemester
    ){
        try {
            List<Section_> courses = studentService.selectChosenCourseInfo(studentId, courseYear, courseSemester);
            return ResponseEntity.ok(courses);
        } catch (Exception e){
            e.printStackTrace();
            return ResponseEntity.status(500).body(null);
        }
    }

    // lmt
    @GetMapping("/{user_id}/CourseTableS")
    public ResponseEntity<TimetableResponse> getCourseTable(
            @PathVariable ("user_id") String studentId,
            @RequestParam(defaultValue = "") Integer courseYear,
            @RequestParam(defaultValue = "") String courseSemester) {

        try {
            // 调用 Service 层获取课表数据
            TimetableResponse response = studentService.getStudentTimetable(studentId, courseYear, courseSemester);

            // 确保至少返回空数据结构，而非null
            if (response.getTimetable() == null) {
                response.setTimetable(Collections.emptyMap());
            }

            // 如果课表为空，返回包含提示信息的响应
            if (response.getTimetable().isEmpty()) {
                response.setErrorMessage("该学期无选课记录");
            }

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            // 错误处理
            TimetableResponse errorResponse = new TimetableResponse();
            errorResponse.setErrorMessage("获取课表失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }


    public static class Section_ {
        private String courseId;
        private String name;
        private String year;
        private String semester;
        private String time;
        private String place;
        private String instructor;
        private String credit;
        private int takes;

        public int getTakes() {return takes;}
        public void setTakes(int takes) {this.takes = takes;}
        public String getCourseId() {return courseId;}
        public String getName() {return name;}
        public String getYear() {return year;}
        public String getSemester() {return semester;}
        public String getTime() {return time;}
        public String getPlace() {return place;}
        public String getInstructor() {return instructor;}
        public String getCredit() {return credit;}

        public void setCourseId(String courseId) {this.courseId = courseId;}
        public void setName(String name) {this.name = name;}
        public void setYear(String year) {this.year = year;}
        public void setSemester(String semester) {this.semester = semester;}
        public void setTime(String time) {this.time = time;}
        public void setPlace(String place) {this.place = place;}
        public void setInstructor(String instructor) {this.instructor = instructor;}
        public void setCredit(String credit) {this.credit = credit;}
    }

    // 课表所需函数结构1
    public static class TimetableResponse {
        private String studentId;
        private int year;
        private String semester;
        private Map<String, List<TimetableEntry>> timetable;
        private String errorMessage;

        // Getters and Setters
        public String getStudentId() {
            return studentId;
        }

        public void setStudentId(String studentId) {
            this.studentId = studentId;
        }

        public int getYear() {
            return year;
        }

        public void setYear(int year) {
            this.year = year;
        }

        public String getSemester() {
            return semester;
        }

        public void setSemester(String semester) {
            this.semester = semester;
        }

        public Map<String, List<TimetableEntry>> getTimetable() {
            return timetable;
        }

        public void setTimetable(Map<String, List<TimetableEntry>> timetable) {
            this.timetable = timetable;
        }

        public String getErrorMessage() {
            return errorMessage;
        }

        public void setErrorMessage(String errorMessage) {
            this.errorMessage = errorMessage;
        }
    }
    // 课表所需函数结构2
    public static class TimetableEntry {
        private String courseName;
        private String location;
        private String dayOfWeek;
        private String period;

        // Getters and Setters
        public String getCourseName() {
            return courseName;
        }

        public void setCourseName(String courseName) {
            this.courseName = courseName;
        }

        public String getLocation() {
            return location;
        }

        public void setLocation(String location) {
            this.location = location;
        }

        public String getDayOfWeek() {
            return dayOfWeek;
        }

        public void setDayOfWeek(String dayOfWeek) {
            this.dayOfWeek = dayOfWeek;
        }

        public String getPeriod() {
            return period;
        }

        public void setPeriod(String period) {
            this.period = period;
        }
    }

}


package org.example.backend.service;

import org.example.backend.controller.StudentController;
import org.example.backend.mapper.CourseMapper;
import org.example.backend.mapper.CurriculumMapper;
import org.example.backend.mapper.StudentMapper;
import org.example.backend.mapper.*;
import org.example.backend.model.Curriculum;
import org.example.backend.model.Section;
import org.example.backend.model.Student;
import org.example.backend.model.Takes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.SQLException;
import java.time.Year;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Arrays;

// 调用mapper层，完成学生能进行的操作功能
@Service
public class StudentService {


    // szx
    public String chooseCourse(int student_id, int sec_id) {
        try {
            System.out.println(student_id+" "+sec_id);
            TakesMapper takesMapper = new TakesMapper();
            SectionMapper sectionMapper = new SectionMapper();
            Section new_section= sectionMapper.selectSection(sec_id);
            //对所有课程进行判断
            List<Takes> Takes_list= takesMapper.selectAll();
            for(Takes takes:Takes_list) {
                System.out.println(takes.getStudent_id()+" "+takes.getSec_id());
                if(takes.getStudent_id()!=student_id) continue; // 只判断当前学生的选课情况
                Section section=sectionMapper.selectSection(takes.getSec_id());
                if(!section.getYear().equals(new_section.getYear())) continue;// 只判断同一年份的课程
                //重复选课
                if(section.getCourse_id()==new_section.getCourse_id()) return "已选择该课程的其他教学班";
                //学期、时间相同
                if(section.getTime_slot_id() == new_section.getTime_slot_id() && (section.getSemester().contains(new_section.getSemester())||new_section.getSemester().contains(section.getSemester())))
                    return "与其他已选课程时间冲突";
            }
            takesMapper.insertTakes(student_id, sec_id);
        }catch (Exception e) {
            e.printStackTrace();
            return "选课失败";
        }
        return "选课成功"; // 假设1表示成功
    }

    // szx
    public String dropCourse(int student_id, int sec_id) {
        try{
            TakesMapper takesMapper= new TakesMapper();
            if(!takesMapper.selectTakes(student_id,sec_id)) return "未选择该课程";
            takesMapper.deleteTakes(student_id,sec_id);
        } catch (SQLException e) {
            return "退课失败";
        }
        return "退课成功"; // 假设1表示成功
    }

    // lmt
    // 查看课表
    public StudentController.TimetableResponse getStudentTimetable(String studentId, int year, String semester) {
        StudentController.TimetableResponse response = new StudentController.TimetableResponse();
        response.setStudentId(studentId);
        response.setYear(year);
        response.setSemester(semester);

        try {
            if (semester == null) {
                throw new IllegalArgumentException("学期不能为空");
            }
            // 打印输入参数
            System.out.println("查询参数: studentId=" + studentId + ", year=" + year + ", semester=" + semester);

            // 创建数据访问对象
            SectionMapper sectionMapper = new SectionMapper();
            CourseMapper courseMapper = new CourseMapper();
            ClassroomMapper classroomMapper = new ClassroomMapper();
            TakesMapper takesMapper = new TakesMapper();

            List<String> targetSemesters = new ArrayList<String>();
            switch (semester) {
                case "春":
                    targetSemesters = Arrays.asList("Spring", "Spring&Summer");
                    break;
                case "夏":
                    targetSemesters = Arrays.asList("Summer", "Spring&Summer");
                    break;
                case "秋":
                    targetSemesters = Arrays.asList("Fall", "Fall&Winter");
                    break;
                case "冬":
                    targetSemesters = Arrays.asList("Winter", "Fall&Winter");
                    break;
                default:
                    targetSemesters = Collections.singletonList(semester);
            }
            // 打印目标学期列表
            System.out.println("目标学期: " + targetSemesters);

            // 1. 获取学生选的section_id
            List<String> sectionIds = takesMapper.getSectionIdByStudentId(studentId, year, targetSemesters);

            // 打印查询结果
            System.out.println("找到 " + sectionIds.size() + " 个选课记录");
            for (String secId : sectionIds) {
                System.out.println("选课ID: " + secId);
            }
            if (sectionIds.isEmpty()) {
                response.setErrorMessage("该学生本学期无选课记录");
                return response;
            }

            // 2. 解析课程段信息并构建课表条目
            Map<String, List<StudentController.TimetableEntry>> timetable = new HashMap<>();
            Map<Integer, String> dayMapping = new HashMap<>();
            dayMapping.put(1, "周一");
            dayMapping.put(2, "周二");
            dayMapping.put(3, "周三");
            dayMapping.put(4, "周四");
            dayMapping.put(5, "周五");

            // 時間段映射
            Map<Integer, String> periodMapping = new HashMap<>();
            periodMapping.put(1, "8:00-8:50");
            periodMapping.put(2, "9:00-9:50");
            periodMapping.put(3, "10:00-10:50");
            periodMapping.put(4, "11:00-11:50");
            periodMapping.put(5, "13:00-13:50");
            periodMapping.put(6, "14:00-14:50");
            periodMapping.put(7, "15:00-15:50");
            periodMapping.put(8, "16:00-16:50");

            for (String sectionId : sectionIds) {
                // 获取课程段（传入年份和学期）
                // 修改查询逻辑：仅通过sectionId查询，不强制要求年份和学期匹配
                List<Section> sections = sectionMapper.getSectionBySectionId(sectionId, null, null);
                if (sections.isEmpty()) {
                    System.out.println("警告：选课ID " + sectionId + " 找不到对应的课程段信息");
                    continue;
                }

                Section section = sections.get(0); // 假设sec_id在学年学期唯一
                String timeSlotId = section.getTime_slot_id();

                // 解析新格式的timeSlotId（例如："[1,2,3,4]"）
                List<Integer> timeSlots = parseTimeSlotIds(timeSlotId);

                // 遍历每个时间段，为每个时间段创建一个课表条目
                for (Integer slot : timeSlots) {
                    // 计算星期和时间段
                    int dayOfWeekNumber = (slot - 1) / 8 + 1; // 1-5表示周一到周五
                    int periodNumber = (slot - 1) % 8 + 1;    // 1-8表示时间段

                    String day = dayMapping.getOrDefault(dayOfWeekNumber, "未知");
                    String period = periodMapping.getOrDefault(periodNumber, "未知时段");

                    // 获取课程名称
                    String courseName = sectionMapper.getCourseNameBySectionIdWithCourse(sectionId);
                    if (courseName == null) courseName = "未知课程";

                    // 获取教室位置
                    String place = classroomMapper.getPlace(section.getClassroom_id());
                    if (place == null) place = "未登记教室";

                    // 构建课表条目
                    StudentController.TimetableEntry entry = new StudentController.TimetableEntry();
                    entry.setCourseName(courseName);
                    entry.setDayOfWeek(day);
                    entry.setPeriod(period);
                    entry.setLocation(place);

                    // 按星期分组
                    timetable.computeIfAbsent(day, k -> new ArrayList<>()).add(entry);
                }

            }
            response.setTimetable(timetable);
        } catch (Exception e){
            response.setErrorMessage("获取课表失败：" +e.getMessage());
            e.printStackTrace();
        }
        return response;
    }

    // lmt
    // 查看選課結果
    public List<StudentController.Section_> selectChosenCourseInfo(String studentId, String courseYear, String courseSemester) {
        // 这里应该有查询已选课程信息的逻辑
        try{
            // 创建数据访问对象
            SectionMapper sectionMapper = new SectionMapper();
            CourseMapper courseMapper = new CourseMapper();
            TeacherMapper teacherMapper = new TeacherMapper();
            ClassroomMapper classroomMapper = new ClassroomMapper();
            TakesMapper takesMapper = new TakesMapper();

            // 通过学号获取已选课程列表
            List<String> sectionIds = takesMapper.getSectionIdByStudentId(studentId);
            if (sectionIds.isEmpty()) {
                return Collections.emptyList();
            }

            // 通过sec_id、年份、学期查询
            List<Section> selectedSections = new ArrayList<>();
            for (String secId : sectionIds) {
                List<Section> sections = sectionMapper.getSectionBySectionId(
                        secId,
                        courseYear,   // 年份参数（可为null）
                        courseSemester // 学期参数（可为null）
                );
                selectedSections.addAll(sections);
            }

            // 组装最终结果
            List<StudentController.Section_> result = new ArrayList<>();
            for (Section section : selectedSections) {
                int courseId = section.getCourse_id();
                int secId = section.getSec_id();
                Year year = section.getYear();
                String semester = section.getSemester();
                int classroomId = section.getClassroom_id();
                String timeSlotIds = section.getTime_slot_id();
                int teacherId = section.getTeacher_id();

                // 获取关联信息
                String title = courseMapper.getTitleByCourseId(courseId);
                String credit = courseMapper.getCreditByCourseId(courseId);
                String teacherName = teacherMapper.getNameByTeacherId(teacherId);
                String time = convertTimeSlotIds(timeSlotIds);
                String place = classroomMapper.getPlace(classroomId);

                // 将英文学期转换为中文
                String chineseSemester = convertToChineseSemester(semester);

                // 构建返回对象
                StudentController.Section_ section_ = new StudentController.Section_();
                section_.setCourseId(String.valueOf(courseId));
                section_.setName(title != null ? title : "未知课程");
                section_.setYear(year.toString());
                section_.setSemester(chineseSemester);
                section_.setTime(time != null ? time : "未知时间");
                section_.setPlace(place != null ? place : "未知教室");
                section_.setInstructor(teacherName != null ? teacherName : "未知教师");
                section_.setCredit(credit != null ? credit : "0");
                result.add(section_);
            }
            return result;
        } catch (Exception e){
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    // lmt
    // 學期中英文轉換
    private String convertToChineseSemester(String englishSemester) {
        if (englishSemester == null) {
            return null;
        }

        return switch (englishSemester.toLowerCase()) {
            case "spring" -> "春";
            case "summer" -> "夏";
            case "fall" -> "秋";
            case "winter" -> "冬";
            case "springsummer" -> "春夏";
            case "fallwinter" -> "秋冬";
            default -> englishSemester;
        };
    }

    // lmt
    // 轉換時間信息
    public String convertTimeSlotIds(String timeSlotIds) {
        // 移除括号和空格
        String cleaned = timeSlotIds.replace("[", "").replace("]", "").replace(" ", "");
        if (cleaned.isEmpty()) {
            return "";
        }

        // 分割字符串为ID数组
        String[] ids = cleaned.split(",");
        StringBuilder timeBuilder = new StringBuilder();

        // 每天的时间段数量
        int slotsPerDay = 8;
        // 星期几的映射
        String[] dayNames = {"", "周一", "周二", "周三", "周四", "周五"};
        // 时间段起始时间（小时）
        int[] startTimeHours = {0, 8, 9, 10, 11, 13, 14, 15, 16};

        // 拼接时间描述
        for (int i = 0; i < ids.length; i++) {
            try {
                int id = Integer.parseInt(ids[i]);
                if (id < 1 || id > dayNames.length * slotsPerDay) {
                    timeBuilder.append("未知时间段");
                } else {
                    // 计算星期几和时间段
                    int dayOfWeek = (id - 1) / slotsPerDay + 1;
                    int timeSlotInDay = (id - 1) % slotsPerDay + 1;

                    // 计算开始时间和结束时间
                    int startHour = startTimeHours[timeSlotInDay];
                    int endHour = startHour;
                    int endMinute = 50;

                    // 构建时间描述
                    String timeDesc = String.format("%s%d:%02d-%d:%02d",
                            dayNames[dayOfWeek],
                            startHour, 0,
                            endHour, endMinute);

                    timeBuilder.append(timeDesc);
                }

                if (i < ids.length - 1) {
                    timeBuilder.append(", ");
                }
            } catch (NumberFormatException | ArrayIndexOutOfBoundsException e) {
                // 处理无效ID
                timeBuilder.append("无效ID");
                if (i < ids.length - 1) {
                    timeBuilder.append(", ");
                }
            }
        }

        return timeBuilder.toString();
    }

    // lmt
    // 解析字符串為整數列表
    private List<Integer> parseTimeSlotIds(String timeSlotIdStr) {
        List<Integer> timeSlots = new ArrayList<>();
        if (timeSlotIdStr == null || timeSlotIdStr.trim().isEmpty()) {
            return timeSlots;
        }

        // 移除方括号并分割字符串
        String cleaned = timeSlotIdStr.replace("[", "").replace("]", "").trim();
        if (cleaned.isEmpty()) {
            return timeSlots;
        }

        String[] parts = cleaned.split(",");
        for (String part : parts) {
            try {
                timeSlots.add(Integer.parseInt(part.trim()));
            } catch (NumberFormatException e) {
                System.out.println("警告：无效的timeSlotId格式：" + part);
            }
        }
        return timeSlots;
    }

    // zza
    public String setPersonalCurriculum(Curriculum curriculum) throws SQLException {
        // 这里应该有设置个人培养方案的逻辑
        CurriculumMapper curriculumMapper = new CurriculumMapper();
        return curriculumMapper.insertCurriculum(curriculum);
    }

    // zza
    public boolean courseInCurriculum(Integer userId, Integer courseId) throws SQLException {
        // 判断是否在个人培养方案中
        CurriculumMapper curriculumMapper = new CurriculumMapper();
        return curriculumMapper.isCourseInCurriculum(userId, courseId);
    }

    // zza
    public String removePersonalCurriculum(Curriculum curriculum) throws SQLException {
        CurriculumMapper curriculumMapper = new CurriculumMapper();
        return curriculumMapper.deleteCurriculum(curriculum);
    }
}

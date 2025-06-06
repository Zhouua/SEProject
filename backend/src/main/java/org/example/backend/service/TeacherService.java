package org.example.backend.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.backend.controller.TeacherController; // 使用 TeacherController 的 Section_ DTO
import org.example.backend.mapper.*;
import org.example.backend.model.Section; //
import org.example.backend.model.Timeslot;
import org.springframework.stereotype.Service; // 导入 Service 注解

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


@Service // 添加 Spring Service 注解
public class TeacherService {

    // It's better to use Spring's dependency injection for mappers
    // For this example, we'll continue with manual instantiation as in the original code
    // but ideally, these would be @Autowired fields.
    private final ObjectMapper objectMapper = new ObjectMapper();


    /**
     * 获取教师的选课结果。
     *
     * @param teacherId        教师ID。
     * @param courseNameFilter 可选的课程名称筛选器。
     * @param courseYear       学年。
     * @param courseSemester   学期。
     * @return 代表课程的 Section_ 对象列表。
     */
    public List<TeacherController.Section_> selectCourseResult(int teacherId, String courseNameFilter, String courseYear, String courseSemester) {
        List<TeacherController.Section_> result = new ArrayList<>();
        SectionMapper sectionMapper;
        CourseMapper courseMapper;
        TakesMapper takesMapper;
        TimeslotMapper timeslotMapper;
        ClassroomMapper classroomMapper;
        TeacherMapper teacherMapper;

        try {
            sectionMapper = new SectionMapper();
            courseMapper = new CourseMapper();
            takesMapper = new TakesMapper();
            timeslotMapper = new TimeslotMapper();
            classroomMapper = new ClassroomMapper();
            teacherMapper = new TeacherMapper();

            List<Section> sectionsTaught = sectionMapper.getSectionsByTeacherAndYearSemester(teacherId, courseYear, courseSemester); //

            String instructorName = teacherMapper.getNameByTeacherId(teacherId); //
            if (instructorName == null) {
                instructorName = "未知教师";
            }

            for (Section section : sectionsTaught) {
                String courseTitle = courseMapper.getTitleByCourseId(section.getCourse_id()); //
                if (courseTitle == null) {
                    courseTitle = "未知课程";
                }

                if (courseNameFilter != null && !courseNameFilter.trim().isEmpty()) {
                    if (!courseTitle.toLowerCase().contains(courseNameFilter.trim().toLowerCase())) {
                        continue;
                    }
                }

                int studentCount = takesMapper.getStudentCountBySectionId(section.getSec_id()); //

                String timeDisplay = "未知时间";
                String timeSlotIdsJson = section.getTime_slot_id(); // This is now a JSON string of IDs
                if (timeSlotIdsJson != null && !timeSlotIdsJson.isEmpty()) {
                    try {
                        List<Integer> timeSlotIdsList = objectMapper.readValue(timeSlotIdsJson, new TypeReference<List<Integer>>() {});
                        if (timeSlotIdsList != null && !timeSlotIdsList.isEmpty()) {
                            List<String> timeStrings = new ArrayList<>();
                            for (Integer tsId : timeSlotIdsList) {
                                String singleTime = timeslotMapper.getTime(tsId); //
                                if (singleTime != null) {
                                    timeStrings.add(singleTime);
                                }
                            }
                            // Sort time strings if necessary or format them
                            timeDisplay = timeStrings.stream().sorted().collect(Collectors.joining("; "));
                        }
                    } catch (IOException e) {
                        System.err.println("Error parsing time_slot_ids JSON: " + timeSlotIdsJson + " for section " + section.getSec_id() + " - " + e.getMessage());
                        // Keep timeDisplay as "未知时间" or handle error appropriately
                    }
                }


                String place = classroomMapper.getPlace(section.getClassroom_id()); //
                if (place == null) {
                    place = "未知地点";
                }
                String credit = courseMapper.getCreditByCourseId(section.getCourse_id()); //
                if (credit == null) {
                    credit = "N/A";
                }

                TeacherController.Section_ sectionDto = new TeacherController.Section_();
                sectionDto.setCourseId(String.valueOf(section.getCourse_id()));
                sectionDto.setName(courseTitle);
                sectionDto.setYear(section.getYear().toString());
                sectionDto.setSemester(section.getSemester());
                sectionDto.setTime(timeDisplay); // Use the processed time display
                sectionDto.setPlace(place);
                sectionDto.setInstructor(instructorName);
                sectionDto.setCredit(credit);
                sectionDto.setTakes(studentCount);

                result.add(sectionDto);
            }

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("获取课程结果时出错: " + e.getMessage(), e);
        } catch (NumberFormatException e) {
            e.printStackTrace();
            throw new RuntimeException("无效的教师ID格式: " + teacherId, e);
        }

        return result;
    }


    /**
     * 获取并组织教师的周课表数据。
     * @param teacherId 教师ID。
     * @param year      学年。
     * @param semester  学期。
     * @return TimetableResponse 包含课表数据。
     */
    public TeacherController.TimetableResponse getTeacherTimetable(int teacherId, String year, String semester) {
        TeacherController.TimetableResponse response = new TeacherController.TimetableResponse();
        response.setTeacherId(teacherId); //
        response.setYear(year); //
        response.setSemester(semester); //

        Map<String, List<TeacherController.TimetableEntry>> weeklyTimetable = new HashMap<>();
        String[] daysOrder = {"周一", "周二", "周三", "周四", "周五", "周六", "周日"}; //
        for (String day : daysOrder) {
            weeklyTimetable.put(day, new ArrayList<>()); //
        }

        try {
            SectionMapper sectionMapper = new SectionMapper();
            CourseMapper courseMapper = new CourseMapper();
            TimeslotMapper timeslotMapper = new TimeslotMapper();
            ClassroomMapper classroomMapper = new ClassroomMapper();
            TakesMapper takesMapper = new TakesMapper();

            List<Section> sections = sectionMapper.getSectionsByTeacherAndYearSemester(teacherId, year, semester); //

            if (sections.isEmpty()) {
                response.setErrorMessage("该教师在此学期无授课安排。"); //
                response.setTimetable(weeklyTimetable);
                return response;
            }

            for (Section section : sections) {
                String courseName = courseMapper.getTitleByCourseId(section.getCourse_id()); //
                if (courseName == null) courseName = "未知课程";

                String location = classroomMapper.getPlace(section.getClassroom_id()); //
                if (location == null) location = "未知地点";

                int studentCount = 0;
                try {
                    studentCount = takesMapper.getStudentCountBySectionId(section.getSec_id()); //
                } catch (Exception e) {
                    System.err.println("获取 section " + section.getSec_id() + " 的选课人数失败: " + e.getMessage());
                }

                String timeSlotIdsJson = section.getTime_slot_id(); // This is now a JSON string of IDs
                if (timeSlotIdsJson == null || timeSlotIdsJson.isEmpty()) {
                    System.err.println("警告: Section " + section.getSec_id() + " (course: " + courseName + ") has null or empty time_slot_ids.");
                    continue;
                }

                try {
                    List<Integer> timeSlotIdsList = objectMapper.readValue(timeSlotIdsJson, new TypeReference<List<Integer>>() {});
                    if (timeSlotIdsList == null || timeSlotIdsList.isEmpty()) {
                        System.err.println("警告: Parsed time_slot_ids list is null or empty for section " + section.getSec_id() + " (course: " + courseName + "). JSON was: " + timeSlotIdsJson);
                        continue;
                    }

                    for (Integer tsId : timeSlotIdsList) {
                        Timeslot timeslot = timeslotMapper.getTimeslotById(tsId); //

                        if (timeslot != null) {
                            String dayOfWeek = timeslot.getDayName(timeslot.getDay()); //
                            String periodDescription;

                            if (timeslot.getStart_time() != null && timeslot.getEnd_time() != null) { //
                                periodDescription = "第" + timeslot.getStart_time().toString() + "-" + timeslot.getEnd_time().toString() + "节"; //
                            } else {
                                periodDescription = "未知时段";
                            }

                            if (!weeklyTimetable.containsKey(dayOfWeek)) { //
                                System.err.println("警告: 从Timeslot获取的dayOfWeek '" + dayOfWeek + "' 未在预定义列表中。跳过课程 '" + courseName + "' 的此条目。");
                                continue;
                            }

                            TeacherController.TimetableEntry entry = new TeacherController.TimetableEntry(courseName, location, periodDescription, studentCount); //
                            weeklyTimetable.get(dayOfWeek).add(entry); //
                        } else {
                            System.err.println("警告: Timeslot not found for ID " + tsId + " in section " + section.getSec_id() + " (course: " + courseName + "). Skipping timetable entry for this specific timeslot.");
                        }
                    }
                    // Sort entries within each day by period/start time if needed for consistent display
                    for (List<TeacherController.TimetableEntry> entries : weeklyTimetable.values()) {
                        entries.sort(Comparator.comparing(TeacherController.TimetableEntry::getPeriod));
                    }


                } catch (IOException e) {
                    System.err.println("Error parsing time_slot_ids JSON: " + timeSlotIdsJson + " for section " + section.getSec_id() + " (course: " + courseName + ") - " + e.getMessage());
                    // Optionally create a single entry with "Error in time" or skip
                }
            }
            response.setTimetable(weeklyTimetable); //

        } catch (NumberFormatException e) {
            response.setErrorMessage("教师ID格式无效。"); //
            e.printStackTrace();
        } catch (SQLException e) {
            response.setErrorMessage("获取课表数据时发生数据库错误。"); //
            e.printStackTrace();
        } catch (Exception e) {
            response.setErrorMessage("获取课表数据时发生未知错误。"); //
            e.printStackTrace();
        }
        return response;
    }

    public String printCourseResult() {
        return "选课结果数据已准备好，前端可进行打印。"; //
    }
}
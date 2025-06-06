package org.example.backend.service;

import org.example.backend.controller.AdminController;
import org.example.backend.mapper.*;
import org.example.backend.model.Section;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class AdminService {
    public String setSelectionTime(AdminController.SelectionTime selectionTime) {
        String filePath = "selectionTime.txt";

        try {
            Path path = Paths.get(filePath); //打开文件
            if (!Files.exists(path)) { //不存在则创建，且文件先初始化为四行
                Files.createFile(path);
                Files.write(path, List.of("", "", "", ""));
            }

            List<String> lines = Files.readAllLines(path);

            if (selectionTime.getPrimaryStart()!=null && selectionTime.getPrimaryEnd()!=null) {
                if (selectionTime.getPrimaryStart().isAfter(selectionTime.getPrimaryEnd())){
                    return "初选开始时间不能晚于初选结束时间";
                }
                else { //如果初选时间有效
                    lines.set(0, selectionTime.getPrimaryStart().toString());
                    lines.set(1, selectionTime.getPrimaryEnd().toString());
                }
            }

            if (selectionTime.getSupplementaryStart()!=null && selectionTime.getSupplementaryEnd()!=null) {
                if (selectionTime.getSupplementaryStart().isAfter(selectionTime.getSupplementaryEnd())){
                    return "补选开始时间不能晚于补选结束时间";
                }
                else { //如果补选时间有效
                    lines.set(2, selectionTime.getSupplementaryStart().toString());
                    lines.set(3, selectionTime.getSupplementaryEnd().toString());
                }
            }
            Files.write(path, lines); //更新文件内容
            return "设置成功";
        } catch (IOException e){
            e.printStackTrace();
            return "设置失败：" + e.getMessage();
        }
    }

    public List<AdminController.Student_> searchStudent(String studentId, String studentName) {
        try {
            StudentMapper studentMapper = new StudentMapper();
            return studentMapper.getStudentWithPerson(studentId,studentName); //根据姓名、学号查询学生
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public List<AdminController.Section_> searchCourse(String courseYear, String courseSemester, String courseName, String courseInstructor) {
        try {
            SectionMapper sectionMapper = new SectionMapper();
            CourseMapper courseMapper = new CourseMapper();
            TeacherMapper teacherMapper = new TeacherMapper();
            TimeslotMapper timeslotMapper = new TimeslotMapper();
            ClassroomMapper classroomMapper = new ClassroomMapper();

            List<Section> sectionsByTitle = new ArrayList<>();
            List<Section> sectionsByInstructor = new ArrayList<>();
            List<Section> resultSections = new ArrayList<>();

            if (courseSemester != null) {
                courseSemester = (courseSemester.equals("春")) ? "Spring" : (courseSemester.equals("夏")) ? "Summer" : (courseSemester.equals("秋")) ? "Fall" : "Winter";
            }

            if (courseName!=null) { //根据课程名和上课年份、学期查找课程
                List<Integer> courseIds = courseMapper.getCourseIdsByTitle(courseName);
                System.out.println("courseIds: " + courseIds.size());
                for (Integer courseId : courseIds) {
                    System.out.println("courseId: " + courseId);
                    sectionsByTitle.addAll(sectionMapper.getSection(courseId.toString(),courseYear,courseSemester,null));
                }
            }
            if (courseInstructor!=null) { //根据课程教师和上课年份、学期查找课程
                List<Integer> teacherIds = teacherMapper.getTeacherIdByName(courseInstructor);

                for (Integer teacherId : teacherIds) {
                    sectionsByInstructor.addAll(sectionMapper.getSection(null,courseYear,courseSemester,teacherId.toString()));
                }
            }

            if (courseName!=null && courseInstructor!=null) { //如果课程名和教师均为查询条件，取交集
                resultSections = getIntersection(sectionsByInstructor,sectionsByTitle);
            } else if (courseName!=null) {
                resultSections = sectionsByTitle;
            } else if (courseInstructor!=null) {
                resultSections = sectionsByInstructor;
            } else { //如果课程名和教师均不是查询条件，仅凭借上课年份和学期进行查询
                resultSections = sectionMapper.getSection(null,courseYear,courseSemester,null);
            }

            List<AdminController.Section_> sections = new ArrayList<>();
            for (Section section : resultSections) { //利用查询结果获得sections
                String title,instuctor,credit,time = "",place;
                if (courseName!=null) {
                    title = courseName;
                } else {
                    title = courseMapper.getTitleByCourseId(section.getCourse_id());
                }
                if (courseInstructor!=null) {
                    instuctor = courseInstructor;
                } else {
                    instuctor = teacherMapper.getNameByTeacherId(section.getTeacher_id());
                }
                credit = courseMapper.getCreditByCourseId(section.getCourse_id());

                String time_slot = section.getTime_slot_id();
                String cleaned = time_slot.replaceAll("[\\[\\]\\s]", ""); // 移除 [] 和空格
                List<Integer> times =  Arrays.stream(cleaned.split(","))
                        .map(String::trim)
                        .map(Integer::parseInt)
                        .collect(Collectors.toList());
                int day = -1;
                for (int time_slot_id : times) {
                    if ((time_slot_id-1)/8+1 != day) {
                        if (day != -1) {
                            time += "节, ";
                        }
                        day = (time_slot_id-1)/8+1;
                        time += "周 " + day + " 第 ";
                    }
                    time += (time_slot_id%8 == 0) ? 8 : time_slot_id%8;
                    time += " ";
                }
                time += "节";

                place = classroomMapper.getPlace(section.getClassroom_id());

                AdminController.Section_ section_ = new AdminController.Section_();
                section_.setCourseId(String.valueOf(section.getCourse_id()));
                section_.setName(title);
                section_.setInstructor(instuctor);
                section_.setCredit(credit);
                section_.setTime(time);
                section_.setPlace(place);
                section_.setSectionId(String.valueOf(section.getSec_id()));
                section_.setCapacity(String.valueOf(section.getRemain_capacity()));
                sections.add(section_);
            }
            return sections;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String helpSelect(String studentId, String sectionId) {
        try {
            SectionMapper sectionMapper = new SectionMapper();
            TakesMapper takesMapper = new TakesMapper();

            String timeslotId = sectionMapper.getTimeSlotIdBySectionId(sectionId);

            String cleaned = timeslotId.replaceAll("[\\[\\]\\s]", ""); // 移除 [] 和空格
            List<Integer> times =  Arrays.stream(cleaned.split(","))
                    .map(String::trim)
                    .map(Integer::parseInt)
                    .collect(Collectors.toList());

            List<String> selectedSections;
            selectedSections = takesMapper.getSectionIdByStudentId(studentId);
            for (String selectedSectionId : selectedSections) { //需判断该课程是否已选过以及该时间段是否有课
                String selectedTimeslotId = sectionMapper.getTimeSlotIdBySectionId(selectedSectionId);

                String cleaned_ = selectedTimeslotId.replaceAll("[\\[\\]\\s]", ""); // 移除 [] 和空格
                List<Integer> selectedTimes =  Arrays.stream(cleaned_.split(","))
                        .map(String::trim)
                        .map(Integer::parseInt)
                        .collect(Collectors.toList());
                boolean is_overlapped = false;
                for (int time : selectedTimes) {
                    if (times.contains(time)) {
                        is_overlapped = true;
                        break;
                    }
                }

                boolean is_selected = sectionMapper.is_selected(sectionId, selectedSectionId);
                if (is_selected) { //课程已选择
                    return "该课程本身已在该学生课表中，请勿重复选择";
                }
                if (is_overlapped) { //已选课程时间和待选课程时间有一致的情况
                    boolean is_sameSemester = sectionMapper.isSameSemester(sectionId,selectedSectionId);
                    if (is_sameSemester) {
                        String selectedCourseName = sectionMapper.getCourseNameBySectionIdWithCourse(selectedSectionId);
                        return "课程时间冲突!\n冲突课程：" + selectedCourseName;
                    }
                }
            }

            String capacity_set_result = sectionMapper.setRemainCapacityBySectionId(sectionId);
            if (capacity_set_result.equals("修改失败")) {
                return "课程余量为0";
            } else{
                takesMapper.insertNewTakes(studentId,sectionId);
                return "选课成功";
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public <T> List<T> getIntersection(List<T> list1, List<T> list2) {
        Set<T> set = new HashSet<>(list1);
        set.retainAll(list2); // 取交集
        return new ArrayList<>(set);
    }
}

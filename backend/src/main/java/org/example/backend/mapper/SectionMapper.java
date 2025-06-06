package org.example.backend.mapper;

import org.example.backend.controller.AdminController;
import org.example.backend.model.DBInternet;
import org.example.backend.model.Section;

import java.sql.*;
import java.time.Year;
import java.util.ArrayList;
import java.util.List;

public class SectionMapper {
    private Connection connection;
    public SectionMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }
    public List<Section> selectAll() throws SQLException {
        try{
            String sql = "select * from section";
            PreparedStatement pStmt = connection.prepareStatement(sql);
            ResultSet rs = pStmt.executeQuery();
            List<Section> list = new java.util.ArrayList<>();
            while (rs.next()) {
                Section section = new Section();
                section.setCourse_id(rs.getInt("course_id"));
                section.setSec_id(rs.getInt("sec_id"));
                section.setSemester(rs.getString("semester"));
                section.setYear(Year.of(rs.getInt("year")));
                section.setClassroom_id(rs.getInt("classroom_id"));
                section.setTeacher_id(rs.getInt("teacher_id"));
                section.setTime_slot_id(rs.getString("time_slot_ids"));
                section.setRemain_capacity(rs.getInt("remain_capacity"));
                list.add(section);
            }
            return list;
        }catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }
    public Section selectSection(int id) {
        try{
            String sql = "select * from section where sec_id = ?";
            PreparedStatement pStmt= connection.prepareStatement(sql);
            pStmt.setInt(1, id);
            ResultSet rs = pStmt.executeQuery();
            if(rs.next()){
                Section section = new Section();
                section.setCourse_id(rs.getInt("course_id"));
                section.setSec_id(rs.getInt("sec_id"));
                section.setSemester(rs.getString("semester"));
                section.setYear(Year.of(rs.getInt("year")));
                section.setClassroom_id(rs.getInt("classroom_id"));
                section.setTeacher_id(rs.getInt("teacher_id"));
                section.setTime_slot_id(rs.getString("time_slot_ids"));
                section.setRemain_capacity(rs.getInt("remain_capacity"));
                return section;
            }
            return null;
        }catch (SQLException e){
            return null;
        }
    }
    public List<Section> getSection(String course_id,String year, String semester, String teacher_id) throws SQLException
    {
        String sql = "SELECT * FROM section WHERE 1=1 " ;
        try {
            if(course_id!= null) {
                sql += "AND course_id = ? ";
            }
            if(year != null) {
                sql += "AND year = ? ";
            }
            if(semester != null) {
                sql += "AND semester = ? ";
            }
            if(teacher_id != null) {
                sql += "AND teacher_id = ? ";
            }

            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            int index = 1;
            if(course_id != null) {
                preparedStatement.setString(index++, course_id);
            }
            if(year != null) {
                preparedStatement.setString(index++, year);
            }
            if(semester != null) {
                preparedStatement.setString(index++, semester);
            }
            if(teacher_id != null) {
                preparedStatement.setString(index++, teacher_id);
            }
            ResultSet resultSet = preparedStatement.executeQuery();

            List<Section> sections = new ArrayList<>();
            while (resultSet.next()) {
                Section section = new Section();
                section.setCourse_id(resultSet.getInt("course_id"));
                section.setSec_id(resultSet.getInt("sec_id"));
                section.setSemester(resultSet.getString("semester"));
                section.setYear(Year.of(resultSet.getInt("year")));
                section.setClassroom_id(resultSet.getInt("classroom_id"));
                section.setTeacher_id(resultSet.getInt("teacher_id"));
                section.setRemain_capacity(resultSet.getInt("remain_capacity"));
                section.setTime_slot_id(resultSet.getString("time_slot_ids"));
                sections.add(section);
            }
            resultSet.close();
            preparedStatement.close();
            return sections;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String getTimeSlotIdBySectionId(String sectionId) {
        String sql = "SELECT time_slot_ids FROM section WHERE sec_id = ? ";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, sectionId);
            ResultSet resultSet = preparedStatement.executeQuery();
            if(resultSet.next()) {
                String timeSlotId = resultSet.getString("time_slot_ids");
                resultSet.close();
                preparedStatement.close();
                return timeSlotId;
            } else {
                resultSet.close();
                preparedStatement.close();
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String setRemainCapacityBySectionId(String sectionId){
        String sql = "UPDATE section SET remain_capacity = remain_capacity-1" +
                " WHERE sec_id = ? AND remain_capacity > 0 ";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, sectionId);
            int rowsAffected = preparedStatement.executeUpdate();
            if (rowsAffected > 0) {
                preparedStatement.close();
                return "修改成功";
            } else {
                preparedStatement.close();
                return "修改失败";
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String getCourseNameBySectionIdWithCourse(String sectionId) {
        String sql = "SELECT title FROM course,section WHERE " +
                "course.course_id = section.course_id AND sec_id = ? ";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, sectionId);
            ResultSet resultSet = preparedStatement.executeQuery();
            if(resultSet.next()) {
                String courseName = resultSet.getString("title");
                resultSet.close();
                preparedStatement.close();
                return courseName;
            } else {
                resultSet.close();
                preparedStatement.close();
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    public boolean is_selected(String sectionId,String selectedSectionId){
        String sql = "SELECT count(DISTINCT course_id) FROM section WHERE sec_id = ? OR sec_id = ? ";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, sectionId);
            preparedStatement.setString(2, selectedSectionId);
            ResultSet resultSet = preparedStatement.executeQuery();
            if(resultSet.next()) {
                boolean isSelected = resultSet.getInt(1) == 1;
                resultSet.close();
                preparedStatement.close();
                return isSelected;
            } else {
                resultSet.close();
                preparedStatement.close();
                return false;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    public boolean isSameSemester(String sectionId,String selectedSectionId){
        String sql = "Select semester FROM section WHERE sec_id = ? ";
        String semester1 = null, semester2 = null;
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, sectionId);
            ResultSet resultSet = preparedStatement.executeQuery();
            if(resultSet.next()) {
                semester1 = resultSet.getString("semester");
            }
            preparedStatement.setString(1, selectedSectionId);
            resultSet = preparedStatement.executeQuery();
            if(resultSet.next()) {
                semester2 = resultSet.getString("semester");
            }
            resultSet.close();
            preparedStatement.close();
            System.out.println("semester1: " + semester1 + ", semester2: " + semester2);
            if(semester1.equals(semester2) || semester1.contains(semester2) || semester2.contains(semester1)) {
                return true;
            } else {
                return false;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    public Section getSectionBySectionId(String section_id) throws SQLException
    {
        String sql = "select * from section where sec_id = ?";
        try(PreparedStatement pstmt = connection.prepareStatement(sql)){
            pstmt.setString(1, section_id);
            try(ResultSet rs = pstmt.executeQuery()){
                if (rs.next()){
                    Section section = new Section();
                    section.setCourse_id(rs.getInt("course_id"));
                    section.setSec_id(rs.getInt("sec_id"));
                    section.setSemester(rs.getString("semester"));
                    section.setYear(Year.of(rs.getInt("year")));
                    section.setClassroom_id(rs.getInt("classroom_id"));
                    section.setTime_slot_id(rs.getString("time_slot_ids"));
                    section.setTeacher_id(rs.getInt("teacher_id"));
                    section.setRemain_capacity(rs.getInt("remain_capacity"));
                    return section;
                } else {
                    return null;
                }
            }
        } catch (SQLException e){
            e.printStackTrace();
            throw new RuntimeException("通过sec_id查询失败: " + e.getMessage());
        }
    }

    public List<Section> getSectionBySectionId(String section_id, String year, String semester) throws SQLException {
        // 基础SQL查询
        StringBuilder sql = new StringBuilder("SELECT * FROM section WHERE sec_id = ?");
        List<Object> params = new ArrayList<>();
        params.add(section_id);

        // 添加年份条件
        if (year != null && !year.isEmpty()) {
            sql.append(" AND year = ?");
            params.add(year);
        }

        // 添加学期条件
        if (semester != null && !semester.isEmpty()) {
            sql.append(" AND semester = ?");
            params.add(semester);
        }

        try (PreparedStatement pstmt = connection.prepareStatement(sql.toString())) {
            // 设置参数
            for (int i = 0; i < params.size(); i++) {
                pstmt.setObject(i + 1, params.get(i));
            }

            // 执行查询
            try (ResultSet rs = pstmt.executeQuery()) {
                List<Section> sections = new ArrayList<>();
                while (rs.next()) {
                    Section section = new Section();
                    section.setCourse_id(rs.getInt("course_id"));
                    section.setSec_id(rs.getInt("sec_id"));
                    section.setSemester(rs.getString("semester"));
                    section.setYear(Year.of(rs.getInt("year")));
                    section.setClassroom_id(rs.getInt("classroom_id"));
                    section.setTime_slot_id(rs.getString("time_slot_ids"));
                    section.setTeacher_id(rs.getInt("teacher_id"));
                    section.setRemain_capacity(rs.getInt("remain_capacity"));
                    sections.add(section);
                }
                return sections;
            }
        } catch (SQLException e) {
            throw new RuntimeException("通过sec_id和条件查询失败: " + e.getMessage());
        }
    }
    public List<Section> getSectionsByTeacherAndYearSemester(int teacherId, String year, String semester) throws SQLException {
        List<Section> sections = new ArrayList<>();

        StringBuilder sql = new StringBuilder("SELECT * FROM section WHERE teacher_id = ?");
        List<Object> params = new ArrayList<>();
        params.add(teacherId);

        if (year != null && !year.trim().isEmpty()) {
            sql.append(" AND year = ?");
            params.add(year);
        }
        if (semester != null && !semester.trim().isEmpty()) {
            sql.append(" AND semester = ?");
            params.add(semester);
        }

        try (PreparedStatement preparedStatement = connection.prepareStatement(sql.toString())) {
            for (int i = 0; i < params.size(); i++) {
                preparedStatement.setObject(i + 1, params.get(i));
            }

            try (ResultSet rs = preparedStatement.executeQuery()) {
                while (rs.next()) {
                    Section section = new Section();
                    section.setCourse_id(rs.getInt("course_id"));
                    section.setSec_id(rs.getInt("sec_id"));
                    section.setSemester(rs.getString("semester"));
                    section.setYear(Year.of(rs.getInt("year"))); // 从INT类型的year列创建Year对象
                    section.setClassroom_id(rs.getInt("classroom_id"));
                    section.setTime_slot_id(rs.getString("time_slot_ids"));
                    section.setTeacher_id(rs.getInt("teacher_id"));
                    section.setRemain_capacity(rs.getInt("remain_capacity"));
                    sections.add(section);
                }
            }
        } catch (NumberFormatException e) {
            // 处理年份可能不是有效整数字符串的情况
            e.printStackTrace();
            throw new IllegalArgumentException("年份参数必须是有效的整数字符串。", e);
        } catch (SQLException e) {
            e.printStackTrace();
            // 抛出更具体的异常或自定义异常
            throw new RuntimeException("为教师 " + teacherId + " 获取课程区段时出错: " + e.getMessage());
        }
        return sections;
    }
}

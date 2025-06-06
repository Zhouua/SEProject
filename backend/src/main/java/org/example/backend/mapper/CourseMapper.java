package org.example.backend.mapper;

import org.example.backend.model.Course;
import org.example.backend.model.DBInternet;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.Mapping;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class CourseMapper {
    private final Connection connection;
    public CourseMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }

    // 返回所有课程
    public List<Course> getAllCourses() {
        // 这里应该连接数据库，查询所有课程信息
        // 返回一个包含所有课程的列表
        List<Course> courses = new ArrayList<>();
        String sql = "SELECT * FROM course";
        try (Statement stmt = connection.createStatement(); ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                int courseId = rs.getInt("course_id");
                String courseTitle = rs.getString("title");
                String deptName = rs.getString("dept_name");
                String courseInfo = rs.getString("course_introduction");
                int credit = rs.getInt("credits");
                int capacity = rs.getInt("capacity");
                Course course = new Course(courseId, courseTitle, deptName, credit, courseInfo, capacity);
                courses.add(course);
            }
            rs.close();
            stmt.close();
            return courses;
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public List<Integer> getCourseIdsByTitle(String courseTitle) {
        String sql = "SELECT course_id FROM course WHERE title LIKE ?";
        try {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setString(1, "%" + courseTitle + "%");
            ResultSet rs = stmt.executeQuery();
            List<Integer> courseIds = new ArrayList<>();
            while (rs.next()) {
                int courseId = rs.getInt("course_id");
                courseIds.add(courseId);
            }
            rs.close();
            stmt.close();
            return courseIds;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String getTitleByCourseId(int courseId) {
        String sql = "SELECT title FROM course WHERE course_id = ?";
        try {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, courseId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                String title = rs.getString("title");
                rs.close();
                stmt.close();
                return title;
            } else {
                rs.close();
                stmt.close();
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String getCreditByCourseId(int courseId) {
        String sql = "SELECT credits FROM course WHERE course_id = ?";
        try {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, courseId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                String credits = rs.getString("credits");
                rs.close();
                stmt.close();
                return credits;
            } else {
                rs.close();
                stmt.close();
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public Course getCourseById(int courseId) {
        // 根据课程ID查询课程信息
        String sql = "SELECT * FROM course WHERE course_id = ?";
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setInt(1, courseId);
            ResultSet rs = pstmt.executeQuery();
            if (rs.next()) {
                String courseTitle = rs.getString("title");
                String deptName = rs.getString("dept_name");
                String courseInfo = rs.getString("course_introduction");
                int credit = rs.getInt("credits");
                int capacity = rs.getInt("capacity");
                return new Course(courseId, courseTitle, deptName, credit, courseInfo, capacity);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null; // 如果没有找到课程，返回null
    }
}

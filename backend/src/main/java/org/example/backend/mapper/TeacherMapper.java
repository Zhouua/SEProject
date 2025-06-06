package org.example.backend.mapper;

import org.example.backend.controller.AdminController;
import org.example.backend.model.DBInternet;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.security.PublicKey;
import java.sql.*;

public class TeacherMapper {
    private final Connection connection;
    public TeacherMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }

    public String getTeacherNameById(int user_id) {
        // 根据教师ID查询教师姓名
        // 这里应该连接数据库，查询教师信息
        // 返回一个包含教师姓名的字符串
        try {
            int person_id=0;
            {
                String sql = "SELECT personal_infor_id FROM user WHERE user_id = ?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, user_id);
                ResultSet rs = pStmt.executeQuery();
                if (rs.next()) { person_id = rs.getInt("personal_infor_id"); }
                else return null;
            }
            {
                String sql = "SELECT name FROM personal_information WHERE personal_infor_id = ?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, person_id);
                ResultSet rs = pStmt.executeQuery();
                if (rs.next()) {
                    return rs.getString("name");
                }
                else return null;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null; // 需要实现具体的查询逻辑
    }
    public List<Integer> getTeacherIdByName(String courseInstructor) {
        String sql = "SELECT teacher.user_id FROM teacher,user,personal_information " +
                "WHERE teacher.user_id = user.user_id AND user.personal_infor_id = personal_information.personal_infor_id " +
                "AND name LIKE ?";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, "%" + courseInstructor + "%");
            ResultSet resultSet = preparedStatement.executeQuery();
            List<Integer> teacherIds = new ArrayList<>();
            while (resultSet.next()) {
                int teacherId = resultSet.getInt("user_id");
                teacherIds.add(teacherId);
            }
            resultSet.close();
            preparedStatement.close();
            return teacherIds;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public String getNameByTeacherId(int teacherId) {
        String sql = "SELECT name FROM teacher,user,personal_information " +
                "WHERE teacher.user_id = user.user_id AND user.personal_infor_id = personal_information.personal_infor_id " +
                "AND teacher.user_id = ?";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, teacherId);
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                String name = resultSet.getString("name");
                resultSet.close();
                preparedStatement.close();
                return name;
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
}

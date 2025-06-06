package org.example.backend.mapper;

import org.example.backend.controller.AdminController;
import org.example.backend.model.DBInternet;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

// 对Student类进行数据库的CURD
public class StudentMapper {
    private Connection connection;
    public StudentMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }


    public boolean isStudentExist(int studentId) throws SQLException {
        String sql = "SELECT * FROM student WHERE user_id = ?";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, studentId);
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                return true;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
        return false;
    }

    public List<AdminController.Student_> getStudentWithPerson(String studentId, String studentName) throws SQLException
    {
        String sql = "SELECT student.user_id,name,dept_name FROM student,user,personal_information " +
                "WHERE student.user_id = user.user_id AND user.personal_infor_id = personal_information.personal_infor_id ";
        try {
            if(studentId != null) {
                sql += "AND student.user_id = ? ";
            }
            if(studentName != null) {
                sql += "AND name LIKE ? ";
            }
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            if(studentId != null) {
                preparedStatement.setInt(1,Integer.parseInt(studentId));
                if(studentName != null) {
                    preparedStatement.setString(2, "%" + studentName + "%");
                }
            }else{
                preparedStatement.setString(1, "%" + studentName + "%");
            }
            ResultSet resultSet = preparedStatement.executeQuery();

            List<AdminController.Student_> students = new ArrayList<>();
            while (resultSet.next()) {
                AdminController.Student_ student = new AdminController.Student_();
                student.setStudent_id(String.valueOf(resultSet.getInt("user_id")));
                student.setStudent_name(resultSet.getString("name"));
                student.setDept_name(resultSet.getString("dept_name"));
                students.add(student);
            }
            resultSet.close();
            preparedStatement.close();
            return students;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }
}

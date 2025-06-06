package org.example.backend.mapper;

import org.example.backend.model.Curriculum;
import org.example.backend.model.DBInternet;
import org.springframework.security.core.parameters.P;

import java.sql.*;

public class CurriculumMapper {
    // 这里应该有数据库操作方法
    // 用于对Curriculum类进行数据库的CURD操作

    private Connection connection;
    public CurriculumMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }


    public String insertCurriculum(Curriculum curriculum) {
        // 检查培养方案是否已存在
        String checkSql = "SELECT COUNT(*) FROM curriculum WHERE user_id = ? AND course_id = ?";
        try (PreparedStatement checkStatement = connection.prepareStatement(checkSql)) {
            checkStatement.setInt(1, curriculum.getUserId());
            checkStatement.setInt(2, curriculum.getCourseId());
            ResultSet resultSet = checkStatement.executeQuery();
            if (resultSet.next() && resultSet.getInt(1) > 0) {
                // 课程已存在培养方案
                return "添加成功";
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return "数据库检查失败：" + e.getMessage();
        }
        // 插入培养方案到数据库
        String sql = "INSERT INTO curriculum (user_id, course_id) VALUES (?, ?)";
        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
            preparedStatement.setInt(1, curriculum.getUserId());
            preparedStatement.setInt(2, curriculum.getCourseId());
            preparedStatement.executeUpdate();
            return "添加成功";
        } catch (SQLException e) {
            e.printStackTrace();
            return "插入失败：" + e.getMessage();
        }
    }

    public void updateCurriculum(Curriculum curriculum) {
        // 更新培养方案到数据库
    }

    public String deleteCurriculum(Curriculum curriculum) {
        // 根据ID删除培养方案
        // 检查培养方案是否已存在
        String checkSql = "SELECT COUNT(*) FROM curriculum WHERE user_id = ? AND course_id = ?";
        try (PreparedStatement checkStatement = connection.prepareStatement(checkSql)) {
            checkStatement.setInt(1, curriculum.getUserId());
            checkStatement.setInt(2, curriculum.getCourseId());
            ResultSet resultSet = checkStatement.executeQuery();
            if (resultSet.next() && resultSet.getInt(1) > 0) {
                // 课程在培养方案
                // 删除对应数据库
                String sql = "DELETE FROM curriculum WHERE user_id = ? AND course_id = ?";
                try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
                    preparedStatement.setInt(1, curriculum.getUserId());
                    preparedStatement.setInt(2, curriculum.getCourseId());
                    preparedStatement.executeUpdate();
                    return "删除成功";
                } catch (SQLException e) {
                    e.printStackTrace();
                    return "删除失败：" + e.getMessage();
                }
            } else {
                // 课程不在培养方案中
                return "删除成功";
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return "数据库检查失败：" + e.getMessage();
        }
    }

    public void getCurriculumById(int id) {
        // 根据ID查询培养方案
    }

    public boolean isCourseInCurriculum(Integer userId, Integer courseId) {
        // 检查课程是否在培养方案中
        String sql = "SELECT * FROM curriculum WHERE user_id = ? AND course_id = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
            preparedStatement.setInt(1, userId);
            preparedStatement.setInt(2, courseId);
            ResultSet resultSet = preparedStatement.executeQuery();
            // 如果查询结果不为空，说明课程在培养方案中
            return resultSet.next();
        } catch (SQLException e) {
            e.printStackTrace();
            return false; // 查询失败时返回false
        }
    }
}

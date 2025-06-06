package org.example.backend.mapper;

import org.example.backend.model.DBInternet;
import org.example.backend.model.Takes;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TakesMapper {
    private final Connection connection;
    private int next_takes_id;
    public TakesMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
        next_takes_id = 1;
        try{PreparedStatement pStmt = connection.prepareStatement("select max(takes_id) from takes");
            ResultSet rs =pStmt.executeQuery();
            while (rs.next()) { next_takes_id = rs.getInt(1) + 1; }
        }catch(SQLException e){
            e.printStackTrace();
        }
    }
    public List<Takes> selectAll() throws SQLException {
        List<Takes> list = new ArrayList<>();
        PreparedStatement pStmt = connection.prepareStatement("select * from takes");
        ResultSet rs = pStmt.executeQuery();
        while (rs.next()) {
            Takes takes = new Takes();
            takes.setTake_id(rs.getInt(1));
            takes.setStudent_id(rs.getInt(2));
            takes.setSec_id(rs.getInt(3));
            list.add(takes);
        }
        return list;
    }
    public boolean selectTakes(int student_id,int sec_id){
        try{
            String sql="select * from takes where student_id=? and sec_id=?";
            PreparedStatement pStmt = connection.prepareStatement(sql);
            pStmt.setInt(1, student_id);
            pStmt.setInt(2, sec_id);
            ResultSet rs = pStmt.executeQuery();
            if(rs.next()) return true;
        }catch (Exception e){
            return false;
        }
        return false;
    }

    public String insertTakes(int student_id, int sec_id){
        try {
            {
                String sql = "select remain_capacity from section where sec_id=?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, sec_id);
                ResultSet rs = pStmt.executeQuery();
                if(rs.next()){
                    if(rs.getInt("remain_capacity")<=0) return "选课失败，课程已满";
                }else return "选课失败，课程不存在";
            }
            {
                String sql ="select * from takes where student_id=? and sec_id=?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, student_id);
                pStmt.setInt(2, sec_id);
                ResultSet rs = pStmt.executeQuery();
                if(rs.next()){ return "选课失败，已选该课程"; }
            }
            {
                String sql ="update section set remain_capacity=remain_capacity-1 where sec_id=?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, sec_id);
                if(pStmt.executeUpdate()==0) return "选课失败";
            }
            {
                String sql = "insert into takes (takes_id, student_id, sec_id) values (?,?,?)";
                PreparedStatement pStmt =  connection.prepareStatement(sql);
                pStmt.setInt(1, next_takes_id++);
                pStmt.setInt(2, student_id);
                pStmt.setInt(3, sec_id);
                if(pStmt.executeUpdate()!=0)  return "选课成功";
            }
        }
        catch (Exception e){
            return "选课失败";
        }
        return "";
    }

    public  String deleteTakes(int student_id,int sec_id){
        try{
            {
                String sql ="update section set remain_capacity=remain_capacity+1 where sec_id=?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, sec_id);
                if(pStmt.executeUpdate()==0) return "选课失败";
            }
            {
                String sql = "delete from takes where student_id=? and sec_id=?";
                PreparedStatement pStmt = connection.prepareStatement(sql);
                pStmt.setInt(1, student_id);
                pStmt.setInt(2, sec_id);
                if (pStmt.executeUpdate() != 0) return "退课成功";
            }
        }catch (Exception e){
            return "退课失败";
        }
        return "";
    }
    public List<String> getSectionIdByStudentId(String studentId) {
        String sql = "select sec_id from takes where student_id = ?";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, studentId);
            ResultSet resultSet = preparedStatement.executeQuery();
            List<String> sectionIds = new ArrayList<>();
            while (resultSet.next()) {
                sectionIds.add(resultSet.getString("sec_id"));
            }
            resultSet.close();
            preparedStatement.close();
            return sectionIds;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    // 重载函数，根据年份和学期获取学生选课的section_id
    public List<String> getSectionIdByStudentId(String studentId, int year, List<String> semesters) {
        if (semesters == null || semesters.isEmpty()) {
            throw new IllegalArgumentException("学期列表不能为空");
        }

        // 构建IN子句的占位符
        StringBuilder placeholders = new StringBuilder();
        for (int i = 0; i < semesters.size(); i++) {
            placeholders.append("?");
            if (i < semesters.size() - 1) placeholders.append(",");
        }

        String sql = "SELECT t.sec_id " +
                "FROM takes t " +
                "JOIN section s ON t.sec_id = s.sec_id " +
                "WHERE t.student_id = ? AND s.year = ? " +
                "AND s.semester IN (" + placeholders + ")";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            int paramIndex = 1;
            stmt.setString(paramIndex++, studentId);
            stmt.setInt(paramIndex++, year);

            for (String sem : semesters) {
                stmt.setString(paramIndex++, sem);
            }

            try (ResultSet rs = stmt.executeQuery()) {
                List<String> sectionIds = new ArrayList<>();
                while (rs.next()) {
                    sectionIds.add(rs.getString("sec_id"));
                }
                return sectionIds;
            }
        } catch (SQLException e) {
            throw new RuntimeException("获取课程段ID失败: " + e.getMessage(), e);
        }
    }
    // 获取教师所教课程的section ID（原始来自用户提供文件的上下文，可能需要根据实际用途调整）
    // 此SQL语句意味着连接takes表和section表，以查找有学生选课且由该教师教授的课程。
    // 更直接查找教师所教课程的方式是仅查询section表。
    // TeacherService可能直接查询SectionMapper来获取教师的课程。
    public List<String> getSectionIdByTeacherId(String teacherId) {
        String sql = "SELECT DISTINCT s.sec_id FROM section s JOIN takes t ON s.sec_id = t.sec_id WHERE s.teacher_id = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
            // 假设 teacherId 是整数类型
            preparedStatement.setString(1, teacherId);
            try(ResultSet resultSet = preparedStatement.executeQuery()) {
                List<String> sectionIds = new ArrayList<>();
                while (resultSet.next()) {
                    sectionIds.add(resultSet.getString("sec_id"));
                }
                return sectionIds;
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }
    public String insertNewTakes(String studentId,String sectionId) {
        String sql = "insert into takes (student_id,sec_id) values(?,?)";
        try {
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, studentId);
            preparedStatement.setString(2, sectionId);
            preparedStatement.execute();
            preparedStatement.close();
            return "插入成功";
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }
    /**
     * 获取特定课程（section）的选课学生人数。
     * @param secId 课程区段ID (section ID)。
     * @return 学生人数。
     * @throws SQLException 如果发生数据库访问错误。
     */
    public int getStudentCountBySectionId(int secId) throws SQLException {
        String sql = "SELECT COUNT(DISTINCT student_id) AS student_count FROM takes WHERE sec_id = ?";
        try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
            preparedStatement.setInt(1, secId);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                if (resultSet.next()) {
                    return resultSet.getInt("student_count");
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
            // 抛出更具体的异常或自定义异常
            throw new RuntimeException("为课程区段 " + secId + " 获取学生人数时出错: " + e.getMessage());
        }
        return 0; // 如果sec_id有效且表存在，则不应发生
    }

}

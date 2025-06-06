package org.example.backend.mapper;
import org.example.backend.model.DBInternet;

import java.sql.*;

public class ClassroomMapper {
    private Connection connection;
    public ClassroomMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }

    public String getPlace(int classroomId) {
        String sql = "SELECT * FROM classroom WHERE classroom_id = ?";
        try {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, classroomId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                String place = rs.getString("campus") + " " + rs.getString("building")
                        + " " + rs.getString("room_number");
                rs.close();
                stmt.close();
                return place;
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
}

package org.example.backend.mapper;


import org.example.backend.model.DBInternet;
import org.example.backend.model.Timeslot;

import java.sql.*;
import java.time.LocalTime;

public class TimeslotMapper {
    private final Connection connection;
    public TimeslotMapper() throws SQLException {
        DBInternet internet = new DBInternet();
        this.connection = DriverManager.getConnection(internet.getUrl(), internet.getUser(), internet.getPassword());
    }

    public Timeslot getTimeslotById(int timeslotId) {
        Timeslot timeslot = null;
        try {
            String sql = "select * from time_slot where time_slot_id = ?";
            PreparedStatement pStmt = connection.prepareStatement(sql);
            pStmt.setInt(1, timeslotId);
            ResultSet rs = pStmt.executeQuery();
            if(rs.next()) {
                timeslot = new Timeslot();
                timeslot.setTime_slot_id(rs.getInt("time_slot_id"));
                timeslot.setDay(rs.getInt("day"));

                java.sql.Time sqlStartTime = rs.getTime("start_time");
                if (sqlStartTime != null) {
                    timeslot.setStart_time(sqlStartTime.toLocalTime());
                } else {
                    timeslot.setStart_time(null);
                }

                java.sql.Time sqlEndTime = rs.getTime("end_time");
                if (sqlEndTime != null) {
                    timeslot.setEnd_time(sqlEndTime.toLocalTime());
                } else {
                    timeslot.setEnd_time(null);
                }
                // Ensure rs and pStmt are closed in a finally block or use try-with-resources for them if not already.
                rs.close();
                pStmt.close();
                return timeslot;
            }
            // Ensure rs and pStmt are closed in a finally block or use try-with-resources
            if(rs!=null) rs.close();
            if(pStmt!=null) pStmt.close();
        } catch (SQLException sqlEx) {
            // Log the exception
            sqlEx.printStackTrace();
            throw new RuntimeException("Database error fetching timeslot with ID " + timeslotId, sqlEx);
        }
        return timeslot; // Returns null if not found
    }
    public String getTimeinStr(String timeSlotIds){System.out.println("timeSlotIds = " + timeSlotIds);
        String cleaned = timeSlotIds.replaceAll("[\\[\\]\\s]", "");
        String timeStr = "";
        String[] ids = cleaned.split(",");
        int lastTimeId=-1;
        LocalTime end_time = null;
        for (String id : ids) {
            int timeslotId = Integer.parseInt(id.trim());
            Timeslot timeslot = getTimeslotById(timeslotId);
            if(lastTimeId%4==0 ||lastTimeId+1<timeslotId) {
                if(lastTimeId!=-1) timeStr += end_time.toString()+",";
                switch(timeslot.getDay()) {
                    case 1: timeStr += "周一 "; break;
                    case 2: timeStr += "周二 "; break;
                    case 3: timeStr += "周三 "; break;
                    case 4: timeStr += "周四 "; break;
                    case 5: timeStr += "周五 "; break;
                    case 6: timeStr += "周六 "; break;
                    case 7: timeStr += "周日 "; break;
                }
                timeStr+=timeslot.getStart_time().toString() + "-" ;
            }
            lastTimeId = timeslotId;
            end_time= timeslot.getEnd_time();
        }
        timeStr+=end_time.toString();
        return timeStr.trim();
    }
    public String getTime(int timeslotId) {
        String sql = "SELECT * FROM time_slot WHERE time_slot_id = ?";
        try {
            PreparedStatement stmt = connection.prepareStatement(sql);
            stmt.setInt(1, timeslotId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                String time = "周" +rs.getString("day") + " " + rs.getString("start_time")
                        + "-" + rs.getString("end_time");
                rs.close();
                stmt.close();
                return time;
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

package org.example.backend.model;

public class DBInternet {
    String url;
    String user;
    String password;
    DBInternet(String url, String user, String password) {
        this.url = url;
        this.user = user;
        this.password = password;
    }
    public DBInternet() {
        // 默认
        this.url = "jdbc:mysql://localhost:3306/inforsystem";
        this.user = "root";
        this.password = "zjh750722828";
    }
    public String getUrl() {
        return url;
    }
    public String getUser() {
        return user;
    }
    public String getPassword() {
        return password;
    }
}

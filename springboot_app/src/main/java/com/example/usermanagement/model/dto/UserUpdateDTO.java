package com.example.usermanagement.model.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Size;

public class UserUpdateDTO {
    @Size(min = 1, max = 100, message = "用户名长度必须在1-100之间")
    private String name;
    
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @Size(min = 6, message = "密码长度不能少于6位")
    private String password;
    
    // getter方法
    public String getName() {
        return name;
    }
    
    public String getEmail() {
        return email;
    }
    
    public String getPassword() {
        return password;
    }
    
    // setter方法
    public void setName(String name) {
        this.name = name;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
}
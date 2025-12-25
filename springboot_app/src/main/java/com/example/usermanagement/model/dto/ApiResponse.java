package com.example.usermanagement.model.dto;

public class ApiResponse {
    private boolean success;
    private String message;
    private Object data;
    
    // 无参构造函数
    public ApiResponse() {
    }
    
    // 全参构造函数
    public ApiResponse(boolean success, String message, Object data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }
    
    // getter方法
    public boolean isSuccess() {
        return success;
    }
    
    public String getMessage() {
        return message;
    }
    
    public Object getData() {
        return data;
    }
    
    // setter方法
    public void setSuccess(boolean success) {
        this.success = success;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public void setData(Object data) {
        this.data = data;
    }
}
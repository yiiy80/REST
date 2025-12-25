package com.example.usermanagement.controller;

import com.example.usermanagement.model.dto.ApiResponse;
import com.example.usermanagement.model.dto.UserCreateDTO;
import com.example.usermanagement.model.dto.UserResponseDTO;
import com.example.usermanagement.model.dto.UserUpdateDTO;
import com.example.usermanagement.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 获取所有用户
    @GetMapping
    public ResponseEntity<List<UserResponseDTO>> getAllUsers() {
        List<UserResponseDTO> users = userService.getAllUsers();
        return new ResponseEntity<>(users, HttpStatus.OK);
    }

    // 根据ID获取用户
    @GetMapping("/{id}")
    public ResponseEntity<?> getUserById(@PathVariable Long id) {
        try {
            UserResponseDTO user = userService.getUserById(id);
            return new ResponseEntity<>(user, HttpStatus.OK);
        } catch (RuntimeException e) {
            // 使用构造函数而不是setter方法
            ApiResponse response = new ApiResponse(false, e.getMessage(), null);
            return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
        }
    }

    // 创建用户
    @PostMapping
    public ResponseEntity<?> createUser(@Valid @RequestBody UserCreateDTO userCreateDTO) {
        try {
            UserResponseDTO createdUser = userService.createUser(userCreateDTO);
            return new ResponseEntity<>(createdUser, HttpStatus.CREATED);
        } catch (RuntimeException e) {
            // 使用构造函数而不是setter方法
            ApiResponse response = new ApiResponse(false, e.getMessage(), null);
            return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
        }
    }

    // 更新用户
    @PutMapping("/{id}")
    public ResponseEntity<?> updateUser(@PathVariable Long id, @Valid @RequestBody UserUpdateDTO userUpdateDTO) {
        try {
            UserResponseDTO updatedUser = userService.updateUser(id, userUpdateDTO);
            return new ResponseEntity<>(updatedUser, HttpStatus.OK);
        } catch (RuntimeException e) {
            // 使用构造函数而不是setter方法
            ApiResponse response = new ApiResponse(false, e.getMessage(), null);
            
            if (e.getMessage().equals("用户不存在")) {
                return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
            }
            return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
        }
    }

    // 删除用户
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteUser(@PathVariable Long id) {
        try {
            UserResponseDTO deletedUser = userService.deleteUser(id);
            
            // 使用构造函数而不是setter方法
            ApiResponse response = new ApiResponse(true, "用户已删除", deletedUser);
            
            return new ResponseEntity<>(response, HttpStatus.OK);
        } catch (RuntimeException e) {
            // 使用构造函数而不是setter方法
            ApiResponse response = new ApiResponse(false, e.getMessage(), null);
            
            return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
        }
    }
}
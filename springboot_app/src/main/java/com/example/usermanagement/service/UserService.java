package com.example.usermanagement.service;

import com.example.usermanagement.model.User;
import com.example.usermanagement.model.dto.UserCreateDTO;
import com.example.usermanagement.model.dto.UserResponseDTO;
import com.example.usermanagement.model.dto.UserUpdateDTO;
import com.example.usermanagement.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {
    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<UserResponseDTO> getAllUsers() {
        return userRepository.findAll().stream()
                .map(this::convertToResponseDTO)
                .collect(Collectors.toList());
    }

    public UserResponseDTO getUserById(Long id) {
        return userRepository.findById(id)
                .map(this::convertToResponseDTO)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
    }

    public UserResponseDTO createUser(UserCreateDTO userCreateDTO) {
        // 检查邮箱是否已存在
        if (userRepository.existsByEmail(userCreateDTO.getEmail())) {
            throw new RuntimeException("邮箱已被注册");
        }

        User user = new User();
        user.setName(userCreateDTO.getName());
        user.setEmail(userCreateDTO.getEmail());
        user.setPassword(userCreateDTO.getPassword()); // 实际应用中应加密存储
        user.setCreatedAt(LocalDateTime.now());
        user.setUpdatedAt(LocalDateTime.now());

        User savedUser = userRepository.save(user);
        return convertToResponseDTO(savedUser);
    }

    public UserResponseDTO updateUser(Long id, UserUpdateDTO userUpdateDTO) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        // 检查邮箱是否被其他用户使用
        if (userUpdateDTO.getEmail() != null && 
            !userUpdateDTO.getEmail().equals(user.getEmail()) && 
            userRepository.existsByEmailAndIdNot(userUpdateDTO.getEmail(), id)) {
            throw new RuntimeException("邮箱已被注册");
        }

        // 更新字段
        if (userUpdateDTO.getName() != null) {
            user.setName(userUpdateDTO.getName());
        }
        if (userUpdateDTO.getEmail() != null) {
            user.setEmail(userUpdateDTO.getEmail());
        }
        if (userUpdateDTO.getPassword() != null) {
            user.setPassword(userUpdateDTO.getPassword()); // 实际应用中应加密存储
        }
        user.setUpdatedAt(LocalDateTime.now());

        User updatedUser = userRepository.save(user);
        return convertToResponseDTO(updatedUser);
    }

    public UserResponseDTO deleteUser(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("用户不存在"));

        userRepository.deleteById(id);
        return convertToResponseDTO(user);
    }

    private UserResponseDTO convertToResponseDTO(User user) {
        return new UserResponseDTO(
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getCreatedAt(),
                user.getUpdatedAt()
        );
    }
}
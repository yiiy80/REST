package com.example.usermanagement.controller;

import com.example.usermanagement.model.dto.ApiResponse;
import com.example.usermanagement.model.dto.UserCreateDTO;
import com.example.usermanagement.model.dto.UserResponseDTO;
import com.example.usermanagement.model.dto.UserUpdateDTO;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Arrays;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/fastapi")
public class FastAPIController {

    private final RestTemplate restTemplate;
    private static final String FASTAPI_BASE_URL = "http://localhost:8000/api/users";

    public FastAPIController() {
        this.restTemplate = new RestTemplate();
    }

    // 获取FastAPI中的所有用户
    @GetMapping("/users")
    public ResponseEntity<?> getAllUsersFromFastAPI() {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
            HttpEntity<String> entity = new HttpEntity<>("parameters", headers);

            ResponseEntity<UserResponseDTO[]> response = restTemplate.exchange(
                    FASTAPI_BASE_URL,
                    HttpMethod.GET,
                    entity,
                    UserResponseDTO[].class);

            return new ResponseEntity<>(response.getBody(), HttpStatus.OK);
        } catch (Exception e) {
            ApiResponse errorResponse = new ApiResponse(false, "调用FastAPI失败: " + e.getMessage(), null);
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    // 根据ID从FastAPI获取用户
    @GetMapping("/users/{id}")
    public ResponseEntity<?> getUserFromFastAPI(@PathVariable Long id) {
        try {
            String url = FASTAPI_BASE_URL + "/" + id;
            HttpHeaders headers = new HttpHeaders();
            headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
            HttpEntity<String> entity = new HttpEntity<>("parameters", headers);

            ResponseEntity<UserResponseDTO> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    entity,
                    UserResponseDTO.class);

            return new ResponseEntity<>(response.getBody(), HttpStatus.OK);
        } catch (Exception e) {
            ApiResponse errorResponse = new ApiResponse(false, "用户不存在或调用FastAPI失败: " + e.getMessage(), null);
            return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
        }
    }

    // 通过FastAPI创建用户
    @PostMapping("/users")
    public ResponseEntity<?> createUserInFastAPI(@RequestBody UserCreateDTO userCreateDTO) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<UserCreateDTO> entity = new HttpEntity<>(userCreateDTO, headers);

            ResponseEntity<UserResponseDTO> response = restTemplate.exchange(
                    FASTAPI_BASE_URL,
                    HttpMethod.POST,
                    entity,
                    UserResponseDTO.class);

            return new ResponseEntity<>(response.getBody(), HttpStatus.CREATED);
        } catch (Exception e) {
            ApiResponse errorResponse = new ApiResponse(false, "创建用户失败: " + e.getMessage(), null);
            return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
        }
    }
}
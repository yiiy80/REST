package com.example.usermanagement.repository;

import com.example.usermanagement.model.User;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Repository
public class UserRepository {
    private final Map<Long, User> userStore = new ConcurrentHashMap<>();
    private Long nextId = 1L;

    public List<User> findAll() {
        return new ArrayList<>(userStore.values());
    }

    public Optional<User> findById(Long id) {
        return Optional.ofNullable(userStore.get(id));
    }

    public User save(User user) {
        if (user.getId() == null) {
            user.setId(nextId++);
        }
        userStore.put(user.getId(), user);
        return user;
    }

    public void deleteById(Long id) {
        userStore.remove(id);
    }

    public boolean existsByEmail(String email) {
        return userStore.values().stream()
                .anyMatch(user -> user.getEmail().equals(email));
    }
    
    public boolean existsByEmailAndIdNot(String email, Long id) {
        return userStore.values().stream()
                .anyMatch(user -> user.getEmail().equals(email) && !user.getId().equals(id));
    }
}
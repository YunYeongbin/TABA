package com.example.taba.repository;

import com.example.taba.model.User;

import java.util.List;

public interface UserRepository {
    public List<User> selectUser(User user);
    public int insertUser(User user);
}

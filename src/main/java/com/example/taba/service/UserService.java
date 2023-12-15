package com.example.taba.service;

import com.example.taba.model.GithubUser;
import com.example.taba.model.User;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import com.example.taba.repository.UserRepository;

import java.util.List;

@Service
@AllArgsConstructor
public class UserService {
    private UserRepository userRepository;
    public List<User> findUsers(User user){
        return userRepository.selectUser(user);
    }
    public int joinUser(User user){
        return userRepository.insertUser(user);
    }
    public void saveOrUpdateUser(GithubUser gitHubUser) {
        User user = new User();
        user.setUsername(gitHubUser.getLogin());
        user.setEmail(gitHubUser.getEmail());
        user.setAvatarUrl(gitHubUser.getAvatar_url());

        userRepository.insertUser(user);
    }

}

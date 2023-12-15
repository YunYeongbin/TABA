package com.example.taba.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class GithubUser {
    private String login;
    private Long id;
    @JsonProperty("avatar_url")
    private String avatar_url;
    private String name;
    private String email;
    // toString 메소드는 디버깅을 위해 유용할 수 있음
    @Override
    public String toString() {
        return "GitHubUser{" +
                "login='" + login + '\'' +
                ", id=" + id +
                ", avatar_url='" + avatar_url + '\'' +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}

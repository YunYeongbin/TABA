package com.example.taba.model;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
    private Long user_id;
    private String username;
    private String email;
    private String avatarUrl;
}

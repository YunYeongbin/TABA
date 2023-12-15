package com.example.taba.model;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Join {
    private String job_title;
    private String skill_name;
    private int cnt;
    private int total_jobs;
    private String year;
    private String apply_date;
}

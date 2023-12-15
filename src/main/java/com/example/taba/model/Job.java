package com.example.taba.model;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Job {
    private String year;
    private String apply_date;
    private String job_title;

}

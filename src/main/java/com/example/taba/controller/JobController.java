package com.example.taba.controller;

import com.example.taba.model.Job;
import com.example.taba.service.JobService;
import jakarta.servlet.http.HttpSession;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

//@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@AllArgsConstructor // 생성자 주입을 위해 Lombok의 AllArgsConstructor 사용
public class JobController {

    private JobService jobService;

    @GetMapping("/job")
    public Map<String, Object> selectJobList(HttpSession session, Job job) {
        Map<String, Object> result = new HashMap<>();
        List<Job> jobList = jobService.findJobs(job);// Job 객체의 필요성 확인 필요
        result.put("jobList", jobList);
        return result;
    }

}

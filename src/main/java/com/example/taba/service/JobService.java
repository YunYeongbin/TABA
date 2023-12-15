package com.example.taba.service;

import com.example.taba.model.Job;
import com.example.taba.repository.JobRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor // 생성자 주입을 위해 Lombok의 AllArgsConstructor 사용
public class JobService {
    private JobRepository jobRepository;

    public List<Job> findJobs(Job job){
        return jobRepository.selectJob(job); // 메소드 명과 리파지토리 메소드 확인 필요
    }
}

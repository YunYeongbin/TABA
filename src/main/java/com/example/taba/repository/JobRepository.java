package com.example.taba.repository;

import com.example.taba.model.Job;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

public interface JobRepository{
    public List<Job> selectJob(Job job);
}

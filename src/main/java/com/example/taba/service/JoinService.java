package com.example.taba.service;

import com.example.taba.model.Join;
import com.example.taba.repository.JoinRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class JoinService {
    private JoinRepository joinRepository;
    public List<Join> findJoins(Join join){
        return joinRepository.selectJoin(join);
    }
}

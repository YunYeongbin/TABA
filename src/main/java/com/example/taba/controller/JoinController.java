package com.example.taba.controller;

import com.example.taba.model.Join;
import com.example.taba.service.JoinService;
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
@AllArgsConstructor
public class JoinController {
    private JoinService joinService;
    @GetMapping("/join")
    public Map<String,Object> selectJoinList(HttpSession session, Join join){
        Map<String,Object> result = new HashMap<>();
        List<Join> joinList = joinService.findJoins(join);
        result.put("joinList",joinList);
        return result;
    }
}

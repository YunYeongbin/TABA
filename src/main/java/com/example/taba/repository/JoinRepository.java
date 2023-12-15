package com.example.taba.repository;

import com.example.taba.model.Join;

import java.util.List;

public interface JoinRepository {
    public List<Join> selectJoin(Join join);
}

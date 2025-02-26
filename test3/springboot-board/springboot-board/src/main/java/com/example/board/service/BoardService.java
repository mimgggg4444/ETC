package com.example.board.service;

import com.example.board.model.Board;
import com.example.board.repository.BoardRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class BoardService {

    @Autowired
    private BoardRepository boardRepository;

    public List<Board> findAll() {
        return boardRepository.findAll();
    }

    public Board findById(Long id) {
        return boardRepository.findById(id).orElse(null);
    }

    public Board save(Board board) {
        board.setCreatedDate(LocalDateTime.now());
        return boardRepository.save(board);
    }

    public void deleteById(Long id) {
        boardRepository.deleteById(id);
    }
}

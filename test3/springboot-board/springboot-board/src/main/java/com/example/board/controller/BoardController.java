package com.example.board.controller;

import com.example.board.model.Board;
import com.example.board.service.BoardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/board")
public class BoardController {

    @Autowired
    private BoardService boardService;

    @GetMapping("/list")
    public String list(Model model) {
        model.addAttribute("boards", boardService.findAll());
        return "board/list";
    }

    @GetMapping("/detail/{id}")
    public String detail(@PathVariable Long id, Model model) {
        model.addAttribute("board", boardService.findById(id));
        return "board/detail";
    }

    @GetMapping("/form")
    public String form(Model model) {
        model.addAttribute("board", new Board());
        return "board/form";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute Board board) {
        boardService.save(board);
        return "redirect:/board/list";
    }

    @GetMapping("/delete/{id}")
    public String delete(@PathVariable Long id) {
        boardService.deleteById(id);
        return "redirect:/board/list";
    }
}

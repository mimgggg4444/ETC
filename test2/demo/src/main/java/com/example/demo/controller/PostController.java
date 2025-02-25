package com.example.demo.controller;

import com.example.demo.model.Post;
import com.example.demo.repository.PostRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
public class PostController {

  @Autowired
  private PostRepository postRepository;

  // 게시글 목록 페이지
  @GetMapping("/")
  public String listPosts(Model model) {
    List<Post> posts = postRepository.findAll();
    model.addAttribute("posts", posts);
    return "list";  // templates/list.html
  }

  // 새 글 작성 폼 페이지
  @GetMapping("/post/new")
  public String newPostForm(Model model) {
    model.addAttribute("post", new Post());
    return "new";  // templates/new.html
  }

  // 새 글 등록 처리
  @PostMapping("/post")
  public String createPost(@ModelAttribute Post post) {
    postRepository.save(post);
    return "redirect:/";  // 글 등록 후 목록으로 이동
  }
}

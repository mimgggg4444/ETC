
스피드런 post 기능 게시판 10분


src
 └─ main
     ├─ java
     │   └─ com.example.demo
     │       ├─ DemoApplication.java       // 메인 클래스
     │       ├─ model
     │       │    └─ Post.java              // 게시글 엔티티
     │       ├─ repository
     │       │    └─ PostRepository.java    // JPA 인터페이스
     │       └─ controller
     │            └─ PostController.java    // 컨트롤러
     └─ resources
         ├─ templates
         │    ├─ list.html                // 게시글 목록 페이지
         │    └─ new.html                 // 새 글 작성 페이지
         └─ application.properties       // 설정 파일

Dependencies
- Spring Web
- Thymeleaf
- Spring Data JPA
- H2 Database

# Maven 

jdk 17


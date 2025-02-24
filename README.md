# ETC


DTO (Data Transfer Object)
→ 데이터를 주고받을 때 사용하는 객체 (예: UserDTO → 이름, 나이 저장).

DAO (Data Access Object)
→ 데이터베이스와 연결해서 데이터를 저장하거나 가져오는 역할 (예: UserDAO → DB에 사용자 정보 저장).

Service
→ 비즈니스 로직을 처리하는 부분 (예: UserService → DAO를 이용해 사용자 정보 저장).

Controller
→ 사용자의 요청을 받아서 처리하는 역할 (예: UserController → Service 호출해서 사용자 생성).

XML
→ 설정 파일 (예: database.xml → DB 연결 정보).

JSON/YAML
→ 설정 정보 저장하는 파일 (예: settings.json, application.yml → 서버 설정, 환경 변수 등 저장).



---

✅ 설정 값을 저장하는 파일
→ key=value 형식으로 설정 정보를 저장하는데, 주로 Java 애플리케이션의 환경 설정에 사용됨.

Java 애플리케이션 환경 설정
Spring Boot에서 application.properties로 많이 사용
DB 연결, 서버 포트, API 키 등 설정 값 저장


Properties → 단순 key=value 형식, 가볍고 심플
JSON/YAML → 구조화된 데이터 저장 가능, 가독성 좋음


---
Controller → Service → DAO → DB 순서로 데이터가 이동하고,
DTO는 데이터를 담아 전달하는 역할


---

@RestController
@CrossOrigin(origins = "http://your-frontend-domain.com") // 실제 프론트엔드 도메인으로 변경
@RequestMapping("/api")
public class DataController {
    // REST API 메서드들
}






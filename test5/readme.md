아래는 해당 Spring Boot 애플리케이션이 구동되고 로그인 처리(데이터베이스 접근 포함)까지의 흐름과, 각 계층별로 어떤 디펜던시와 어노테이션이 사용되는지, 그리고 프로젝트의 파일 구성에 대해 정리한 내용입니다.


---

1. Spring Boot 구동 순서

엔트리 포인트 (Main Method)

메인 클래스
프로젝트의 실행은 main 패키지 내에 위치한 메인 클래스(예: EapSupportApplication.java)에서 시작됩니다.
이 클래스는 보통 @SpringBootApplication 어노테이션을 갖고 있으며, 내부에서 SpringApplication.run(Application.class, args)를 호출합니다.


자동 설정 및 컴포넌트 스캔

자동 설정 (Auto-Configuration)
@SpringBootApplication은 내부적으로 @EnableAutoConfiguration을 포함하여, 클래스패스에 있는 의존성(예, 웹, 보안, 데이터 등)에 따라 필요한 설정들을 자동으로 구성합니다.

컴포넌트 스캔
기본적으로 com.eap.eapsupport 패키지 하위에 있는 모든 컴포넌트(@Controller, @Service, @Repository 등)를 스캔하여 빈(Bean)으로 등록합니다.


환경 설정 및 초기화

설정 파일 로딩
resources 폴더에 있는 apjcatjon.properties (아마도 application.properties의 오타일 가능성이 있음)와 로그 설정 파일들(log4dvx.log4j2.properites, logvaxk-spring.xml)이 로드되어 애플리케이션의 전역 설정을 적용합니다.

서블릿 초기화 (WAR 배포 시)
sercletinitiallzer와 wevapplocation 클래스는 전통적 애플리케이션 서버(EAP 등)에 배포할 경우, SpringBootServletInitializer를 상속받아 서블릿 컨테이너에 애플리케이션을 등록하는 역할을 합니다.




---

2. MVC 패턴을 이용한 로그인 처리 로직

로그인 기능을 구현하는 과정은 전형적인 MVC(Model-View-Controller) 패턴을 따르며, 각 계층은 다음과 같이 구성됩니다.

Controller Layer

위치: common/xontroller_serivce 폴더 내

역할: 클라이언트의 로그인 요청을 받아 URL 매핑(@RequestMapping, @PostMapping 등)된 메서드를 통해 요청을 처리합니다.

사용 어노테이션: @Controller 또는 REST API일 경우 @RestController


Service Layer

위치: 보통 login 또는 관련 서비스 전용 패키지 내

역할: 컨트롤러로부터 전달받은 데이터를 기반으로 로그인에 필요한 비즈니스 로직을 수행하고, DAO를 호출하여 사용자 정보를 조회합니다.

사용 어노테이션: @Service


DAO (Data Access Object) Layer

위치: dao 폴더 내

역할: 데이터베이스(예: Couchbase 혹은 다른 DB)와의 인터랙션을 담당하여, 사용자 정보나 인증 데이터를 조회 및 수정합니다.

사용 어노테이션: @Repository


DTO (Data Transfer Object)

위치: dto 폴더 내

역할: 컨트롤러, 서비스, DAO 계층 간의 데이터 전달을 명확히 하기 위해 사용되는 객체들을 정의합니다.




---

3. 사용되는 디펜던시와 어노테이션

디펜던시 관리

빌드 도구: Maven(pom.xml) 또는 Gradle(build.gradle)을 통해 의존성이 관리됩니다.

주요 스타터 의존성:

spring-boot-starter-web
→ 웹 애플리케이션(MVC, 내장 톰캣) 기능 제공

spring-boot-starter-security
→ 로그인, 인증, 권한 관리 관련 기능 제공

spring-boot-starter-data-<DB타입>
→ 데이터 접근 라이브러리 (예를 들어, Couchbase를 사용한다면 spring-boot-starter-data-couchbase)

spring-boot-starter-mail
→ 메일 전송 기능 제공

그 외 로그 관련 라이브러리 (Log4j2 설정 파일 참고)



주요 어노테이션

@SpringBootApplication
→ 메인 클래스에 사용, 자동 설정, 컴포넌트 스캔, 설정 클래스를 포함

@Controller / @RestController
→ 웹 요청을 처리하는 컨트롤러에 사용

@Service
→ 비즈니스 로직을 담당하는 서비스 클래스에 사용

@Repository
→ 데이터베이스 접근 계층(DAO)에 사용

@Autowired
→ 의존성 주입을 위해 사용

@Configuration
→ 추가 설정이나 Bean 정의를 위한 클래스에 사용




---

4. 프로젝트 전체 파일 구조와 역할

main/java/com/eap/eapsupport

common 폴더

config: 전역 설정, Bean 구성 관련 클래스

xontroller_serivce: 컨트롤러와 서비스 관련 클래스 (로그인, 메인, 테스트 등)

dao: 데이터베이스 접근을 위한 DAO 클래스

dto: 데이터 전송 객체들

login: 로그인 처리에 관련된 로직

main: 애플리케이션의 메인 실행 클래스

scheduler: 스케줄링 작업 관련 클래스

sexurity: (아마도 security의 오타) 보안 설정 및 관련 기능

test_index: 테스트용 인덱스 혹은 기본 테스트 코드

rootxontriller: 최상위 컨트롤러(루트 URL 요청 처리)


추가 구성 클래스

rootsecurityconfig: Spring Security 설정 (예: @EnableWebSecurity 적용)

sercletinitiallzer / wevapplocation: 전통적 WAR 배포 시 서블릿 초기화를 위한 설정



resources 폴더

mappers: MyBatis 등의 매퍼 파일이나 XML 기반 데이터 매핑 파일

static: CSS, JavaScript, 이미지 등 정적 리소스

templates: 템플릿 엔진(예: Thymeleaf)용 뷰 파일

설정 파일들:

apjcatjon.properties (애플리케이션 기본 설정)

log4dvx.log4j2.properites, logvaxk-spring.xml (로그 설정)



webapp 폴더

웹 관련 추가 리소스 및 배포용 파일




---

5. EAP 쪽에서 사용 중인 기능 및 메일 보내기 기능

EAP 관련 구성

EAP(Enterprise Application Platform) 환경에서는 위에 언급한 서블릿 초기화(sercletinitiallzer)와 보안 설정(rootsecurityconfig)을 통해 전통적인 WAS 환경에 맞는 구성이 적용됩니다.

추가로, 스케줄러나 테스트 관련 기능(scheduler, test_index) 등이 포함되어 있으며, 엔터프라이즈급의 확장성을 고려한 구조로 설계되어 있습니다.


메일 보내기 기능

구현:
메일 전송은 spring-boot-starter-mail 의존성을 통해 구현됩니다. 전용 메일 서비스 클래스에서 JavaMailSender를 주입받아 메일 전송 로직을 처리합니다.

설정:
메일 서버 및 관련 설정은 apjcatjon.properties (또는 application.properties) 파일에 정의되어 있으며, 이를 통해 SMTP 서버 정보, 인증 정보 등을 로드합니다.




---

결론

전체적으로 이 프로젝트는 Spring Boot의 자동 설정과 컴포넌트 스캔 기능을 통해 필요한 빈들을 등록하고, MVC 패턴으로 로그인 처리 로직을 구성하고 있습니다.

부트 순서: 메인 클래스 실행 → 자동 설정 및 컴포넌트 스캔 → 환경 설정 파일 적용 → 서블릿 초기화(필요 시)

MVC 로그인 처리:
컨트롤러(요청 처리, URL 매핑) → 서비스(비즈니스 로직 수행) → DAO(데이터베이스 접근) → DTO(데이터 전달)

디펜던시 및 어노테이션: Maven/Gradle 의존성을 통해 spring-boot-starter-web, security, data-..., mail 등이 포함되며, 각 계층은 @Controller, @Service, @Repository, @Autowired 등으로 구성됩니다.

프로젝트 구성: Java 소스는 com.eap.eapsupport 하위에, 리소스 및 설정 파일은 resources 폴더에, 웹 관련 파일은 webapp에 위치하여 관리됩니다.

EAP 환경 및 메일 기능: EAP 서버 배포를 위한 서블릿 초기화 및 보안 설정과 함께, 메일 전송 기능도 별도의 서비스로 구현되어 있습니다.


이와 같이 구성되어 있는 프로젝트의 구조와 구동 방식, 그리고 각 계층에서 사용되는 의존성과 어노테이션을 이해하면, 로그인부터 데이터베이스 접근, 그리고 메일 전송 등 전체적인 애플리케이션의 흐름을 명확하게 파악할 수 있습니다.


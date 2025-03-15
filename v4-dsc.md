주요 함수들과 그 기능은 다음과 같습니다:

1. list_project_files(directory, extensions): 주어진 디렉토리 내에서 특정 확장자를 가진 파일들을 재귀적으로 검색하여 리스트로 반환합니다.


2. classify_file(file_path): 파일 경로를 분석하여 해당 파일이 DTO, DAO, Controller 등 어떤 유형에 속하는지 분류합니다.


3. analyze_java_file(file_path): Java 파일을 분석하여 패키지, 임포트, 클래스, 메서드, 주석 및 어노테이션 정보를 추출합니다.


4. analyze_xml_file(file_path): XML 파일을 분석하여 루트 태그 및 속성 정보를 추출합니다.


5. analyze_json_file(file_path): JSON 파일을 분석하여 데이터 구조를 로드하고 구조를 출력합니다.


6. analyze_yaml_file(file_path): YAML 파일을 분석하여 데이터 구조를 로드하고 구조를 출력합니다.


7. analyze_project(directory): 주어진 디렉토리 내의 파일들을 분석하여 각각의 파일 유형에 맞는 분석 결과를 리스트로 반환합니다.




아래는 이전에 소개한 모든 도구들을 실행 시 명령줄 인자가 아닌, 프로그램 실행 후 사용자에게 입력을 받아 처리하도록 변경한 코드 예제입니다.


---

1. Spring Boot Actuator 검사툴 (Python)

Spring Boot 서버 URL을 실행 시 입력받아 /actuator/health와 /actuator/info 엔드포인트를 검사하는 예제입니다.

import requests

def check_endpoint(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)

def main():
    base_url = input("Spring Boot 서버 URL을 입력하세요 (예: http://localhost:8080): ").strip()
    endpoints = {
        "Health": "/actuator/health",
        "Info": "/actuator/info"
    }
    
    print("\nSpring Boot 검사 시작...\n")
    for name, endpoint in endpoints.items():
        full_url = base_url.rstrip("/") + endpoint
        status, content = check_endpoint(full_url)
        if status is None:
            print(f"[{name}] 검사 실패: {content}")
        else:
            print(f"[{name}] HTTP 상태 코드: {status}")
            print("응답 내용:")
            print(content)
            print("-" * 40)

if __name__ == "__main__":
    main()

사용법:

1. 위 코드를 예를 들어 springboot_checker.py로 저장합니다.


2. 터미널에서 python springboot_checker.py 명령어로 실행한 후, 안내 메시지에 따라 서버 URL을 입력합니다.




---

2. Python 코드 검사툴 (문법 및 린트 검사)

실행 시 검사할 파일의 경로를 입력받아 문법 검사와 flake8을 이용한 코드 스타일 검사를 수행합니다.

import os
import subprocess

def check_syntax(file_path):
    """
    파일의 Python 구문 오류를 검사합니다.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, file_path, 'exec')
        print("문법 검사: 오류가 없습니다.")
        return True
    except SyntaxError as e:
        print("문법 검사: 오류가 발견되었습니다!")
        print(e)
        return False

def check_lint(file_path):
    """
    flake8를 이용해 코드 스타일(린트) 검사를 수행합니다.
    """
    try:
        result = subprocess.run(["flake8", file_path], capture_output=True, text=True)
        if result.returncode == 0:
            print("코드 스타일 검사: 문제가 없습니다.")
        else:
            print("코드 스타일 검사 결과:")
            print(result.stdout)
    except FileNotFoundError:
        print("flake8가 설치되어 있지 않습니다. 'pip install flake8'로 설치 후 다시 시도하세요.")

def main():
    file_path = input("검사할 Python 파일의 경로를 입력하세요: ").strip()
    if not os.path.exists(file_path):
        print("지정한 파일이 존재하지 않습니다.")
        return

    print("\nPython 코드 검사를 시작합니다...\n")
    if check_syntax(file_path):
        check_lint(file_path)

if __name__ == "__main__":
    main()

사용법:

1. 위 코드를 예를 들어 code_checker.py로 저장합니다.


2. 터미널에서 python code_checker.py를 실행하고, 안내 메시지에 따라 검사할 파일 경로를 입력합니다.




---

3. Python 코드 분석툴 (Radon 기반)

실행 시 분석할 Python 파일 경로를 입력받아 순환 복잡도, 유지보수성 지수, Halstead 지표를 계산합니다.

import os
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit

def analyze_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"파일 읽기 중 오류 발생: {e}")
        return

    print("=== Cyclomatic Complexity (순환 복잡도) 분석 ===")
    try:
        blocks = cc_visit(code)
        if blocks:
            for block in blocks:
                print(f"{block.name} (라인 {block.lineno}): 복잡도 = {block.complexity}")
        else:
            print("분석할 코드 블록이 없습니다.")
    except Exception as e:
        print(f"복잡도 분석 중 오류: {e}")

    print("\n=== Maintainability Index (유지보수성 지수) 분석 ===")
    try:
        mi_score = mi_visit(code, multi=True)
        print(f"유지보수성 지수: {mi_score:.2f}")
    except Exception as e:
        print(f"유지보수성 지수 분석 중 오류: {e}")

    print("\n=== Halstead Metrics (Halstead 지표) 분석 ===")
    try:
        h_metrics = h_visit(code)
        if h_metrics:
            for key, value in h_metrics.items():
                print(f"{key}: {value}")
        else:
            print("Halstead 지표를 계산할 수 없습니다.")
    except Exception as e:
        print(f"Halstead metrics 분석 중 오류: {e}")

def main():
    file_path = input("분석할 Python 파일의 경로를 입력하세요: ").strip()
    if not os.path.exists(file_path):
        print("지정한 파일이 존재하지 않습니다.")
        return
    
    print("\n코드 분석을 시작합니다...\n")
    analyze_code(file_path)

if __name__ == "__main__":
    main()

사용법:

1. 위 코드를 예를 들어 analysis_tool.py로 저장합니다.


2. 터미널에서 python analysis_tool.py를 실행하고, 안내 메시지에 따라 파일 경로를 입력합니다.




---

4. Spring Boot 프로젝트 분석툴 (MVC 및 전체 파일 분석)

실행 시 분석할 Spring Boot 프로젝트의 루트 디렉토리 경로를 입력받아, 하위 모든 Java 파일을 대상으로 클래스별 어노테이션 및 메서드(매핑 여부 포함) 정보를 분석합니다.

import os
import javalang

def analyze_file(file_path):
    """
    한 개의 Java 파일을 파싱하여 클래스별 어노테이션 및 메서드 정보를 반환합니다.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"[오류] 파일 읽기 실패 ({file_path}): {e}")
        return None

    try:
        tree = javalang.parse.parse(code)
    except Exception as e:
        print(f"[오류] 파싱 실패 ({file_path}): {e}")
        return None

    file_results = []
    
    # 파일 내의 타입 선언(클래스, 인터페이스, enum 등)을 탐색
    for _, node in tree.filter(javalang.tree.TypeDeclaration):
        if isinstance(node, javalang.tree.ClassDeclaration):
            class_info = {}
            class_info['class_name'] = node.name
            # 클래스에 사용된 어노테이션 추출 (예: @Controller, @Service 등)
            class_annotations = [annotation.name for annotation in node.annotations]
            class_info['annotations'] = class_annotations

            # 스프링 관련 주요 어노테이션에 따라 컴포넌트 타입 분류
            if 'RestController' in class_annotations or 'Controller' in class_annotations:
                component_type = 'Controller'
            elif 'Service' in class_annotations:
                component_type = 'Service'
            elif 'Repository' in class_annotations:
                component_type = 'Repository'
            else:
                component_type = 'Component'
            class_info['component_type'] = component_type

            # 클래스 내 메서드 분석
            methods_info = []
            for m in node.methods:
                method_info = {}
                method_info['name'] = m.name
                method_annotations = [ann.name for ann in m.annotations]
                method_info['annotations'] = method_annotations
                # 매핑 어노테이션 (Spring MVC 관련) 여부 판단
                mapping_annotations = [
                    'RequestMapping', 'GetMapping', 'PostMapping',
                    'PutMapping', 'DeleteMapping', 'PatchMapping'
                ]
                method_info['is_mapping'] = any(ann in mapping_annotations for ann in method_annotations)
                methods_info.append(method_info)
            class_info['methods'] = methods_info

            file_results.append(class_info)
    
    return file_results

def analyze_directory(root_dir):
    """
    지정한 루트 디렉토리 및 하위 디렉토리의 모든 Java 파일을 분석합니다.
    """
    results = {}
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(dirpath, file)
                analysis = analyze_file(file_path)
                if analysis:
                    results[file_path] = analysis
    return results

def main():
    print("Spring Boot 프로젝트 분석 도구")
    root_dir = input("분석할 Spring Boot 프로젝트의 루트 디렉토리 경로를 입력하세요: ").strip()
    if not os.path.exists(root_dir):
        print("지정한 디렉토리가 존재하지 않습니다.")
        return

    print("\n분석을 시작합니다...\n")
    results = analyze_directory(root_dir)

    # 분석 결과 출력
    for file_path, classes in results.items():
        print(f"파일: {file_path}")
        for class_info in classes:
            annotations = ', '.join(class_info['annotations']) if class_info['annotations'] else "없음"
            print(f"  클래스명: {class_info['class_name']}")
            print(f"  컴포넌트 타입: {class_info['component_type']} (어노테이션: {annotations})")
            if class_info['methods']:
                print("  메서드:")
                for m in class_info['methods']:
                    m_annotations = ', '.join(m['annotations']) if m['annotations'] else "없음"
                    mapping_note = " [매핑 메서드]" if m['is_mapping'] else ""
                    print(f"    - {m['name']} (어노테이션: {m_annotations}){mapping_note}")
            else:
                print("  메서드: 없음")
            print("  " + "-" * 40)
        print("=" * 60)

if __name__ == "__main__":
    main()

사용법:

1. 위 코드를 예를 들어 springboot_analysis_tool.py로 저장합니다.


2. 터미널에서 python springboot_analysis_tool.py를 실행하고, 안내 메시지에 따라 프로젝트 루트 디렉토리 경로를 입력합니다.




---

각 도구는 실행 시 사용자로부터 필요한 입력을 받고, 입력받은 경로나 URL을 바탕으로 분석을 수행합니다. 필요에 따라 기능이나 출력 형식을 추가로 확장할 수 있습니다.


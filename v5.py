import os
import re
import xml.etree.ElementTree as ET
import json
import yaml

def list_project_files(directory, extensions):
    """
    디렉터리에서 특정 확장자를 가진 파일을 검색합니다.
    :param directory: 프로젝트 루트 디렉토리
    :param extensions: 검색할 파일 확장자 목록
    :return: 확장자에 해당하는 모든 파일 경로 리스트
    """
    project_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                project_files.append(os.path.normpath(os.path.join(root, file)))
    return project_files

def classify_file(file_path):
    """
    파일 경로를 기반으로 DTO, DAO, Controller 등의 유형을 분류합니다.
    :param file_path: 분석할 파일의 경로
    :return: 파일의 유형 (DTO, DAO, Controller 등)
    """
    lower_path = file_path.lower()
    if "dto" in lower_path:
        return "DTO"
    elif "dao" in lower_path:
        return "DAO"
    elif "controller" in lower_path:
        return "Controller"
    elif "service" in lower_path:
        return "Service"
    elif file_path.endswith(".xml"):
        return "XML"
    elif file_path.endswith(".properties"):
        return "Properties"
    elif file_path.endswith(".json"):
        return "JSON"
    elif file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return "YAML"
    else:
        return "Other"

def clean_comment(comment):
    """
    주석 문자열에서 불필요한 공백, 탭, 개행 문자를 제거하고 정리합니다.
    :param comment: 원본 주석 문자열
    :return: 정리된 주석 문자열
    """
    # 주석 시작 기호 제거
    comment = re.sub(r'^\s*(/\*\*|\*/|/\*|\*|//)', '', comment, flags=re.MULTILINE)
    
    # 여러 줄 주석의 각 줄에서 앞에 있는 별표(*) 제거
    comment = re.sub(r'^\s*\*', '', comment, flags=re.MULTILINE)
    
    # 연속된 공백, 탭, 개행 문자를 하나의 공백으로 치환
    comment = re.sub(r'\s+', ' ', comment)
    
    return comment.strip()

def analyze_java_file(file_path):
    """
    Java 파일을 분석하여 패키지, 임포트, 클래스, 메서드, 주석 및 어노테이션 정보를 추출합니다.
    :param file_path: Java 파일 경로
    :return: 분석된 파일 정보 딕셔너리
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='euc-kr') as file:
                content = file.read()
        except UnicodeDecodeError:
            return {
                "file": os.path.normpath(file_path),
                "category": classify_file(file_path),
                "error": "파일 인코딩을 확인할 수 없습니다."
            }

    analysis = {
        "file": os.path.normpath(file_path),
        "category": classify_file(file_path),
        "package": None,
        "imports": [],
        "classes": [],
        "methods": [],
        "comments": [],
        "annotations": []
    }

    # 패키지 정보 추출
    package_match = re.search(r'package\s+([\w.]+);', content)
    if package_match:
        analysis["package"] = package_match.group(1)

    # 임포트 정보 추출
    analysis["imports"] = re.findall(r'import\s+([\w.]+);', content)
    
    # 클래스 정보 추출
    analysis["classes"] = re.findall(r'class\s+(\w+)', content)
    
    # 메서드 정보 추출 - 개선된 정규식 패턴
    method_pattern = r'(?:public|private|protected|static|\s)+[\w\<\>\[\]]+\s+(\w+)\s*\([^\)]*\)\s*(?:\{|throws)'
    analysis["methods"] = re.findall(method_pattern, content)
    
    # 주석 정보 추출 및 정리
    single_line_comments = re.findall(r'//.*', content)
    multi_line_comments = re.findall(r'/\*\*.*?\*/|/\*.*?\*/', content, re.DOTALL)
    
    comments = []
    for comment in single_line_comments + multi_line_comments:
        cleaned_comment = clean_comment(comment)
        if cleaned_comment:  # 빈 주석은 제외
            comments.append(cleaned_comment)
    
    analysis["comments"] = comments

    # 어노테이션 정보 추출 (중복 제거)
    annotations = re.findall(r'@\w+', content)
    analysis["annotations"] = list(set(annotations))  # 중복 제거

    return analysis

def analyze_xml_file(file_path):
    """
    XML 파일을 분석하여 루트 태그 및 간단한 정보를 추출합니다.
    :param file_path: XML 파일 경로
    :return: 분석된 파일 정보 딕셔너리
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return {
            "file": os.path.normpath(file_path),
            "category": classify_file(file_path),
            "root_tag": root.tag,
            "attributes": root.attrib
        }
    except Exception as e:
        return {
            "file": os.path.normpath(file_path),
            "category": "XML",
            "error": str(e)
        }

def analyze_json_file(file_path):
    """
    JSON 파일을 분석하여 데이터를 로드합니다.
    :param file_path: JSON 파일 경로
    :return: 분석된 파일 정보 딕셔너리
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 큰 데이터의 경우 구조만 추출
        if isinstance(data, dict):
            structure = {k: type(v).__name__ for k, v in data.items()}
        elif isinstance(data, list) and data:
            structure = f"List[{len(data)}]"
            if data and isinstance(data[0], dict):
                structure += f" Sample keys: {list(data[0].keys())[:5]}"
        else:
            structure = type(data).__name__
            
        return {
            "file": os.path.normpath(file_path),
            "category": classify_file(file_path),
            "structure": structure
        }
    except Exception as e:
        return {
            "file": os.path.normpath(file_path),
            "category": "JSON",
            "error": str(e)
        }

def analyze_yaml_file(file_path):
    """
    YAML 파일을 분석하여 데이터를 로드합니다.
    :param file_path: YAML 파일 경로
    :return: 분석된 파일 정보 딕셔너리
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        # 큰 데이터의 경우 구조만 추출
        if isinstance(data, dict):
            structure = {k: type(v).__name__ for k, v in data.items()}
        elif isinstance(data, list) and data:
            structure = f"List[{len(data)}]"
            if data and isinstance(data[0], dict):
                structure += f" Sample keys: {list(data[0].keys())[:5]}"
        else:
            structure = type(data).__name__
            
        return {
            "file": os.path.normpath(file_path),
            "category": classify_file(file_path),
            "structure": structure
        }
    except Exception as e:
        return {
            "file": os.path.normpath(file_path),
            "category": "YAML",
            "error": str(e)
        }

def analyze_project(directory):
    """
    프로젝트 내 특정 확장자를 가진 모든 파일을 분석합니다.
    :param directory: 분석할 프로젝트 디렉토리
    :return: 분석된 파일 정보 리스트
    """
    extensions = [".java", ".xml", ".json", ".yml", ".yaml"]
    project_files = list_project_files(directory, extensions)
    results = []
    for file_path in project_files:
        if file_path.endswith(".java"):
            results.append(analyze_java_file(file_path))
        elif file_path.endswith(".xml"):
            results.append(analyze_xml_file(file_path))
        elif file_path.endswith(".json"):
            results.append(analyze_json_file(file_path))
        elif file_path.endswith(".yml") or file_path.endswith(".yaml"):
            results.append(analyze_yaml_file(file_path))
        else:
            results.append({
                "file": os.path.normpath(file_path),
                "category": classify_file(file_path),
                "info": "지원하지 않는 파일 형식"
            })
    return results

def main():
    """
    사용자로부터 프로젝트 경로를 입력받아 분석을 수행하고 결과를 출력합니다.
    """
    project_directory = input("분석할 프로젝트 디렉토리를 입력하세요: ").strip()
    if not os.path.isdir(project_directory):
        print("유효하지 않은 디렉토리입니다.")
        return

    results = analyze_project(project_directory)
    # 분석 결과를 JSON 포맷으로 출력합니다.
    print(json.dumps(results, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
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
                project_files.append(os.path.join(root, file))
    return project_files

def classify_file(file_path):
    """
    파일 경로를 기반으로 DTO, DAO, Controller 등의 유형을 분류합니다.
    :param file_path: 분석할 파일의 경로
    :return: 파일의 유형 (DTO, DAO, Controller 등)
    """
    if "dto" in file_path.lower():
        return "DTO"
    elif "dao" in file_path.lower():
        return "DAO"
    elif "controller" in file_path.lower():
        return "Controller"
    elif "service" in file_path.lower():
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

def analyze_java_file(file_path):
    """
    Java 파일을 분석하여 패키지, 임포트, 클래스, 메서드, 주석 정보를 추출합니다.
    :param file_path: Java 파일 경로
    :return: 분석된 파일 정보 딕셔너리
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    analysis = {
        "file": file_path,
        "category": classify_file(file_path),
        "package": None,
        "imports": [],
        "classes": [],
        "methods": [],
        "comments": []
    }
    
    package_match = re.search(r'package\s+([\w.]+);', content)
    if package_match:
        analysis["package"] = package_match.group(1)
    
    analysis["imports"] = re.findall(r'import\s+([\w.]+);', content)
    
    class_matches = re.findall(r'class\s+(\w+)', content)
    analysis["classes"] = class_matches
    
    method_matches = re.findall(r'(?:public|private|protected|static|\s)\s+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{', content)
    analysis["methods"] = method_matches
    
    comment_matches = re.findall(r'//.*|/\*\*.*?\*/', content, re.DOTALL)
    analysis["comments"] = [comment.strip() for comment in comment_matches]
    
    return analysis

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
    
    return results

def main():
    """
    사용자로부터 프로젝트 경로를 입력받아 분석을 수행하고 결과를 출력합니다.
    """
    project_directory = input("분석할 프로젝트 디렉토리를 입력하세요: ")
    results = analyze_project(project_directory)
    
    for result in results:
        print(f"\n파일: {result['file']}")
        print(f"분류: {result['category']}")
        for key, value in result.items():
            if key not in ["file", "category"]:
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()

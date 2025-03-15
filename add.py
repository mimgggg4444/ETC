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
        normalized_path = os.path.normpath(file_path).replace("/", "\\")  # 윈도우 경로 형태로 변환  
        
        if file_path.endswith(".java"):  
            analysis = analyze_java_file(file_path)  
        elif file_path.endswith(".xml"):  
            analysis = analyze_xml_file(file_path)  
        elif file_path.endswith(".json"):  
            analysis = analyze_json_file(file_path)  
        elif file_path.endswith(".yml") or file_path.endswith(".yaml"):  
            analysis = analyze_yaml_file(file_path)  
        else:  
            analysis = {  
                "file": normalized_path,  
                "category": classify_file(file_path),  
                "info": "지원하지 않는 파일 형식"  
            }  
        
        # 경로를 수정하여 저장  
        analysis["file"] = normalized_path  
        results.append(analysis)  

    return results
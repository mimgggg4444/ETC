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
    for path, node in tree.filter(javalang.tree.TypeDeclaration):
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
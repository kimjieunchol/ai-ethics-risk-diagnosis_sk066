import os
import json
from datetime import datetime
from typing import Dict, Any

def ensure_directory(directory: str):
    """디렉토리가 없으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✅ 디렉토리 생성: {directory}")

def save_json(data: Dict, filepath: str):
    """JSON 파일로 저장"""
    ensure_directory(os.path.dirname(filepath))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON 저장: {filepath}")

def load_json(filepath: str) -> Dict:
    """JSON 파일 로드"""
    if not os.path.exists(filepath):
        print(f"⚠️  파일 없음: {filepath}")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_report(content: str, filename: str, output_dir: str = "outputs/reports"):
    """보고서를 마크다운 파일로 저장"""
    ensure_directory(output_dir)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 보고서 저장: {filepath}")
    return filepath

def get_timestamp() -> str:
    """현재 시간 문자열 반환"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def print_progress(message: str, level: int = 0):
    """진행 상황 출력"""
    indent = "  " * level
    print(f"{indent}{message}")

def format_score_display(score: float, max_score: float = 5.0) -> str:
    """점수를 시각적으로 표시"""
    filled = int((score / max_score) * 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"{bar} {score:.1f}/{max_score}"

def validate_service_names(services: list, max_count: int = 3) -> bool:
    """서비스 이름 유효성 검사"""
    if not services:
        print("❌ 서비스가 지정되지 않았습니다.")
        return False
    
    if len(services) > max_count:
        print(f"❌ 최대 {max_count}개 서비스만 분석 가능합니다.")
        return False
    
    for service in services:
        if not service or not service.strip():
            print("❌ 유효하지 않은 서비스명이 있습니다.")
            return False
    
    return True

def validate_guidelines(guidelines: list, supported: list) -> bool:
    """가이드라인 유효성 검사"""
    if not guidelines:
        print("❌ 가이드라인이 지정되지 않았습니다.")
        return False
    
    for guideline in guidelines:
        if guideline not in supported:
            print(f"❌ 지원하지 않는 가이드라인: {guideline}")
            print(f"   지원 가이드라인: {', '.join(supported)}")
            return False
    
    return True

def create_state_snapshot(state: Dict) -> Dict:
    """State의 현재 상태 스냅샷 생성"""
    snapshot = {
        "timestamp": get_timestamp(),
        "services": state.get("service_names", []),
        "current_service": state.get("current_service", None),
        "completed_analyses": len(state.get("service_analysis", {})),
        "completed_assessments": len(state.get("risk_assessment", {}))
    }
    return snapshot

def print_section_header(title: str):
    """섹션 헤더 출력"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_section_footer():
    """섹션 푸터 출력"""
    print(f"\n{'='*60}\n")
"""
출력 포맷팅 유틸리티
"""
import json
import os
from datetime import datetime
from typing import Dict
from src.config import OUTPUT_PATHS


def save_json(data: Dict, filename: str, output_type: str = "evaluations"):
    """
    JSON 형식으로 데이터 저장
    
    Args:
        data: 저장할 데이터
        filename: 파일명
        output_type: 출력 타입 (evaluations, reports, visualizations)
    """
    output_dir = OUTPUT_PATHS[output_type]
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved: {filepath}")
    return filepath


def save_markdown(content: str, filename: str):
    """
    Markdown 형식으로 보고서 저장
    
    Args:
        content: Markdown 내용
        filename: 파일명
    """
    output_dir = OUTPUT_PATHS["reports"]
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📄 Saved: {filepath}")
    return filepath


def generate_filename(service_name: str, extension: str = "json") -> str:
    """
    타임스탬프 포함 파일명 생성
    
    Args:
        service_name: 서비스명
        extension: 파일 확장자
    
    Returns:
        파일명
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = service_name.replace(" ", "_").lower()
    return f"{clean_name}_{timestamp}.{extension}"
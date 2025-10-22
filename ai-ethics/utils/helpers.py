import json
from typing import Any, Dict

def save_json(data: Any, filepath: str):
    """JSON 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath: str) -> Dict:
    """JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_section(title: str, char: str = "=", width: int = 60):
    """섹션 헤더 출력"""
    print(f"\n{char*width}")
    print(f"  {title}")
    print(f"{char*width}\n")

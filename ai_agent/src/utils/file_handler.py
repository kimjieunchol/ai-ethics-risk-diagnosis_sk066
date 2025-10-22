import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class FileHandler:
    """파일 입출력 유틸리티"""
    
    @staticmethod
    def save_json(data: Dict, filepath: str):
        """JSON 저장"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def load_json(filepath: str) -> Dict:
        """JSON 로드"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_report(content: str, service_name: str, output_dir: str = "outputs/reports"):
        """보고서 저장"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{service_name.replace(' ', '_')}_{timestamp}.md"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    @staticmethod
    def save_state(state: Dict[str, Any], output_dir: str = "state"):
        """State 저장"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"state_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        # JSON 직렬화 가능한 형태로 변환
        serializable_state = {}
        for key, value in state.items():
            try:
                json.dumps(value)
                serializable_state[key] = value
            except (TypeError, ValueError):
                serializable_state[key] = str(value)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_state, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
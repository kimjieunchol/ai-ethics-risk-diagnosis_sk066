from typing import TypedDict, List, Dict, Optional, Annotated
from langchain_core.messages import BaseMessage
import operator

class EthicsAssessmentState(TypedDict):
    """AI 윤리성 리스크 진단 State"""
    
    # 입력 정보
    service_names: List[str]  # 분석 대상 AI 서비스 이름 (최대 3개)
    guidelines: List[str]  # 사용할 윤리 가이드라인 (EU AI Act, UNESCO, OECD)
    
    # 서비스 분석 결과
    service_analysis: Dict[str, Dict]  # 각 서비스별 분석 결과
    # {
    #   "ChatGPT": {
    #     "overview": "...",
    #     "key_features": [...],
    #     "target_users": "...",
    #     "data_usage": "..."
    #   }
    # }
    
    # 윤리 리스크 진단 결과
    risk_assessment: Dict[str, Dict]  # 각 서비스별 리스크 평가
    # {
    #   "ChatGPT": {
    #     "bias": {"score": 3, "description": "...", "evidence": [...]},
    #     "privacy": {"score": 4, "description": "...", "evidence": [...]},
    #     "transparency": {"score": 2, "description": "...", "evidence": [...]},
    #     "accountability": {"score": 3, "description": "...", "evidence": [...]}
    #   }
    # }
    
    # 개선안
    improvement_suggestions: Dict[str, List[Dict]]  # 각 서비스별 개선안
    # {
    #   "ChatGPT": [
    #     {"risk_area": "transparency", "suggestion": "...", "priority": "high"},
    #     ...
    #   ]
    # }
    
    # 최종 보고서
    final_report: Optional[str]  # Markdown 형식 최종 보고서
    
    # 참고 문헌
    references: Annotated[List[Dict], operator.add]  # 수집된 참고 자료
    # [{"title": "...", "url": "...", "source": "web/rag"}]
    
    # 메시지 (디버깅용)
    messages: Annotated[List[BaseMessage], operator.add]
    
    # 현재 처리 중인 서비스
    current_service: Optional[str]
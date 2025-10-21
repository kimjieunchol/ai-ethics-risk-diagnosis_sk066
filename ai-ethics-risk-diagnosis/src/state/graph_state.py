"""
LangGraph State 정의
"""
from typing import TypedDict, List, Dict, Optional, Annotated
from langgraph.graph.message import add_messages


class EthicsRiskState(TypedDict):
    """AI 윤리성 리스크 진단 State"""
    
    # 입력 정보
    target_service: str  # 분석 대상 AI 서비스명
    
    # 메시지 히스토리
    messages: Annotated[List, add_messages]
    
    # 1. 서비스 분석 결과
    service_overview: Optional[Dict]  # 서비스 개요
    # {
    #     "name": "서비스명",
    #     "description": "서비스 설명",
    #     "key_features": ["기능1", "기능2", ...],
    #     "target_users": "대상 사용자",
    #     "data_usage": "데이터 사용 방식"
    # }
    
    # 2. 윤리 리스크 평가 결과
    ethics_evaluation: Optional[Dict]  # 윤리성 평가
    # {
    #     "bias": {
    #         "score": 7.5,
    #         "risk_level": "low",
    #         "findings": ["발견사항1", "발견사항2"],
    #         "evidence": ["근거1", "근거2"]
    #     },
    #     "privacy": {...},
    #     "transparency": {...},
    #     "accountability": {...},
    #     "safety": {...},
    #     "overall_score": 7.2,
    #     "overall_risk_level": "low"
    # }
    
    # 3. 개선안 제안 결과
    improvement_proposals: Optional[List[Dict]]  # 개선 제안
    # [
    #     {
    #         "criterion": "bias",
    #         "priority": "high",
    #         "recommendation": "개선 권고사항",
    #         "implementation": "구체적 실행 방안",
    #         "expected_impact": "기대 효과"
    #     },
    #     ...
    # ]
    
    # 4. 최종 보고서
    final_report: Optional[str]  # Markdown 형식 보고서
    
    # 5. 참조 문서
    references: Optional[List[Dict]]  # 참조한 문서들
    # [
    #     {
    #         "source": "EU AI Act",
    #         "section": "Article 5",
    #         "content": "내용"
    #     },
    #     ...
    # ]
    
    # 워크플로우 제어
    current_step: str  # 현재 진행 단계
    errors: List[str]  # 에러 로그
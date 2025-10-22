from typing import TypedDict, List, Dict, Annotated
import operator


class AIEthicsState(TypedDict):
    """AI 윤리 진단 상태"""
    
    # 입력 정보
    service_name: str
    service_description: str
    service_features: List[str]
    target_users: str
    data_types: List[str]
    
    # 서비스 분석
    service_analysis: Dict
    
    # 윤리 리스크 평가
    bias_risk: Dict
    privacy_risk: Dict
    transparency_risk: Dict
    fairness_risk: Dict
    safety_risk: Dict
    accountability_risk: Dict
    
    # 검색된 가이드라인
    retrieved_guidelines: Annotated[List[Dict], operator.add]
    
    # 종합 결과
    overall_risk_score: float
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    high_risk_areas: List[str]
    
    # 개선 방안
    recommendations: List[Dict]
    priority_actions: List[str]
    
    # 참고 문헌
    references: List[str]
    
    # 최종 보고서
    final_report: str
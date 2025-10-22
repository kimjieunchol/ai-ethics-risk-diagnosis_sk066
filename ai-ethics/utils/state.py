from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class AssessmentState:
    """평가 상태 관리"""
    
    # 입력
    service_names: List[str] = field(default_factory=list)
    
    # 서비스 분석 결과
    service_analyses: Dict[str, Dict] = field(default_factory=dict)
    
    # 리스크 평가 결과
    risk_assessments: Dict[str, Dict] = field(default_factory=dict)
    
    # 개선안
    improvement_suggestions: Dict[str, List[Dict]] = field(default_factory=dict)
    
    # 비교 분석
    comparison_analysis: str = ""
    
    # 최종 보고서
    final_report: str = ""
    
    # 메타데이터
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_service_analysis(self, service_name: str, analysis: Dict):
        """서비스 분석 결과 추가"""
        self.service_analyses[service_name] = analysis
    
    def add_risk_assessment(self, service_name: str, assessment: Dict):
        """리스크 평가 추가"""
        self.risk_assessments[service_name] = assessment
    
    def add_improvements(self, service_name: str, improvements: List[Dict]):
        """개선안 추가"""
        self.improvement_suggestions[service_name] = improvements
    
    def get_summary(self) -> Dict:
        """상태 요약"""
        return {
            "services_count": len(self.service_names),
            "services": self.service_names,
            "analyses_completed": len(self.service_analyses),
            "assessments_completed": len(self.risk_assessments),
            "improvements_generated": len(self.improvement_suggestions),
            "comparison_done": bool(self.comparison_analysis),
            "report_generated": bool(self.final_report)
        }


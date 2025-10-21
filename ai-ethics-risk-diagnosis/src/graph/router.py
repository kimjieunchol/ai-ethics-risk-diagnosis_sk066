"""
조건부 라우팅 로직
"""
from src.state import EthicsRiskState


def should_continue(state: EthicsRiskState) -> str:
    """
    다음 단계로 진행할지 결정
    
    Args:
        state: 현재 상태
    
    Returns:
        다음 노드 이름 또는 "end"
    """
    current_step = state.get("current_step", "")
    errors = state.get("errors", [])
    
    # 에러가 있으면 종료
    if errors:
        print(f"\n⚠️ Workflow stopped due to errors: {errors[-1]}")
        return "end"
    
    # 단계별 라우팅
    if current_step == "service_analysis_completed":
        return "ethics_evaluation"
    
    elif current_step == "ethics_evaluation_completed":
        return "improvement_proposals"
    
    elif current_step == "improvement_proposals_completed":
        return "report_generation"
    
    elif current_step == "report_completed":
        return "end"
    
    # 실패한 경우
    elif "failed" in current_step:
        return "end"
    
    # 기본값
    return "end"


def check_service_analysis(state: EthicsRiskState) -> str:
    """서비스 분석 후 다음 단계 결정"""
    return should_continue(state)


def check_ethics_evaluation(state: EthicsRiskState) -> str:
    """윤리 평가 후 다음 단계 결정"""
    return should_continue(state)


def check_improvement_proposals(state: EthicsRiskState) -> str:
    """개선안 제안 후 다음 단계 결정"""
    return should_continue(state)
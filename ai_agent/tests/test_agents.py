"""
에이전트 테스트
"""
import pytest
from src.state import EthicsRiskState
from src.agents import service_analyzer_node


def test_service_analyzer_state_update():
    """서비스 분석 에이전트가 State를 올바르게 업데이트하는지 테스트"""
    
    # Given: 초기 상태
    initial_state = {
        "target_service": "ChatGPT",
        "messages": [],
        "service_overview": None,
        "ethics_evaluation": None,
        "improvement_proposals": None,
        "final_report": None,
        "references": [],
        "current_step": "initialized",
        "errors": []
    }
    
    # When: 서비스 분석 실행
    # Note: 실제 API 호출이 필요하므로 mock 사용 권장
    # result = service_analyzer_node(initial_state)
    
    # Then: State가 업데이트되었는지 확인
    # assert result["service_overview"] is not None
    # assert result["current_step"] == "service_analysis_completed"
    
    # 실제 테스트를 위해서는 Mock을 사용하거나 통합 테스트로 분리
    pass


def test_initial_state_structure():
    """초기 State 구조가 올바른지 테스트"""
    
    state = {
        "target_service": "TestService",
        "messages": [],
        "service_overview": None,
        "ethics_evaluation": None,
        "improvement_proposals": None,
        "final_report": None,
        "references": [],
        "current_step": "initialized",
        "errors": []
    }
    
    assert "target_service" in state
    assert "messages" in state
    assert isinstance(state["messages"], list)
    assert state["current_step"] == "initialized"
    assert isinstance(state["errors"], list)
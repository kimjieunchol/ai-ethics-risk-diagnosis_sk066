"""
도구 함수 테스트
"""
import pytest
from src.tools import calculate_risk_level, calculate_weighted_score


def test_calculate_risk_level():
    """리스크 레벨 계산 테스트"""
    
    assert calculate_risk_level(2.0) == "high_risk"
    assert calculate_risk_level(4.5) == "medium_risk"
    assert calculate_risk_level(7.0) == "low_risk"
    assert calculate_risk_level(9.5) == "low_risk"


def test_calculate_weighted_score():
    """가중치 적용 점수 계산 테스트"""
    
    criterion_scores = {
        "bias": 8.0,
        "privacy": 7.0,
        "transparency": 6.0,
        "accountability": 7.5,
        "safety": 8.5
    }
    
    result = calculate_weighted_score(criterion_scores)
    
    assert isinstance(result, float)
    assert 0 <= result <= 10
    assert result > 0  # 모든 점수가 0보다 크므로


def test_calculate_weighted_score_empty():
    """빈 점수 딕셔너리 처리 테스트"""
    
    result = calculate_weighted_score({})
    assert result == 0.0
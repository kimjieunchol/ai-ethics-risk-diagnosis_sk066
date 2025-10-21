"""
평가 점수 계산 유틸리티
"""
from typing import Dict, List
from src.config import ETHICS_CRITERIA, SCORE_RANGE


def calculate_risk_level(score: float) -> str:
    """
    점수에 따른 리스크 레벨 계산
    
    Args:
        score: 평가 점수 (0-10)
    
    Returns:
        리스크 레벨 (high_risk, medium_risk, low_risk)
    """
    for level, (min_score, max_score) in SCORE_RANGE.items():
        if min_score <= score < max_score:
            return level
    return "low_risk"  # 기본값


def calculate_weighted_score(criterion_scores: Dict[str, float]) -> float:
    """
    가중치 적용 종합 점수 계산
    
    Args:
        criterion_scores: 기준별 점수 딕셔너리
            예: {"bias": 7.5, "privacy": 8.0, ...}
    
    Returns:
        가중 평균 점수
    """
    total_score = 0.0
    total_weight = 0.0
    
    for criterion, score in criterion_scores.items():
        if criterion in ETHICS_CRITERIA:
            weight = ETHICS_CRITERIA[criterion]["weight"]
            total_score += score * weight
            total_weight += weight
    
    if total_weight == 0:
        return 0.0
    
    return round(total_score / total_weight, 2)


def prioritize_improvements(evaluation: Dict) -> List[Dict]:
    """
    개선 우선순위 결정
    
    Args:
        evaluation: 윤리 평가 결과
    
    Returns:
        우선순위가 부여된 개선 항목 리스트
    """
    priorities = []
    
    for criterion, data in evaluation.items():
        if criterion in ["overall_score", "overall_risk_level"]:
            continue
        
        score = data.get("score", 10)
        risk_level = data.get("risk_level", "low_risk")
        weight = ETHICS_CRITERIA.get(criterion, {}).get("weight", 0)
        
        # 우선순위 점수 계산 (낮은 점수 + 높은 가중치 = 높은 우선순위)
        priority_score = (10 - score) * weight
        
        # 우선순위 레벨 결정
        if risk_level == "high_risk":
            priority = "high"
        elif risk_level == "medium_risk" and score < 5:
            priority = "high"
        elif risk_level == "medium_risk":
            priority = "medium"
        else:
            priority = "low"
        
        priorities.append({
            "criterion": criterion,
            "score": score,
            "risk_level": risk_level,
            "priority": priority,
            "priority_score": priority_score
        })
    
    # 우선순위 점수 기준 내림차순 정렬
    priorities.sort(key=lambda x: x["priority_score"], reverse=True)
    
    return priorities


def format_score_display(score: float) -> str:
    """점수를 시각적으로 표현"""
    bars = "█" * int(score) + "░" * (10 - int(score))
    return f"{score}/10 [{bars}]"
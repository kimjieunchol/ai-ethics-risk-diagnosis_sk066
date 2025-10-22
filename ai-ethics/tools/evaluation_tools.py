from typing import Dict, List
from config.settings import ETHICS_DIMENSIONS

class EvaluationTools:
    """윤리성 점수 계산 및 개선 우선순위 도구"""

    @staticmethod
    def calculate_overall_score(risk_scores: Dict[str, float]) -> float:
        """가중 평균 기반 전체 점수 계산 (float)"""
        total_score, total_weight = 0.0, 0.0
        for dimension, score in risk_scores.items():
            if dimension in ETHICS_DIMENSIONS:
                weight = ETHICS_DIMENSIONS[dimension]["weight"]
                total_score += score * weight
                total_weight += weight
        return round(total_score / total_weight, 2) if total_weight > 0 else 0.0

    @staticmethod
    def get_risk_level(score: float) -> str:
        """점수 기반 리스크 레벨 반환"""
        if score <= 1.5:
            return "매우 높음"
        elif score <= 2.5:
            return "높음"
        elif score <= 3.5:
            return "중간"
        elif score <= 4.5:
            return "낮음"
        else:
            return "매우 낮음"

    @staticmethod
    def prioritize_improvements(risk_assessment: Dict) -> List[Dict]:
        """점수와 가중치 기반 개선 우선순위 계산"""
        improvements = []
        for dimension, data in risk_assessment.items():
            if dimension == "overall_score" or not isinstance(data, dict):
                continue
            score = float(data.get("score", 5.0))
            weight = ETHICS_DIMENSIONS.get(dimension, {}).get("weight", 0)
            if score <= 3.5:  # 중간 리스크 이상만 개선 대상
                priority = "높음" if score <= 2.5 else "중간"
                improvements.append({
                    "dimension": dimension,
                    "current_score": score,
                    "priority": priority,
                    "priority_score": (5.0 - score) * weight,
                    "description": data.get("description", "")
                })
        improvements.sort(key=lambda x: x["priority_score"], reverse=True)
        return improvements

    @staticmethod
    def compare_services(all_assessments: Dict[str, Dict]) -> Dict:
        """여러 서비스의 윤리 점수 비교"""
        comparison = {"best_performers": {}, "worst_performers": {}, "average_scores": {}}
        dimension_scores = {dim: {} for dim in ETHICS_DIMENSIONS.keys()}

        for service, assessment in all_assessments.items():
            for dimension in ETHICS_DIMENSIONS.keys():
                if dimension in assessment and isinstance(assessment[dimension], dict):
                    score = float(assessment[dimension].get("score", 0))
                    dimension_scores[dimension][service] = score

        for dimension, scores in dimension_scores.items():
            if scores:
                max_score = max(scores.values())
                min_score = min(scores.values())
                best_services = [s for s, v in scores.items() if v == max_score]
                worst_services = [s for s, v in scores.items() if v == min_score]
                avg = sum(scores.values()) / len(scores)
                comparison["best_performers"][dimension] = {"services": best_services, "score": max_score}
                comparison["worst_performers"][dimension] = {"services": worst_services, "score": min_score}
                comparison["average_scores"][dimension] = round(avg, 2)
        return comparison

from typing import Dict, List
import json

class EvaluationTools:
    """평가 관련 도구 모음"""
    
    @staticmethod
    def load_ethics_criteria() -> Dict:
        """윤리 평가 기준 로드"""
        # 실제로는 config/ethics_criteria.json에서 로드
        return {
            "fairness": {
                "name": "공정성 및 편향성",
                "description": "AI 시스템이 다양한 사용자 그룹에 대해 공정하게 작동하는지 평가",
                "weight": 1.0,
                "evaluation_points": [
                    "편향성 테스트 수행 및 결과 공개",
                    "다양한 인구 집단에 대한 동등한 성능",
                    "편향 완화 메커니즘 구현"
                ]
            },
            "privacy": {
                "name": "프라이버시 보호",
                "description": "개인정보 보호 및 데이터 관리의 적절성 평가",
                "weight": 1.0
            },
            "transparency": {
                "name": "투명성 및 설명가능성",
                "description": "AI 시스템의 작동 방식과 의사결정 과정의 투명성 평가",
                "weight": 1.0
            },
            "accountability": {
                "name": "책임성 및 거버넌스",
                "description": "AI 시스템의 책임 소재와 관리 체계 평가",
                "weight": 1.0
            },
            "safety": {
                "name": "안전성 및 보안",
                "description": "AI 시스템의 안전성과 보안 수준 평가",
                "weight": 1.0
            }
        }
    
    @staticmethod
    def get_risk_level(score: float) -> str:
        """점수를 리스크 레벨로 변환"""
        if score >= 4.5:
            return "매우 낮음"
        elif score >= 3.5:
            return "낮음"
        elif score >= 2.5:
            return "중간"
        elif score >= 1.5:
            return "높음"
        else:
            return "매우 높음"
    
    @staticmethod
    def calculate_overall_score(dimension_scores: Dict[str, float]) -> float:
        """전체 점수 계산 (가중 평균)"""
        if not dimension_scores:
            return 0.0
        
        criteria = EvaluationTools.load_ethics_criteria()
        
        total_weight = 0
        weighted_sum = 0
        
        for dimension, score in dimension_scores.items():
            weight = criteria.get(dimension, {}).get("weight", 1.0)
            weighted_sum += score * weight
            total_weight += weight
        
        return round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0
    
    @staticmethod
    def prioritize_improvements(risk_assessment: Dict) -> List[Dict]:
        """개선 우선순위 결정"""
        priority_areas = []
        
        for dimension, assessment in risk_assessment.items():
            if dimension in ["overall_score", "overall_risk_level"]:
                continue
            
            score = assessment.get("score", 3)
            
            # 점수가 3.5 이하인 영역을 개선 대상으로
            if score <= 3.5:
                if score <= 2:
                    priority = "상"
                elif score <= 3:
                    priority = "중"
                else:
                    priority = "하"
                
                priority_areas.append({
                    "dimension": dimension,
                    "current_score": score,
                    "risk_level": assessment.get("risk_level", "중간"),
                    "priority": priority,
                    "issues": assessment.get("risks_identified", [])
                })
        
        # 점수 낮은 순으로 정렬
        priority_areas.sort(key=lambda x: x["current_score"])
        
        return priority_areas
    
    @staticmethod
    def compare_services(assessments: Dict[str, Dict]) -> Dict:
        """여러 서비스 비교"""
        comparison = {
            "service_rankings": [],
            "dimension_comparison": {},
            "statistics": {}
        }
        
        criteria = EvaluationTools.load_ethics_criteria()
        
        # 전체 점수로 순위 매기기
        rankings = []
        for service_name, assessment in assessments.items():
            overall = assessment.get("overall_score", 0)
            rankings.append({
                "service": service_name,
                "overall_score": overall,
                "risk_level": EvaluationTools.get_risk_level(overall)
            })
        
        rankings.sort(key=lambda x: x["overall_score"], reverse=True)
        comparison["service_rankings"] = rankings
        
        # 차원별 비교
        for dimension in criteria.keys():
            dim_scores = {}
            for service_name, assessment in assessments.items():
                if dimension in assessment:
                    dim_scores[service_name] = assessment[dimension].get("score", 0)
            
            if dim_scores:
                best_service = max(dim_scores, key=dim_scores.get)
                worst_service = min(dim_scores, key=dim_scores.get)
                avg_score = sum(dim_scores.values()) / len(dim_scores)
                
                comparison["dimension_comparison"][dimension] = {
                    "scores": dim_scores,
                    "best": {
                        "service": best_service,
                        "score": dim_scores[best_service]
                    },
                    "worst": {
                        "service": worst_service,
                        "score": dim_scores[worst_service]
                    },
                    "average": round(avg_score, 2)
                }
        
        return comparison
    
    @staticmethod
    def automated_checklist_evaluation(
        service_analysis: Dict, 
        dimension: str
    ) -> Dict:
        """자동화된 체크리스트 평가"""
        
        # 서비스 분석 내용을 텍스트로 변환
        service_text = json.dumps(service_analysis, ensure_ascii=False).lower()
        
        checklist = {
            "privacy": [
                ("개인정보처리방침", lambda x: "privacy policy" in x or "개인정보" in x or "프라이버시" in x),
                ("GDPR/법규 준수", lambda x: "gdpr" in x or "개인정보보호법" in x or "규정" in x),
                ("암호화", lambda x: "encrypt" in x or "암호화" in x),
                ("데이터 삭제", lambda x: "삭제" in x or "delete" in x or "제거" in x),
                ("동의 획득", lambda x: "동의" in x or "consent" in x),
            ],
            "transparency": [
                ("AI 사용 명시", lambda x: "ai" in x or "인공지능" in x or "artificial intelligence" in x),
                ("설명가능성", lambda x: "explain" in x or "설명" in x or "interpretable" in x),
                ("알고리즘 공개", lambda x: "algorithm" in x or "알고리즘" in x or "model" in x),
                ("데이터 출처", lambda x: "data source" in x or "데이터 출처" in x or "학습 데이터" in x),
            ],
            "fairness": [
                ("편향성 테스트", lambda x: "bias" in x or "편향" in x or "fairness test" in x),
                ("공정성 평가", lambda x: "fair" in x or "공정" in x or "평등" in x),
                ("다양성 고려", lambda x: "diversity" in x or "다양성" in x or "inclusive" in x),
            ],
            "accountability": [
                ("책임자 명시", lambda x: "책임" in x or "responsible" in x or "accountability" in x),
                ("감사 체계", lambda x: "audit" in x or "감사" in x or "monitoring" in x),
                ("거버넌스", lambda x: "governance" in x or "거버넌스" in x or "oversight" in x),
            ],
            "safety": [
                ("보안 조치", lambda x: "security" in x or "보안" in x or "안전" in x),
                ("리스크 평가", lambda x: "risk assessment" in x or "위험 평가" in x),
                ("안전장치", lambda x: "safety" in x or "safeguard" in x or "보호장치" in x),
            ]
        }
        
        checks = checklist.get(dimension, [])
        passed_checks = []
        
        for name, check_fn in checks:
            if check_fn(service_text):
                passed_checks.append(name)
        
        passed = len(passed_checks)
        total = len(checks)
        
        # 체크리스트 점수 (참고용)
        checklist_score = (passed / total) * 5 if total > 0 else 0
        
        return {
            "checklist_score": round(checklist_score, 1),
            "passed_checks": passed,
            "total_checks": total,
            "passed_items": passed_checks
        }

from typing import Dict, List
import numpy as np


class RiskCalculator:
    """리스크 점수 계산 및 분석 유틸리티"""
    
    @staticmethod
    def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
        """가중치 적용 점수 계산"""
        if weights is None:
            # 기본 가중치 (모두 동일)
            weights = {key: 1.0 for key in scores.keys()}
        
        total_weight = sum(weights.values())
        weighted_sum = sum(scores[key] * weights.get(key, 1.0) for key in scores.keys())
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    @staticmethod
    def categorize_risk_level(score: float) -> str:
        """점수를 리스크 레벨로 변환"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "MINIMAL"
    
    @staticmethod
    def calculate_risk_distribution(risk_assessments: Dict[str, Dict]) -> Dict[str, int]:
        """리스크 분포 계산"""
        distribution = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "MINIMAL": 0
        }
        
        for assessment in risk_assessments.values():
            level = assessment.get('risk_level', 'UNKNOWN')
            if level in distribution:
                distribution[level] += 1
        
        return distribution
    
    @staticmethod
    def identify_critical_findings(risk_assessments: Dict[str, Dict]) -> List[Dict]:
        """심각한 발견사항 식별"""
        critical_findings = []
        
        for category, assessment in risk_assessments.items():
            findings = assessment.get('findings', [])
            for finding in findings:
                if isinstance(finding, dict) and finding.get('severity') in ['HIGH', 'CRITICAL']:
                    critical_findings.append({
                        'category': category,
                        'finding': finding
                    })
        
        return critical_findings
    
    @staticmethod
    def generate_risk_matrix(risk_assessments: Dict[str, Dict]) -> Dict[str, Dict]:
        """리스크 매트릭스 생성 (Likelihood x Impact)"""
        matrix = {}
        
        for category, assessment in risk_assessments.items():
            score = assessment.get('risk_score', 0)
            
            # 점수를 likelihood와 impact로 분해 (간단한 휴리스틱)
            likelihood = "HIGH" if score >= 50 else "MEDIUM" if score >= 30 else "LOW"
            impact = "HIGH" if score >= 60 else "MEDIUM" if score >= 30 else "LOW"
            
            matrix[category] = {
                'likelihood': likelihood,
                'impact': impact,
                'risk_score': score
            }
        
        return matrix


class RiskTrendAnalyzer:
    """리스크 트렌드 분석 (향후 다중 평가 비교용)"""
    
    @staticmethod
    def compare_assessments(current: Dict, previous: Dict) -> Dict:
        """두 평가 결과 비교"""
        comparison = {
            'improved_areas': [],
            'worsened_areas': [],
            'unchanged_areas': [],
            'score_changes': {}
        }
        
        for category in current.keys():
            if category.endswith('_risk'):
                current_score = current.get(category, {}).get('risk_score', 0)
                previous_score = previous.get(category, {}).get('risk_score', 0)
                
                change = current_score - previous_score
                comparison['score_changes'][category] = change
                
                if change < -5:  # 개선
                    comparison['improved_areas'].append(category)
                elif change > 5:  # 악화
                    comparison['worsened_areas'].append(category)
                else:  # 변화 없음
                    comparison['unchanged_areas'].append(category)
        
        return comparison
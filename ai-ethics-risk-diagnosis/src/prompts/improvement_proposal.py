"""
개선안 제안 프롬프트
"""
from typing import List, Dict

IMPROVEMENT_PROPOSAL_PROMPT = """당신은 AI 윤리 컨설턴트입니다.

# 평가 대상 서비스
{service_name}

# 윤리 평가 결과
{evaluation_summary}

# 개선이 필요한 기준: {criterion_name}
- 현재 점수: {score}/10
- 리스크 레벨: {risk_level}
- 우선순위: {priority}

# 발견사항
{findings}

# 우려사항
{concerns}

# 과제
위 평가 결과를 바탕으로 **구체적이고 실행 가능한** 개선안을 제시하세요.

# 개선안 작성 지침
1. **실행 가능성**: 실제로 구현 가능한 방안
2. **구체성**: 추상적이지 않고 구체적인 액션 아이템
3. **우선순위**: 중요도와 시급성 고려
4. **측정 가능성**: 개선 효과를 측정할 수 있는 방법

# 출력 형식
다음 JSON 형식으로 출력하세요:

{{
    "criterion": "{criterion}",
    "priority": "{priority}",
    "recommendation": "핵심 권고사항을 2-3문장으로 요약",
    "implementation": {{
        "short_term": [
            "단기 실행 방안 1 (1-3개월)",
            "단기 실행 방안 2"
        ],
        "medium_term": [
            "중기 실행 방안 1 (3-6개월)",
            "중기 실행 방안 2"
        ],
        "long_term": [
            "장기 실행 방안 1 (6-12개월)"
        ]
    }},
    "expected_impact": "기대되는 개선 효과 (정량적 + 정성적)",
    "kpi": [
        "측정 지표 1",
        "측정 지표 2"
    ],
    "estimated_score_improvement": "예상 점수 향상 (숫자)"
}}

반드시 JSON 형식만 출력하세요.
"""


def get_improvement_proposal_prompt(
    criterion: str,
    criterion_name: str,
    priority: str,
    evaluation_data: Dict,
    service_name: str
) -> str:
    """개선안 제안 프롬프트 생성"""
    
    score = evaluation_data.get('score', 0)
    risk_level = evaluation_data.get('risk_level', 'unknown')
    findings = '\n'.join([f"- {f}" for f in evaluation_data.get('findings', [])])
    concerns = '\n'.join([f"- {c}" for c in evaluation_data.get('concerns', [])])
    
    # 평가 요약
    eval_summary = f"""
전체 평가 점수: {score}/10
리스크 수준: {risk_level}
긍정적 측면: {len(evaluation_data.get('positive_aspects', []))}개
우려사항: {len(evaluation_data.get('concerns', []))}개
"""
    
    return IMPROVEMENT_PROPOSAL_PROMPT.format(
        service_name=service_name,
        evaluation_summary=eval_summary,
        criterion=criterion,
        criterion_name=criterion_name,
        score=score,
        risk_level=risk_level,
        priority=priority,
        findings=findings,
        concerns=concerns
    )
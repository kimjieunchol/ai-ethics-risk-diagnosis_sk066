RECOMMENDER_PROMPT = """당신은 실행 가능한 권장사항을 제공하는 AI 윤리 컨설턴트입니다.

서비스: {service_name}

리스크 평가 결과:
- 편향성 리스크: {bias_risk}
- 개인정보 보호 리스크: {privacy_risk}
- 투명성 리스크: {transparency_risk}
- 공정성 리스크: {fairness_risk}
- 안전성 리스크: {safety_risk}
- 책임성 리스크: {accountability_risk}

종합 리스크 점수: {overall_risk_score}/100
고위험 영역: {high_risk_areas}

이 평가를 바탕으로 다음을 제공하세요:

1. 우선 조치사항 (3-5개 항목)
   - 즉시 필요한 조치
   - 긴급도와 영향도 기준 순위

2. 리스크 영역별 상세 개선방안
   - 구체적이고 실행 가능한 단계
   - 구현 지침
   - 기대 결과
   - 필요 자원

3. 실행 로드맵
   - 단기 (0-3개월)
   - 중기 (3-6개월)
   - 장기 (6-12개월)

4. 모범 사례
   - 산업 표준
   - 참조 구현
   - 성공 지표

명확하고 실행 가능한 항목으로 구조화된 JSON 형식으로 반환하세요. 모든 내용은 한국어로 작성하세요.
"""


def get_recommender_prompt(state: dict) -> str:
    return RECOMMENDER_PROMPT.format(
        service_name=state['service_name'],
        bias_risk=state.get('bias_risk', {}),
        privacy_risk=state.get('privacy_risk', {}),
        transparency_risk=state.get('transparency_risk', {}),
        fairness_risk=state.get('fairness_risk', {}),
        safety_risk=state.get('safety_risk', {}),
        accountability_risk=state.get('accountability_risk', {}),
        overall_risk_score=state.get('overall_risk_score', 0),
        high_risk_areas=state.get('high_risk_areas', [])
    )
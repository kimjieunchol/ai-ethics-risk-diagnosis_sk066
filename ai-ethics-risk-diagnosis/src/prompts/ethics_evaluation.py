"""
윤리 평가 프롬프트
"""

ETHICS_EVALUATION_PROMPT = """당신은 AI 윤리 평가 전문가입니다.

# 평가 대상 서비스
{service_overview}

# 평가 기준: {criterion_name}
{criterion_description}

# 참고 가이드라인
{guidelines}

# 웹 검색 정보
{web_search_results}

# 평가 수행
다음 관점에서 **{criterion_name}** 리스크를 평가하세요:

1. **현황 분석**
   - 현재 서비스가 이 기준을 얼마나 준수하고 있는가?
   - 긍정적인 측면은 무엇인가?
   - 우려되는 측면은 무엇인가?

2. **구체적 발견사항**
   - 최소 2-3가지 구체적 발견사항
   - 각 발견사항에 대한 근거

3. **리스크 점수** (0-10점)
   - 0-3점: 높은 리스크 (심각한 문제)
   - 3-6점: 중간 리스크 (개선 필요)
   - 6-10점: 낮은 리스크 (양호)

4. **근거 자료**
   - 점수를 부여한 구체적 근거
   - 참조한 가이드라인 조항

# 출력 형식
다음 JSON 형식으로 출력하세요:

{{
    "criterion": "{criterion}",
    "score": 7.5,
    "risk_level": "low_risk",
    "findings": [
        "발견사항 1: 구체적 내용",
        "발견사항 2: 구체적 내용",
        "발견사항 3: 구체적 내용"
    ],
    "evidence": [
        "근거 1: 출처와 함께",
        "근거 2: 출처와 함께"
    ],
    "positive_aspects": [
        "긍정적 측면 1",
        "긍정적 측면 2"
    ],
    "concerns": [
        "우려사항 1",
        "우려사항 2"
    ]
}}

반드시 JSON 형식만 출력하세요.
"""


def get_ethics_evaluation_prompt(
    criterion: str,
    criterion_info: Dict,
    service_overview: Dict,
    guidelines: List[Dict],
    web_search_results: List[Dict]
) -> str:
    """윤리 평가 프롬프트 생성"""
    
    # 서비스 개요 포맷팅
    service_text = f"""
서비스명: {service_overview.get('name', 'N/A')}
설명: {service_overview.get('description', 'N/A')}
주요 기능: {', '.join(service_overview.get('key_features', []))}
데이터 사용: {service_overview.get('data_usage', 'N/A')}
"""
    
    # 가이드라인 포맷팅
    guideline_text = "\n\n".join([
        f"## {g['source']} (Page {g['page']})\n{g['content']}"
        for g in guidelines[:3]
    ]) if guidelines else "가이드라인 정보 없음"
    
    # 웹 검색 결과 포맷팅
    web_text = "\n\n".join([
        f"## {r['title']}\n{r['content'][:500]}..."
        for r in web_search_results[:3]
    ]) if web_search_results else "추가 정보 없음"
    
    return ETHICS_EVALUATION_PROMPT.format(
        service_overview=service_text,
        criterion=criterion,
        criterion_name=criterion_info['name'],
        criterion_description=criterion_info['description'],
        guidelines=guideline_text,
        web_search_results=web_text
    )
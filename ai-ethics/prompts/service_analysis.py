SERVICE_ANALYSIS_PROMPT = """당신은 AI 서비스 분석 전문가입니다.

주어진 AI 서비스에 대한 정보를 분석하여 다음 항목들을 정리해주세요:

# 분석 대상 서비스
{service_name}

# 수집된 정보
{collected_info}

# 분석 요구사항
다음 항목들을 상세히 분석해주세요:

1. **서비스 개요**
   - 서비스의 주요 목적과 기능
   - 타겟 사용자층
   - 제공하는 핵심 기능 3-5가지

2. **기술적 특징**
   - 사용된 AI 기술 (예: LLM, Computer Vision, 생성형 AI 등)
   - 학습 데이터 특성 (공개된 정보가 있다면)
   - 기술적 강점

3. **데이터 처리 방식**
   - 사용자 데이터 수집 범위
   - 데이터 저장 및 처리 방식
   - 개인정보 취급 정책

4. **현재 알려진 이슈**
   - 윤리적 논란이나 문제점
   - 사용자 불만사항
   - 규제 관련 이슈

# 출력 형식
JSON 형식으로 출력해주세요:
{{
  "overview": "서비스 개요 설명",
  "key_features": ["기능1", "기능2", "기능3"],
  "target_users": "타겟 사용자 설명",
  "ai_technology": "사용된 AI 기술",
  "data_usage": "데이터 처리 방식 설명",
  "known_issues": ["이슈1", "이슈2"]
}}

분석을 시작하세요:"""

SERVICE_SEARCH_QUERY_PROMPT = """AI 서비스 '{service_name}'에 대해 '{query_type}' 정보를 검색하기 위한 최적의 검색 쿼리를 생성해주세요.

쿼리 타입: {query_type}
- overview: 서비스 개요, 주요 기능
- ethics: 윤리적 이슈, 논란
- privacy: 개인정보 보호 정책
- transparency: 투명성, 작동 원리

검색 쿼리 (한글 + 영문 키워드 조합):"""
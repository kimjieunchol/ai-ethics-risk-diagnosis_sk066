"""
서비스 분석 프롬프트
"""
from typing import List, Dict

SERVICE_ANALYSIS_PROMPT = """당신은 AI 서비스 분석 전문가입니다.

# 목표
{service_name} AI 서비스에 대한 종합적인 분석을 수행하세요.

# 분석할 정보
{search_results}

# 분석 항목
다음 항목들을 상세히 분석하세요:

1. **서비스 개요**
   - 서비스의 주요 목적과 기능
   - 핵심 기술 스택
   - 제공 형태 (웹, 앱, API 등)

2. **주요 기능**
   - 핵심 기능 3-5가지
   - 각 기능의 작동 방식

3. **대상 사용자**
   - 주요 사용자 그룹
   - 사용 사례

4. **데이터 사용 방식**
   - 어떤 데이터를 수집하는가?
   - 데이터를 어떻게 처리하는가?
   - 사용자 데이터 저장 및 관리 방식

5. **AI/ML 기술**
   - 사용된 AI 기술 (LLM, Computer Vision 등)
   - 모델 학습 방식

# 출력 형식
다음 JSON 형식으로 출력하세요:

{{
    "name": "서비스명",
    "description": "서비스 설명 (2-3문장)",
    "key_features": ["기능1", "기능2", "기능3"],
    "target_users": "대상 사용자 설명",
    "data_usage": "데이터 사용 방식 설명",
    "ai_technology": "사용된 AI 기술 설명"
}}

반드시 JSON 형식만 출력하세요. 다른 설명은 포함하지 마세요.
"""


def get_service_analysis_prompt(service_name: str, search_results: List[Dict]) -> str:
    """서비스 분석 프롬프트 생성"""
    
    # 검색 결과 포맷팅
    formatted_results = "\n\n".join([
        f"## Source {i+1}: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content:\n{result['content']}"
        for i, result in enumerate(search_results[:5])
    ])
    
    return SERVICE_ANALYSIS_PROMPT.format(
        service_name=service_name,
        search_results=formatted_results
    )
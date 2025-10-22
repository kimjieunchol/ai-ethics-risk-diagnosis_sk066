SERVICE_ANALYSIS_PROMPT = """
다음 AI 서비스에 대한 종합 분석을 수행하세요.

## 서비스명
{service_name}

## 수집된 정보
### 개요 정보
{overview_info}

### 윤리 관련 정보
{ethics_info}

## 분석 요구사항
다음 항목을 포함하여 서비스를 분석하세요:
1. 서비스 개요 (주요 기능, 사용 목적, 대상 사용자)
2. 기술적 특징 (AI 모델 유형, 데이터 사용 방식)
3. 윤리성 관련 특이사항
4. 공개된 정책 및 가이드라인
5. 알려진 이슈나 논란

응답은 다음 JSON 형식으로만 작성하세요 (다른 텍스트 없이):
{{
  "service_overview": {{
    "description": "<서비스 설명>",
    "main_features": ["<기능1>", "<기능2>", "<기능3>"],
    "target_users": "<대상 사용자>",
    "use_cases": ["<사용 사례1>", "<사용 사례2>"]
  }},
  "technical_details": {{
    "ai_type": "<AI 유형 (예: LLM, Computer Vision, 등)>",
    "data_usage": "<데이터 사용 방식>",
    "model_info": "<모델 정보 (알려진 경우)>"
  }},
  "ethics_aspects": {{
    "public_policies": ["<정책1>", "<정책2>"],
    "known_issues": ["<이슈1>", "<이슈2>"],
    "positive_aspects": ["<긍정적 측면1>", "<긍정적 측면2>"]
  }},
  "additional_notes": "<기타 중요 사항>"
}}
"""
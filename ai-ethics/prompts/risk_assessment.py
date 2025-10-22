RISK_ASSESSMENT_PROMPT = """
다음 AI 서비스를 '{dimension}' 차원에서 평가하세요.

## 서비스 정보
서비스명: {service_name}

## 서비스 분석 결과
{service_analysis}

## 평가 차원: {dimension} ({dimension_description})

## 평가 기준
{evaluation_criteria}

## 참고 가이드라인
{guideline_context}

## 추가 검색 정보
{search_context}

## 점수 평가 기준 (1-5점)
**5점 (매우 우수)**: 가이드라인을 완벽히 준수하며 모범 사례를 따름. 명확한 증거와 문서화가 있음.
**4점 (우수)**: 대부분의 요구사항을 충족하며 경미한 개선사항만 존재. 
**3점 (보통)**: 기본 요구사항은 충족하나 여러 개선이 필요. 일부 영역에서 불확실성 존재.
**2점 (미흡)**: 중요한 요구사항이 누락되었거나 명백한 리스크가 존재.
**1점 (매우 미흡)**: 심각한 윤리적 리스크가 존재하며 즉각적 개선 필요.

## 평가 시 반드시 확인할 사항
1. EU AI Act 준수 여부 및 근거
2. UNESCO AI Ethics 원칙 부합도
3. OECD AI Principles 반영 정도
4. 실제 구현 증거 (정책 문서, 기술 문서, 공개 정보)
5. 알려진 사고/이슈 이력

## 응답 형식 (JSON만 출력)
{{
  "score": <1-5 사이의 정수>,
  "description": "<평가 근거 상세 설명 (최소 200자 이상). 구체적인 사실과 증거를 포함하세요.>",
  "evidence": [
    "<구체적 증거 1: 출처와 함께>",
    "<구체적 증거 2: 출처와 함께>",
    "<구체적 증거 3: 출처와 함께>"
  ],
  "guideline_compliance": {{
    "EU AI Act": "<준수/부분준수/미준수/해당없음> - 구체적 근거",
    "UNESCO": "<준수/부분준수/미준수> - 구체적 근거",
    "OECD": "<준수/부분준수/미준수> - 구체적 근거"
  }},
  "reasoning": "<점수를 매긴 구체적 이유. 왜 이 점수인지 최소 150자 이상 설명>",
  "risks_identified": [
    "<발견된 리스크 1>",
    "<발견된 리스크 2>"
  ],
  "strengths": [
    "<강점 1>",
    "<강점 2>"
  ]
}}
"""


# ============================================
# prompts/service_analysis.py
# ============================================
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

응답은 다음 JSON 형식으로 작성하세요:
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

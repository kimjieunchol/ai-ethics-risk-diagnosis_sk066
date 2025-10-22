from typing import List, Dict
IMPROVEMENT_SUGGESTION_PROMPT = """당신은 AI 윤리 컨설턴트입니다.

# 서비스 정보
서비스명: {service_name}

# 리스크 평가 결과
{risk_assessment}

# 개선 우선순위
{priority_areas}

# 임무
위의 리스크 평가 결과를 바탕으로, 각 리스크 영역에 대한 구체적이고 실행 가능한 개선안을 제시해주세요.

# 개선안 작성 가이드
1. **구체성**: "투명성을 높인다"가 아닌 "사용자 대시보드에 AI 의사결정 과정을 단계별로 표시"처럼 구체적으로
2. **실행 가능성**: 현실적으로 구현 가능한 방안
3. **우선순위**: 긴급성과 중요도를 고려한 순서
4. **참고 사례**: 가능하다면 타 기업의 모범 사례 언급

# 출력 형식
각 리스크 영역별로 다음 JSON 형식으로 작성:

[
  {{
    "risk_area": "리스크 영역 (bias/privacy/transparency/accountability)",
    "current_score": 현재점수,
    "target_score": 목표점수,
    "priority": "우선순위 (높음/중간/낮음)",
    "short_term": [
      {{
        "action": "단기 개선안 (3개월 이내)",
        "expected_impact": "예상 효과",
        "implementation_difficulty": "구현 난이도 (상/중/하)"
      }}
    ],
    "mid_term": [
      {{
        "action": "중기 개선안 (6-12개월)",
        "expected_impact": "예상 효과",
        "implementation_difficulty": "구현 난이도 (상/중/하)"
      }}
    ],
    "long_term": [
      {{
        "action": "장기 개선안 (1년 이상)",
        "expected_impact": "예상 효과",
        "implementation_difficulty": "구현 난이도 (상/중/하)"
      }}
    ],
    "best_practices": [
      "업계 모범 사례 1",
      "업계 모범 사례 2"
    ],
    "estimated_cost": "예상 비용 수준 (상/중/하)",
    "regulatory_compliance": "관련 규제 대응 여부"
  }}
]

개선안을 작성하세요:"""

COMPARISON_PROMPT = """당신은 AI 서비스 비교 분석 전문가입니다.

# 분석 대상 서비스들
{services_list}

# 각 서비스별 리스크 평가 결과
{all_assessments}

# 임무
여러 AI 서비스들의 윤리성 평가 결과를 비교 분석하여, 다음 내용을 작성해주세요:

1. **종합 순위**: 전체 윤리성 점수 기준 순위
2. **차원별 강자**: 각 윤리 차원(편향성, 프라이버시, 투명성, 책임성)에서 가장 우수한 서비스
3. **주요 차별점**: 서비스들 간의 핵심적인 차이점
4. **업계 트렌드**: 공통적으로 나타나는 강점과 약점
5. **벤치마킹 포인트**: 서로 배울 수 있는 점

# 출력 형식
구조화된 분석 텍스트 (마크다운 형식):

## 종합 비교 분석

### 1. 전체 순위
(서비스별 종합 점수와 순위)

### 2. 차원별 최우수 서비스
(각 차원별로 가장 우수한 서비스와 그 이유)

### 3. 주요 차별점
(서비스들의 핵심 차이점 3-5가지)

### 4. 업계 공통 트렌드
- 공통 강점
- 공통 약점

### 5. 벤치마킹 포인트
(각 서비스가 다른 서비스에게서 배울 수 있는 점)

비교 분석을 시작하세요:"""
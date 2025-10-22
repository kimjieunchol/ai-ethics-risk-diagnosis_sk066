REPORT_GENERATOR_PROMPT = """당신은 AI 윤리 리스크 평가 보고서를 작성하는 전문 보고서 작성자입니다.

다음 구조로 마크다운 형식의 종합 보고서를 생성하세요:

# AI 윤리성 리스크 진단 보고서

## 요약 (SUMMARY)
- 서비스: {service_name}
- 종합 리스크 점수: {overall_risk_score}/100
- 리스크 수준: {risk_level}
- 평가 일자: [현재 날짜]
- 주요 발견사항: [핵심 발견사항 3-5개 항목]
- 우선 조치사항: [즉시 필요한 상위 3개 조치]

## 1. 개요
[서비스 및 평가 목적에 대한 간결한 개요]

## 2. 서비스 분석
{service_analysis}

## 3. 윤리 리스크 평가

### 3.1 편향성 리스크
{bias_risk}

### 3.2 개인정보 보호 리스크
{privacy_risk}

### 3.3 투명성 리스크
{transparency_risk}

### 3.4 공정성 리스크
{fairness_risk}

### 3.5 안전성 및 보안 리스크
{safety_risk}

### 3.6 책임성 리스크
{accountability_risk}

## 4. 개선 방안

### 4.1 우선 조치사항
{priority_actions}

### 4.2 상세 개선 계획
{recommendations}

### 4.3 실행 로드맵
[마일스톤이 포함된 구조화된 타임라인]

## 5. 결론
[전반적인 평가 요약 및 전략적 권장사항]

## 참고 문헌 (REFERENCES)
{references}

## 부록 (APPENDIX)

### A. 평가 방법론
- 사용된 가이드라인: EU AI Act, UNESCO AI 윤리, OECD AI 원칙
- 리스크 점수 산정 방법: [설명]
- 평가 기준: [상세 기준]

### B. 리스크 점수 매트릭스
[리스크 카테고리와 점수를 보여주는 표]

### C. 용어 설명
[주요 용어 및 정의]

---
*본 보고서는 AI 윤리 리스크 평가 시스템에 의해 생성되었습니다*
*문의사항이나 추가 설명이 필요한 경우 윤리 규정 준수 팀에 문의하시기 바랍니다*

보고서는 전문적이고 실행 가능하며 체계적으로 작성되어야 합니다. 모든 내용은 한국어로 작성하세요.
"""


def get_report_prompt(state: dict) -> str:
    return REPORT_GENERATOR_PROMPT.format(**state)
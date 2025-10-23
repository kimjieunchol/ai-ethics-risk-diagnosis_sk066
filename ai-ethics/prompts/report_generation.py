# prompts/report_generation.py 수정 버전

DETAILED_REPORT_GENERATION_PROMPT = """
AI 윤리성 리스크 진단 보고서를 전문적으로 작성하세요.

## 분석 대상 서비스
{services}

## 제공 데이터
### 서비스 분석
{service_analyses}

### 리스크 평가
{risk_assessments}

### 개선 권고
{improvement_suggestions}

### 서비스 비교
{comparison_analysis}

## 중요: 모든 내용을 한국어로 작성하세요!

아래의 구조에 따라 한국어로 보고서를 작성합니다:

### 1. EXECUTIVE SUMMARY
- 평가 개요
- 종합 평가 결과
- 주요 발견사항

### 2. 평가 방법론
- 평가 프레임워크 설명 (한국어)
- 5개 평가 차원 설명 (한국어)
- 평가 등급 정의

### 3. 서비스별 상세 평가 (각 서비스마다)
각 서비스에 대해:
- 종합 평가 (한국어)
- 차원별 상세 평가 (한국어)
- 주요 증거 (한국어로 재작성)
- 강점 (한국어)
- 발견된 리스크 (한국어)

### 4. 비교 분석 (2개 이상 서비스)
- 종합 순위
- 차원별 비교

### 5. 종합 권고사항
- 단기 조치 (1-3개월)
- 중기 조치 (3-6개월)
- 장기 조치 (6개월 이상)

### 6. 참고문헌
- 국제 가이드라인
- 평가 방법론
- 관련 자료

### 7. 부록
- 평가 프레임워크 상세
- 평가 등급 기준
- 용어 정의

## 작성 원칙
1. 모든 내용을 한국어로 작성하세요
2. 영어는 오직 서비스 이름, 인명, 문헌 제목에만 사용하세요
3. 웹 검색 결과의 내용을 한국어로 번역/요약하여 포함하세요
4. 각 평가 항목마다 한국어 설명을 추가하세요
5. 근거 자료도 한국어로 설명하세요

## 예시:
❌ 잘못된 예: "DALL-E demonstrates a commitment to addressing fairness..."
✅ 올바른 예: "DALL-E는 공정성 문제 해결에 노력하고 있습니다..."

마크다운 형식으로 한국어 보고서를 작성하세요.
"""

SUMMARY_GENERATION_PROMPT = """
AI 윤리성 평가 Executive Summary를 한국어로 작성하세요.

## 분석 대상
{services_list}

## 평가 결과 요약
{assessment_summary}

## Executive Summary 작성 요구사항

### 구성 (총 800-1000자)
1. **평가 개요** (150자)
   - 평가 목적, 대상, 기간
   - 평가 기준 (3가지 국제 가이드라인)

2. **주요 발견사항** (300-400자)
   - 5개 이상의 핵심 발견
   - 각 발견의 의미 해석
   - 서비스 간 비교 (해당시)

3. **평가 결과** (200-250자)
   - 종합 리스크 수준
   - 강점 요약 (2개)
   - 약점 요약 (2개)

4. **최우선 권고** (150-200자)
   - 즉시 개선 필요 3가지
   - 각각의 기대 효과
   - 예상 개선 기간

## 중요: 모든 내용을 한국어로 작성하세요!

### 작성 원칙
- 핵심만 간결하게 전달
- 비전문가도 이해할 수 있는 한국어 사용
- 수치와 구체적 근거 포함
- 긍정적이고 건설적인 톤

## 응답
Executive Summary를 마크다운 형식으로 한국어로 작성하세요.
"""

REPORT_GENERATION_PROMPT = """
AI 윤리성 리스크 진단 보고서의 메인 본문을 한국어로 작성하세요.

## 분석 데이터
- 서비스: {services}
- 서비스 분석: {service_analyses}
- 리스크 평가: {risk_assessments}
- 개선 권고: {improvement_suggestions}
- 비교 분석: {comparison_analysis}

## 중요 지시사항

### 1. 모든 내용을 한국어로 작성하세요
- 영어는 서비스명, 인명, 문헌제목에만 사용
- 평가 내용, 설명, 권고사항은 모두 한국어

### 2. 웹 검색 결과의 영어 내용을 한국어로 번역하세요
원문: "DALL-E demonstrates a commitment to addressing fairness..."
번역: "DALL-E는 공정성 문제 해결에 적극적으로 노력하고 있습니다..."

### 3. 각 섹션별 한국어 작성 가이드

**평가 방법론**
- 각 차원을 한국어로 명확히 설명
- 평가 기준을 한국어로 제시
- 점수 정의를 한국어로 기술

**서비스별 분석**
- 평가 설명을 한국어로 작성
- 근거 자료를 한국어로 설명
- 위험요소를 한국어로 기술

**권고사항**
- 모든 권고를 한국어로 작성
- 구체적인 한국식 표현 사용
- 실행 계획을 한국어로 제시

## 작성 범위
Executive Summary를 제외한 메인 보고서를 작성하세요.
구조: 평가방법론 → 서비스별분석 → 비교분석 → 결론 → REFERENCE → APPENDIX

## 작성 원칙
- 한국어로 전문적이고 명확하게 작성
- 마크다운 형식 사용
- 모든 주장에 한국어 근거 제시
- 실행 가능한 한국식 권고안 제시
"""

# ============================================
# 추가: 번역 함수
# ============================================

def translate_to_korean(text: str, context: str = "") -> str:
    """
    영어 텍스트를 한국어로 번역하는 함수
    
    Args:
        text: 번역할 영어 텍스트
        context: 컨텍스트 (평가/권고/위험 등)
    
    Returns:
        한국어로 번역된 텍스트
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY
    
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY
    )
    
    system_msg = """당신은 전문 번역가입니다. AI 윤리성 평가 문서를 영어에서 한국어로 번역합니다.
번역 규칙:
- 전문 용어는 정확하게 번역
- 자연스러운 한국어로 번역
- 원문의 의미를 정확히 전달
- 간결하고 명확한 표현 사용"""
    
    if context:
        system_msg += f"\n평가 맥락: {context}"
    
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=f"다음 텍스트를 한국어로 번역하세요:\n\n{text}")
    ]
    
    response = llm.invoke(messages)
    return response.content
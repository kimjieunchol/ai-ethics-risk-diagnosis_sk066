"""
보고서 생성 프롬프트
"""

REPORT_GENERATION_PROMPT = """당신은 전문 리포트 작성자입니다.

# 보고서 작성 대상
서비스명: {service_name}

# 서비스 정보
{service_overview}

# 윤리 평가 결과
{evaluation_results}

# 개선 제안
{improvement_proposals}

# 참조 문서
{references}

# 과제
위 정보를 바탕으로 전문적인 **AI 윤리성 리스크 진단 보고서**를 작성하세요.

# 보고서 구성 (Markdown 형식)

## SUMMARY
- 보고서 핵심 메시지 (3-5개 bullet points)
- 전체 평가 점수와 리스크 레벨
- 주요 발견사항 요약

## 1. Executive Summary
- 진단 목적
- 진단 방법론
- 주요 결과 요약

## 2. 서비스 개요
- 서비스 소개
- 주요 기능
- AI 기술 활용 현황

## 3. 윤리성 평가 결과

### 3.1 편향성 (Bias)
- 평가 점수: X/10
- 주요 발견사항
- 리스크 분석

### 3.2 프라이버시 (Privacy)
- 평가 점수: X/10
- 주요 발견사항
- 리스크 분석

### 3.3 투명성 (Transparency)
- 평가 점수: X/10
- 주요 발견사항
- 리스크 분석

### 3.4 책임성 (Accountability)
- 평가 점수: X/10
- 주요 발견사항
- 리스크 분석

### 3.5 안전성 (Safety)
- 평가 점수: X/10
- 주요 발견사항
- 리스크 분석

## 4. 종합 평가
- 전체 평가 점수
- 강점과 약점 종합
- 리스크 매트릭스

## 5. 개선 권고사항
각 기준별 구체적 개선안 (우선순위별)

### High Priority
...

### Medium Priority
...

### Low Priority
...

## 6. 결론
- 최종 의견
- 향후 모니터링 필요 사항

## REFERENCES
참조한 가이드라인 및 출처 목록

## APPENDIX
### A. 평가 방법론
### B. 평가 기준 상세
### C. 점수 산정 로직

---

# 작성 지침
1. **전문성**: 전문적이고 신뢰할 수 있는 톤
2. **객관성**: 편향 없이 사실에 근거
3. **명확성**: 기술 용어는 설명과 함께 사용
4. **실용성**: 실행 가능한 권고사항
5. **시각화**: 가능한 곳에 표 활용

Markdown 형식으로 완전한 보고서를 작성하세요.
"""


def get_report_generation_prompt(
    service_name: str,
    service_overview: Dict,
    evaluation_results: Dict,
    improvement_proposals: List[Dict],
    references: List[Dict]
) -> str:
    """보고서 생성 프롬프트 생성"""
    
    # 서비스 개요 포맷팅
    service_text = f"""
**서비스명**: {service_overview.get('name')}
**설명**: {service_overview.get('description')}
**주요 기능**: {', '.join(service_overview.get('key_features', []))}
**대상 사용자**: {service_overview.get('target_users')}
**데이터 사용**: {service_overview.get('data_usage')}
**AI 기술**: {service_overview.get('ai_technology')}
"""
    
    # 평가 결과 포맷팅
    eval_text = ""
    for criterion, data in evaluation_results.items():
        if criterion not in ["overall_score", "overall_risk_level"]:
            eval_text += f"\n### {criterion.upper()}\n"
            eval_text += f"- 점수: {data.get('score')}/10\n"
            eval_text += f"- 리스크: {data.get('risk_level')}\n"
            eval_text += f"- 발견사항: {len(data.get('findings', []))}개\n"
    
    # 개선 제안 포맷팅
    proposal_text = ""
    for prop in improvement_proposals:
        proposal_text += f"\n### {prop.get('criterion').upper()}\n"
        proposal_text += f"- 우선순위: {prop.get('priority')}\n"
        proposal_text += f"- 권고: {prop.get('recommendation')}\n"
    
    # 참조 문헌 포맷팅
    ref_text = "\n".join([
        f"- {ref.get('source')}: {ref.get('content')[:100]}..."
        for ref in references[:5]
    ]) if references else "없음"
    
    return REPORT_GENERATION_PROMPT.format(
        service_name=service_name,
        service_overview=service_text,
        evaluation_results=eval_text,
        improvement_proposals=proposal_text,
        references=ref_text
    )
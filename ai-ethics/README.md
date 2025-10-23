# ⚖️ AI 윤리성 리스크 진단 시스템

특정 AI 서비스를 대상으로 윤리적 리스크(편향성, 프라이버시 침해, 투명성 부족 등)를 종합적으로 분석하고, 국제 표준 기반의 구체적인 개선 권고안을 제시하는 멀티 에이전트 시스템입니다.

## 📋 목차

- [주요 기능](#-주요-기능)
- [시스템 구조](#-시스템-구조)
- [평가 프레임워크](#-평가-프레임워크)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [프로젝트 구조](#-프로젝트-구조)
- [기술 스택](#-기술-스택)

## ✨ 주요 기능

### 1. 5개 차원 심층 평가

- **공정성 및 편향성 (Fairness)**: 알고리즘의 편향성, 차별 가능성 평가
- **프라이버시 보호 (Privacy)**: 개인정보 처리 및 보호 수준 분석
- **투명성 및 설명가능성 (Transparency)**: AI 의사결정의 투명성 검증
- **책임성 및 거버넌스 (Accountability)**: 조직의 책임 체계 평가
- **안전성 및 보안 (Safety)**: 시스템의 안전성과 보안 수준 분석

### 2. 국제 표준 기반 평가

- **EU AI Act**: 유럽연합의 AI 규제 프레임워크
- **UNESCO AI Ethics**: 유네스코 AI 윤리 권고안
- **OECD AI Principles**: OECD AI 원칙

### 3. 종합 보고서 생성

- 마크다운 형식의 상세 보고서
- PDF 형식의 전문 보고서 (차트, 표, 시각화 포함)
- JSON 형식의 구조화된 데이터

### 4. 비교 분석

- 최대 3개 서비스 동시 비교
- 차원별 강점/약점 분석
- 업계 벤치마크 제공

### 5. 실행 가능한 개선안

- 우선순위 기반 개선 과제 도출
- 단계별 구현 계획 제시
- 성과 지표(KPI) 제공

## 🏗️ 시스템 구조

### 멀티 에이전트 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                   AI 윤리성 리스크 진단 시스템                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         AIEthicsAssessmentSystem        │
        │         (오케스트레이션 레이어)             │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   에이전트1    │     │   에이전트2    │     │   에이전트3    │
│              │     │              │     │              │
│   Service    │────▶│    Risk      │────▶│ Improvement  │
│   Analyzer   │     │   Assessor   │     │   Advisor    │
│              │     │              │     │              │
│ 서비스 분석   │     │ 리스크 평가   │     │  개선안 제안  │
└──────────────┘     └──────────────┘     └──────────────┘
                              │
                              ▼
                     ┌──────────────┐
                     │   에이전트4    │
                     │              │
                     │    Report    │
                     │    Writer    │
                     │              │
                     │  보고서 생성  │
                     └──────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Markdown    │     │     PDF      │     │     JSON     │
│   Report     │     │    Report    │     │     Data     │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 에이전트 상세 설명

#### 1️⃣ ServiceAnalyzer (서비스 분석 에이전트)

**역할**: AI 서비스의 기본 정보 수집 및 분석

- 웹 검색을 통한 서비스 정보 수집
- 주요 기능 및 특징 파악
- 기술적 세부사항 분석
- 윤리 관련 공개 정보 수집

**출력**:

```json
{
  "service_overview": {
    "description": "서비스 설명",
    "main_features": ["기능1", "기능2"],
    "target_users": "대상 사용자",
    "use_cases": ["사용 사례1", "사용 사례2"]
  },
  "technical_details": {
    "ai_type": "AI 모델 유형",
    "data_usage": "데이터 사용 방식",
    "model_info": "모델 정보"
  },
  "ethics_aspects": {
    "public_policies": ["정책1", "정책2"],
    "known_issues": ["이슈1", "이슈2"],
    "positive_aspects": ["긍정적 측면1"]
  }
}
```

#### 2️⃣ RiskAssessor (리스크 평가 에이전트)

**역할**: 5개 윤리 차원에 대한 정량적/정성적 리스크 평가

- 각 차원별 1-5점 평가
- 자동화된 체크리스트 검증
- RAG 기반 가이드라인 참조
- 웹 검색을 통한 추가 증거 수집
- 가이드라인 준수 여부 검증

**평가 프로세스**:

```
1. 자동 체크리스트 평가 → 2. RAG 가이드라인 검색
                ↓
3. 웹 검색 추가 정보 수집 → 4. LLM 종합 평가
                ↓
        5. 점수 및 리스크 레벨 산출
```

**출력**:

```json
{
  "fairness": {
    "score": 4,
    "risk_level": "낮음",
    "description": "공정성 평가 설명",
    "evidence": ["증거1", "증거2"],
    "guideline_compliance": {
      "EU AI Act": "준수",
      "UNESCO": "부분준수",
      "OECD": "준수"
    },
    "risks_identified": ["위험1"],
    "strengths": ["강점1"]
  },
  "overall_score": 4.2,
  "overall_risk_level": "낮음"
}
```

#### 3️⃣ ImprovementAdvisor (개선안 제안 에이전트)

**역할**: 리스크 평가 기반 구체적이고 실행 가능한 개선 방향 제시

- 개선 우선순위 자동 파악 (3.5점 미만 차원)
- 단계별 구현 계획 제시
- 성과 지표(KPI) 정의
- 리소스 및 타임라인 추정
- 여러 서비스 비교 분석

**출력**:

```json
[
  {
    "dimension": "공정성 및 편향성",
    "current_score": 3.2,
    "target_score": 4.5,
    "priority": "상",
    "current_issues": ["문제점1", "문제점2"],
    "improvements": [
      {
        "title": "개선 조치 제목",
        "description": "상세 설명",
        "implementation_steps": ["단계1", "단계2"],
        "expected_impact": "기대 효과",
        "success_metrics": ["KPI1", "KPI2"],
        "timeline": "3-6개월",
        "resources_needed": "필요 리소스",
        "guideline_reference": "관련 가이드라인"
      }
    ]
  }
]
```

#### 4️⃣ ReportWriter (보고서 작성 에이전트)

**역할**: 분석 결과를 전문적인 보고서로 작성

- Executive Summary 생성
- 서비스별 상세 평가 작성
- 비교 분석 (2개 이상 서비스)
- 종합 권고사항 도출
- 마크다운 + PDF 보고서 생성

**보고서 구조**:

```
1. Executive Summary
2. 평가 방법론
3. 서비스별 상세 평가
4. 비교 분석 (해당 시)
5. 종합 권고사항
6. 참고문헌
7. 부록
```

## 📊 평가 프레임워크

### 평가 차원 및 기준

| 차원           | 평가 항목                                               | 주요 체크포인트                                                               |
| -------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **공정성**     | - 알고리즘 편향성<br>- 데이터 대표성<br>- 공정성 테스트 | • 편향성 감사 실시 여부<br>• 다양성 보장 메커니즘<br>• 공정성 정책 문서화     |
| **프라이버시** | - 데이터 수집 정책<br>- 보안 조치<br>- 사용자 통제      | • 명확한 개인정보 처리방침<br>• 암호화 및 접근 제어<br>• 사용자 동의 메커니즘 |
| **투명성**     | - 설명가능성<br>- 정보 공개<br>- 의사결정 추적          | • 알고리즘 설명 제공<br>• 모델 카드/데이터시트<br>• 결정 근거 제공            |
| **책임성**     | - 거버넌스 구조<br>- 책임 주체<br>- 감사 체계           | • AI 윤리 위원회 존재<br>• 명확한 책임 체계<br>• 정기 감사 프로세스           |
| **안전성**     | - 오류 처리<br>- 악용 방지<br>- 안전장치                | • 에러 핸들링 메커니즘<br>• 악용 방지 조치<br>• 사고 대응 계획                |

### 평가 등급 기준

| 등급   | 점수 범위 | 위험도    | 정의      | 권고사항                     |
| ------ | --------- | --------- | --------- | ---------------------------- |
| **A+** | 4.8-5.0   | 매우 낮음 | 모범 사례 | 현상 유지 및 지속적 모니터링 |
| **A**  | 4.5-4.7   | 낮음      | 우수      | 경미한 개선사항 적용         |
| **B+** | 4.2-4.4   | 낮음      | 양호      | 일부 개선 권장               |
| **B**  | 3.8-4.1   | 중간      | 보통      | 개선 계획 수립 필요          |
| **C**  | 3.0-3.7   | 중간      | 미흡      | 즉시 개선 조치 필요          |
| **D**  | 2.0-2.9   | 높음      | 부족      | 긴급 개선 조치 필수          |
| **F**  | 1.0-1.9   | 매우 높음 | 위험      | 전면 재검토 필요             |

## 🚀 설치 방법

### 1. 필수 요구사항

- Python 3.8 이상
- OpenAI API 키

### 2. 설치

```bash
# 저장소 클론
git clone <repository-url>
cd ai-ethics-assessment

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경 설정

`.env` 파일을 생성하고 다음 내용을 입력:

```env
OPENAI_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-4o  # 또는 gpt-4-turbo
LLM_TEMPERATURE=0.3
```

### 4. 프로젝트 구조

```
ai-ethics-assessment/
├── agents/                          # 에이전트 모듈
│   ├── __init__.py
│   ├── service_analyzer.py          # 서비스 분석 에이전트
│   ├── risk_assessor.py             # 리스크 평가 에이전트
│   ├── improvement_advisor.py       # 개선안 제안 에이전트
│   └── report_writer.py             # 보고서 작성 에이전트
├── tools/                           # 도구 모듈
│   ├── __init__.py
│   ├── rag_tools.py                 # RAG 도구
│   ├── search_tools.py              # 웹 검색 도구
│   ├── evaluation_tools.py          # 평가 도구
│   └── report_pdf_enhanced.py       # PDF 생성 도구
├── prompts/                         # 프롬프트 템플릿
│   ├── __init__.py
│   ├── service_analysis.py
│   ├── risk_assessment.py
│   ├── improvement.py
│   └── report_generation.py
├── config/                          # 설정 파일
│   ├── __init__.py
│   └── settings.py
├── utils/                           # 유틸리티
│   ├── __init__.py
│   ├── state.py
│   └── helpers.py
├── data/                            # 데이터 디렉토리
│   ├── guidelines/                  # 가이드라인 문서
│   └── embeddings/                  # 벡터 임베딩
├── outputs/                         # 출력 결과
│   ├── reports/                     # 생성된 보고서
│   └── data/                        # JSON 데이터
├── app.py                           # 메인 애플리케이션
├── streamlit_app.py                 # Streamlit UI
├── requirements.txt                 # 의존성 목록
├── .env                             # 환경 변수
└── README.md                        # 이 문서
```

## 💻 사용 방법

### 방법 1: 커맨드라인 인터페이스

```python
from app import AIEthicsAssessmentSystem

# 시스템 초기화
system = AIEthicsAssessmentSystem()

# 분석할 서비스 선택 (최대 3개)
services = ["ChatGPT", "Claude"]

# 분석 실행
result = system.analyze_services(
    service_names=services,
    output_dir="outputs"
)

print(f"보고서 위치: {result['output_dir']}")
print(f"마크다운: {result['markdown_report'][:500]}...")
```

### 방법 2: Streamlit 웹 인터페이스

```bash
# Streamlit 앱 실행
streamlit run streamlit_app.py
```

웹 브라우저에서 자동으로 열리며, 다음 기능을 제공합니다:

1. **서비스 선택**: 분석할 AI 서비스 선택 (최대 3개)
2. **실시간 진행 상황**: 분석 단계별 진행 모니터링
3. **대시보드**:
   - 종합 평가 대시보드
   - 차원별 상세 평가
   - 개선 권고안
   - 비교 분석
   - 최종 보고서
4. **보고서 다운로드**: 마크다운, PDF, JSON, CSV 형식

### 사용 예시

#### 예시 1: 단일 서비스 분석

```python
from app import AIEthicsAssessmentSystem

system = AIEthicsAssessmentSystem()
result = system.analyze_services(
    service_names=["ChatGPT"],
    output_dir="outputs/chatgpt_analysis"
)
```

**출력**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI 윤리성 리스크 진단 시스템 초기화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔧 도구 초기화 중...
  🤖 에이전트 초기화 중...
  ✅ 초기화 완료!

============================================================
1단계: 서비스 분석
============================================================
🔍 [ChatGPT] 서비스 분석 시작
  📡 정보 수집 중...
     - 검색 결과: 15건
  🤖 LLM 분석 중...
  ✅ 분석 완료
     - 주요 기능: 8개
     - 발견된 이슈: 3개

============================================================
2단계: 윤리 리스크 평가
============================================================
⚖️  [ChatGPT] 윤리 리스크 진단 시작
  📊 공정성 및 편향성 평가 중...
     → LLM 점수: 4/5 (낮음)
     → 자동체크: 7/10 통과
  ...
  ✅ 종합 평가: 4.1/5 (리스크 수준: 낮음)

============================================================
3단계: 개선안 제안
============================================================
💡 [ChatGPT] 개선안 제안 생성
  📌 개선 필요 영역: 2개
     - 투명성 및 설명가능성: 3.8/5 (우선순위: 중)
     - 책임성 및 거버넌스: 3.5/5 (우선순위: 상)
  🤖 구체적 개선안 생성 중...
  ✅ 개선안 생성 완료! (2개 영역)

============================================================
5단계: 최종 보고서 작성 (마크다운 + PDF)
============================================================
  📋 Executive Summary 작성 중...
  ✍️  본문 작성 중...
  ✅ 한국어 마크다운 보고서 작성 완료!
  📄 PDF 보고서 생성 중...
  ✅ PDF 보고서 생성 완료!

============================================================
6단계: 결과 저장
============================================================
  📄 마크다운 보고서: outputs/chatgpt_analysis/ethics_assessment_20250123_143022.md
  📄 PDF 보고서: outputs/chatgpt_analysis/ethics_report_20250123_143022.pdf
  💾 상세 데이터: outputs/chatgpt_analysis/ethics_assessment_20250123_143022_data.json
  📊 요약: outputs/chatgpt_analysis/ethics_assessment_20250123_143022_summary.json
```

#### 예시 2: 여러 서비스 비교

```python
system = AIEthicsAssessmentSystem()
result = system.analyze_services(
    service_names=["ChatGPT", "Claude", "Gemini"],
    output_dir="outputs/comparison"
)
```

비교 분석이 포함된 보고서가 생성됩니다:

- 종합 순위
- 차원별 비교
- 강점/약점 분석
- 모범 사례 식별

## 📈 출력 결과

### 1. 마크다운 보고서

```
ethics_assessment_YYYYMMDD_HHMMSS.md
```

- 전체 분석 내용을 마크다운 형식으로 제공
- GitHub, Notion 등에서 바로 활용 가능

### 2. PDF 보고서

```
ethics_report_YYYYMMDD_HHMMSS.pdf
```

- 전문적인 레이아웃의 PDF 보고서
- 차트, 표, 시각화 포함
- 인쇄 및 공유에 최적화

### 3. JSON 데이터

```
ethics_assessment_YYYYMMDD_HHMMSS_data.json
```

- 구조화된 평가 데이터
- 추가 분석 및 통합에 활용 가능

### 4. 요약 JSON

```
ethics_assessment_YYYYMMDD_HHMMSS_summary.json
```

- 핵심 지표 요약
- 대시보드 생성에 활용

## 🎯 고급 사용법

### 커스텀 설정

`config/settings.py`에서 설정 변경 가능:

```python
# LLM 모델 변경
LLM_MODEL = "gpt-4o"  # 또는 "gpt-4-turbo", "gpt-3.5-turbo"

# Temperature 조정 (0.0 - 1.0)
LLM_TEMPERATURE = 0.3  # 낮을수록 일관된 결과

# 분석 서비스 개수 제한
MAX_SERVICES = 3
```

### 프로그래매틱 사용

```python
from app import AIEthicsAssessmentSystem
from utils.state import AssessmentState

# 시스템 초기화
system = AIEthicsAssessmentSystem()

# 상태 관리 객체 생성
state = AssessmentState(service_names=["ChatGPT"])

# 단계별 실행
system._analyze_all_services(state)
system._assess_all_risks(state)
system._suggest_all_improvements(state)

# 결과 확인
print(state.get_summary())
```

### 평가 기준 커스터마이징

`tools/evaluation_tools.py`에서 평가 기준 수정:

```python
ETHICS_CRITERIA = {
    "fairness": {
        "name": "공정성 및 편향성",
        "weight": 1.2,  # 가중치 조정
        "evaluation_points": [
            "알고리즘 편향성 테스트 실시 여부",
            "데이터셋 다양성 및 대표성",
            # 평가 항목 추가/수정
        ]
    },
    # 다른 차원들...
}
```

## 🔧 기술 스택

### 핵심 기술

- **LangChain**: 멀티 에이전트 오케스트레이션
- **OpenAI GPT-4**: LLM 기반 분석 및 평가
- **RAG (Retrieval-Augmented Generation)**: 가이드라인 참조
- **Web Search**: 실시간 정보 수집

### 주요 라이브러리

```
langchain>=0.1.0
langchain-openai>=0.0.5
openai>=1.12.0
chromadb>=0.4.22
streamlit>=1.31.0
plotly>=5.18.0
pandas>=2.2.0
reportlab>=4.0.9
python-dotenv>=1.0.1
```

### UI 프레임워크

- **Streamlit**: 인터랙티브 웹 대시보드
- **Plotly**: 고급 데이터 시각화

## 📊 성능 및 제한사항

### 성능 지표

- **분석 속도**: 서비스당 평균 3-5분
- **정확도**: LLM 기반 평가 + 자동 체크리스트 이중 검증
- **재현성**: Temperature 0.3 설정으로 일관된 결과

### 제한사항

1. **서비스 개수**: 최대 3개 동시 분석
2. **API 비용**: OpenAI API 사용료 발생
3. **정보 의존성**: 공개된 정보 기반 평가
4. **언어**: 한국어 보고서 생성

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.

## 🙏 감사의 말

- EU AI Act, UNESCO, OECD의 윤리 가이드라인 제공
- LangChain 및 OpenAI 커뮤니티
- 오픈소스 기여자들

---

**⚖️ AI 윤리성 리스크 진단 시스템** - 신뢰할 수 있는 AI를 위한 첫걸음

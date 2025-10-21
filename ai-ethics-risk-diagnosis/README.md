# AI Ethics Risk Diagnosis System

본 프로젝트는 **AI 서비스의 윤리성 리스크를 진단**하고 개선 권고안을 제시하는 Multi-Agent 시스템입니다.

## 📋 Overview

- **Objective**: AI 서비스의 윤리적 리스크(편향성, 프라이버시, 투명성 등)를 종합 평가하고 실행 가능한 개선안 제시
- **Methods**: Multi-Agent Architecture (Sequential), RAG, Web Search
- **Tools**: LangGraph, LangChain, FAISS, Tavily Search, OpenAI API

## ✨ Features

- **자동화된 서비스 분석**: 웹 검색을 통한 AI 서비스 정보 수집 및 분석
- **5가지 윤리 기준 평가**: 편향성, 프라이버시, 투명성, 책임성, 안전성
- **가이드라인 기반 평가**: EU AI Act, UNESCO 등 국제 윤리 가이드라인 참조
- **우선순위 기반 개선안**: 리스크 수준에 따른 구체적이고 실행 가능한 권고사항
- **전문 보고서 생성**: Markdown 형식의 상세 진단 보고서 자동 작성

## 🛠 Tech Stack

| Category  | Details                            |
| --------- | ---------------------------------- |
| Framework | LangGraph, LangChain, Python 3.10+ |
| LLM       | GPT-4o-mini via OpenAI API         |
| Retrieval | FAISS                              |
| Embedding | OpenAI text-embedding-3-small      |
| Search    | Tavily API                         |
| Output    | Markdown, JSON                     |

## 🤖 Agents

본 시스템은 4개의 전문 에이전트로 구성되어 있습니다:

1. **Service Analyzer Agent**: AI 서비스의 기능, 데이터 사용 방식 등을 분석
2. **Ethics Evaluator Agent**: 5가지 윤리 기준에 따라 리스크를 평가하고 점수 부여
3. **Improvement Proposer Agent**: 평가 결과를 바탕으로 우선순위별 개선안 제안
4. **Report Writer Agent**: 종합 분석 보고서 작성

## 📊 State

```python
{
    "target_service": str,              # 분석 대상 서비스명
    "service_overview": Dict,           # 서비스 분석 결과
    "ethics_evaluation": Dict,          # 윤리 평가 결과 (5개 기준 + 종합)
    "improvement_proposals": List[Dict], # 개선 제안 목록
    "final_report": str,                # 최종 보고서 (Markdown)
    "references": List[Dict],           # 참조 문서
    "current_step": str,                # 현재 진행 단계
    "errors": List[str]                 # 에러 로그
}
```

## 🏗 Architecture

```
START
  ↓
[Service Analysis]
  ├─ Web Search
  └─ LLM Analysis
  ↓
[Ethics Evaluation]
  ├─ RAG Retrieval (Guidelines)
  ├─ Web Search
  └─ LLM Evaluation (×5 criteria)
  ↓
[Improvement Proposals]
  ├─ Priority Analysis
  └─ LLM Recommendation
  ↓
[Report Generation]
  └─ Comprehensive Report
  ↓
END
```

### Workflow Visualization

워크플로우 그래프는 실행 시 자동으로 `./outputs/workflow_graph.png`에 저장됩니다.

## 📁 Directory Structure

```
ai-ethics-risk-diagnosis/
├── data/
│   ├── guidelines/              # AI 윤리 가이드라인 PDF (EU AI Act, UNESCO 등)
│   └── target_services/         # 서비스 정보 (선택사항)
├── src/
│   ├── config/                  # 설정 파일
│   ├── state/                   # State 정의
│   ├── agents/                  # 4개 에이전트 모듈
│   ├── tools/                   # 도구 함수 (검색, RAG, 점수 계산)
│   ├── prompts/                 # 프롬프트 템플릿
│   ├── graph/                   # LangGraph 워크플로우
│   └── utils/                   # 유틸리티 (PDF 로딩, Vector Store 등)
├── outputs/
│   ├── reports/                 # 생성된 보고서 (.md)
│   ├── evaluations/             # 평가 결과 (.json)
│   └── visualizations/          # 그래프 이미지
├── notebooks/                   # 실험용 노트북
├── tests/                       # 테스트 코드
├── app.py                       # 메인 실행 스크립트
├── requirements.txt
└── README.md
```

## 🚀 Installation

### 1. 저장소 클론 및 가상환경 설정

```bash
git clone <repository-url>
cd ai-ethics-risk-diagnosis

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:

```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. 가이드라인 문서 준비 (선택사항)

RAG 기능을 사용하려면 `./data/guidelines/` 폴더에 윤리 가이드라인 PDF를 추가하세요:

- EU AI Act
- UNESCO Ethics Guidelines
- OECD AI Principles
- 기타 관련 문서

**주의**: 각 문서는 30페이지 이하, 최대 2개 문서 권장

## 💻 Usage

### 기본 실행

```bash
python app.py
```

실행 후 분석할 서비스를 선택하세요:

```
1. ChatGPT
2. GitHub Copilot
3. Midjourney

Select service number to analyze (or 'all' for all services): 1
```

### 분석 대상 서비스 변경

`src/config/settings.py`에서 `TARGET_SERVICES` 수정:

```python
TARGET_SERVICES = [
    "ChatGPT",
    "Claude",
    "Gemini"
]
```

### 평가 기준 커스터마이징

`src/config/settings.py`에서 `ETHICS_CRITERIA` 수정:

```python
ETHICS_CRITERIA = {
    "bias": {
        "name": "편향성 (Bias)",
        "weight": 0.25,
        "description": "AI 시스템의 공정성과 차별 방지"
    },
    # ... 추가 기준
}
```

## 📤 Output

### 1. 평가 보고서 (Markdown)

경로: `./outputs/reports/{service_name}_{timestamp}.md`

구성:

- SUMMARY: 핵심 메시지 요약
- Executive Summary
- 서비스 개요
- 윤리성 평가 결과 (5개 기준)
- 종합 평가
- 개선 권고사항 (우선순위별)
- 결론
- REFERENCES
- APPENDIX

### 2. 평가 데이터 (JSON)

경로: `./outputs/evaluations/{service_name}_{timestamp}.json`

구성:

```json
{
  "service_name": "ChatGPT",
  "timestamp": "2024-01-01T10:00:00",
  "service_overview": {...},
  "ethics_evaluation": {...},
  "improvement_proposals": [...],
  "references": [...]
}
```

### 3. 워크플로우 그래프 (PNG)

경로: `./outputs/workflow_graph.png`

## 🧪 Testing

```bash
# 전체 테스트 실행
python -m pytest tests/

# 특정 테스트 실행
python -m pytest tests/test_agents.py
```

## 🔧 Troubleshooting

### 1. Vector Store 에러

```bash
# Vector Store 재생성
rm -rf ./data/vector_store
python app.py
```

### 2. API 호출 제한

- OpenAI API: Rate limit 확인
- Tavily API: 무료 플랜은 월 1000 요청 제한

### 3. PDF 로딩 실패

- PDF 파일 크기 확인 (30페이지 이하 권장)
- 인코딩 문제: UTF-8 인코딩 확인

## 📝 Configuration

주요 설정은 `src/config/settings.py`에서 관리:

```python
# LLM 설정
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 4000

# 평가 점수 범위
SCORE_RANGE = {
    "high_risk": (0, 3),
    "medium_risk": (3, 6),
    "low_risk": (6, 10)
}

# 분석 대상 서비스 (최대 3개 권장)
TARGET_SERVICES = ["ChatGPT", "GitHub Copilot", "Midjourney"]
```

## 👥 Contributors

- 개발자 이름: Architecture Design, Agent Development, Prompt Engineering

## 📄 License

MIT License

## 🙏 Acknowledgments

- LangChain & LangGraph Community
- OpenAI API
- Tavily Search
- EU AI Act, UNESCO Ethics Guidelines

---

**Note**: 본 프로젝트는 교육 목적으로 개발되었습니다. 실제 윤리성 평가에는 전문가의 검토가 필요합니다.

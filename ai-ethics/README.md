# AI 윤리성 리스크 진단 시스템

본 프로젝트는 AI 서비스의 윤리성 리스크를 진단하고 개선안을 제시하는 멀티 에이전트 시스템입니다.

## Overview

- **Objective**: AI 서비스의 윤리적 리스크(편향성, 프라이버시, 투명성, 책임성)를 종합 평가하고 개선 방안 제시
- **Methods**: Multi-Agent Workflow, RAG, Web Search
- **Tools**: LangGraph, LangChain, FAISS, Tavily Search

## Features

- ✅ 최대 3개 AI 서비스 동시 분석
- ✅ EU AI Act, UNESCO, OECD 가이드라인 기반 평가
- ✅ 4가지 윤리 차원 (편향성, 프라이버시, 투명성, 책임성) 평가
- ✅ 웹 검색 + RAG를 통한 최신 정보 수집
- ✅ 단기/중기/장기 개선안 제시
- ✅ 서비스 간 비교 분석 (2개 이상 시)
- ✅ 전문적인 평가 보고서 자동 생성

## Tech Stack

| Category  | Details                       |
| --------- | ----------------------------- |
| Framework | LangGraph, LangChain, Python  |
| LLM       | GPT-4o-mini via OpenAI API    |
| Retrieval | FAISS                         |
| Embedding | OpenAI text-embedding-3-small |
| Search    | Tavily Search API             |

## Architecture

### Multi-Agent Workflow

```
┌─────────────┐
│ Initialize  │ - 가이드라인 문서 로딩 (RAG)
└──────┬──────┘
       │
       v
┌─────────────────┐
│ Service Analyzer│ - 웹 검색으로 서비스 정보 수집
│                 │ - LLM으로 서비스 분석
└────────┬────────┘
         │ (반복: 각 서비스마다)
         v
┌─────────────────┐
│ Risk Assessor   │ - RAG로 가이드라인 기준 검색
│                 │ - 웹 검색으로 리스크 정보 수집
│                 │ - 4개 차원 평가 (1-5점)
└────────┬────────┘
         │ (반복: 각 서비스마다)
         v
┌──────────────────────┐
│ Improvement Advisor  │ - 리스크 우선순위 결정
│                      │ - 개선안 생성
└──────────┬───────────┘
           │ (반복: 각 서비스마다)
           v
┌──────────────────────┐
│ Service Comparator   │ - 서비스 간 비교 분석
│                      │ - 벤치마킹 포인트 도출
└──────────┬───────────┘
           │
           v
┌──────────────────┐
│ Report Writer    │ - Executive Summary 생성
│                  │ - 최종 보고서 작성
└──────────────────┘
```

## Agents

### 1. Service Analyzer (서비스 분석 에이전트)

- 역할: AI 서비스의 개요, 주요 기능, 데이터 처리 방식 분석
- 도구: Tavily Web Search
- 출력: 서비스 분석 리포트

### 2. Risk Assessor (리스크 평가 에이전트)

- 역할: 4가지 윤리 차원별 리스크 평가 (1-5점)
  - 편향성 (Bias)
  - 프라이버시 (Privacy)
  - 투명성 (Transparency)
  - 책임성 (Accountability)
- 도구: RAG (FAISS), Web Search
- 출력: 차원별 점수 및 근거

### 3. Improvement Advisor (개선안 제안 에이전트)

- 역할: 리스크 평가 기반 개선안 제안, 서비스 간 비교
- 도구: LLM 분석
- 출력: 단기/중기/장기 개선안, 비교 분석

### 4. Report Writer (보고서 작성 에이전트)

- 역할: 최종 평가 보고서 생성
- 출력: Markdown 형식 전문 보고서

## State

| Key                     | Type       | Description                        |
| ----------------------- | ---------- | ---------------------------------- |
| service_names           | List[str]  | 분석 대상 서비스 리스트 (최대 3개) |
| guidelines              | List[str]  | 평가 기준 가이드라인               |
| service_analysis        | Dict       | 서비스별 분석 결과                 |
| risk_assessment         | Dict       | 서비스별 리스크 평가 결과          |
| improvement_suggestions | Dict       | 서비스별 개선안                    |
| comparison_analysis     | str        | 서비스 간 비교 분석                |
| final_report            | str        | 최종 보고서 (Markdown)             |
| references              | List[Dict] | 참고 문헌                          |
| current_service         | str        | 현재 처리 중인 서비스              |

## Installation

### 1. 저장소 클론

```bash
git clone <your-repo-url>
cd ai-ethics-risk-assessment
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env` 파일을 생성하고 API 키를 입력하세요:

```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. 가이드라인 문서 준비

`data/guidelines/` 폴더에 다음 PDF 파일을 준비하세요:

- `eu_ai_act.pdf` (EU AI Act 문서)
- `unesco_ethics.pdf` (UNESCO AI 윤리 가이드)
- `oecd_principles.pdf` (OECD AI 원칙)

각 문서는 30페이지 이내로 준비하세요.

## Usage

### 기본 실행

```bash
python app.py
```

### 실행 예시

```
📋 분석 설정을 입력해주세요.

분석할 AI 서비스를 입력하세요 (최대 3개, 쉼표로 구분):
예시: ChatGPT, Midjourney, GitHub Copilot
>>> ChatGPT, Midjourney

✅ 분석 대상: ChatGPT, Midjourney

사용할 윤리 가이드라인을 선택하세요:
지원 가이드라인: EU AI Act, UNESCO, OECD
여러 개 선택 가능 (쉼표로 구분), 엔터 입력 시 모두 선택
>>>

✅ 평가 기준: EU AI Act, UNESCO, OECD
```

## Output

### 1. 최종 보고서

- 위치: `outputs/reports/ethics_report_YYYYMMDD_HHMMSS.md`
- 형식: Markdown
- 구성:
  - Executive Summary
  - 서비스별 상세 분석
  - 리스크 평가 결과
  - 개선 권고사항
  - 비교 분석 (2개 이상 서비스)
  - References
  - Appendix

### 2. 상세 로그

- 위치: `outputs/logs/result_YYYYMMDD_HHMMSS.json`
- 형식: JSON
- 내용: 전체 분석 데이터 (State 전체)

## Evaluation Criteria

### 평가 척도 (1-5점)

- **5점**: 매우 낮은 리스크 - 양호한 수준
- **4점**: 낮은 리스크 - 장기적 모니터링 필요
- **3점**: 중간 리스크 - 중기적 개선 권장
- **2점**: 높은 리스크 - 단기적 개선 필요
- **1점**: 매우 높은 리스크 - 즉각적인 개선 필요

### 평가 차원

#### 1. 편향성 (Bias) - 가중치 30%

- 학습 데이터의 다양성과 대표성
- 소수 집단에 대한 성능 격차
- 편향 완화 메커니즘
- 정기적인 편향성 테스트

#### 2. 프라이버시 (Privacy) - 가중치 30%

- 개인정보 수집의 적절성
- 데이터 보안 조치
- 사용자 동의 프로세스
- 데이터 권리 보장

#### 3. 투명성 (Transparency) - 가중치 20%

- AI 시스템 작동 원리 공개
- 설명 가능성
- 정보 제공의 충분성
- 감사 가능성

#### 4. 책임성 (Accountability) - 가중치 20%

- 책임 소재의 명확성
- 피해 구제 메커니즘
- 윤리 거버넌스
- 영향 평가

## Directory Structure

```
ai-ethics-risk-assessment/
├── data/
│   ├── guidelines/          # AI 윤리 가이드라인 PDF
│   └── services/            # 서비스 정보 JSON
├── agents/                  # 에이전트 모듈
│   ├── service_analyzer.py
│   ├── risk_assessor.py
│   ├── improvement_advisor.py
│   └── report_writer.py
├── prompts/                 # 프롬프트 템플릿
│   ├── service_analysis.py
│   ├── risk_assessment.py
│   ├── improvement.py
│   └── report_generation.py
├── tools/                   # 도구 함수
│   ├── search_tools.py      # 웹 검색
│   ├── rag_tools.py         # RAG 기능
│   └── evaluation_tools.py  # 평가 로직
├── utils/                   # 유틸리티
│   ├── state.py             # State 정의
│   ├── graph.py             # LangGraph 구조
│   └── helpers.py           # 헬퍼 함수
├── config/                  # 설정
│   ├── settings.py
│   └── ethics_criteria.json
├── outputs/                 # 결과 저장
│   ├── reports/             # 최종 보고서
│   └── logs/                # 실행 로그
├── app.py                   # 메인 실행 스크립트
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Notes

### API 키 관리

- `.env` 파일은 반드시 `.gitignore`에 포함시키세요
- 공개 저장소에 API 키가 노출되지 않도록 주의하세요

### 가이드라인 문서

- PDF 문서는 최대 30페이지 이내로 준비
- 최대 2개 가이드라인 문서 사용 권장 (성능 최적화)

### 성능

- 서비스 1개당 분석 시간: 약 3-5분
- 3개 서비스 + 보고서 생성: 약 15-20분

## Troubleshooting

### 1. PDF 로드 오류

```
FileNotFoundError: data/guidelines/eu_ai_act.pdf
```

**해결**: `data/guidelines/` 폴더에 PDF 파일을 배치하세요.

### 2. API 키 오류

```
openai.error.AuthenticationError
```

**해결**: `.env` 파일에 올바른 API 키가 설정되어 있는지 확인하세요.

### 3. 메모리 오류

**해결**: PDF 문서 크기를 줄이거나, `config/settings.py`에서 `CHUNK_SIZE`를 조정하세요.

## Contributors

- 김철수: Architecture Design, Agent Development
- 이영희: Prompt Engineering, Evaluation Logic

## License

This project is for educational purposes only.

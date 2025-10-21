"""
프로젝트 전역 설정
"""
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LLM 설정
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 4000

# Embedding 설정
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_CHUNK_SIZE = 1000
EMBEDDING_CHUNK_OVERLAP = 200

# Vector Store 설정
VECTOR_STORE_TYPE = "faiss"  # "faiss" or "chroma"
VECTOR_STORE_PATH = "./data/vector_store"

# 분석 대상 AI 서비스 (최대 3개)
TARGET_SERVICES = [
    "ChatGPT",
    "GitHub Copilot",
    "Midjourney"
]

# 윤리 평가 기준
ETHICS_CRITERIA = {
    "bias": {
        "name": "편향성 (Bias)",
        "weight": 0.25,
        "description": "AI 시스템의 공정성과 차별 방지"
    },
    "privacy": {
        "name": "프라이버시 (Privacy)",
        "weight": 0.25,
        "description": "개인정보 보호 및 데이터 처리의 적절성"
    },
    "transparency": {
        "name": "투명성 (Transparency)",
        "weight": 0.20,
        "description": "AI 의사결정 과정의 설명 가능성"
    },
    "accountability": {
        "name": "책임성 (Accountability)",
        "weight": 0.15,
        "description": "AI 시스템의 책임 소재 명확성"
    },
    "safety": {
        "name": "안전성 (Safety)",
        "weight": 0.15,
        "description": "AI 시스템의 안전한 운영과 피해 예방"
    }
}

# 평가 점수 범위
SCORE_RANGE = {
    "high_risk": (0, 3),      # 높은 리스크
    "medium_risk": (3, 6),    # 중간 리스크
    "low_risk": (6, 10)       # 낮은 리스크
}

# 가이드라인 문서 경로
GUIDELINE_PATHS = [
    "./data/guidelines/eu_ai_act.pdf",
    "./data/guidelines/unesco_ethics.pdf"
]

# 출력 경로
OUTPUT_PATHS = {
    "reports": "./outputs/reports",
    "evaluations": "./outputs/evaluations",
    "visualizations": "./outputs/visualizations"
}
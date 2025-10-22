import os
from dotenv import load_dotenv

load_dotenv(override=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LLM Settings
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.3

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-small"
TOP_K_RESULTS = 5

# Service Settings
MAX_SERVICES = 3  # 최대 분석 가능 서비스 수

# Guideline Settings
SUPPORTED_GUIDELINES = ["EU AI Act", "UNESCO", "OECD"]
GUIDELINES_PATH = "data/guidelines"

# Output Settings
REPORTS_PATH = "outputs/reports"
LOGS_PATH = "outputs/logs"

# Ethics Criteria
ETHICS_DIMENSIONS = {
    "bias": {
        "weight": 0.3,
        "description": "편향성 및 차별 리스크",
        "keywords": ["bias", "discrimination", "fairness", "equity"]
    },
    "privacy": {
        "weight": 0.3,
        "description": "개인정보 보호 및 프라이버시",
        "keywords": ["privacy", "data protection", "personal information", "GDPR"]
    },
    "transparency": {
        "weight": 0.2,
        "description": "투명성 및 설명가능성",
        "keywords": ["transparency", "explainability", "interpretability", "black box"]
    },
    "accountability": {
        "weight": 0.2,
        "description": "책임성 및 거버넌스",
        "keywords": ["accountability", "governance", "responsibility", "oversight"]
    }
}
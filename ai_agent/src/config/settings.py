import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent.parent.parent / "tests" / ".env"
load_dotenv(env_path)

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 디렉토리 설정 - 절대 경로 사용
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUT_DIR / "reports"
STATE_DIR = PROJECT_ROOT / "state"

# 디렉토리 생성
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
STATE_DIR.mkdir(exist_ok=True)

# OpenAI 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# LLM 설정
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.3

# Embedding 설정
EMBEDDING_MODEL = "text-embedding-3-small"

# RAG 설정
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 5

# 가이드라인 URL
GUIDELINE_URLS = {
    "EU_AI_ACT": "https://artificialintelligenceact.eu/",
    "UNESCO": "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
    "OECD": "https://oecd.ai/en/ai-principles"
}

print("✓ Configuration loaded successfully")
print(f"  DATA_DIR: {DATA_DIR}")
print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
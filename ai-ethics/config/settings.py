import os
from dotenv import load_dotenv

load_dotenv(override=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LLM Settings
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.3

# Service Limits
MAX_SERVICES = 3

# Ethics Guidelines
ETHICS_GUIDELINES = ["EU AI Act", "UNESCO AI Ethics", "OECD AI Principles"]

# Ethics Dimensions
ETHICS_DIMENSIONS = {
    "fairness": {
        "name": "공정성 및 편향성",
        "description": "AI 시스템이 다양한 사용자 그룹에 대해 공정하게 작동하는지 평가",
        "weight": 1.0
    },
    "privacy": {
        "name": "프라이버시 보호",
        "description": "개인정보 보호 및 데이터 관리의 적절성 평가",
        "weight": 1.0
    },
    "transparency": {
        "name": "투명성 및 설명가능성",
        "description": "AI 시스템의 작동 방식과 의사결정 과정의 투명성 평가",
        "weight": 1.0
    },
    "accountability": {
        "name": "책임성 및 거버넌스",
        "description": "AI 시스템의 책임 소재와 관리 체계 평가",
        "weight": 1.0
    },
    "safety": {
        "name": "안전성 및 보안",
        "description": "AI 시스템의 안전성과 보안 수준 평가",
        "weight": 1.0
    }
}
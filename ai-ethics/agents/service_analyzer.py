from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
import json
from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY
from tools.search_tools import SearchTools
from prompts.service_analysis import SERVICE_ANALYSIS_PROMPT

class ServiceAnalyzer:
    """서비스 분석 에이전트 - AI 서비스 개요 파악"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        self.search_tools = SearchTools()
    
    def analyze_service(self, service_name: str) -> Dict:
        """
        AI 서비스 종합 분석
        - 대상 기능 정리
        - 주요 특징 파악
        - 윤리 관련 정보 수집
        """
        
        print(f"\n{'='*60}")
        print(f"🔍 [{service_name}] 서비스 분석 시작")
        print(f"{'='*60}\n")
        
        # 1. 웹 검색으로 정보 수집
        print(f"  📡 정보 수집 중...")
        overview_results = self.search_tools.search_service_info(
            service_name=service_name,
            query_type="overview"
        )
        
        ethics_results = self.search_tools.search_service_info(
            service_name=service_name,
            query_type="fairness"
        )
        
        privacy_results = self.search_tools.search_service_info(
            service_name=service_name,
            query_type="privacy"
        )
        
        print(f"     - 검색 결과: {len(overview_results) + len(ethics_results) + len(privacy_results)}건")
        
        # 2. LLM으로 종합 분석
        print(f"  🤖 LLM 분석 중...")
        
        overview_info = self._format_search_results(overview_results)
        ethics_info = self._format_search_results(ethics_results + privacy_results)
        
        prompt = SERVICE_ANALYSIS_PROMPT.format(
            service_name=service_name,
            overview_info=overview_info,
            ethics_info=ethics_info
        )
        
        messages = [
            SystemMessage(content="당신은 AI 서비스 분석 전문가입니다. 객관적이고 상세한 분석을 수행하세요."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            analysis = self._parse_analysis(response.content)
            
            # 참고 문헌 추가
            analysis["references"] = overview_results + ethics_results + privacy_results
            analysis["service_name"] = service_name
            
            print(f"  ✅ 분석 완료")
            print(f"     - 주요 기능: {len(analysis.get('service_overview', {}).get('main_features', []))}개")
            print(f"     - 발견된 이슈: {len(analysis.get('ethics_aspects', {}).get('known_issues', []))}개")
            
            return analysis
            
        except Exception as e:
            print(f"  ⚠️  분석 오류: {e}")
            return self._get_default_analysis(service_name, overview_results)
    
    def _format_search_results(self, results: List[Dict]) -> str:
        """검색 결과 포맷팅"""
        if not results:
            return "관련 정보 없음"
        
        formatted = []
        for i, result in enumerate(results[:5], 1):
            formatted.append(
                f"[{i}] {result.get('title', '제목 없음')}\n"
                f"출처: {result.get('url', '')}\n"
                f"내용: {result.get('content', '')[:600]}..."
            )
        
        return "\n\n".join(formatted)
    
    def _parse_analysis(self, content: str) -> Dict:
        """분석 결과 파싱"""
        # JSON 추출
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        return json.loads(content.strip())
    
    def _get_default_analysis(self, service_name: str, references: List[Dict]) -> Dict:
        """기본 분석 결과"""
        return {
            "service_name": service_name,
            "service_overview": {
                "description": f"{service_name}에 대한 자동 분석 실패",
                "main_features": ["정보 수집 필요"],
                "target_users": "알 수 없음",
                "use_cases": []
            },
            "technical_details": {
                "ai_type": "알 수 없음",
                "data_usage": "알 수 없음",
                "model_info": "알 수 없음"
            },
            "ethics_aspects": {
                "public_policies": [],
                "known_issues": [],
                "positive_aspects": []
            },
            "additional_notes": "자동 분석 중 오류 발생. 수동 검토 필요.",
            "references": references
        }

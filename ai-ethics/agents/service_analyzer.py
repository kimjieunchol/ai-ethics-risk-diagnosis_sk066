from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
import json
from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY
from tools.search_tools import SearchTools
from prompts.service_analysis import SERVICE_ANALYSIS_PROMPT

class ServiceAnalyzer:
    """AI 서비스 분석 에이전트"""
    
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
        
        Args:
            service_name: 분석할 AI 서비스 이름
            
        Returns:
            분석 결과 딕셔너리
        """
        print(f"\n{'='*50}")
        print(f"🔍 [{service_name}] 서비스 분석 시작...")
        print(f"{'='*50}\n")
        
        # 1. 여러 측면에서 정보 수집
        collected_info = self._collect_service_info(service_name)
        
        # 2. LLM을 통한 종합 분석
        analysis_result = self._analyze_with_llm(service_name, collected_info)
        
        print(f"✅ [{service_name}] 서비스 분석 완료!\n")
        
        return analysis_result
    
    def _collect_service_info(self, service_name: str) -> Dict[str, List[Dict]]:
        """서비스 정보 수집"""
        info = {}
        
        query_types = ["overview", "ethics", "privacy", "transparency"]
        
        for query_type in query_types:
            print(f"  📡 {query_type} 정보 검색 중...")
            results = self.search_tools.search_service_info(service_name, query_type)
            info[query_type] = results
            print(f"     → {len(results)}개 결과 수집")
        
        return info
    
    def _analyze_with_llm(self, service_name: str, collected_info: Dict) -> Dict:
        """LLM을 통한 정보 분석"""
        print(f"  🤖 LLM 분석 중...")
        
        # 수집된 정보를 텍스트로 포맷팅
        info_text = self._format_collected_info(collected_info)
        
        # 프롬프트 생성
        prompt = SERVICE_ANALYSIS_PROMPT.format(
            service_name=service_name,
            collected_info=info_text
        )
        
        # LLM 호출
        messages = [
            SystemMessage(content="당신은 AI 서비스 분석 전문가입니다."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # JSON 파싱
        try:
            # JSON 코드 블록 제거
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            analysis = json.loads(content.strip())
            return analysis
        
        except json.JSONDecodeError as e:
            print(f"  ⚠️  JSON 파싱 오류: {e}")
            # 기본 구조 반환
            return {
                "overview": response.content[:500],
                "key_features": [],
                "target_users": "알 수 없음",
                "ai_technology": "알 수 없음",
                "data_usage": "알 수 없음",
                "known_issues": []
            }
    
    def _format_collected_info(self, collected_info: Dict) -> str:
        """수집된 정보를 텍스트로 포맷팅"""
        formatted = []
        
        for query_type, results in collected_info.items():
            formatted.append(f"\n## {query_type.upper()} 정보\n")
            
            for i, result in enumerate(results[:3], 1):  # 상위 3개만
                formatted.append(f"### 출처 {i}: {result['title']}")
                formatted.append(f"URL: {result['url']}")
                formatted.append(f"{result['content'][:500]}...\n")
        
        return "\n".join(formatted)
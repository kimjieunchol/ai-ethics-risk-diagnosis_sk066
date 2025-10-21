"""
서비스 분석 에이전트
"""
import json
from typing import Dict
from langchain_openai import ChatOpenAI
from src.state import EthicsRiskState
from src.tools import WebSearchTool
from src.prompts import get_service_analysis_prompt
from src.config import LLM_MODEL, LLM_TEMPERATURE


class ServiceAnalyzerAgent:
    """AI 서비스 분석 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
        self.web_search = WebSearchTool()
    
    def analyze(self, state: EthicsRiskState) -> EthicsRiskState:
        """
        AI 서비스 분석 수행
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태
        """
        print("\n" + "="*50)
        print("🔍 STEP 1: Service Analysis")
        print("="*50)
        
        service_name = state["target_service"]
        print(f"📌 Target Service: {service_name}")
        
        try:
            # 1. 웹 검색으로 서비스 정보 수집
            print(f"\n🌐 Searching information about {service_name}...")
            search_results = self.web_search.search_service_info(service_name)
            
            if not search_results:
                raise ValueError("No search results found")
            
            print(f"✅ Found {len(search_results)} search results")
            
            # 2. LLM을 통한 서비스 분석
            print(f"\n🤖 Analyzing service with LLM...")
            prompt = get_service_analysis_prompt(service_name, search_results)
            
            response = self.llm.invoke(prompt)
            analysis_text = response.content
            
            # JSON 파싱
            # LLM이 ```json ``` 로 감쌀 수 있으므로 제거
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif "```" in analysis_text:
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
            service_overview = json.loads(analysis_text)
            
            print(f"\n✅ Service Analysis Completed")
            print(f"   - Name: {service_overview.get('name')}")
            print(f"   - Features: {len(service_overview.get('key_features', []))} identified")
            
            # State 업데이트
            state["service_overview"] = service_overview
            state["current_step"] = "service_analysis_completed"
            state["messages"].append({
                "role": "assistant",
                "content": f"Service analysis for {service_name} completed successfully."
            })
            
            # 참조 문서 추가
            references = []
            for result in search_results[:3]:
                references.append({
                    "source": result["title"],
                    "url": result["url"],
                    "content": result["content"][:200]
                })
            
            state["references"] = references
            
        except Exception as e:
            error_msg = f"Service analysis failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            state["errors"].append(error_msg)
            state["current_step"] = "service_analysis_failed"
        
        return state


def service_analyzer_node(state: EthicsRiskState) -> EthicsRiskState:
    """서비스 분석 노드"""
    agent = ServiceAnalyzerAgent()
    return agent.analyze(state)
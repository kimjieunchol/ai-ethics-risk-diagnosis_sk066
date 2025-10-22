from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.graph.state import AIEthicsState
from src.prompts.analyst_prompt import get_analyst_prompt
import json
import os


class ServiceAnalystAgent:
    """서비스 분석 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def analyze(self, state: AIEthicsState) -> AIEthicsState:
        """서비스 분석 수행"""
        print("\n🔍 서비스 분석 중...")
        
        prompt = get_analyst_prompt(state)
        
        messages = [
            {"role": "system", "content": "당신은 AI 서비스 분석 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            # JSON 파싱
            analysis = json.loads(response.content)
        except json.JSONDecodeError:
            # JSON이 아닌 경우 텍스트를 구조화
            analysis = {
                "개요": response.content,
                "파싱됨": False
            }
        
        state['service_analysis'] = analysis
        print("✓ 서비스 분석 완료")
        
        return state


def service_analyst_node(state: AIEthicsState) -> AIEthicsState:
    """LangGraph 노드 함수"""
    agent = ServiceAnalystAgent()
    return agent.analyze(state)
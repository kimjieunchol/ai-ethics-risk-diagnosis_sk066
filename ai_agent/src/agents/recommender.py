from langchain_openai import ChatOpenAI
from src.graph.state import AIEthicsState
from src.prompts.recommender_prompt import get_recommender_prompt
import json
import os


class RecommendationAgent:
    """개선 방안 제안 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.4,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def generate_recommendations(self, state: AIEthicsState) -> AIEthicsState:
        """개선 방안 생성"""
        print("\n💡 개선 방안 생성 중...")
        
        prompt = get_recommender_prompt(state)
        
        messages = [
            {"role": "system", "content": "당신은 AI 윤리 컨설턴트로서 실행 가능한 개선 방안을 제공합니다."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            recommendations_data = json.loads(response.content)
        except json.JSONDecodeError:
            recommendations_data = {
                "우선조치사항": ["AI 시스템 전반 재검토"],
                "상세개선방안": [{"영역": "일반", "권고사항": response.content[:500]}],
                "실행로드맵": {},
                "모범사례": []
            }
        
        # State에 저장
        state['priority_actions'] = recommendations_data.get('우선조치사항', [])
        state['recommendations'] = recommendations_data.get('상세개선방안', [])
        
        print(f"✓ {len(state['priority_actions'])}개의 우선 조치사항 생성")
        print(f"✓ {len(state['recommendations'])}개의 상세 개선방안 생성")
        
        return state


def recommendation_node(state: AIEthicsState) -> AIEthicsState:
    """LangGraph 노드 함수"""
    agent = RecommendationAgent()
    return agent.generate_recommendations(state)
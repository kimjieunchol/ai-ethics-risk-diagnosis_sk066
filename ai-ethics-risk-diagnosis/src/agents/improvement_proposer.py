"""
개선안 제안 에이전트
"""
import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from src.state import EthicsRiskState
from src.tools import prioritize_improvements
from src.prompts import get_improvement_proposal_prompt
from src.config import LLM_MODEL, LLM_TEMPERATURE, ETHICS_CRITERIA


class ImprovementProposerAgent:
    """개선안 제안 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
    
    def propose(self, state: EthicsRiskState) -> EthicsRiskState:
        """
        개선안 제안 수행
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태
        """
        print("\n" + "="*50)
        print("💡 STEP 3: Improvement Proposals")
        print("="*50)
        
        service_name = state["target_service"]
        ethics_evaluation = state.get("ethics_evaluation", {})
        
        if not ethics_evaluation:
            state["errors"].append("Ethics evaluation not found")
            return state
        
        try:
            # 우선순위 결정
            priorities = prioritize_improvements(ethics_evaluation)
            
            print(f"\n📋 Priority Analysis:")
            for p in priorities[:3]:  # 상위 3개만 표시
                print(f"   - {p['criterion']}: {p['priority']} priority (score: {p['score']}/10)")
            
            improvement_proposals = []
            
            # 각 기준별 개선안 생성 (우선순위 순)
            for priority_item in priorities:
                criterion = priority_item['criterion']
                priority = priority_item['priority']
                
                # 낮은 우선순위는 스킵 (선택적)
                if priority == "low" and priority_item['score'] >= 7:
                    print(f"\n⏭️  Skipping {criterion} (low priority, good score)")
                    continue
                
                criterion_info = ETHICS_CRITERIA.get(criterion, {})
                evaluation_data = ethics_evaluation.get(criterion, {})
                
                print(f"\n💭 Generating proposal for: {criterion_info.get('name')}")
                
                # LLM을 통한 개선안 생성
                prompt = get_improvement_proposal_prompt(
                    criterion=criterion,
                    criterion_name=criterion_info.get('name', criterion),
                    priority=priority,
                    evaluation_data=evaluation_data,
                    service_name=service_name
                )
                
                response = self.llm.invoke(prompt)
                proposal_text = response.content
                
                # JSON 파싱
                if "```json" in proposal_text:
                    proposal_text = proposal_text.split("```json")[1].split("```")[0].strip()
                elif "```" in proposal_text:
                    proposal_text = proposal_text.split("```")[1].split("```")[0].strip()
                
                proposal = json.loads(proposal_text)
                improvement_proposals.append(proposal)
                
                print(f"   ✅ Proposal generated ({priority} priority)")
            
            print(f"\n{'='*50}")
            print(f"📝 Total Proposals: {len(improvement_proposals)}")
            print(f"{'='*50}")
            
            # State 업데이트
            state["improvement_proposals"] = improvement_proposals
            state["current_step"] = "improvement_proposals_completed"
            state["messages"].append({
                "role": "assistant",
                "content": f"Generated {len(improvement_proposals)} improvement proposals."
            })
            
        except Exception as e:
            error_msg = f"Improvement proposal failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            state["errors"].append(error_msg)
            state["current_step"] = "improvement_proposals_failed"
        
        return state


def improvement_proposer_node(state: EthicsRiskState) -> EthicsRiskState:
    """개선안 제안 노드"""
    agent = ImprovementProposerAgent()
    return agent.propose(state)
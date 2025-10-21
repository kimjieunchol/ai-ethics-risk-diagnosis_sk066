"""
윤리 리스크 평가 에이전트
"""
import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from src.state import EthicsRiskState
from src.tools import WebSearchTool, RAGRetriever
from src.tools import calculate_risk_level, calculate_weighted_score
from src.prompts import get_ethics_evaluation_prompt
from src.config import LLM_MODEL, LLM_TEMPERATURE, ETHICS_CRITERIA


class EthicsEvaluatorAgent:
    """AI 윤리성 평가 에이전트"""
    
    def __init__(self, rag_retriever: RAGRetriever):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
        self.web_search = WebSearchTool()
        self.rag_retriever = rag_retriever
    
    def evaluate(self, state: EthicsRiskState) -> EthicsRiskState:
        """
        윤리성 리스크 평가 수행
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태
        """
        print("\n" + "="*50)
        print("⚖️ STEP 2: Ethics Evaluation")
        print("="*50)
        
        service_name = state["target_service"]
        service_overview = state.get("service_overview", {})
        
        if not service_overview:
            state["errors"].append("Service overview not found")
            return state
        
        try:
            ethics_evaluation = {}
            criterion_scores = {}
            
            # 각 윤리 기준별 평가
            for criterion, criterion_info in ETHICS_CRITERIA.items():
                print(f"\n📊 Evaluating: {criterion_info['name']}")
                
                # 1. 가이드라인 검색
                print(f"   📚 Retrieving guidelines for {criterion}...")
                guidelines = self.rag_retriever.retrieve_for_criterion(
                    criterion,
                    service_context=service_overview.get('description', '')
                )
                
                # 2. 웹 검색
                print(f"   🌐 Searching ethics information...")
                web_results = self.web_search.search_ethics_info(service_name, criterion)
                
                # 3. LLM 평가
                print(f"   🤖 Analyzing with LLM...")
                prompt = get_ethics_evaluation_prompt(
                    criterion=criterion,
                    criterion_info=criterion_info,
                    service_overview=service_overview,
                    guidelines=guidelines,
                    web_search_results=web_results
                )
                
                response = self.llm.invoke(prompt)
                eval_text = response.content
                
                # JSON 파싱
                if "```json" in eval_text:
                    eval_text = eval_text.split("```json")[1].split("```")[0].strip()
                elif "```" in eval_text:
                    eval_text = eval_text.split("```")[1].split("```")[0].strip()
                
                eval_result = json.loads(eval_text)
                
                # 리스크 레벨 계산
                score = eval_result.get("score", 5)
                eval_result["risk_level"] = calculate_risk_level(score)
                
                ethics_evaluation[criterion] = eval_result
                criterion_scores[criterion] = score
                
                print(f"   ✅ Score: {score}/10 ({eval_result['risk_level']})")
                
                # 참조 문서에 가이드라인 추가
                if guidelines and state.get("references"):
                    for guide in guidelines[:1]:  # 각 기준당 1개만
                        state["references"].append({
                            "source": guide["source"],
                            "section": f"Related to {criterion_info['name']}",
                            "content": guide["content"][:200]
                        })
            
            # 종합 점수 계산
            overall_score = calculate_weighted_score(criterion_scores)
            overall_risk_level = calculate_risk_level(overall_score)
            
            ethics_evaluation["overall_score"] = overall_score
            ethics_evaluation["overall_risk_level"] = overall_risk_level
            
            print(f"\n{'='*50}")
            print(f"📈 Overall Score: {overall_score}/10")
            print(f"⚠️  Overall Risk Level: {overall_risk_level}")
            print(f"{'='*50}")
            
            # State 업데이트
            state["ethics_evaluation"] = ethics_evaluation
            state["current_step"] = "ethics_evaluation_completed"
            state["messages"].append({
                "role": "assistant",
                "content": f"Ethics evaluation completed. Overall score: {overall_score}/10"
            })
            
        except Exception as e:
            error_msg = f"Ethics evaluation failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            state["errors"].append(error_msg)
            state["current_step"] = "ethics_evaluation_failed"
        
        return state


def ethics_evaluator_node(state: EthicsRiskState, rag_retriever: RAGRetriever) -> EthicsRiskState:
    """윤리 평가 노드"""
    agent = EthicsEvaluatorAgent(rag_retriever)
    return agent.evaluate(state)
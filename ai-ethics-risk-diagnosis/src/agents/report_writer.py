"""
보고서 작성 에이전트
"""
from langchain_openai import ChatOpenAI
from src.state import EthicsRiskState
from src.prompts import get_report_generation_prompt
from src.utils import save_markdown, generate_filename
from src.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


class ReportWriterAgent:
    """보고서 작성 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0.3,  # 보고서는 조금 더 창의적으로
            max_tokens=LLM_MAX_TOKENS
        )
    
    def write_report(self, state: EthicsRiskState) -> EthicsRiskState:
        """
        최종 보고서 작성
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태
        """
        print("\n" + "="*50)
        print("📄 STEP 4: Report Generation")
        print("="*50)
        
        service_name = state["target_service"]
        service_overview = state.get("service_overview", {})
        ethics_evaluation = state.get("ethics_evaluation", {})
        improvement_proposals = state.get("improvement_proposals", [])
        references = state.get("references", [])
        
        if not all([service_overview, ethics_evaluation, improvement_proposals]):
            state["errors"].append("Incomplete data for report generation")
            return state
        
        try:
            print(f"\n📝 Generating comprehensive report for {service_name}...")
            
            # LLM을 통한 보고서 생성
            prompt = get_report_generation_prompt(
                service_name=service_name,
                service_overview=service_overview,
                evaluation_results=ethics_evaluation,
                improvement_proposals=improvement_proposals,
                references=references
            )
            
            response = self.llm.invoke(prompt)
            report_content = response.content
            
            # Markdown 코드 블록 제거 (있을 경우)
            if "```markdown" in report_content:
                report_content = report_content.split("```markdown")[1].split("```")[0].strip()
            elif report_content.startswith("```") and report_content.endswith("```"):
                report_content = report_content.strip("`").strip()
            
            print(f"\n✅ Report generated ({len(report_content)} characters)")
            
            # 보고서 저장
            filename = generate_filename(service_name, "md")
            filepath = save_markdown(report_content, filename)
            
            print(f"💾 Report saved: {filepath}")
            
            # State 업데이트
            state["final_report"] = report_content
            state["current_step"] = "report_completed"
            state["messages"].append({
                "role": "assistant",
                "content": f"Final report generated and saved to {filepath}"
            })
            
            # 최종 요약 출력
            print(f"\n{'='*50}")
            print(f"✅ DIAGNOSIS COMPLETED")
            print(f"{'='*50}")
            print(f"📊 Service: {service_name}")
            print(f"📈 Overall Score: {ethics_evaluation.get('overall_score')}/10")
            print(f"⚠️  Risk Level: {ethics_evaluation.get('overall_risk_level')}")
            print(f"💡 Proposals: {len(improvement_proposals)}")
            print(f"📄 Report: {filepath}")
            print(f"{'='*50}\n")
            
        except Exception as e:
            error_msg = f"Report generation failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            state["errors"].append(error_msg)
            state["current_step"] = "report_generation_failed"
        
        return state


def report_writer_node(state: EthicsRiskState) -> EthicsRiskState:
    """보고서 작성 노드"""
    agent = ReportWriterAgent()
    return agent.write_report(state)
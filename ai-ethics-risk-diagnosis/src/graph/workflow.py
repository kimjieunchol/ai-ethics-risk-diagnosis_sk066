"""
LangGraph 워크플로우 정의
"""
from typing import Dict
from langgraph.graph import StateGraph, END
from src.state import EthicsRiskState
from src.agents import (
    service_analyzer_node,
    ethics_evaluator_node,
    improvement_proposer_node,
    report_writer_node
)
from src.graph.router import (
    check_service_analysis,
    check_ethics_evaluation,
    check_improvement_proposals
)
from src.utils import VectorStoreManager


def create_workflow(rag_retriever) -> StateGraph:
    """
    AI 윤리성 리스크 진단 워크플로우 생성
    
    Args:
        rag_retriever: RAG 검색기 인스턴스
    
    Returns:
        컴파일된 StateGraph
    """
    
    # StateGraph 생성
    workflow = StateGraph(EthicsRiskState)
    
    # 노드 추가
    workflow.add_node("service_analysis", service_analyzer_node)
    
    # ethics_evaluator는 rag_retriever가 필요하므로 람다로 래핑
    workflow.add_node(
        "ethics_evaluation", 
        lambda state: ethics_evaluator_node(state, rag_retriever)
    )
    
    workflow.add_node("improvement_proposals", improvement_proposer_node)
    workflow.add_node("report_generation", report_writer_node)
    
    # 엣지 추가
    # 시작 -> 서비스 분석
    workflow.set_entry_point("service_analysis")
    
    # 서비스 분석 -> 조건부 라우팅
    workflow.add_conditional_edges(
        "service_analysis",
        check_service_analysis,
        {
            "ethics_evaluation": "ethics_evaluation",
            "end": END
        }
    )
    
    # 윤리 평가 -> 조건부 라우팅
    workflow.add_conditional_edges(
        "ethics_evaluation",
        check_ethics_evaluation,
        {
            "improvement_proposals": "improvement_proposals",
            "end": END
        }
    )
    
    # 개선안 제안 -> 조건부 라우팅
    workflow.add_conditional_edges(
        "improvement_proposals",
        check_improvement_proposals,
        {
            "report_generation": "report_generation",
            "end": END
        }
    )
    
    # 보고서 생성 -> 종료
    workflow.add_edge("report_generation", END)
    
    # 워크플로우 컴파일
    app = workflow.compile()
    
    return app


def visualize_workflow(app, output_path: str = "./outputs/workflow_graph.png"):
    """
    워크플로우 시각화
    
    Args:
        app: 컴파일된 워크플로우
        output_path: 저장 경로
    """
    try:
        from IPython.display import Image, display
        import os
        
        # 그래프 이미지 생성
        graph_image = app.get_graph().draw_mermaid_png()
        
        # 파일로 저장
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(graph_image)
        
        print(f"📊 Workflow graph saved to: {output_path}")
        
        # Jupyter에서 실행 중이면 표시
        try:
            display(Image(graph_image))
        except:
            pass
            
    except Exception as e:
        print(f"⚠️ Could not visualize workflow: {e}")
        print("   (Install: pip install pygraphviz)")


def print_workflow_structure():
    """워크플로우 구조를 텍스트로 출력"""
    print("\n" + "="*60)
    print("🔄 WORKFLOW STRUCTURE")
    print("="*60)
    print("""
    START
      ↓
    [1] Service Analysis
      ├─ Web Search: Service information
      └─ LLM Analysis: Service overview
      ↓
    [2] Ethics Evaluation
      ├─ For each criterion (bias, privacy, transparency, etc.):
      │   ├─ RAG Retrieval: Guideline documents
      │   ├─ Web Search: Ethics information
      │   └─ LLM Evaluation: Score & risk assessment
      └─ Calculate overall score
      ↓
    [3] Improvement Proposals
      ├─ Prioritize issues
      └─ Generate actionable recommendations
      ↓
    [4] Report Generation
      ├─ Compile all results
      └─ Generate comprehensive Markdown report
      ↓
    END
    """)
    print("="*60 + "\n")
from langgraph.graph import StateGraph, END
from src.graph.state import AIEthicsState
from src.agents.service_analyst import service_analyst_node
from src.agents.ethics_evaluator import ethics_evaluator_node
from src.agents.recommender import recommendation_node
from src.agents.report_generator import report_generator_node


def create_ethics_assessment_graph():
    """AI 윤리 평가 그래프 생성"""
    
    # 그래프 초기화
    workflow = StateGraph(AIEthicsState)
    
    # 노드 추가
    workflow.add_node("service_analyst", service_analyst_node)
    workflow.add_node("ethics_evaluator", ethics_evaluator_node)
    workflow.add_node("recommender", recommendation_node)
    workflow.add_node("report_generator", report_generator_node)
    
    # 엣지 정의
    workflow.set_entry_point("service_analyst")
    workflow.add_edge("service_analyst", "ethics_evaluator")
    workflow.add_edge("ethics_evaluator", "recommender")
    workflow.add_edge("recommender", "report_generator")
    workflow.add_edge("report_generator", END)
    
    # 컴파일
    app = workflow.compile()
    
    return app


def visualize_graph(app):
    """그래프 시각화"""
    try:
        from IPython.display import Image, display
        display(Image(app.get_graph().draw_mermaid_png()))
    except Exception as e:
        print(f"Graph visualization failed: {e}")
        print("Graph structure:")
        print("START -> service_analyst -> ethics_evaluator -> recommender -> report_generator -> END")
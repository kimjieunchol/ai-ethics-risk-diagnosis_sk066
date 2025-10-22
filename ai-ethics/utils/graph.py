from langgraph.graph import StateGraph, END
from typing import Dict, List
from utils.state import EthicsAssessmentState
from agents.service_analyzer import ServiceAnalyzer
from agents.risk_assessor import RiskAssessor
from agents.improvement_advisor import ImprovementAdvisor
from agents.report_writer import ReportWriter
from tools.rag_tools import RAGTools

class EthicsAssessmentGraph:
    """AI 윤리성 진단 워크플로우 그래프"""
    
    def __init__(self):
        self.service_analyzer = ServiceAnalyzer()
        self.rag_tools = RAGTools()
        self.risk_assessor = RiskAssessor(self.rag_tools)
        self.improvement_advisor = ImprovementAdvisor()
        self.report_writer = ReportWriter()
        
        # 그래프 구성
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """LangGraph 구성"""
        
        workflow = StateGraph(EthicsAssessmentState)
        
        # 노드 추가
        workflow.add_node("initialize", self.initialize_node)
        workflow.add_node("analyze_service", self.analyze_service_node)
        workflow.add_node("assess_risks", self.assess_risks_node)
        workflow.add_node("suggest_improvements", self.suggest_improvements_node)
        workflow.add_node("compare_services", self.compare_services_node)
        workflow.add_node("generate_report", self.generate_report_node)
        
        # 엣지 정의
        workflow.set_entry_point("initialize")
        
        workflow.add_edge("initialize", "analyze_service")
        workflow.add_conditional_edges(
            "analyze_service",
            self.should_continue_analysis,
            {
                "continue": "analyze_service",
                "done": "assess_risks"
            }
        )
        
        workflow.add_conditional_edges(
            "assess_risks",
            self.should_continue_assessment,
            {
                "continue": "assess_risks",
                "done": "suggest_improvements"
            }
        )
        
        workflow.add_conditional_edges(
            "suggest_improvements",
            self.should_continue_improvements,
            {
                "continue": "suggest_improvements",
                "done": "compare_services"
            }
        )
        
        workflow.add_edge("compare_services", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    # ========== 노드 함수들 ==========
    
    def initialize_node(self, state: EthicsAssessmentState) -> EthicsAssessmentState:
        """초기화 노드"""
        print("\n🚀 AI 윤리성 리스크 진단 시작\n")
        
        # RAG 초기화
        print("📚 윤리 가이드라인 문서 로딩 중...")
        success = self.rag_tools.load_guidelines(state["guidelines"])
        
        if not success:
            print("⚠️  일부 가이드라인 문서를 로드하지 못했습니다.")
        
        # 초기화
        state["service_analysis"] = {}
        state["risk_assessment"] = {}
        state["improvement_suggestions"] = {}
        state["references"] = []
        
        return state
    
    def analyze_service_node(self, state: EthicsAssessmentState) -> EthicsAssessmentState:
        """서비스 분석 노드"""
        # 현재 분석할 서비스 결정
        analyzed = len(state.get("service_analysis", {}))
        if analyzed >= len(state["service_names"]):
            return state
        
        service_name = state["service_names"][analyzed]
        state["current_service"] = service_name
        
        # 서비스 분석 수행
        analysis = self.service_analyzer.analyze_service(service_name)
        
        # State 업데이트
        if "service_analysis" not in state:
            state["service_analysis"] = {}
        
        state["service_analysis"][service_name] = analysis
        
        return state
    
    def assess_risks_node(self, state: EthicsAssessmentState) -> EthicsAssessmentState:
        """리스크 평가 노드"""
        # 현재 평가할 서비스 결정
        assessed = len(state.get("risk_assessment", {}))
        if assessed >= len(state["service_names"]):
            return state
        
        service_name = state["service_names"][assessed]
        state["current_service"] = service_name
        
        service_analysis = state["service_analysis"][service_name]
        
        # 리스크 평가 수행
        assessment = self.risk_assessor.assess_risks(
            service_name=service_name,
            service_analysis=service_analysis,
            guidelines=state["guidelines"]
        )
        
        # State 업데이트
        if "risk_assessment" not in state:
            state["risk_assessment"] = {}
        
        state["risk_assessment"][service_name] = assessment
        
        return state
    
    def suggest_improvements_node(self, state: EthicsAssessmentState) -> EthicsAssessmentState:
        """개선안 제안 노드"""
        # 현재 개선안 생성할 서비스 결정
        improved = len(state.get("improvement_suggestions", {}))
        if improved >= len(state["service_names"]):
            return state
        
        service_name = state["service_names"][improved]
        state["current_service"] = service_name
        
        risk_assessment = state["risk_assessment"][service_name]
        
        # 개선안 생성
        improvements = self.improvement_advisor.suggest_improvements(
            service_name=service_name,
            risk_assessment=risk_assessment
        )
        
        # State 업데이트
        if "improvement_suggestions" not in state:
            state["improvement_suggestions"] = {}
        
        state["improvement_suggestions"][service_name] = improvements
        
        return state
    
    def compare_services_node(self, state: EthicsAssessmentState) -> EthicsAssessmentState:
        """서비스 비교 노드"""
        if len(state["service_names"]) < 2:
            state["comparison_analysis"] = ""
            return state
        
        # 비교 분석 데이터 구성
        services_data = {}
        for service in state["service_names"]:
            services_data[service] = {
                "analysis": state["service_analysis"].get(service, {}),
                "risk_assessment": state["risk_assessment"].get(service, {}),
                "improvements": state["improvement_suggestions"].get(service, [])
            }
        
        # 비교 분석 수행
        comparison = self.improvement_advisor.compare_services(services_data)
        
        state["comparison_analysis"] = comparison
        
        return state
    
    def generate_report_node(self, state: EthicsAssessmentState) -> EthicsAssessmentState:
        """보고서 생성 노드"""
        
        # 최종 보고서 생성
        final_report = self.report_writer.generate_report(
            services=state["service_names"],
            service_analyses=state["service_analysis"],
            risk_assessments=state["risk_assessment"],
            improvement_suggestions=state["improvement_suggestions"],
            comparison_analysis=state.get("comparison_analysis", ""),
            references=state.get("references", [])
        )
        
        state["final_report"] = final_report
        
        return state
    
    # ========== 조건 함수들 ==========
    
    def should_continue_analysis(self, state: EthicsAssessmentState) -> str:
        """다음 서비스 분석 계속 여부"""
        analyzed = len(state.get("service_analysis", {}))
        total = len(state["service_names"])
        
        print(f"  📊 진행 상황: {analyzed}/{total} 서비스 분석 완료")
        
        if analyzed < total:
            return "continue"
        
        return "done"
    
    def should_continue_assessment(self, state: EthicsAssessmentState) -> str:
        """다음 서비스 평가 계속 여부"""
        assessed = len(state.get("risk_assessment", {}))
        total = len(state["service_names"])
        
        print(f"  📊 진행 상황: {assessed}/{total} 서비스 평가 완료")
        
        if assessed < total:
            return "continue"
        
        return "done"
    
    def should_continue_improvements(self, state: EthicsAssessmentState) -> str:
        """다음 서비스 개선안 계속 여부"""
        improved = len(state.get("improvement_suggestions", {}))
        total = len(state["service_names"])
        
        print(f"  📊 진행 상황: {improved}/{total} 서비스 개선안 완료")
        
        if improved < total:
            return "continue"
        
        return "done"
    
    def run(self, initial_state: Dict) -> Dict:
        """그래프 실행"""
        return self.graph.invoke(initial_state)
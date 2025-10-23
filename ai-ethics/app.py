import os
from typing import List
from datetime import datetime

from config.settings import MAX_SERVICES
from tools.rag_tools import RAGTools
from agents.service_analyzer import ServiceAnalyzer
from agents.risk_assessor import RiskAssessor
from agents.improvement_advisor import ImprovementAdvisor
from agents.report_writer import ReportWriter
from utils.state import AssessmentState
from utils.helpers import save_json, print_section


class AIEthicsAssessmentSystem:
    """
    AI 윤리성 리스크 진단 시스템
    
    에이전트 구성:
    1. ServiceAnalyzer: AI 서비스 개요 파악 (대상 기능 정리, 주요 특징)
    2. RiskAssessor: 편향성, 개인정보, 설명가능성 등 윤리성 항목별 리스크 평가
    3. ImprovementAdvisor: 윤리성 강화 위한 구체적 개선 방향 제안
    4. ReportWriter: 진단 결과 및 권고사항 리포트 생성 (마크다운 + PDF)
    """
    
    def __init__(self):
        print_section("AI 윤리성 리스크 진단 시스템 초기화", char="#")
        
        # 도구 초기화
        print("  🔧 도구 초기화 중...")
        self.rag_tools = RAGTools()
        
        # 에이전트 초기화
        print("  🤖 에이전트 초기화 중...")
        self.service_analyzer = ServiceAnalyzer()
        self.risk_assessor = RiskAssessor(self.rag_tools)
        self.improvement_advisor = ImprovementAdvisor()
        self.report_writer = ReportWriter()
        
        print("  ✅ 초기화 완료!\n")
    
    def analyze_services(
        self, 
        service_names: List[str],
        output_dir: str = "outputs"
    ) -> dict:
        """
        여러 AI 서비스 분석 및 보고서 생성
        
        Args:
            service_names: 분석할 서비스 목록 (최대 3개)
            output_dir: 출력 디렉토리
        
        Returns:
            결과 딕셔너리 (markdown, pdf_path 포함)
        """
        
        # 검증
        if len(service_names) > MAX_SERVICES:
            raise ValueError(f"최대 {MAX_SERVICES}개 서비스까지만 분석 가능합니다.")
        
        if not service_names:
            raise ValueError("최소 1개 서비스를 지정해야 합니다.")
        
        # 상태 초기화
        state = AssessmentState(service_names=service_names)
        state.metadata['start_time'] = datetime.now().isoformat()
        
        print_section(f"분석 시작: {', '.join(service_names)}", char="#")
        
        # 단계별 처리
        try:
            # 1. 서비스 분석
            self._analyze_all_services(state)
            
            # 2. 리스크 평가
            self._assess_all_risks(state)
            
            # 3. 개선안 제안
            self._suggest_all_improvements(state)
            
            # 4. 비교 분석 (2개 이상)
            if len(service_names) >= 2:
                self._compare_services(state)
            
            # 5. 최종 보고서 생성 (마크다운 + PDF)
            report_result = self._generate_final_report(state, output_dir)
            
            # 6. 결과 저장
            self._save_results(state, output_dir, report_result)
            
            state.metadata['end_time'] = datetime.now().isoformat()
            
            print_section("분석 완료!", char="#")
            print(f"  📊 상태 요약:")
            for key, value in state.get_summary().items():
                print(f"     - {key}: {value}")
            
            return {
                'markdown_report': report_result['markdown'],
                'pdf_path': report_result.get('pdf_path'),
                'output_dir': output_dir
            }
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            raise
    
    def _analyze_all_services(self, state: AssessmentState):
        """모든 서비스 분석"""
        print_section("1단계: 서비스 분석", char="=")
        
        for service_name in state.service_names:
            analysis = self.service_analyzer.analyze_service(service_name)
            state.add_service_analysis(service_name, analysis)
    
    def _assess_all_risks(self, state: AssessmentState):
        """모든 서비스 리스크 평가"""
        print_section("2단계: 윤리 리스크 평가", char="=")
        
        for service_name in state.service_names:
            analysis = state.service_analyses[service_name]
            assessment = self.risk_assessor.assess_risks(service_name, analysis)
            state.add_risk_assessment(service_name, assessment)
    
    def _suggest_all_improvements(self, state: AssessmentState):
        """모든 서비스 개선안 제안"""
        print_section("3단계: 개선안 제안", char="=")
        
        for service_name in state.service_names:
            assessment = state.risk_assessments[service_name]
            improvements = self.improvement_advisor.suggest_improvements(
                service_name, assessment
            )
            state.add_improvements(service_name, improvements)
    
    def _compare_services(self, state: AssessmentState):
        """서비스 비교 분석"""
        print_section("4단계: 서비스 비교 분석", char="=")
        
        services_data = {
            name: {
                'analysis': state.service_analyses[name],
                'risk_assessment': state.risk_assessments[name],
                'improvements': state.improvement_suggestions[name]
            }
            for name in state.service_names
        }
        
        comparison = self.improvement_advisor.compare_services(services_data)
        state.comparison_analysis = comparison
    
    def _generate_final_report(self, state: AssessmentState, output_dir: str) -> dict:
        """최종 보고서 생성 (마크다운 + PDF)"""
        print_section("5단계: 최종 보고서 작성 (마크다운 + PDF)", char="=")
        
        report_result = self.report_writer.generate_report(
            services=state.service_names,
            service_analyses=state.service_analyses,
            risk_assessments=state.risk_assessments,
            improvement_suggestions=state.improvement_suggestions,
            comparison_analysis=state.comparison_analysis,
            output_dir=output_dir
        )
        
        return report_result
    
    def _save_results(self, state: AssessmentState, output_dir: str, report_result: dict):
        """결과 저장"""
        print_section("6단계: 결과 저장", char="=")
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"ethics_assessment_{timestamp}"
        
        # 마크다운 보고서 저장
        report_path = os.path.join(output_dir, f"{base_name}.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_result['markdown'])
        print(f"  📄 마크다운 보고서: {report_path}")
        
        # PDF 경로 출력
        if report_result.get('pdf_path'):
            print(f"  📄 PDF 보고서: {report_result['pdf_path']}")
        
        # 상세 데이터 저장 (JSON)
        data_path = os.path.join(output_dir, f"{base_name}_data.json")
        save_json({
            'metadata': state.metadata,
            'services': state.service_names,
            'service_analyses': state.service_analyses,
            'risk_assessments': state.risk_assessments,
            'improvement_suggestions': state.improvement_suggestions,
            'comparison_analysis': state.comparison_analysis
        }, data_path)
        print(f"  💾 상세 데이터: {data_path}")
        
        # 요약 저장
        summary_path = os.path.join(output_dir, f"{base_name}_summary.json")
        save_json(state.get_summary(), summary_path)
        print(f"  📊 요약: {summary_path}")


# ============================================
# 실행 예시
# ============================================
def main():
    """메인 실행 함수"""
    
    # 시스템 초기화
    system = AIEthicsAssessmentSystem()
    
    # 분석할 서비스 목록 (최대 3개)
    services_to_analyze = [
        "ChatGPT",
        "Claude"
    ]
    
    try:
        # 분석 실행
        result = system.analyze_services(
            service_names=services_to_analyze,
            output_dir="outputs"
        )
        
        print("\n" + "="*60)
        print("✅ 분석이 성공적으로 완료되었습니다!")
        print("="*60)
        print(f"\n📁 출력 디렉토리: {result['output_dir']}")
        print(f"📄 마크다운 보고서: {result['output_dir']}/ethics_assessment_*.md")
        if result.get('pdf_path'):
            print(f"📄 PDF 보고서: {result['pdf_path']}")
        
        # 보고서 미리보기
        print("\n" + "-"*60)
        print("📋 보고서 미리보기 (처음 500자):")
        print("-"*60)
        print(result['markdown_report'][:500] + "...")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
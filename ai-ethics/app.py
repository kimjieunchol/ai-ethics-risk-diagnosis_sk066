import os
from dotenv import load_dotenv
from utils.graph import EthicsAssessmentGraph
from utils.helpers import (
    validate_service_names,
    validate_guidelines,
    save_report,
    save_json,
    get_timestamp,
    print_section_header,
    print_section_footer
)
from config.settings import MAX_SERVICES, SUPPORTED_GUIDELINES

# 환경변수 로드
load_dotenv(override=True)

def main():
    """메인 실행 함수"""
    
    print_section_header("AI 윤리성 리스크 진단 시스템")
    
    # ========== 1. 사용자 입력 ==========
    print("📋 분석 설정을 입력해주세요.\n")
    
    # 분석 대상 서비스 입력
    print(f"분석할 AI 서비스를 입력하세요 (최대 {MAX_SERVICES}개, 쉼표로 구분):")
    print("예시: ChatGPT, Midjourney, GitHub Copilot")
    services_input = input(">>> ").strip()
    
    service_names = [s.strip() for s in services_input.split(",") if s.strip()]
    
    # 유효성 검사
    if not validate_service_names(service_names, MAX_SERVICES):
        return
    
    print(f"\n✅ 분석 대상: {', '.join(service_names)}")
    
    # 가이드라인 선택
    print(f"\n사용할 윤리 가이드라인을 선택하세요:")
    print(f"지원 가이드라인: {', '.join(SUPPORTED_GUIDELINES)}")
    print("여러 개 선택 가능 (쉼표로 구분), 엔터 입력 시 모두 선택")
    guidelines_input = input(">>> ").strip()
    
    if not guidelines_input:
        guidelines = SUPPORTED_GUIDELINES
    else:
        guidelines = [g.strip() for g in guidelines_input.split(",") if g.strip()]
    
    # 유효성 검사
    if not validate_guidelines(guidelines, SUPPORTED_GUIDELINES):
        return
    
    print(f"\n✅ 평가 기준: {', '.join(guidelines)}")
    
    print_section_footer()
    
    # ========== 2. 초기 State 구성 ==========
    initial_state = {
        "service_names": service_names,
        "guidelines": guidelines,
        "service_analysis": {},
        "risk_assessment": {},
        "improvement_suggestions": {},
        "comparison_analysis": "",
        "final_report": None,
        "references": [],
        "messages": [],
        "current_service": None
    }
    
    # ========== 3. 그래프 실행 ==========
    print_section_header("분석 시작")
    
    try:
        graph = EthicsAssessmentGraph()
        
        print("🔄 워크플로우 실행 중...\n")
        result_state = graph.run(initial_state)
        
        print_section_footer()
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # ========== 4. 결과 저장 ==========
    print_section_header("결과 저장")
    
    timestamp = get_timestamp()
    
    # 최종 보고서 저장
    if result_state.get("final_report"):
        report_filename = f"ethics_report_{timestamp}.md"
        report_path = save_report(
            content=result_state["final_report"],
            filename=report_filename
        )
        print(f"📄 보고서: {report_path}")
    
    # 전체 결과 JSON 저장
    result_data = {
        "timestamp": timestamp,
        "services": result_state["service_names"],
        "guidelines": result_state["guidelines"],
        "service_analysis": result_state.get("service_analysis", {}),
        "risk_assessment": result_state.get("risk_assessment", {}),
        "improvement_suggestions": result_state.get("improvement_suggestions", {}),
        "comparison_analysis": result_state.get("comparison_analysis", "")
    }
    
    json_filename = f"outputs/logs/result_{timestamp}.json"
    save_json(result_data, json_filename)
    print(f"💾 상세 결과: {json_filename}")
    
    print_section_footer()
    
    # ========== 5. 요약 출력 ==========
    print_section_header("분석 요약")
    
    print("📊 평가 결과 요약:\n")
    
    for service_name in result_state["service_names"]:
        assessment = result_state["risk_assessment"].get(service_name, {})
        overall_score = assessment.get("overall_score", 0)
        
        print(f"🔹 {service_name}")
        print(f"   종합 점수: {overall_score:.2f}/5.0")
        
        # 각 차원별 점수
        dimensions = ["bias", "privacy", "transparency", "accountability"]
        for dim in dimensions:
            if dim in assessment:
                score = assessment[dim].get("score", 0)
                risk_level = assessment[dim].get("risk_level", "알 수 없음")
                
                dim_names = {
                    "bias": "편향성",
                    "privacy": "프라이버시",
                    "transparency": "투명성",
                    "accountability": "책임성"
                }
                
                print(f"   - {dim_names[dim]}: {score}/5 ({risk_level})")
        
        print()
    
    print_section_footer()
    
    print("✅ 모든 작업이 완료되었습니다!\n")
    print(f"📁 보고서 위치: outputs/reports/")
    print(f"📁 상세 로그: outputs/logs/\n")

if __name__ == "__main__":
    main()
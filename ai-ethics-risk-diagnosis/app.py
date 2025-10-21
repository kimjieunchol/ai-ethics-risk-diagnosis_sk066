"""
AI 윤리성 리스크 진단 시스템 - 메인 실행 스크립트
"""
import os
import sys
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import (
    TARGET_SERVICES,
    GUIDELINE_PATHS,
    VECTOR_STORE_PATH,
    OUTPUT_PATHS
)
from src.state import EthicsRiskState
from src.utils import (
    load_pdf_documents,
    VectorStoreManager,
    save_json,
    generate_filename
)
from src.tools import RAGRetriever
from src.graph import create_workflow, print_workflow_structure


def setup_vector_store() -> VectorStoreManager:
    """
    Vector Store 초기화
    
    Returns:
        VectorStoreManager 인스턴스
    """
    print("\n" + "="*60)
    print("🔧 SETUP: Vector Store Initialization")
    print("="*60)
    
    vsm = VectorStoreManager()
    
    # 기존 Vector Store가 있으면 로드
    if os.path.exists(VECTOR_STORE_PATH):
        print(f"\n📂 Loading existing vector store from {VECTOR_STORE_PATH}")
        try:
            vsm.load_vector_store()
            print("✅ Vector store loaded successfully")
            return vsm
        except Exception as e:
            print(f"⚠️ Could not load vector store: {e}")
            print("   Creating new vector store...")
    
    # 새로운 Vector Store 생성
    print("\n📚 Loading guideline documents...")
    
    # 가이드라인 문서 확인
    available_guidelines = [path for path in GUIDELINE_PATHS if os.path.exists(path)]
    
    if not available_guidelines:
        print("⚠️ No guideline documents found!")
        print("   Please add PDF files to ./data/guidelines/")
        print("   Expected files:")
        for path in GUIDELINE_PATHS:
            print(f"     - {path}")
        print("\n   Continuing without RAG functionality...")
        return vsm
    
    print(f"   Found {len(available_guidelines)} guideline documents")
    
    # 문서 로드 및 Vector Store 생성
    documents = load_pdf_documents(available_guidelines)
    
    if documents:
        vsm.create_vector_store(documents)
        vsm.save_vector_store()
        print("\n✅ Vector store created and saved")
    else:
        print("\n⚠️ No documents loaded for vector store")
    
    return vsm


def create_initial_state(service_name: str) -> EthicsRiskState:
    """
    초기 State 생성
    
    Args:
        service_name: 분석 대상 AI 서비스명
    
    Returns:
        초기화된 EthicsRiskState
    """
    return {
        "target_service": service_name,
        "messages": [
            {
                "role": "user",
                "content": f"Analyze ethics risks for {service_name}"
            }
        ],
        "service_overview": None,
        "ethics_evaluation": None,
        "improvement_proposals": None,
        "final_report": None,
        "references": [],
        "current_step": "initialized",
        "errors": []
    }


def run_diagnosis(service_name: str, workflow_app):
    """
    단일 서비스에 대한 윤리성 진단 실행
    
    Args:
        service_name: 분석 대상 AI 서비스명
        workflow_app: 컴파일된 워크플로우
    """
    print("\n" + "="*60)
    print(f"🎯 DIAGNOSIS START: {service_name}")
    print("="*60)
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 초기 State 생성
    initial_state = create_initial_state(service_name)
    
    try:
        # 워크플로우 실행
        final_state = workflow_app.invoke(initial_state)
        
        # 결과 저장
        if final_state.get("final_report"):
            # 평가 결과를 JSON으로 저장
            evaluation_data = {
                "service_name": service_name,
                "timestamp": datetime.now().isoformat(),
                "service_overview": final_state.get("service_overview"),
                "ethics_evaluation": final_state.get("ethics_evaluation"),
                "improvement_proposals": final_state.get("improvement_proposals"),
                "references": final_state.get("references")
            }
            
            json_filename = generate_filename(service_name, "json")
            save_json(evaluation_data, json_filename, "evaluations")
        
        # 에러 확인
        if final_state.get("errors"):
            print(f"\n⚠️ Completed with errors:")
            for error in final_state["errors"]:
                print(f"   - {error}")
        
        print(f"\n⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return final_state
        
    except Exception as e:
        print(f"\n❌ Diagnosis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """메인 실행 함수"""
    print("\n" + "="*60)
    print("🤖 AI ETHICS RISK DIAGNOSIS SYSTEM")
    print("="*60)
    print(f"Version: 1.0")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)
    
    # 출력 디렉토리 생성
    for path in OUTPUT_PATHS.values():
        os.makedirs(path, exist_ok=True)
    
    # Vector Store 초기화
    vsm = setup_vector_store()
    rag_retriever = RAGRetriever(vsm)
    
    # 워크플로우 생성
    print("\n🔄 Creating workflow...")
    workflow_app = create_workflow(rag_retriever)
    print("✅ Workflow created successfully")
    
    # 워크플로우 구조 출력
    print_workflow_structure()
    
    # 분석 대상 서비스 선택
    print("\n📋 Available Services for Analysis:")
    for i, service in enumerate(TARGET_SERVICES, 1):
        print(f"   {i}. {service}")
    
    print(f"\n💡 Tip: You can modify TARGET_SERVICES in src/config/settings.py")
    print(f"   Current limit: {len(TARGET_SERVICES)} services (recommended: max 3)")
    
    # 사용자 입력 받기
    print("\n" + "="*60)
    choice = input("Select service number to analyze (or 'all' for all services): ").strip()
    
    if choice.lower() == 'all':
        selected_services = TARGET_SERVICES
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(TARGET_SERVICES):
                selected_services = [TARGET_SERVICES[idx]]
            else:
                print(f"❌ Invalid choice. Please select 1-{len(TARGET_SERVICES)}")
                return
        except ValueError:
            print("❌ Invalid input. Please enter a number or 'all'")
            return
    
    # 선택된 서비스들에 대해 진단 실행
    results = []
    for service in selected_services:
        result = run_diagnosis(service, workflow_app)
        results.append({
            "service": service,
            "success": result is not None and not result.get("errors"),
            "state": result
        })
        
        # 서비스 간 구분선
        if len(selected_services) > 1:
            print("\n" + "-"*60 + "\n")
    
    # 최종 요약
    print("\n" + "="*60)
    print("📊 DIAGNOSIS SUMMARY")
    print("="*60)
    
    for result in results:
        status = "✅ Success" if result["success"] else "❌ Failed"
        print(f"{status} - {result['service']}")
        
        if result["success"] and result["state"]:
            score = result["state"].get("ethics_evaluation", {}).get("overall_score", "N/A")
            risk = result["state"].get("ethics_evaluation", {}).get("overall_risk_level", "N/A")
            print(f"         Score: {score}/10, Risk: {risk}")
    
    print("\n" + "="*60)
    print(f"📁 Reports saved to: {OUTPUT_PATHS['reports']}")
    print(f"📁 Evaluations saved to: {OUTPUT_PATHS['evaluations']}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
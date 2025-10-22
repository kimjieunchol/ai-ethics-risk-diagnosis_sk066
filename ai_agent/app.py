#!/usr/bin/env python3
"""
AI 윤리성 리스크 진단 시스템
메인 애플리케이션 진입점
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

from src.graph.workflow import create_ethics_assessment_graph
from src.graph.state import AIEthicsState
from src.tools.guideline_crawler import GuidelineCrawler
from src.tools.rag_retriever import GuidelineRetriever
from src.utils.file_handler import FileHandler
from src.config.settings import DATA_DIR
import json


def setup_guidelines():
    """가이드라인 수집 및 벡터 스토어 구축"""
    print("=" * 60)
    print("1단계: AI 윤리 가이드라인 설정")
    print("=" * 60)
    
    # 절대 경로로 변환
    data_dir = Path(DATA_DIR).resolve()
    
    # 가이드라인 파일 확인
    guideline_files = [
        data_dir / "eu_ai_act.json",
        data_dir / "unesco_ethics.json",
        data_dir / "oecd_principles.json"
    ]
    
    if not all(f.exists() for f in guideline_files):
        print("\n📥 AI 윤리 가이드라인 수집 중...")
        crawler = GuidelineCrawler(output_dir=str(data_dir))
        crawler.crawl_all()
    else:
        print("\n✓ 가이드라인이 이미 수집되었습니다")
    
    # 벡터 스토어 구축
    print("\n🔨 벡터 스토어 구축 중...")
    retriever = GuidelineRetriever(data_dir=str(data_dir))
    
    vectorstore_path = data_dir / "vectorstore"
    
    # index.faiss 파일 존재 여부로 확인
    if (vectorstore_path / "index.faiss").exists():
        print("✓ 벡터 스토어가 이미 존재합니다")
        try:
            retriever.load_vectorstore(str(vectorstore_path))
        except Exception as e:
            print(f"기존 벡터 스토어 로드 실패: {e}")
            print("새로 구축합니다...")
            retriever.build_vectorstore()
            retriever.save_vectorstore(str(vectorstore_path))
    else:
        print("새로운 벡터 스토어를 구축합니다...")
        retriever.build_vectorstore()
        retriever.save_vectorstore(str(vectorstore_path))
    
    print("\n✓ 설정 완료!\n")


def run_assessment(service_info: dict):
    """AI 윤리 평가 실행"""
    print("=" * 60)
    print("2단계: AI 윤리성 리스크 진단 실행")
    print("=" * 60)
    
    # 초기 상태 생성
    initial_state: AIEthicsState = {
        "service_name": service_info['name'],
        "service_description": service_info['description'],
        "service_features": service_info['features'],
        "target_users": service_info.get('target_users', '일반 대중'),
        "data_types": service_info.get('data_types', ['사용자 데이터']),
        "service_analysis": {},
        "bias_risk": {},
        "privacy_risk": {},
        "transparency_risk": {},
        "fairness_risk": {},
        "safety_risk": {},
        "accountability_risk": {},
        "retrieved_guidelines": [],
        "overall_risk_score": 0.0,
        "risk_level": "알 수 없음",
        "high_risk_areas": [],
        "recommendations": [],
        "priority_actions": [],
        "references": [],
        "final_report": ""
    }
    
    # 그래프 생성 및 실행
    print("\n🚀 평가 워크플로우 시작...\n")
    app = create_ethics_assessment_graph()
    
    # 평가 실행
    final_state = app.invoke(initial_state)
    
    # 결과 저장
    print("\n" + "=" * 60)
    print("3단계: 결과 저장")
    print("=" * 60)
    
    file_handler = FileHandler()
    state_path = file_handler.save_state(final_state)
    print(f"\n✓ 상태 저장 완료: {state_path}")
    
    # 최종 보고서 출력
    print("\n" + "=" * 60)
    print("평가 완료")
    print("=" * 60)
    print(f"\n📊 종합 리스크 점수: {final_state['overall_risk_score']}/100")
    print(f"⚠️  리스크 수준: {final_state['risk_level']}")
    print(f"\n🎯 고위험 영역:")
    for area in final_state.get('high_risk_areas', []):
        print(f"   - {area}")
    
    print(f"\n💡 우선 조치사항:")
    for i, action in enumerate(final_state.get('priority_actions', [])[:3], 1):
        print(f"   {i}. {action}")
    
    print(f"\n📄 전체 보고서 위치: outputs/reports/")
    
    return final_state


def main():
    """메인 실행 함수"""
    print("\n" + "=" * 60)
    print(" AI 윤리성 리스크 진단 시스템")
    print("=" * 60 + "\n")
    
    # 1. 가이드라인 설정
    setup_guidelines()
    
    # 2. 평가할 서비스 정보 입력
    service_info = {
        "name": "AI 채용 심사 시스템",
        "description": """
        지원서와 이력서를 자동으로 분석하여 최적의 후보자를 식별하는 AI 기반 시스템입니다. 
        머신러닝을 사용하여 이력서를 분석하고, 핵심 정보를 추출하며, 직무 요구사항에 따라 
        지원자의 순위를 매깁니다. 채용 담당자에게 상위 후보자 명단을 제공합니다.
        """,
        "features": [
            "자동 이력서 파싱 및 정보 추출",
            "직무 요구사항 기반 지원자 순위 매김",
            "스킬 매칭 및 평가",
            "자동화된 1차 심사 결정",
            "지원자 추적 시스템 통합"
        ],
        "target_users": "인사팀 및 채용 담당자",
        "data_types": [
            "개인정보 (이름, 연락처, 인구통계정보)",
            "학력 배경",
            "경력 이력",
            "기술 및 자격증"
        ]
    }
    
    print("📋 평가 대상 서비스:")
    print(f"   서비스명: {service_info['name']}")
    print(f"   설명: {service_info['description'].strip()[:100]}...")
    print()
    
    # 3. 평가 실행
    final_state = run_assessment(service_info)
    
    print("\n" + "=" * 60)
    print("✅ 평가가 성공적으로 완료되었습니다!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
from langchain_openai import ChatOpenAI
from src.graph.state import AIEthicsState
from src.prompts.evaluator_prompt import get_evaluator_prompt
from src.tools.rag_retriever import GuidelineRetriever
from src.config.settings import DATA_DIR
from pathlib import Path
import json
import os
from typing import Dict, List


class EthicsRiskEvaluator:
    """윤리 리스크 평가 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 올바른 data 경로 사용
        data_dir = Path(DATA_DIR).resolve()
        self.retriever = GuidelineRetriever(data_dir=str(data_dir))
        
        # vectorstore 경로 지정
        vectorstore_path = data_dir / "vectorstore"
        
        # vectorstore 로드
        if (vectorstore_path / "index.faiss").exists():
            print(f"  벡터 스토어 로드: {vectorstore_path}")
            self.retriever.load_vectorstore(str(vectorstore_path))
        else:
            print(f"  경고: 벡터 스토어를 찾을 수 없습니다: {vectorstore_path}")
            print(f"  setup_guidelines()를 먼저 실행해야 합니다.")
            raise ValueError("벡터 스토어가 초기화되지 않았습니다. setup_guidelines()를 먼저 실행하세요.")
        
        self.risk_categories = {
            'bias': '편향성 및 차별',
            'privacy': '개인정보 보호',
            'transparency': '투명성 및 설명가능성',
            'fairness': '공정성',
            'safety': '안전성 및 보안',
            'accountability': '책임성 및 거버넌스'
        }
    
    def evaluate_risk_category(
        self, 
        service_analysis: Dict, 
        category: str,
        category_name: str
    ) -> Dict:
        """특정 카테고리의 리스크 평가"""
        print(f"  {category_name} 평가 중...")
        
        # 관련 가이드라인 검색
        guidelines = self.retriever.retrieve_by_category(category, k=4)
        
        # 프롬프트 생성
        prompt = get_evaluator_prompt(
            service_analysis=service_analysis,
            guidelines=guidelines,
            risk_category=category_name
        )
        
        messages = [
            {"role": "system", "content": "당신은 AI 윤리 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            risk_assessment = json.loads(response.content)
        except json.JSONDecodeError:
            risk_assessment = {
                "리스크_점수": 50,
                "리스크_수준": "중간",
                "발견사항": [{"이슈": response.content[:500]}],
                "규정_갭": [],
                "주요_우려사항": []
            }
        
        # 가이드라인 참조 추가
        risk_assessment['검색된_가이드라인'] = guidelines
        
        return risk_assessment
    
    def evaluate_all(self, state: AIEthicsState) -> AIEthicsState:
        """모든 리스크 카테고리 평가"""
        print("\n⚖️ 윤리 리스크 평가 중...")
        
        service_analysis = state.get('service_analysis', {})
        retrieved_guidelines = []
        
        # 각 카테고리별 평가
        for category, category_name in self.risk_categories.items():
            risk_assessment = self.evaluate_risk_category(
                service_analysis,
                category,
                category_name
            )
            
            # State에 저장
            state[f'{category}_risk'] = risk_assessment
            
            # 가이드라인 수집
            if '검색된_가이드라인' in risk_assessment:
                retrieved_guidelines.extend(risk_assessment['검색된_가이드라인'])
        
        # 중복 제거
        state['retrieved_guidelines'] = retrieved_guidelines
        
        # 종합 리스크 점수 계산
        risk_scores = [
            state.get(f'{cat}_risk', {}).get('리스크_점수', 0)
            for cat in self.risk_categories.keys()
        ]
        overall_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        state['overall_risk_score'] = round(overall_score, 2)
        
        # 리스크 레벨 결정
        if overall_score >= 80:
            state['risk_level'] = "매우 높음"
        elif overall_score >= 60:
            state['risk_level'] = "높음"
        elif overall_score >= 40:
            state['risk_level'] = "중간"
        else:
            state['risk_level'] = "낮음"
        
        # 고위험 영역 식별
        high_risk_areas = []
        for category, category_name in self.risk_categories.items():
            risk_data = state.get(f'{category}_risk', {})
            if risk_data.get('리스크_점수', 0) >= 60:
                high_risk_areas.append(category_name)
        
        state['high_risk_areas'] = high_risk_areas
        
        print(f"✓ 종합 리스크 점수: {overall_score:.1f}/100 ({state['risk_level']})")
        
        return state


def ethics_evaluator_node(state: AIEthicsState) -> AIEthicsState:
    """LangGraph 노드 함수"""
    evaluator = EthicsRiskEvaluator()
    return evaluator.evaluate_all(state)
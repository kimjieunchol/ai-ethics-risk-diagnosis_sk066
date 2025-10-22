from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
import json
from config.settings import (
    LLM_MODEL, 
    LLM_TEMPERATURE, 
    OPENAI_API_KEY,
    ETHICS_DIMENSIONS
)
from tools.rag_tools import RAGTools
from tools.search_tools import SearchTools
from tools.evaluation_tools import EvaluationTools
from prompts.risk_assessment import (
    RISK_ASSESSMENT_PROMPT,
    DIMENSION_CRITERIA_MAP
)

class RiskAssessor:
    """윤리 리스크 진단 에이전트"""
    
    def __init__(self, rag_tools: RAGTools):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        self.rag_tools = rag_tools
        self.search_tools = SearchTools()
        self.eval_tools = EvaluationTools()
    
    def assess_risks(
        self, 
        service_name: str, 
        service_analysis: Dict,
        guidelines: List[str]
    ) -> Dict:
        """
        서비스의 윤리 리스크 종합 평가
        
        Args:
            service_name: 서비스명
            service_analysis: 서비스 분석 결과
            guidelines: 평가 기준 가이드라인 리스트
            
        Returns:
            차원별 리스크 평가 결과
        """
        print(f"\n{'='*50}")
        print(f"⚖️  [{service_name}] 윤리 리스크 평가 시작...")
        print(f"{'='*50}\n")
        
        risk_assessment = {}
        
        # 각 윤리 차원별로 평가
        for dimension, config in ETHICS_DIMENSIONS.items():
            print(f"  📊 {dimension}({config['description']}) 평가 중...")
            
            assessment = self._assess_dimension(
                service_name=service_name,
                service_analysis=service_analysis,
                dimension=dimension,
                dimension_description=config['description'],
                guidelines=guidelines
            )
            
            risk_assessment[dimension] = assessment
            print(f"     → 점수: {assessment['score']}/5 ({assessment['risk_level']})")
        
        # 전체 점수 계산
        scores = {dim: data['score'] for dim, data in risk_assessment.items()}
        overall_score = self.eval_tools.calculate_overall_score(scores)
        risk_assessment['overall_score'] = overall_score
        
        print(f"\n  ✅ 종합 점수: {overall_score}/5")
        print(f"{'='*50}\n")
        
        return risk_assessment
    
    def _assess_dimension(
        self,
        service_name: str,
        service_analysis: Dict,
        dimension: str,
        dimension_description: str,
        guidelines: List[str]
    ) -> Dict:
        """특정 윤리 차원에 대한 평가"""
        
        # 1. 가이드라인 컨텍스트 가져오기 (RAG)
        guideline_context = self.rag_tools.get_guideline_context(
            dimension=dimension,
            guidelines=guidelines
        )
        
        # 2. 웹 검색으로 추가 정보 수집
        search_results = self.search_tools.search_service_info(
            service_name=service_name,
            query_type=dimension
        )
        
        search_context = "\n\n".join([
            f"[{r['title']}] {r['content'][:300]}..."
            for r in search_results[:2]
        ])
        
        # 3. 평가 기준
        evaluation_criteria = DIMENSION_CRITERIA_MAP.get(dimension, "")
        
        # 4. LLM을 통한 평가
        prompt = RISK_ASSESSMENT_PROMPT.format(
            service_name=service_name,
            service_analysis=json.dumps(service_analysis, ensure_ascii=False, indent=2),
            dimension=dimension,
            dimension_description=dimension_description,
            guideline_context=guideline_context + "\n\n추가 정보:\n" + search_context,
            evaluation_criteria=evaluation_criteria
        )
        
        messages = [
            SystemMessage(content="당신은 AI 윤리 리스크 평가 전문가입니다."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # JSON 파싱
        try:
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            assessment = json.loads(content.strip())
            
            # 리스크 레벨 자동 계산 (일관성 보장)
            assessment['risk_level'] = self.eval_tools.get_risk_level(assessment['score'])
            
            return assessment
        
        except json.JSONDecodeError as e:
            print(f"    ⚠️  JSON 파싱 오류: {e}")
            # 기본값 반환
            return {
                "score": 3,
                "risk_level": "중간",
                "description": "평가 오류 발생",
                "evidence": [],
                "guideline_compliance": {}
            }
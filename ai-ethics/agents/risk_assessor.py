from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
import json
from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY, ETHICS_GUIDELINES
from tools.rag_tools import RAGTools
from tools.search_tools import SearchTools
from tools.evaluation_tools import EvaluationTools
from prompts.risk_assessment import RISK_ASSESSMENT_PROMPT

class RiskAssessor:
    """윤리 리스크 진단 에이전트 - 편향성, 프라이버시, 투명성 등 평가"""
    
    def __init__(self, rag_tools: RAGTools):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        self.rag_tools = rag_tools
        self.search_tools = SearchTools()
        self.eval_tools = EvaluationTools()
        self.criteria = self.eval_tools.load_ethics_criteria()
    
    def assess_risks(
        self, 
        service_name: str, 
        service_analysis: Dict
    ) -> Dict:
        """서비스의 윤리 리스크 종합 평가"""
        
        print(f"\n{'='*60}")
        print(f"⚖️  [{service_name}] 윤리 리스크 진단 시작")
        print(f"{'='*60}\n")
        
        risk_assessment = {}
        
        # 각 윤리 차원별로 평가
        for dimension, config in self.criteria.items():
            print(f"  📊 {config['name']} 평가 중...")
            
            assessment = self._assess_dimension(
                service_name=service_name,
                service_analysis=service_analysis,
                dimension=dimension,
                dimension_config=config
            )
            
            risk_assessment[dimension] = assessment
            
            # 체크리스트 결과 표시
            auto_check = assessment.get('automated_checks', {})
            print(f"     → LLM 점수: {assessment['score']}/5 ({assessment['risk_level']})")
            print(f"     → 자동체크: {auto_check.get('passed_checks', 0)}/{auto_check.get('total_checks', 0)} 통과")
        
        # 전체 점수 계산
        scores = {dim: data['score'] for dim, data in risk_assessment.items()}
        overall_score = self.eval_tools.calculate_overall_score(scores)
        overall_risk = self.eval_tools.get_risk_level(overall_score)
        
        risk_assessment['overall_score'] = overall_score
        risk_assessment['overall_risk_level'] = overall_risk
        
        print(f"\n  ✅ 종합 평가: {overall_score}/5 (리스크 수준: {overall_risk})")
        print(f"{'='*60}\n")
        
        return risk_assessment
    
    def _assess_dimension(
        self,
        service_name: str,
        service_analysis: Dict,
        dimension: str,
        dimension_config: Dict
    ) -> Dict:
        """특정 윤리 차원에 대한 평가"""
        
        # 1. 자동 체크리스트 평가
        checklist_result = self.eval_tools.automated_checklist_evaluation(
            service_analysis, dimension
        )
        
        # 2. RAG로 가이드라인 컨텍스트 가져오기
        guideline_context = self.rag_tools.get_guideline_context(
            dimension=dimension,
            guidelines=ETHICS_GUIDELINES
        )
        
        # 3. 웹 검색으로 추가 정보 수집
        search_results = self.search_tools.search_service_info(
            service_name=service_name,
            query_type=dimension
        )
        
        search_context = "\n\n".join([
            f"[{r['title']}]\n{r['content'][:500]}..."
            for r in search_results[:2]
        ]) if search_results else "추가 검색 정보 없음"
        
        # 4. 평가 기준 생성
        evaluation_criteria = self._format_evaluation_criteria(dimension_config)
        
        # 5. LLM 평가
        prompt = RISK_ASSESSMENT_PROMPT.format(
            service_name=service_name,
            service_analysis=json.dumps(service_analysis, ensure_ascii=False, indent=2),
            dimension=dimension,
            dimension_description=dimension_config['description'],
            guideline_context=guideline_context,
            search_context=search_context,
            evaluation_criteria=evaluation_criteria
        )
        
        messages = [
            SystemMessage(content="당신은 AI 윤리 리스크 평가 전문가입니다. EU AI Act, UNESCO, OECD 가이드라인을 기반으로 객관적이고 근거 있는 평가를 수행하세요."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            assessment = self._parse_and_validate_assessment(response.content)
            
            # 리스크 레벨 계산
            assessment['risk_level'] = self.eval_tools.get_risk_level(assessment['score'])
            assessment['automated_checks'] = checklist_result
            
            # LLM vs 체크리스트 점수 비교
            score_diff = abs(assessment['score'] - checklist_result['checklist_score'])
            if score_diff > 2:
                print(f"     ⚠️  평가 점수 차이 큼 (LLM: {assessment['score']}, 자동: {checklist_result['checklist_score']:.1f})")
            
            return assessment
            
        except Exception as e:
            print(f"    ⚠️  평가 오류: {e}")
            return self._get_default_assessment(dimension, checklist_result)
    
    def _format_evaluation_criteria(self, config: Dict) -> str:
        """평가 기준 포맷팅"""
        criteria_text = f"{config['name']}\n\n평가 항목:\n"
        
        for i, point in enumerate(config.get('evaluation_points', []), 1):
            criteria_text += f"{i}. {point}\n"
        
        return criteria_text
    
    def _parse_and_validate_assessment(self, content: str) -> Dict:
        """평가 결과 파싱 및 검증"""
        
        # JSON 추출
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        assessment = json.loads(content.strip())
        
        # 필수 필드 검증
        required = ['score', 'description', 'evidence', 'guideline_compliance', 'reasoning']
        for field in required:
            if field not in assessment:
                raise ValueError(f"필수 필드 누락: {field}")
        
        # 점수 검증 및 정규화
        score = assessment['score']
        if not isinstance(score, (int, float)) or score < 1 or score > 5:
            raise ValueError(f"유효하지 않은 점수: {score}")
        
        assessment['score'] = int(round(score))
        
        # 품질 검증
        if len(assessment['evidence']) < 2:
            print("    ⚠️  증거 부족")
        
        if len(assessment['description']) < 100:
            print("    ⚠️  설명 부족")
        
        return assessment
    
    def _get_default_assessment(self, dimension: str, checklist_result: Dict) -> Dict:
        """기본 평가 결과"""
        
        score = 3
        if checklist_result:
            score = max(1, min(5, int(round(checklist_result['checklist_score']))))
        
        return {
            "score": score,
            "risk_level": self.eval_tools.get_risk_level(score),
            "description": f"{dimension} 평가 중 오류 발생. 체크리스트 기반 평가 사용.",
            "evidence": ["자동 평가", "체크리스트 기반"],
            "guideline_compliance": {
                "EU AI Act": "확인 불가",
                "UNESCO": "확인 불가",
                "OECD": "확인 불가"
            },
            "reasoning": "평가 오류로 인한 기본값",
            "risks_identified": ["평가 불가"],
            "strengths": [],
            "automated_checks": checklist_result
        }

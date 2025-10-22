from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
import json
from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY
from tools.evaluation_tools import EvaluationTools
from prompts.improvement import IMPROVEMENT_SUGGESTION_PROMPT, COMPARISON_PROMPT

class ImprovementAdvisor:
    """개선안 제안 에이전트 - 윤리성 강화 위한 구체적 개선 방향 제안"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        self.eval_tools = EvaluationTools()
    
    def suggest_improvements(
        self,
        service_name: str,
        risk_assessment: Dict
    ) -> List[Dict]:
        """리스크 평가 기반 개선안 제안"""
        
        print(f"\n{'='*60}")
        print(f"💡 [{service_name}] 개선안 제안 생성")
        print(f"{'='*60}\n")
        
        # 1. 개선 우선순위 파악
        priority_areas = self.eval_tools.prioritize_improvements(risk_assessment)
        
        if not priority_areas:
            print(f"  ✅ 즉각적인 개선이 필요한 영역 없음 (모든 점수 3.5 이상)")
            return []
        
        print(f"  📌 개선 필요 영역: {len(priority_areas)}개")
        for area in priority_areas:
            print(f"     - {area['dimension']}: {area['current_score']}/5 (우선순위: {area['priority']})")
        
        # 2. LLM으로 개선안 생성
        print(f"\n  🤖 구체적 개선안 생성 중...")
        improvements = self._generate_improvements(
            service_name=service_name,
            risk_assessment=risk_assessment,
            priority_areas=priority_areas
        )
        
        if improvements:
            print(f"  ✅ 개선안 생성 완료! ({len(improvements)}개 영역)")
        
        return improvements
    
    def _generate_improvements(
        self,
        service_name: str,
        risk_assessment: Dict,
        priority_areas: List[Dict]
    ) -> List[Dict]:
        """LLM을 통한 개선안 생성"""
        
        prompt = IMPROVEMENT_SUGGESTION_PROMPT.format(
            service_name=service_name,
            risk_assessment=json.dumps(risk_assessment, ensure_ascii=False, indent=2),
            priority_areas=json.dumps(priority_areas, ensure_ascii=False, indent=2)
        )
        
        messages = [
            SystemMessage(content="당신은 AI 윤리 컨설턴트입니다. 실행 가능하고 구체적이며 측정 가능한 개선안을 제시하세요."),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            improvements = json.loads(content.strip())
            return improvements
        
        except Exception as e:
            print(f"  ⚠️  개선안 생성 오류: {e}")
            return []
    
    def compare_services(
        self,
        services_data: Dict[str, Dict]
    ) -> str:
        """여러 서비스 비교 분석"""
        
        if len(services_data) < 2:
            return ""
        
        print(f"\n{'='*60}")
        print(f"📊 서비스 비교 분석")
        print(f"{'='*60}\n")
        
        services_list = ", ".join(services_data.keys())
        
        # 리스크 평가 결과 추출
        all_assessments = {
            name: data['risk_assessment']
            for name, data in services_data.items()
        }
        
        # 평가 도구로 비교
        comparison_data = self.eval_tools.compare_services(all_assessments)
        
        print(f"  📋 종합 순위:")
        for i, rank in enumerate(comparison_data['service_rankings'], 1):
            print(f"     {i}위: {rank['service']} - {rank['overall_score']}/5 ({rank['risk_level']})")
        
        # LLM 비교 분석
        prompt = COMPARISON_PROMPT.format(
            services_list=services_list,
            all_assessments=json.dumps(all_assessments, ensure_ascii=False, indent=2)
        )
        
        messages = [
            SystemMessage(content="당신은 AI 서비스 비교 분석 전문가입니다. 객관적이고 균형잡힌 통찰을 제공하세요."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        print(f"  ✅ 비교 분석 완료\n")
        
        return response.content

from langchain_openai import ChatOpenAI
from src.graph.state import AIEthicsState
from src.prompts.report_prompt import get_report_prompt
from datetime import datetime
from pathlib import Path
import os


class ReportGeneratorAgent:
    """보고서 생성 에이전트"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def prepare_references(self, state: AIEthicsState) -> list:
        """참고 문헌 정리"""
        guidelines = state.get('retrieved_guidelines', [])
        
        # 중복 제거 및 정리
        references = {}
        for guideline in guidelines:
            source = guideline.get('source', '출처 불명')
            url = guideline.get('url', '')
            if source not in references:
                references[source] = url
        
        return [
            f"- {source}: {url}" if url else f"- {source}"
            for source, url in references.items()
        ]
    
    def format_risk_section(self, risk_data: dict, category_name: str) -> str:
        """리스크 섹션 포맷팅"""
        if not risk_data:
            return f"{category_name} 평가 결과를 사용할 수 없습니다."
        
        section = f"**리스크 점수:** {risk_data.get('리스크_점수', 'N/A')}/100\n\n"
        section += f"**리스크 수준:** {risk_data.get('리스크_수준', '알 수 없음')}\n\n"
        
        findings = risk_data.get('발견사항', [])
        if findings:
            section += "**주요 발견사항:**\n"
            for finding in findings[:3]:  # 상위 3개
                if isinstance(finding, dict):
                    section += f"- {finding.get('이슈', 'N/A')}\n"
                    section += f"  - 심각도: {finding.get('심각도', 'N/A')}\n"
                    section += f"  - 잠재적 피해: {finding.get('잠재적_피해', 'N/A')}\n"
        
        return section
    
    def generate_report(self, state: AIEthicsState) -> AIEthicsState:
        """최종 보고서 생성"""
        print("\n📝 최종 보고서 생성 중...")
        
        # 참고 문헌 준비
        references = self.prepare_references(state)
        state['references'] = references
        
        # 리스크 섹션 포맷팅
        formatted_state = state.copy()
        formatted_state['편향성_리스크_포맷'] = self.format_risk_section(
            state.get('bias_risk', {}), '편향성'
        )
        formatted_state['개인정보_리스크_포맷'] = self.format_risk_section(
            state.get('privacy_risk', {}), '개인정보 보호'
        )
        formatted_state['투명성_리스크_포맷'] = self.format_risk_section(
            state.get('transparency_risk', {}), '투명성'
        )
        formatted_state['공정성_리스크_포맷'] = self.format_risk_section(
            state.get('fairness_risk', {}), '공정성'
        )
        formatted_state['안전성_리스크_포맷'] = self.format_risk_section(
            state.get('safety_risk', {}), '안전성'
        )
        formatted_state['책임성_리스크_포맷'] = self.format_risk_section(
            state.get('accountability_risk', {}), '책임성'
        )
        
        # 날짜 추가
        formatted_state['평가일자'] = datetime.now().strftime('%Y년 %m월 %d일')
        
        # 프롬프트 생성
        prompt = f"""AI 윤리성 리스크 진단 보고서를 마크다운 형식으로 작성해주세요.

서비스명: {state['service_name']}
종합 리스크 점수: {state.get('overall_risk_score', 0)}/100
리스크 수준: {state.get('risk_level', '알 수 없음')}
평가 일자: {formatted_state['평가일자']}

고위험 영역: {', '.join(state.get('high_risk_areas', []))}

서비스 분석:
{state.get('service_analysis', {})}

리스크 평가 결과:

편향성 리스크:
{formatted_state['편향성_리스크_포맷']}

개인정보 보호 리스크:
{formatted_state['개인정보_리스크_포맷']}

투명성 리스크:
{formatted_state['투명성_리스크_포맷']}

공정성 리스크:
{formatted_state['공정성_리스크_포맷']}

안전성 리스크:
{formatted_state['안전성_리스크_포맷']}

책임성 리스크:
{formatted_state['책임성_리스크_포맷']}

우선 조치사항:
{chr(10).join(f"{i+1}. {action}" for i, action in enumerate(state.get('priority_actions', [])))}

개선 방안:
{state.get('recommendations', [])}

참고 문헌:
{chr(10).join(references)}

다음 구조로 전문적이고 체계적인 보고서를 작성해주세요:
1. 요약 (SUMMARY)
2. 각 카테고리별 상세 리스크 분석
3. 실행 가능한 개선 방안
4. 참고 문헌 및 부록

깔끔한 마크다운 형식으로 작성하고, 적절한 헤더, 목록, 표를 사용해주세요.
모든 내용은 한국어로 작성해주세요.
"""
        
        messages = [
            {"role": "system", "content": "당신은 전문 기술 보고서 작성자입니다. 모든 내용을 한국어로 작성합니다."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.invoke(messages)
        report = response.content
        
        state['final_report'] = report
        
        # 보고서 저장
        self.save_report(report, state['service_name'])
        
        print("✓ 최종 보고서 생성 완료")
        
        return state
    
    def save_report(self, report: str, service_name: str):
        """보고서 파일로 저장"""
        output_dir = Path("outputs/reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{service_name.replace(' ', '_')}_{timestamp}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ 보고서 저장 완료: {filepath}")


def report_generator_node(state: AIEthicsState) -> AIEthicsState:
    """LangGraph 노드 함수"""
    agent = ReportGeneratorAgent()
    return agent.generate_report(state)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
from datetime import datetime
import json
from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY
from prompts.report_generation import REPORT_GENERATION_PROMPT, SUMMARY_PROMPT

class ReportWriter:
    """리포트 작성 에이전트 - 진단 결과 및 권고사항 리포트 생성"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
    
    def generate_report(
        self,
        services: List[str],
        service_analyses: Dict[str, Dict],
        risk_assessments: Dict[str, Dict],
        improvement_suggestions: Dict[str, List[Dict]],
        comparison_analysis: str
    ) -> str:
        """최종 보고서 생성"""
        
        print(f"\n{'='*60}")
        print(f"📝 최종 보고서 작성")
        print(f"{'='*60}\n")
        
        # 1. 참고문헌 수집
        all_references = []
        for analysis in service_analyses.values():
            all_references.extend(analysis.get('references', []))
        
        # 2. 메인 보고서 생성
        print(f"  ✍️  본문 작성 중...")
        main_report = self._generate_main_report(
            services=services,
            service_analyses=service_analyses,
            risk_assessments=risk_assessments,
            improvement_suggestions=improvement_suggestions,
            comparison_analysis=comparison_analysis,
            references=all_references
        )
        
        # 3. Executive Summary 생성
        print(f"  📋 Executive Summary 작성 중...")
        summary = self._generate_summary(main_report, services, risk_assessments)
        
        # 4. 최종 조합
        final_report = self._assemble_final_report(
            summary=summary,
            main_report=main_report,
            services=services
        )
        
        print(f"\n  ✅ 보고서 작성 완료!")
        print(f"     - 총 길이: {len(final_report):,} 자")
        print(f"     - 단어 수: {len(final_report.split()):,} 개")
        
        return final_report
    
    def _generate_main_report(
        self,
        services: List[str],
        service_analyses: Dict,
        risk_assessments: Dict,
        improvement_suggestions: Dict,
        comparison_analysis: str,
        references: List[Dict]
    ) -> str:
        """메인 보고서 생성"""
        
        formatted_refs = self._format_references(references)
        
        prompt = REPORT_GENERATION_PROMPT.format(
            services=", ".join(services),
            service_analyses=json.dumps(service_analyses, ensure_ascii=False, indent=2),
            risk_assessments=json.dumps(risk_assessments, ensure_ascii=False, indent=2),
            improvement_suggestions=json.dumps(improvement_suggestions, ensure_ascii=False, indent=2),
            comparison_analysis=comparison_analysis if comparison_analysis else "단일 서비스 분석"
        )
        
        messages = [
            SystemMessage(content="당신은 전문 기술 리포트 작성자입니다. 명확하고 구조화되며 실행 가능한 보고서를 작성하세요."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # 참고문헌 추가
        return response.content + "\n\n---\n\n# 참고 문헌\n\n" + formatted_refs
    
    def _generate_summary(
        self, 
        report_content: str,
        services: List[str],
        risk_assessments: Dict
    ) -> str:
        """Executive Summary 생성"""
        
        # 보고서가 너무 길면 일부만 사용
        if len(report_content) > 10000:
            report_content = report_content[:10000] + "\n...(이하 생략)..."
        
        prompt = SUMMARY_PROMPT.format(report_content=report_content)
        
        messages = [
            SystemMessage(content="당신은 전문 리포트 작성자입니다. 핵심을 간결하고 명확하게 요약하세요."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return response.content
    
    def _assemble_final_report(
        self,
        summary: str,
        main_report: str,
        services: List[str]
    ) -> str:
        """최종 보고서 조합"""
        
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        
        header = f"""# AI 윤리성 리스크 진단 보고서

**분석 대상**: {", ".join(services)}  
**작성일**: {current_date}  
**평가 기준**: EU AI Act, UNESCO AI Ethics, OECD AI Principles

---

"""
        
        executive_summary = f"""# EXECUTIVE SUMMARY

{summary}

---

"""
        
        final_report = header + executive_summary + main_report
        
        return final_report
    
    def _format_references(self, references: List[Dict]) -> str:
        """참고문헌 포맷팅"""
        
        if not references:
            return "참고 자료 없음"
        
        # 중복 제거 (URL 기준)
        unique_refs = {}
        for ref in references:
            url = ref.get('url', '')
            if url and url not in unique_refs:
                unique_refs[url] = ref
        
        # 출처별 분류
        web_refs = [r for r in unique_refs.values() if r.get('source') == 'web']
        
        formatted = []
        
        if web_refs:
            formatted.append("## 웹 검색 자료\n")
            for i, ref in enumerate(web_refs, 1):
                title = ref.get('title', '제목 없음')
                url = ref.get('url', '')
                formatted.append(f"{i}. [{title}]({url})")
        
        return "\n".join(formatted) if formatted else "참고 자료 없음"


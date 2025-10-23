# agents/report_writer.py - 한국어 버전

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List
from datetime import datetime
import json
import os
from config.settings import LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY

try:
    from prompts.report_generation import (
        DETAILED_REPORT_GENERATION_PROMPT,
        SUMMARY_GENERATION_PROMPT
    )
except ImportError:
    DETAILED_REPORT_GENERATION_PROMPT = "한국어로 보고서를 작성하세요."
    SUMMARY_GENERATION_PROMPT = "한국어로 Executive Summary를 작성하세요."

try:
    from tools.report_pdf_enhanced import EnhancedPDFReportGenerator
except ImportError:
    EnhancedPDFReportGenerator = None


class ReportWriter:
    """리포트 작성 에이전트 - 한국어 보고서 생성"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        
        if EnhancedPDFReportGenerator:
            self.pdf_generator = EnhancedPDFReportGenerator()
        else:
            self.pdf_generator = None
    
    def generate_report(
        self,
        services: List[str],
        service_analyses: Dict[str, Dict],
        risk_assessments: Dict[str, Dict],
        improvement_suggestions: Dict[str, List[Dict]],
        comparison_analysis: str,
        output_dir: str = "outputs"
    ) -> Dict[str, str]:
        """최종 보고서 생성"""
        
        print(f"\n{'='*60}")
        print(f"📝 최종 보고서 작성 (한국어)")
        print(f"{'='*60}\n")
        
        # 1. 참고문헌 수집
        all_references = []
        for analysis in service_analyses.values():
            all_references.extend(analysis.get('references', []))
        
        # 2. Executive Summary 생성
        print(f"  📋 Executive Summary 작성 중...")
        summary = self._generate_summary(
            services=services,
            risk_assessments=risk_assessments
        )
        
        # 3. 메인 보고서 생성
        print(f"  ✍️  본문 작성 중...")
        main_report = self._generate_main_report(
            services=services,
            service_analyses=service_analyses,
            risk_assessments=risk_assessments,
            improvement_suggestions=improvement_suggestions
        )
        
        # 4. 최종 조합
        markdown_report = self._assemble_final_report(
            summary=summary,
            main_report=main_report,
            services=services
        )
        
        print(f"\n  ✅ 한국어 마크다운 보고서 작성 완료!")
        
        # 5. PDF 생성
        pdf_path = None
        if self.pdf_generator:
            print(f"  📄 PDF 보고서 생성 중...")
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pdf_path = os.path.join(output_dir, f"ethics_report_{timestamp}.pdf")
                os.makedirs(output_dir, exist_ok=True)
                
                detailed_data = {
                    'service_analyses': service_analyses,
                    'risk_assessments': risk_assessments,
                    'improvement_suggestions': improvement_suggestions
                }
                
                self.pdf_generator.generate_report(
                    output_path=pdf_path,
                    services=services,
                    detailed_data=detailed_data,
                    report_text=markdown_report
                )
                
                print(f"  ✅ PDF 보고서 생성 완료!")
            except Exception as e:
                print(f"  ⚠️  PDF 생성 오류: {e}")
                pdf_path = None
        
        return {
            'markdown': markdown_report,
            'pdf_path': pdf_path
        }
    
    def _generate_summary(self, services: List[str], risk_assessments: Dict) -> str:
        """Executive Summary 생성 (한국어)"""
        try:
            total_score = sum([v['overall_score'] for v in risk_assessments.values()]) / len(services)
            
            system_msg = """당신은 전문 AI 윤리 리포트 작성자입니다.
다음 요구사항을 반드시 지켜주세요:
1. 모든 내용을 한국어로 작성하세요
2. 영어는 서비스명, 인명, 문헌제목에만 사용
3. 명확하고 전문적인 한국어 사용
4. 구체적인 수치와 근거 포함"""
            
            user_msg = f"""다음 AI 서비스들의 평가 결과를 바탕으로 Executive Summary를 한국어로 작성해주세요.

서비스: {', '.join(services)}
평균 점수: {total_score:.1f}/5

각 서비스의 상세 평가:
{json.dumps(risk_assessments, ensure_ascii=False, indent=2)}

Executive Summary 작성 요구사항:
1. 평가 개요 (150자) - 평가 목적, 대상, 기준
2. 주요 발견사항 (300-400자) - 5개 이상의 핵심 포인트
3. 평가 결과 (200-250자) - 종합 리스크, 강점, 약점
4. 최우선 권고 (150-200자) - 즉시 개선 필요 3가지

한국어로 명확하고 전문적으로 작성해주세요."""
            
            messages = [
                SystemMessage(content=system_msg),
                HumanMessage(content=user_msg)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            print(f"요약 생성 오류: {e}")
            return "# Executive Summary\n\n요약 생성에 실패했습니다."
    
    def _generate_main_report(
        self,
        services: List[str],
        service_analyses: Dict,
        risk_assessments: Dict,
        improvement_suggestions: Dict
    ) -> str:
        """메인 보고서 생성 (한국어)"""
        try:
            system_msg = """당신은 전문 AI 윤리 평가 리포트 작성자입니다.
요구사항:
1. 모든 내용을 한국어로 작성하세요
2. 각 서비스에 대해 차원별로 상세히 분석하세요
3. 웹 검색 결과의 내용을 한국어로 번역/요약하세요
4. 구체적인 근거와 데이터를 포함하세요
5. 영어 텍스트가 나오면 한국어로 변환하세요"""
            
            user_msg = f"""다음 데이터를 바탕으로 한국어 보고서를 작성해주세요.

분석 서비스: {', '.join(services)}

서비스 분석:
{json.dumps(service_analyses, ensure_ascii=False, indent=2)}

리스크 평가:
{json.dumps(risk_assessments, ensure_ascii=False, indent=2)}

개선 권고:
{json.dumps(improvement_suggestions, ensure_ascii=False, indent=2)}

다음 구조로 작성해주세요:
1. 평가 방법론 - 각 차원을 한국어로 설명
2. 서비스별 상세 평가 - 각 서비스마다 종합평가 및 차원별 분석 (한국어)
3. 비교 분석 - 서비스 간 비교 (해당시)
4. 종합 권고사항 - 단기/중기/장기 조치 (한국어)

중요: 모든 내용을 한국어로 작성하고, 영어 텍스트가 있으면 한국어로 변환하세요."""
            
            messages = [
                SystemMessage(content=system_msg),
                HumanMessage(content=user_msg)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            print(f"메인 보고서 생성 오류: {e}")
            return "# 보고서\n\n보고서 생성에 실패했습니다."
    
    def _assemble_final_report(
        self,
        summary: str,
        main_report: str,
        services: List[str]
    ) -> str:
        """최종 보고서 조합"""
        
        header = f"""# AI 윤리성 리스크 진단 보고서

**분석 대상**: {', '.join(services)}  
**작성일**: {datetime.now().strftime('%Y년 %m월 %d일')}  
**평가 기준**: EU AI Act, UNESCO AI Ethics, OECD AI Principles

---

"""
        
        footer = f"""

---

# 참고문헌

- 유럽위원회 (2021). '인공지능에 관한 규정(AI Act)' 제안
- 유네스코 (2021). '인공지능 윤리에 관한 권고'
- OECD (2019). 'OECD AI 원칙'
- NIST (2023). 'AI 위험 관리 프레임워크'

---

# 부록

## 평가 등급 기준

| 등급 | 점수 범위 | 위험도 | 정의 |
|------|---------|-------|------|
| A+ | 4.8-5.0 | 매우 낮음 | 모범 사례 |
| A | 4.5-4.7 | 낮음 | 우수 |
| B+ | 4.2-4.4 | 낮음 | 양호 |
| B | 3.8-4.1 | 중간 | 보통 |
| C | 3.0-3.7 | 중간 | 미흡 |
| D | 2.0-2.9 | 높음 | 부족 |
| F | 1.0-1.9 | 매우 높음 | 위험 |

"""
        
        return header + summary + main_report + footer
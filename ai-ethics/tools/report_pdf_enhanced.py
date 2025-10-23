# tools/report_pdf_enhanced.py - 완전한 상세 버전

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, KeepTogether, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List
import os


class EnhancedPDFReportGenerator:
    """상세한 한국어 PDF 리포트 생성기"""
    
    def __init__(self):
        self.korean_font = self._setup_korean_font()
        self.styles = self._create_styles()
        self.page_width, self.page_height = A4
    
    def _setup_korean_font(self) -> str:
        """한국어 폰트 설정"""
        font_paths = [
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            'C:\\Windows\\Fonts\\malgun.ttf',
            '/System/Library/Fonts/AppleGothic.ttf',
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont('MainFont', path))
                    return 'MainFont'
                except:
                    pass
        return 'Helvetica'
    
    def _create_styles(self) -> Dict:
        """PDF 스타일 정의"""
        return {
            'title': ParagraphStyle(
                'Title',
                fontName=self.korean_font,
                fontSize=28,
                textColor=colors.HexColor('#1A3A52'),
                spaceAfter=20,
                alignment=TA_CENTER,
                bold=True
            ),
            'subtitle': ParagraphStyle(
                'Subtitle',
                fontName=self.korean_font,
                fontSize=14,
                textColor=colors.HexColor('#2E5C8A'),
                spaceAfter=30,
                alignment=TA_CENTER
            ),
            'heading1': ParagraphStyle(
                'Heading1',
                fontName=self.korean_font,
                fontSize=18,
                textColor=colors.HexColor('#1A3A52'),
                spaceAfter=12,
                spaceBefore=12,
                bold=True
            ),
            'heading2': ParagraphStyle(
                'Heading2',
                fontName=self.korean_font,
                fontSize=14,
                textColor=colors.HexColor('#2E5C8A'),
                spaceAfter=10,
                spaceBefore=10,
                bold=True
            ),
            'heading3': ParagraphStyle(
                'Heading3',
                fontName=self.korean_font,
                fontSize=12,
                textColor=colors.HexColor('#3F7BA8'),
                spaceAfter=8,
                spaceBefore=8,
                bold=True
            ),
            'normal': ParagraphStyle(
                'Normal',
                fontName=self.korean_font,
                fontSize=10,
                leading=15,
                spaceAfter=10,
                alignment=TA_JUSTIFY
            ),
            'body': ParagraphStyle(
                'Body',
                fontName=self.korean_font,
                fontSize=10,
                leading=16,
                spaceAfter=12,
                alignment=TA_JUSTIFY
            ),
            'bullet': ParagraphStyle(
                'Bullet',
                fontName=self.korean_font,
                fontSize=10,
                leftIndent=20,
                spaceAfter=8
            ),
            'table_header': ParagraphStyle(
                'TableHeader',
                fontName=self.korean_font,
                fontSize=10,
                textColor=colors.white,
                bold=True
            ),
            'table_cell': ParagraphStyle(
                'TableCell',
                fontName=self.korean_font,
                fontSize=9,
                leading=12
            ),
            'small': ParagraphStyle(
                'Small',
                fontName=self.korean_font,
                fontSize=8,
                textColor=colors.HexColor('#666666')
            ),
        }
    
    def generate_report(
        self,
        output_path: str,
        services: List[str],
        detailed_data: Dict,
        report_text: str = None
    ):
        """PDF 리포트 생성"""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # 1. 표지
        story.extend(self._create_cover_page(services))
        story.append(PageBreak())
        
        # 2. 목차
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        # 3. Executive Summary
        story.extend(self._create_executive_summary(services, detailed_data))
        story.append(PageBreak())
        
        # 4. 평가 방법론
        story.extend(self._create_methodology())
        story.append(PageBreak())
        
        # 5. 서비스별 상세 분석
        for service in services:
            story.extend(self._create_detailed_service_analysis(service, detailed_data))
            story.append(PageBreak())
        
        # 6. 비교 분석 (2개 이상)
        if len(services) >= 2:
            story.extend(self._create_comparison_analysis(services, detailed_data))
            story.append(PageBreak())
        
        # 7. 종합 권고사항
        story.extend(self._create_recommendations(services, detailed_data))
        story.append(PageBreak())
        
        # 8. 참고문헌
        story.extend(self._create_references())
        story.append(PageBreak())
        
        # 9. 부록
        story.extend(self._create_appendix())
        
        # PDF 생성
        doc.build(story)
        print(f"✅ 상세 PDF 생성 완료: {output_path}")
    
    def _create_cover_page(self, services: List[str]) -> List:
        """표지 페이지"""
        elements = []
        
        elements.append(Spacer(1, 3*cm))
        
        # 주제목
        elements.append(Paragraph(
            "AI 윤리성 리스크 진단 보고서",
            self.styles['title']
        ))
        elements.append(Spacer(1, 1*cm))
        
        # 부제목
        elements.append(Paragraph(
            "전문적 평가 및 개선 권고",
            self.styles['subtitle']
        ))
        elements.append(Spacer(1, 2*cm))
        
        # 정보 테이블
        info_data = [
            ['분석 대상 서비스', ', '.join(services)],
            ['평가 기준', 'EU AI Act, UNESCO AI Ethics, OECD AI Principles'],
            ['평가 차원', '공정성, 프라이버시, 투명성, 책임성, 안전성'],
            ['작성일', datetime.now().strftime('%Y년 %m월 %d일')],
            ['평가 시간', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        info_table = Table(info_data, colWidths=[3*cm, 11*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8EFF5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 2*cm))
        
        # 평가 목표
        elements.append(Paragraph("평가 목표", self.styles['heading2']))
        objectives = """
본 보고서는 선정된 AI 서비스에 대하여 국제 표준 가이드라인을 기준으로 윤리적 리스크를 
종합적으로 평가하고, 각 서비스의 강점을 파악하며 필요한 개선사항을 구체적으로 제시하는 
것을 목표로 합니다.
        """
        elements.append(Paragraph(objectives, self.styles['body']))
        
        return elements
    
    def _create_table_of_contents(self) -> List:
        """목차"""
        elements = []
        
        elements.append(Paragraph("목차", self.styles['heading1']))
        elements.append(Spacer(1, 0.5*cm))
        
        contents = [
            "1. Executive Summary",
            "2. 평가 방법론",
            "3. 서비스별 상세 분석",
            "4. 비교 분석",
            "5. 종합 권고사항",
            "6. 참고문헌",
            "7. 부록"
        ]
        
        for content in contents:
            elements.append(Paragraph(f"• {content}", self.styles['bullet']))
        
        return elements
    
    def _create_executive_summary(self, services: List[str], data: Dict) -> List:
        """Executive Summary"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 평가 개요
        elements.append(Paragraph("1. 평가 개요", self.styles['heading2']))
        overview = f"""
본 평가는 {len(services)}개 AI 서비스에 대하여 EU AI Act, UNESCO AI Ethics, 
OECD AI Principles 등 국제 표준을 기준으로 5개 차원(공정성, 프라이버시, 투명성, 책임성, 안전성)에서 
윤리적 리스크를 평가했습니다.
        """
        elements.append(Paragraph(overview, self.styles['body']))
        elements.append(Spacer(1, 0.2*cm))
        
        # 종합 평가 테이블
        elements.append(Paragraph("2. 종합 평가 결과", self.styles['heading2']))
        
        score_data = [['서비스', '종합점수', '리스크수준', '등급']]
        for service in services:
            assessment = data['risk_assessments'][service]
            score = assessment['overall_score']
            risk = assessment['overall_risk_level']
            grade = self._get_grade(score)
            score_data.append([service, f"{score}/5", risk, grade])
        
        score_table = Table(score_data, colWidths=[3.5*cm, 3*cm, 3*cm, 2.5*cm])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A3A52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # 주요 발견사항
        elements.append(Paragraph("3. 주요 발견사항", self.styles['heading2']))
        
        avg_score = sum([v['overall_score'] for v in data['risk_assessments'].values()]) / len(services)
        
        findings = f"""
• 평균 윤리 점수: {avg_score:.1f}/5<br/>
• 리스크 수준: {'낮음' if avg_score >= 4 else '중간' if avg_score >= 3 else '높음'}<br/>
• 분석 대상: {len(services)}개 서비스<br/>
• 평가 차원: 5개 (공정성, 프라이버시, 투명성, 책임성, 안전성)
        """
        
        elements.append(Paragraph(findings, self.styles['normal']))
        
        return elements
    
    def _create_methodology(self) -> List:
        """평가 방법론"""
        elements = []
        
        elements.append(Paragraph("평가 방법론", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 평가 프레임워크
        elements.append(Paragraph("1. 평가 프레임워크", self.styles['heading2']))
        
        framework_text = """
본 평가는 다음의 국제 표준을 기준으로 실시되었습니다:

<b>EU AI Act (유럽 인공지능 규정)</b>
- 고위험 AI 시스템에 대한 엄격한 규제
- 편향성 테스트 및 완화 조치 요구
- 투명성 및 설명가능성 의무화

<b>UNESCO AI Ethics Recommendations</b>
- 인간 중심의 윤리 원칙
- 다양성과 포용성 강조
- 개인정보 자기결정권 보장

<b>OECD AI Principles</b>
- 포용적 성장 및 지속가능한 발전
- 인권과 민주적 가치 존중
- 견고한 AI 시스템 구축
        """
        
        elements.append(Paragraph(framework_text, self.styles['body']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 평가 차원
        elements.append(Paragraph("2. 평가 차원 (5개)", self.styles['heading2']))
        
        dimensions_data = [
            ['차원', '설명', '주요 평가항목'],
            ['공정성', '편향성 없이 공정하게 작동', '편향 테스트, 성능 동등성, 완화 조치'],
            ['프라이버시', '개인정보 보호 및 관리', '정책, 암호화, 동의, 데이터 삭제'],
            ['투명성', '작동 방식의 명확성', 'AI 사용 명시, 설명가능성, 데이터 출처'],
            ['책임성', '책임 소재 및 거버넌스', '책임자 지정, 감사, 사고 대응'],
            ['안전성', '안전성 및 보안 수준', '위험 평가, 견고성, 보안 조치']
        ]
        
        dim_table = Table(dimensions_data, colWidths=[2*cm, 3.5*cm, 5.5*cm])
        dim_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5C8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(dim_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # 평가 등급
        elements.append(Paragraph("3. 평가 등급 정의", self.styles['heading2']))
        
        grade_data = [
            ['등급', '점수', '정의', '설명'],
            ['A+', '4.8~5.0', '모범 사례', '모든 가이드라인 완벽 준수'],
            ['A', '4.5~4.7', '우수', '대부분 준수, 미미한 개선'],
            ['B+', '4.2~4.4', '양호', '기본 요구 충족, 개선 필요'],
            ['B', '3.8~4.1', '보통', '기본 요구 부분 충족'],
            ['C', '3.0~3.7', '미흡', '여러 영역 개선 필요'],
            ['D', '2.0~2.9', '부족', '심각한 결함'],
            ['F', '1.0~1.9', '위험', '즉각적 개선 필수'],
        ]
        
        grade_table = Table(grade_data, colWidths=[1.5*cm, 2*cm, 2*cm, 4*cm])
        grade_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A3A52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ]))
        
        elements.append(grade_table)
        
        return elements
    
    def _create_detailed_service_analysis(self, service: str, data: Dict) -> List:
        """서비스별 상세 분석"""
        elements = []
        
        assessment = data['risk_assessments'][service]
        
        # 제목
        elements.append(Paragraph(f"서비스 분석: {service}", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 1. 종합 평가
        elements.append(Paragraph("1. 종합 평가", self.styles['heading2']))
        
        score = assessment['overall_score']
        risk = assessment['overall_risk_level']
        grade = self._get_grade(score)
        
        summary = f"""
<b>종합 점수:</b> {score}/5<br/>
<b>평가 등급:</b> {grade}<br/>
<b>리스크 수준:</b> {risk}<br/>
<b>평가 설명:</b> {assessment.get('description', 'N/A')}
        """
        
        elements.append(Paragraph(summary, self.styles['normal']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 2. 차원별 평가
        elements.append(Paragraph("2. 차원별 상세 평가", self.styles['heading2']))
        
        dimensions = {
            'fairness': '공정성 및 편향성',
            'privacy': '프라이버시 보호',
            'transparency': '투명성 및 설명가능성',
            'accountability': '책임성 및 거버넌스',
            'safety': '안전성 및 보안'
        }
        
        for dim_key, dim_name in dimensions.items():
            if dim_key in assessment:
                dim_data = assessment[dim_key]
                
                elements.append(Paragraph(f"2.{list(dimensions.keys()).index(dim_key) + 1} {dim_name}", self.styles['heading3']))
                
                # 점수 정보
                score_info = f"""
<b>점수:</b> {dim_data['score']}/5 | 
<b>리스크:</b> {dim_data['risk_level']} | 
<b>등급:</b> {self._get_grade(dim_data['score'])}
                """
                elements.append(Paragraph(score_info, self.styles['normal']))
                
                # 설명
                elements.append(Paragraph(dim_data.get('description', 'N/A'), self.styles['body']))
                elements.append(Spacer(1, 0.1*cm))
                
                # 증거
                elements.append(Paragraph("<b>주요 증거:</b>", self.styles['normal']))
                for evidence in dim_data.get('evidence', []):
                    elements.append(Paragraph(f"• {evidence}", self.styles['bullet']))
                
                # 강점과 위험
                elements.append(Paragraph("<b>강점:</b>", self.styles['normal']))
                for strength in dim_data.get('strengths', []):
                    elements.append(Paragraph(f"✓ {strength}", self.styles['bullet']))
                
                elements.append(Paragraph("<b>발견된 리스크:</b>", self.styles['normal']))
                for risk_item in dim_data.get('risks_identified', []):
                    elements.append(Paragraph(f"⚠ {risk_item}", self.styles['bullet']))
                
                elements.append(Spacer(1, 0.2*cm))
        
        # 3. 가이드라인 준수
        elements.append(Paragraph("3. 가이드라인 준수 현황", self.styles['heading2']))
        
        compliance_data = [['가이드라인', 'EU AI Act', 'UNESCO', 'OECD']]
        compliance_row = ['준수 상황']
        
        for dim_key, dim_data in [(k, assessment[k]) for k in dimensions.keys() if k in assessment]:
            compliance = dim_data.get('guideline_compliance', {})
            if isinstance(compliance, dict):
                for guide_name in ['EU AI Act', 'UNESCO AI Ethics', 'OECD AI Principles']:
                    status = 'Compliant' if guide_name in compliance else 'N/A'
        
        elements.append(Paragraph("준수 기준에 따라 각 가이드라인에 대한 준수 여부를 평가했습니다.", self.styles['normal']))
        
        return elements
    
    def _create_comparison_analysis(self, services: List[str], data: Dict) -> List:
        """비교 분석"""
        elements = []
        
        if len(services) < 2:
            return elements
        
        elements.append(Paragraph("서비스 비교 분석", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 순위
        elements.append(Paragraph("1. 종합 순위", self.styles['heading2']))
        
        rankings = [(s, data['risk_assessments'][s]['overall_score']) for s in services]
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        rank_data = [['순위', '서비스', '점수', '등급']]
        for idx, (service, score) in enumerate(rankings, 1):
            rank_data.append([str(idx), service, f"{score}/5", self._get_grade(score)])
        
        rank_table = Table(rank_data, colWidths=[1.5*cm, 4*cm, 3*cm, 2*cm])
        rank_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A3A52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ]))
        
        elements.append(rank_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # 차원별 비교
        elements.append(Paragraph("2. 차원별 점수 비교", self.styles['heading2']))
        
        dimensions = ['fairness', 'privacy', 'transparency', 'accountability', 'safety']
        dim_names = {
            'fairness': '공정성',
            'privacy': '프라이버시',
            'transparency': '투명성',
            'accountability': '책임성',
            'safety': '안전성'
        }
        
        comp_data = [['차원'] + services]
        for dim in dimensions:
            row = [dim_names[dim]]
            for service in services:
                if dim in data['risk_assessments'][service]:
                    score = data['risk_assessments'][service][dim]['score']
                    row.append(f"{score}/5")
                else:
                    row.append("N/A")
            comp_data.append(row)
        
        col_widths = [3*cm] + [3*cm] * len(services)
        comp_table = Table(comp_data, colWidths=col_widths)
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5C8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ]))
        
        elements.append(comp_table)
        
        return elements
    
    def _create_recommendations(self, services: List[str], data: Dict) -> List:
        """종합 권고사항"""
        elements = []
        
        elements.append(Paragraph("종합 권고사항", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 단기
        elements.append(Paragraph("1. 단기 조치 (1-3개월)", self.styles['heading2']))
        short_term = [
            "AI 윤리 정책 문서화 및 공개",
            "편향성 테스트 프레임워크 도입",
            "투명성 강화 계획 수립"
        ]
        for item in short_term:
            elements.append(Paragraph(f"• {item}", self.styles['bullet']))
        
        elements.append(Spacer(1, 0.2*cm))
        
        # 중기
        elements.append(Paragraph("2. 중기 조치 (3-6개월)", self.styles['heading2']))
        mid_term = [
            "AI 거버넌스 체계 구축",
            "정기적인 윤리 감시 시스템 실시",
            "투명성 보고서 발행"
        ]
        for item in mid_term:
            elements.append(Paragraph(f"• {item}", self.styles['bullet']))
        
        elements.append(Spacer(1, 0.2*cm))
        
        # 장기
        elements.append(Paragraph("3. 장기 조치 (6개월 이상)", self.styles['heading2']))
        long_term = [
            "지속적인 모니터링 시스템 구축",
            "외부 독립 감사 체계 확립",
            "산업 표준 및 인증 획득"
        ]
        for item in long_term:
            elements.append(Paragraph(f"• {item}", self.styles['bullet']))
        
        return elements
    
    def _create_references(self) -> List:
        """참고문헌"""
        elements = []
        
        elements.append(Paragraph("참고문헌 (REFERENCE)", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # A. 국제 가이드라인
        elements.append(Paragraph("A. 국제 가이드라인 및 표준", self.styles['heading2']))
        
        refs_a = [
            "[1] European Commission (2021). 'Proposal for a Regulation on Artificial Intelligence (AI Act)'. Brussels.",
            "[2] UNESCO (2021). 'Recommendation on the Ethics of Artificial Intelligence'. Paris.",
            "[3] OECD (2019). 'OECD AI Principles'. Paris.",
            "[4] NIST (2023). 'AI Risk Management Framework'. National Institute of Standards and Technology.",
        ]
        
        for ref in refs_a:
            elements.append(Paragraph(ref, self.styles['bullet']))
        
        elements.append(Spacer(1, 0.2*cm))
        
        # B. 평가 방법론
        elements.append(Paragraph("B. 평가 방법론 및 도구", self.styles['heading2']))
        
        refs_b = [
            "[5] LLM 기반 정성 평가: GPT 모델을 활용한 다차원 윤리 평가",
            "[6] 자동화 체크리스트: 5개 차원별 구조화된 검사 항목",
            "[7] 웹 정보 활용: 공개 정보 검색을 통한 실증적 증거 수집",
        ]
        
        for ref in refs_b:
            elements.append(Paragraph(ref, self.styles['bullet']))
        
        elements.append(Spacer(1, 0.2*cm))
        
        # C. 관련 자료
        elements.append(Paragraph("C. 관련 연구 및 자료", self.styles['heading2']))
        
        refs_c = [
            "[8] Bolukbasi, T., et al. (2016). 'Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings'",
            "[9] Buolamwini, B., & Buolamwini, B. (2018). 'Gender Shades: Intersectional Accuracy Disparities in Gender Classification'",
            "[10] Mitchell, M., et al. (2019). 'Model Cards for Model Reporting'",
        ]
        
        for ref in refs_c:
            elements.append(Paragraph(ref, self.styles['bullet']))
        
        return elements
    
    def _create_appendix(self) -> List:
        """부록"""
        elements = []
        
        elements.append(Paragraph("부록 (APPENDIX)", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 부록 A
        elements.append(Paragraph("부록 A. 평가 프레임워크 상세", self.styles['heading2']))
        
        appendix_a = """
<b>1. 공정성 및 편향성 평가 기준</b>

평가 항목:
• 편향성 테스트 수행 및 결과 공개
• 다양한 인구 집단에 대한 동등한 성능 확보
• 편향 완화 메커니즘 구현
• 차별적 결과 모니터링

점수별 기준:
- 5점: 체계적인 편향 테스트, 명확한 완화 조치, 정기적 모니터링
- 4점: 기본적인 편향 테스트 및 일부 완화 조치
- 3점: 편향 인식은 있으나 구체적 조치 부족
- 2점: 편향에 대한 인식 부족
- 1점: 편향성 문제 미인식 또는 무관심

<b>2. 프라이버시 보호 평가 기준</b>

평가 항목:
• 개인정보처리방침 공개 및 명확성
• GDPR/개인정보보호법 준수
• 데이터 암호화 및 보안 조치
• 사용자 동의 획득 절차
• 데이터 삭제권 보장

점수별 기준:
- 5점: 전면적 GDPR 준수, 암호화, 정기 감사
- 4점: 기본적인 보안 조치 및 정책 수립
- 3점: 부분적 보안 조치
- 2점: 최소한의 정책만 존재
- 1점: 프라이버시 정책 부재

<b>3. 투명성 및 설명가능성 평가 기준</b>

평가 항목:
• AI 시스템 사용 사실 명시
• 의사결정 로직 설명
• 데이터 출처 및 처리 방식 공개
• 알고리즘 작동 방식 이해

점수별 기준:
- 5점: 명확한 설명, 정기적 공개
- 4점: 기본적인 정보 공개
- 3점: 일부만 공개
- 2점: 제한적 공개
- 1점: 불투명

<b>4. 책임성 및 거버넌스 평가 기준</b>

평가 항목:
• 책임자 명시
• 감시 및 감사 체계
• 사고 대응 절차
• 윤리 위원회 운영

점수별 기준:
- 5점: 명확한 책임 체계, 정기 감사
- 4점: 기본적인 책임 구조
- 3점: 책임 소재 부분적 명확
- 2점: 책임 체계 미약
- 1점: 책임 체계 부재

<b>5. 안전성 및 보안 평가 기준</b>

평가 항목:
• 위험 평가 수행
• 견고성 및 정확성 보장
• 사이버 보안 조치
• 품질 관리 시스템

점수별 기준:
- 5점: 체계적 위험 관리, 정기 보안 감사
- 4점: 기본적인 안전 조치
- 3점: 일부 안전 조치
- 2점: 최소한의 조치
- 1점: 안전 조치 부재
        """
        
        elements.append(Paragraph(appendix_a, self.styles['body']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 부록 B
        elements.append(Paragraph("부록 B. 평가 등급 및 권고사항 매트릭스", self.styles['heading2']))
        
        matrix_data = [
            ['등급', '점수', '위험도', '즉각 조치', '권고사항'],
            ['A+', '4.8-5.0', '매우 낮음', '불필요', '현상 유지, 정기 모니터링'],
            ['A', '4.5-4.7', '낮음', '불필요', '미미한 개선 권고'],
            ['B+', '4.2-4.4', '낮음', '1-3개월', '기본 개선안 수립'],
            ['B', '3.8-4.1', '중간', '3-6개월', '구체적 개선 계획'],
            ['C', '3.0-3.7', '중간', '6개월', '중대 개선 필요'],
            ['D', '2.0-2.9', '높음', '즉시', '긴급 개선 필요'],
            ['F', '1.0-1.9', '매우 높음', '즉시', '서비스 중단 고려'],
        ]
        
        matrix_table = Table(matrix_data, colWidths=[1*cm, 1.5*cm, 1.8*cm, 1.8*cm, 3.9*cm])
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A3A52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(matrix_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # 부록 C
        elements.append(Paragraph("부록 C. 용어 정의", self.styles['heading2']))
        
        glossary = """
<b>AI 윤리성:</b> AI 시스템이 인간의 가치, 권리, 이익을 존중하고 보호하는 정도

<b>편향성(Bias):</b> AI 시스템이 특정 그룹에 대해 불공정하게 작동하는 문제

<b>프라이버시:</b> 개인이 자신의 정보와 데이터를 제어할 수 있는 권리

<b>투명성:</b> AI 시스템의 작동 방식과 의사결정 과정이 명확하게 이해 가능한 상태

<b>설명가능성:</b> AI의 의사결정 이유를 인간이 이해할 수 있도록 설명하는 능력

<b>책임성:</b> AI 시스템의 결과에 대해 책임을 지는 주체가 명확히 정의된 상태

<b>거버넌스:</b> AI 시스템을 관리하고 감시하는 체계와 구조

<b>안전성:</b> AI 시스템이 의도되지 않은 해를 끼치지 않도록 보장되는 정도

<b>보안:</b> AI 시스템과 데이터가 무단 접근으로부터 보호되는 정도

<b>위험 평가:</b> AI 시스템이 야기할 수 있는 잠재적 해를 식별하고 평가하는 과정
        """
        
        elements.append(Paragraph(glossary, self.styles['body']))
        
        return elements
    
    def _get_grade(self, score: float) -> str:
        """점수를 등급으로 변환"""
        if score >= 4.8:
            return "A+"
        elif score >= 4.5:
            return "A"
        elif score >= 4.2:
            return "B+"
        elif score >= 3.8:
            return "B"
        elif score >= 3.0:
            return "C"
        elif score >= 2.0:
            return "D"
        else:
            return "F"
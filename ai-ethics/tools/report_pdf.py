from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import Dict, List
import os


class PDFReportGenerator:
    """한국어 PDF 리포트 생성기"""
    
    def __init__(self):
        # 한국어 폰트 등록
        font_path = self._get_korean_font()
        if font_path:
            try:
                pdfmetrics.registerFont(TTFont('NanumGothic', font_path))
                self.korean_font = 'NanumGothic'
                print(f"  ✅ 한국어 폰트 로드 성공: {font_path}")
            except Exception as e:
                print(f"  ⚠️  폰트 로드 실패, 기본 폰트 사용: {e}")
                self.korean_font = 'Helvetica'
        else:
            print("  ⚠️  한국어 폰트를 찾을 수 없습니다. 기본 폰트 사용")
            self.korean_font = 'Helvetica'
        
        self.styles = self._create_styles()
    
    def _get_korean_font(self) -> str:
        """한국어 폰트 경로 찾기"""
        possible_paths = [
            # Linux
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
            # Windows
            'C:\\Windows\\Fonts\\malgun.ttf',
            'C:\\Windows\\Fonts\\gulim.ttc',
            # macOS
            '/System/Library/Fonts/AppleGothic.ttf',
            '/Library/Fonts/NanumGothic.ttf',
            # 프로젝트 내
            'fonts/NanumGothic.ttf',
            '../fonts/NanumGothic.ttf',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _create_styles(self) -> Dict:
        """PDF 스타일 정의"""
        styles = getSampleStyleSheet()
        
        custom_styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontName=self.korean_font,
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=30,
                alignment=1
            ),
            'Heading1': ParagraphStyle(
                'CustomHeading1',
                parent=styles['Heading1'],
                fontName=self.korean_font,
                fontSize=18,
                textColor=colors.HexColor('#34495E'),
                spaceAfter=12,
                spaceBefore=12
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=styles['Heading2'],
                fontName=self.korean_font,
                fontSize=14,
                textColor=colors.HexColor('#5D6D7E'),
                spaceAfter=10,
                spaceBefore=10
            ),
            'Normal': ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName=self.korean_font,
                fontSize=10,
                leading=14,
                spaceAfter=6
            ),
            'Bullet': ParagraphStyle(
                'CustomBullet',
                parent=styles['Normal'],
                fontName=self.korean_font,
                fontSize=10,
                leftIndent=20,
                spaceAfter=6
            )
        }
        
        return custom_styles
    
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
        
        # 4. 서비스별 상세 분석
        for service in services:
            story.extend(self._create_service_analysis(service, detailed_data))
            story.append(PageBreak())
        
        # 5. 비교 분석 (2개 이상)
        if len(services) >= 2:
            story.extend(self._create_comparison_analysis(services, detailed_data))
            story.append(PageBreak())
        
        # 6. 종합 권고사항
        story.extend(self._create_recommendations(services, detailed_data))
        
        # PDF 생성
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        
        return output_path
    
    def _header_footer(self, canvas, doc):
        """헤더/푸터"""
        canvas.saveState()
        canvas.setFont(self.korean_font, 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(
            2*cm, 1*cm,
            f"AI 윤리성 리스크 진단 보고서 | {datetime.now().strftime('%Y-%m-%d')}"
        )
        canvas.drawRightString(
            A4[0] - 2*cm, 1*cm,
            f"페이지 {doc.page}"
        )
        canvas.restoreState()
    
    def _create_cover_page(self, services: List[str]) -> List:
        """표지 페이지"""
        elements = []
        
        title = Paragraph(
            "AI 윤리성 리스크<br/>진단 보고서",
            self.styles['Title']
        )
        elements.append(Spacer(1, 3*cm))
        elements.append(title)
        elements.append(Spacer(1, 1*cm))
        
        service_text = Paragraph(
            f"<b>분석 대상:</b> {', '.join(services)}",
            self.styles['Normal']
        )
        elements.append(service_text)
        elements.append(Spacer(1, 0.5*cm))
        
        date_text = Paragraph(
            f"<b>작성일:</b> {datetime.now().strftime('%Y년 %m월 %d일')}",
            self.styles['Normal']
        )
        elements.append(date_text)
        elements.append(Spacer(1, 1*cm))
        
        criteria_text = Paragraph(
            "<b>평가 기준:</b><br/>" +
            "• EU AI Act<br/>" +
            "• UNESCO AI Ethics Recommendations<br/>" +
            "• OECD AI Principles",
            self.styles['Normal']
        )
        elements.append(criteria_text)
        
        return elements
    
    def _create_table_of_contents(self) -> List:
        """목차"""
        elements = []
        
        elements.append(Paragraph("목차", self.styles['Heading1']))
        elements.append(Spacer(1, 0.5*cm))
        
        toc_items = [
            "1. Executive Summary",
            "2. 서비스별 상세 분석",
            "3. 비교 분석",
            "4. 종합 권고사항"
        ]
        
        for item in toc_items:
            elements.append(Paragraph(item, self.styles['Bullet']))
        
        return elements
    
    def _create_executive_summary(self, services: List[str], data: Dict) -> List:
        """Executive Summary"""
        elements = []
        
        elements.append(Paragraph("1. Executive Summary", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 종합 점수 테이블
        table_data = [['서비스', '종합점수', '리스크수준']]
        
        for service in services:
            assessment = data['risk_assessments'][service]
            score = assessment['overall_score']
            risk = assessment['overall_risk_level']
            table_data.append([service, f"{score}/5", risk])
        
        table = Table(table_data, colWidths=[6*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*cm))
        
        # 주요 발견사항
        elements.append(Paragraph("주요 발견사항", self.styles['Heading2']))
        
        avg_score = sum([data['risk_assessments'][s]['overall_score'] for s in services]) / len(services)
        
        findings = [
            f"• 전체 평균 윤리 점수: {avg_score:.1f}/5",
            f"• 분석 서비스 수: {len(services)}개",
            "• 평가 차원: 공정성, 프라이버시, 투명성, 책임성, 안전성",
        ]
        
        for finding in findings:
            elements.append(Paragraph(finding, self.styles['Bullet']))
        
        return elements
    
    def _create_service_analysis(self, service: str, data: Dict) -> List:
        """서비스별 상세 분석"""
        elements = []
        
        assessment = data['risk_assessments'][service]
        
        elements.append(Paragraph(f"서비스 분석: {service}", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        score_text = Paragraph(
            f"<b>종합 점수:</b> {assessment['overall_score']}/5<br/>" +
            f"<b>리스크 수준:</b> {assessment['overall_risk_level']}",
            self.styles['Normal']
        )
        elements.append(score_text)
        elements.append(Spacer(1, 0.5*cm))
        
        # 차원별 평가 테이블
        elements.append(Paragraph("차원별 상세 평가", self.styles['Heading2']))
        
        dimensions = {
            'fairness': '공정성 및 편향성',
            'privacy': '프라이버시 보호',
            'transparency': '투명성 및 설명가능성',
            'accountability': '책임성 및 거버넌스',
            'safety': '안전성 및 보안'
        }
        
        table_data = [['평가 차원', '점수', '리스크']]
        
        for dim_key, dim_name in dimensions.items():
            if dim_key in assessment:
                dim_data = assessment[dim_key]
                table_data.append([
                    dim_name,
                    f"{dim_data['score']}/5",
                    dim_data['risk_level']
                ])
        
        table = Table(table_data, colWidths=[7*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*cm))
        
        # 개선 권고사항
        improvements = data['improvement_suggestions'].get(service, [])
        if improvements:
            elements.append(Paragraph("주요 개선 권고사항", self.styles['Heading2']))
            
            for idx, imp in enumerate(improvements[:3], 1):
                imp_text = Paragraph(
                    f"<b>{idx}. {imp['dimension']}</b> (우선순위: {imp['priority']})<br/>" +
                    f"현재 점수: {imp['current_score']}/5 → 목표: {imp['target_score']}/5",
                    self.styles['Bullet']
                )
                elements.append(imp_text)
        
        return elements
    
    def _create_comparison_analysis(self, services: List[str], data: Dict) -> List:
        """비교 분석"""
        elements = []
        
        elements.append(Paragraph("서비스 비교 분석", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 종합 순위
        rankings = []
        for service in services:
            score = data['risk_assessments'][service]['overall_score']
            rankings.append((service, score))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        elements.append(Paragraph("종합 순위", self.styles['Heading2']))
        
        for rank, (service, score) in enumerate(rankings, 1):
            rank_text = Paragraph(
                f"{rank}위: {service} - {score}/5",
                self.styles['Bullet']
            )
            elements.append(rank_text)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # 차원별 비교
        elements.append(Paragraph("차원별 비교", self.styles['Heading2']))
        
        dimensions = {
            'fairness': '공정성',
            'privacy': '프라이버시',
            'transparency': '투명성',
            'accountability': '책임성',
            'safety': '안전성'
        }
        
        table_data = [['차원'] + services]
        
        for dim_key, dim_name in dimensions.items():
            row = [dim_name]
            for service in services:
                if dim_key in data['risk_assessments'][service]:
                    score = data['risk_assessments'][service][dim_key]['score']
                    row.append(f"{score}")
                else:
                    row.append("N/A")
            table_data.append(row)
        
        col_widths = [4*cm] + [3*cm] * len(services)
        table = Table(table_data, colWidths=col_widths)
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_recommendations(self, services: List[str], data: Dict) -> List:
        """종합 권고사항"""
        elements = []
        
        elements.append(Paragraph("종합 권고사항", self.styles['Heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 단기 조치
        elements.append(Paragraph("단기 조치 (1-3개월)", self.styles['Heading2']))
        short_term = [
            "AI 윤리 정책 문서화 및 공개",
            "편향성 테스트 프레임워크 도입",
            "개인정보 처리 방침 강화"
        ]
        for item in short_term:
            elements.append(Paragraph(f"• {item}", self.styles['Bullet']))
        
        elements.append(Spacer(1, 0.3*cm))
        
        # 중기 조치
        elements.append(Paragraph("중기 조치 (3-6개월)", self.styles['Heading2']))
        mid_term = [
            "AI 거버넌스 체계 구축",
            "정기적인 윤리 감사 시행",
            "투명성 보고서 발행"
        ]
        for item in mid_term:
            elements.append(Paragraph(f"• {item}", self.styles['Bullet']))
        
        elements.append(Spacer(1, 0.3*cm))
        
        # 장기 조치
        elements.append(Paragraph("장기 조치 (6개월 이상)", self.styles['Heading2']))
        long_term = [
            "지속적인 모니터링 시스템 구축",
            "외부 독립 감사 체계 확립",
            "산업 표준 및 인증 획득"
        ]
        for item in long_term:
            elements.append(Paragraph(f"• {item}", self.styles['Bullet']))
        
        return elements
# tools/report_pdf_enhanced.py - 완전 한국어화 고급 PDF 생성기
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime
from typing import Dict, List
import os


class EnhancedPDFReportGenerator:
    """아름답고 전문적인 한국어 PDF 리포트 생성기"""
    
    def __init__(self):
        self.korean_font = self._setup_korean_font()
        self.styles = self._create_styles()
        self.page_width, self.page_height = A4
        
        # 색상 테마
        self.colors = {
            'primary': colors.HexColor('#1A3A52'),      # 진한 네이비
            'secondary': colors.HexColor('#2E5C8A'),    # 중간 블루
            'accent': colors.HexColor('#3498DB'),       # 밝은 블루
            'success': colors.HexColor('#27AE60'),      # 초록
            'warning': colors.HexColor('#F39C12'),      # 주황
            'danger': colors.HexColor('#E74C3C'),       # 빨강
            'gray_light': colors.HexColor('#ECF0F1'),   # 연한 회색
            'gray_medium': colors.HexColor('#95A5A6'),  # 중간 회색
            'gray_dark': colors.HexColor('#34495E'),    # 진한 회색
        }
    
    def _setup_korean_font(self) -> str:
        """한국어 폰트 설정"""
        font_paths = [
            # Windows
            ('C:\\Windows\\Fonts\\malgun.ttf', 'MalgunGothic'),
            ('C:\\Windows\\Fonts\\batang.ttc', 'Batang'),
            # Linux
            ('/usr/share/fonts/truetype/nanum/NanumGothic.ttf', 'NanumGothic'),
            ('/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf', 'NanumBarun'),
            # macOS
            ('/System/Library/Fonts/AppleGothic.ttf', 'AppleGothic'),
            ('/Library/Fonts/NanumGothic.ttf', 'NanumGothic'),
        ]
        
        for path, name in font_paths:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont(name, path))
                    print(f"  ✅ 한국어 폰트 로드 성공: {name} ({path})")
                    return name
                except Exception as e:
                    print(f"  ⚠️  폰트 {name} 로드 시도 실패: {e}")
        
        print("  ⚠️  한국어 폰트를 찾을 수 없습니다. 기본 폰트 사용 (한글 깨질 수 있음)")
        return 'Helvetica'
    
    def _create_styles(self) -> Dict:
        """전문적인 PDF 스타일 정의"""
        base_styles = getSampleStyleSheet()
        
        return {
            # 제목 스타일
            'cover_title': ParagraphStyle(
                'CoverTitle',
                fontName=self.korean_font,
                fontSize=32,
                textColor=colors.HexColor('#1A3A52'),
                spaceAfter=20,
                alignment=TA_CENTER,
                leading=40
            ),
            'cover_subtitle': ParagraphStyle(
                'CoverSubtitle',
                fontName=self.korean_font,
                fontSize=16,
                textColor=colors.HexColor('#2E5C8A'),
                spaceAfter=30,
                alignment=TA_CENTER,
                leading=24
            ),
            
            # 헤딩 스타일
            'heading1': ParagraphStyle(
                'Heading1',
                fontName=self.korean_font,
                fontSize=20,
                textColor=colors.HexColor('#1A3A52'),
                spaceAfter=15,
                spaceBefore=20,
                leading=28,
                borderWidth=2,
                borderColor=colors.HexColor('#3498DB'),
                borderPadding=10,
                backColor=colors.HexColor('#EBF5FB')
            ),
            'heading2': ParagraphStyle(
                'Heading2',
                fontName=self.korean_font,
                fontSize=16,
                textColor=colors.HexColor('#2E5C8A'),
                spaceAfter=12,
                spaceBefore=15,
                leading=22,
                leftIndent=10,
                borderWidth=0,
                borderPadding=5
            ),
            'heading3': ParagraphStyle(
                'Heading3',
                fontName=self.korean_font,
                fontSize=13,
                textColor=colors.HexColor('#34495E'),
                spaceAfter=10,
                spaceBefore=12,
                leading=18,
                leftIndent=20
            ),
            
            # 본문 스타일
            'body': ParagraphStyle(
                'Body',
                fontName=self.korean_font,
                fontSize=10,
                leading=18,
                spaceAfter=12,
                alignment=TA_JUSTIFY,
                textColor=colors.HexColor('#2C3E50')
            ),
            'body_indent': ParagraphStyle(
                'BodyIndent',
                fontName=self.korean_font,
                fontSize=10,
                leading=18,
                spaceAfter=10,
                leftIndent=30,
                alignment=TA_JUSTIFY,
                textColor=colors.HexColor('#2C3E50')
            ),
            
            # 리스트 스타일
            'bullet': ParagraphStyle(
                'Bullet',
                fontName=self.korean_font,
                fontSize=10,
                leftIndent=30,
                spaceAfter=8,
                leading=16,
                textColor=colors.HexColor('#2C3E50')
            ),
            'bullet_sub': ParagraphStyle(
                'BulletSub',
                fontName=self.korean_font,
                fontSize=9,
                leftIndent=50,
                spaceAfter=6,
                leading=14,
                textColor=colors.HexColor('#34495E')
            ),
            
            # 특수 스타일
            'info_box': ParagraphStyle(
                'InfoBox',
                fontName=self.korean_font,
                fontSize=10,
                leading=16,
                backColor=colors.HexColor('#E8F6F3'),
                borderWidth=1,
                borderColor=colors.HexColor('#27AE60'),
                borderPadding=15,
                spaceAfter=15,
                textColor=colors.HexColor('#145A32')
            ),
            'warning_box': ParagraphStyle(
                'WarningBox',
                fontName=self.korean_font,
                fontSize=10,
                leading=16,
                backColor=colors.HexColor('#FEF9E7'),
                borderWidth=1,
                borderColor=colors.HexColor('#F39C12'),
                borderPadding=15,
                spaceAfter=15,
                textColor=colors.HexColor('#784212')
            ),
            'danger_box': ParagraphStyle(
                'DangerBox',
                fontName=self.korean_font,
                fontSize=10,
                leading=16,
                backColor=colors.HexColor('#FADBD8'),
                borderWidth=1,
                borderColor=colors.HexColor('#E74C3C'),
                borderPadding=15,
                spaceAfter=15,
                textColor=colors.HexColor('#641E16')
            ),
            
            # 테이블 내용 스타일
            'table_header': ParagraphStyle(
                'TableHeader',
                fontName=self.korean_font,
                fontSize=11,
                textColor=colors.white,
                alignment=TA_CENTER
            ),
            'table_cell': ParagraphStyle(
                'TableCell',
                fontName=self.korean_font,
                fontSize=9,
                leading=14,
                alignment=TA_CENTER
            ),
            'table_cell_left': ParagraphStyle(
                'TableCellLeft',
                fontName=self.korean_font,
                fontSize=9,
                leading=14,
                alignment=TA_LEFT
            ),
            
            # 기타
            'footer': ParagraphStyle(
                'Footer',
                fontName=self.korean_font,
                fontSize=8,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_CENTER
            ),
            'caption': ParagraphStyle(
                'Caption',
                fontName=self.korean_font,
                fontSize=8,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_CENTER,
                spaceAfter=10
            ),
        }
    
    def generate_report(
        self,
        output_path: str,
        services: List[str],
        detailed_data: Dict,
        report_text: str = None
    ):
        """아름다운 PDF 리포트 생성"""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        print("  📄 PDF 생성 중...")
        print("     - 표지 페이지 생성 중...")
        story.extend(self._create_professional_cover(services))
        story.append(PageBreak())
        
        print("     - 목차 생성 중...")
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        print("     - Executive Summary 생성 중...")
        story.extend(self._create_executive_summary(services, detailed_data))
        story.append(PageBreak())
        
        print("     - 평가 방법론 생성 중...")
        story.extend(self._create_methodology())
        story.append(PageBreak())
        
        print(f"     - 서비스별 분석 생성 중 ({len(services)}개)...")
        for idx, service in enumerate(services, 1):
            print(f"       {idx}/{len(services)}: {service}")
            story.extend(self._create_detailed_service_analysis(service, detailed_data))
            story.append(PageBreak())
        
        if len(services) >= 2:
            print("     - 비교 분석 생성 중...")
            story.extend(self._create_comparison_analysis(services, detailed_data))
            story.append(PageBreak())
        
        print("     - 종합 권고사항 생성 중...")
        story.extend(self._create_comprehensive_recommendations(services, detailed_data))
        story.append(PageBreak())
        
        print("     - 참고문헌 생성 중...")
        story.extend(self._create_references())
        story.append(PageBreak())
        
        print("     - 부록 생성 중...")
        story.extend(self._create_appendix())
        
        # PDF 빌드
        print("     - PDF 파일 빌드 중...")
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        
        print(f"  ✅ PDF 생성 완료: {output_path}")
        return output_path
    
    def _header_footer(self, canvas, doc):
        """전문적인 헤더/푸터"""
        canvas.saveState()
        
        # 헤더 라인
        canvas.setStrokeColor(self.colors['accent'])
        canvas.setLineWidth(2)
        canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)
        
        # 푸터
        try:
            canvas.setFont(self.korean_font, 8)
        except Exception:
            canvas.setFont("Helvetica", 8)
        canvas.setFillColor(self.colors['gray_medium'])
        
        # 왼쪽: 문서 정보
        canvas.drawString(
            2*cm, 1.5*cm,
            f"AI 윤리성 리스크 진단 보고서 | {datetime.now().strftime('%Y년 %m월 %d일')}"
        )
        
        # 오른쪽: 페이지 번호
        canvas.drawRightString(
            A4[0] - 2*cm, 1.5*cm,
            f"페이지 {doc.page}"
        )
        
        # 푸터 라인
        canvas.setStrokeColor(self.colors['gray_light'])
        canvas.setLineWidth(1)
        canvas.line(2*cm, 1.2*cm, A4[0] - 2*cm, 1.2*cm)
        
        canvas.restoreState()
    
    def _create_professional_cover(self, services: List[str]) -> List:
        """전문적인 표지 페이지"""
        elements = []
        
        # 상단 여백
        elements.append(Spacer(1, 2*cm))
        
        # 메인 타이틀
        elements.append(Paragraph(
            "AI 윤리성 리스크<br/>진단 보고서",
            self.styles['cover_title']
        ))
        
        # 구분선
        elements.append(Spacer(1, 0.5*cm))
        hr = HRFlowable(
            width="80%",
            thickness=3,
            color=self.colors['accent'],
            spaceAfter=0.5*cm,
            spaceBefore=0,
            hAlign='CENTER'
        )
        elements.append(hr)
        
        # 부제목
        elements.append(Paragraph(
            "국제 표준 기반 종합 평가 및 개선 권고",
            self.styles['cover_subtitle']
        ))
        
        elements.append(Spacer(1, 2*cm))
        
        # 정보 박스
        info_data = [
            ['', ''],  # 빈 헤더
            ['📊 분석 대상 서비스', '<br/>'.join(services)],
            ['📚 평가 기준', 'EU AI Act (유럽연합 AI 규제)<br/>UNESCO AI Ethics (유네스코 AI 윤리)<br/>OECD AI Principles (OECD AI 원칙)'],
            ['⚖️ 평가 차원', '공정성 및 편향성<br/>프라이버시 보호<br/>투명성 및 설명가능성<br/>책임성 및 거버넌스<br/>안전성 및 보안'],
            ['📅 작성일', datetime.now().strftime('%Y년 %m월 %d일')],
            ['🕐 평가 시간', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ]
        
        info_table = Table(info_data, colWidths=[4.5*cm, 9*cm])
        info_table.setStyle(TableStyle([
            # 헤더 숨김
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('LINEBELOW', (0, 0), (-1, 0), 0, colors.white),
            
            # 본문
            ('BACKGROUND', (0, 1), (0, -1), self.colors['primary']),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.white),
            ('BACKGROUND', (1, 1), (1, -1), colors.white),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 1), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 1), (-1, -1), 15),
            ('RIGHTPADDING', (0, 1), (-1, -1), 15),
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
            ('GRID', (0, 1), (-1, -1), 1.5, self.colors['gray_light']),
            ('BOX', (0, 1), (-1, -1), 2, self.colors['primary']),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 2*cm))
        
        # 평가 목표 박스
        elements.append(Paragraph("📌 평가 목표", self.styles['heading2']))
        
        objective_text = """
본 보고서는 선정된 AI 서비스에 대하여 <b>국제 표준 가이드라인</b>을 기준으로 
<b>윤리적 리스크</b>를 종합적으로 평가하고, 각 서비스의 <b>강점</b>을 파악하며 
필요한 <b>개선사항</b>을 구체적으로 제시하는 것을 목표로 합니다.
<br/><br/>
평가 결과는 AI 서비스 개발사의 윤리성 강화, 규제 당국의 사전 심사, 
투자사의 리스크 평가 등 다양한 목적으로 활용될 수 있습니다.
        """
        
        elements.append(Paragraph(objective_text, self.styles['info_box']))
        
        return elements
    
    def _create_table_of_contents(self) -> List:
        """목차"""
        elements = []
        
        elements.append(Paragraph("📑 목차", self.styles['heading1']))
        elements.append(Spacer(1, 0.5*cm))
        
        toc_data = [
            ['장', '제목', '페이지'],
            ['1', 'Executive Summary (종합 요약)', '3'],
            ['2', '평가 방법론', '4'],
            ['3', '서비스별 상세 분석', '5'],
            ['4', '비교 분석 (2개 이상 서비스)', '10'],
            ['5', '종합 권고사항', '12'],
            ['6', '참고문헌', '14'],
            ['7', '부록', '15'],
        ]
        
        toc_table = Table(toc_data, colWidths=[1.5*cm, 10*cm, 2*cm])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['secondary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['gray_light']]),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['gray_medium']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(toc_table)
        
        return elements
    
    def _create_executive_summary(self, services: List[str], data: Dict) -> List:
        """Executive Summary (한국어)"""
        elements = []
        
        elements.append(Paragraph("1. EXECUTIVE SUMMARY (종합 요약)", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 1.1 평가 개요
        elements.append(Paragraph("1.1 평가 개요", self.styles['heading2']))
        
        overview_text = f"""
본 평가는 <b>{len(services)}개 AI 서비스</b>에 대하여 EU AI Act, UNESCO AI Ethics, 
OECD AI Principles 등 <b>국제 표준</b>을 기준으로 5개 차원(공정성, 프라이버시, 투명성, 
책임성, 안전성)에서 윤리적 리스크를 평가했습니다.
<br/><br/>
평가는 <b>LLM 기반 정성 평가</b>와 <b>자동화된 체크리스트</b>를 결합한 이중 검증 
시스템을 통해 진행되었으며, 웹 검색을 통한 실증적 증거 수집으로 객관성을 확보했습니다.
        """
        
        elements.append(Paragraph(overview_text, self.styles['body']))
        elements.append(Spacer(1, 0.4*cm))
        
        # 1.2 종합 평가 결과
        elements.append(Paragraph("1.2 종합 평가 결과", self.styles['heading2']))
        
        score_data = [['서비스', '종합 점수', '리스크 수준', '평가 등급', '종합 평가']]
        
        for service in services:
            assessment = data['risk_assessments'].get(service, {})
            score = assessment.get('overall_score', 0)
            risk = assessment.get('overall_risk_level', '알수없음')
            grade = self._get_grade(score)
            
            # 종합 평가 문구
            if score >= 4.5:
                status = "매우 우수"
            elif score >= 4.0:
                status = "우수"
            elif score >= 3.5:
                status = "양호"
            elif score >= 3.0:
                status = "보통"
            elif score >= 2.0:
                status = "미흡"
            else:
                status = "부족"
            
            score_data.append([
                service,
                f"{score}/5",
                risk,
                grade,
                status
            ])
        
        score_table = Table(score_data, colWidths=[2.8*cm, 2*cm, 2.2*cm, 1.8*cm, 2*cm])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['gray_light']]),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['gray_medium']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # 1.3 주요 발견사항
        elements.append(Paragraph("1.3 주요 발견사항", self.styles['heading2']))
        
        avg_score = 0.0
        try:
            avg_score = sum([v.get('overall_score', 0) for v in data.get('risk_assessments', {}).values()]) / max(len(services), 1)
        except Exception:
            avg_score = 0.0
        
        # 최고/최저 점수 서비스
        scores = [(s, data.get('risk_assessments', {}).get(s, {}).get('overall_score', 0)) for s in services]
        if scores:
            best_service = max(scores, key=lambda x: x[1])
            worst_service = min(scores, key=lambda x: x[1])
        else:
            best_service = ("-","0")
            worst_service = ("-","0")
        
        findings_text = f"""
<b>1) 전체 평균 윤리 점수:</b> {avg_score:.1f}/5<br/>
   → 전반적으로 {'우수한' if avg_score >= 4 else '양호한' if avg_score >= 3.5 else '개선이 필요한'} 수준입니다.
<br/><br/>
<b>2) 최고 평가 서비스:</b> {best_service[0]} ({best_service[1]}/5)<br/>
   → 윤리성 측면에서 가장 앞서가는 서비스로 평가됩니다.
<br/><br/>
<b>3) 개선 필요 서비스:</b> {worst_service[0]} ({worst_service[1]}/5)<br/>
   → 여러 차원에서 개선이 필요한 것으로 나타났습니다.
<br/><br/>
<b>4) 공통 강점:</b><br/>
   • 대부분의 서비스가 기본적인 개인정보 보호 정책을 수립하고 있습니다.<br/>
   • 투명성 강화를 위한 노력이 증가하고 있습니다.
<br/><br/>
<b>5) 공통 약점:</b><br/>
   • 편향성 테스트 및 완화 조치가 부족한 경우가 많습니다.<br/>
   • 명확한 책임 체계와 거버넌스가 미흡한 서비스가 있습니다.
        """
        
        elements.append(Paragraph(findings_text, self.styles['body']))
        elements.append(Spacer(1, 0.4*cm))
        
        # 1.4 최우선 권고사항
        elements.append(Paragraph("1.4 최우선 권고사항", self.styles['heading2']))
        
        recommendations_text = """
<b>1) 즉시 조치 필요 (1개월 이내):</b><br/>
   • AI 윤리 정책 문서 작성 및 공개<br/>
   • 편향성 테스트 계획 수립<br/>
   • 개인정보 처리방침 강화
<br/><br/>
<b>2) 단기 개선 (1-3개월):</b><br/>
   • 편향성 감지 및 완화 메커니즘 도입<br/>
   • 투명성 보고서 발행 준비<br/>
   • 사용자 피드백 수집 체계 구축
<br/><br/>
<b>3) 중장기 개선 (3-6개월 이상):</b><br/>
   • AI 거버넌스 체계 수립 및 윤리 위원회 구성<br/>
   • 정기적인 윤리 감사 프로세스 확립<br/>
   • 국제 표준 및 인증 획득 추진
        """
        
        elements.append(Paragraph(recommendations_text, self.styles['warning_box']))
        
        return elements
    
    def _create_methodology(self) -> List:
        """평가 방법론 (한국어)"""
        elements = []
        
        elements.append(Paragraph("2. 평가 방법론", self.styles['heading1']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 2.1 평가 프레임워크
        elements.append(Paragraph("2.1 평가 프레임워크", self.styles['heading2']))
        
        framework_text = """
본 평가는 다음의 <b>3대 국제 표준</b>을 기준으로 실시되었습니다:
        """
        
        elements.append(Paragraph(framework_text, self.styles['body']))
        
        # 국제 표준 테이블
        standards_data = [
            ['표준', '주요 내용 요약'],
            ['EU AI Act', '위험 기반 규제 프레임워크, 고위험 AI 시스템에 대한 의무 규정'],
            ['UNESCO AI Ethics', '인간 중심의 AI 윤리 원칙(존엄성, 공정성 등)'],
            ['OECD AI Principles', '투명성, 책임성, 안전성 강조']
        ]
        
        standards_table = Table(standards_data, colWidths=[4*cm, 10*cm])
        standards_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['secondary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['gray_light']]),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['gray_medium']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(standards_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # 2.2 평가 절차
        elements.append(Paragraph("2.2 평가 절차", self.styles['heading2']))
        procedure_text = """
평가는 다음 절차로 수행되었습니다:
• 데이터 수집: 공개 문서, 서비스 이용약관, 개인정보처리방침, 기술백서, 공개 API 문서 등.
• 정성평가: 전문가 및 LLM 기반 정성검토를 통해 정책·절차·거버넌스 요소 평가.
• 자동체크리스트: 규격화된 체크리스트를 통해 누락 요소 및 기술적·절차적 통제 점검.
• 종합점수 산출: 5점 척도(5:매우 우수 ~ 0:부족)를 사용해 차원별 가중평균 산출.
        """
        elements.append(Paragraph(procedure_text, self.styles['body']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 2.3 한계점
        elements.append(Paragraph("2.3 한계점", self.styles['heading2']))
        limitations_text = """
본 평가는 공개자료 기반이며, 내부 시스템 코드나 비공개 구성에 접근할 수 없었습니다. 
따라서 내부 통제의 정확성은 내부 감사 또는 실무 검증을 통해 보완되어야 합니다.
        """
        elements.append(Paragraph(limitations_text, self.styles['body']))
        
        return elements
    
    def _create_detailed_service_analysis(self, service: str, data: Dict) -> List:
        """서비스별 상세 분석 페이지 생성"""
        elements = []
        elements.append(Paragraph(f"3. {service} - 상세 분석", self.styles['heading1']))
        elements.append(Spacer(1, 0.2*cm))
        
        assessment = data.get('risk_assessments', {}).get(service, {})
        # 차원별 점수 수집 (기본키 존재 여부 방어)
        dimensions = assessment.get('dimensions', {
            'fairness': {'score': assessment.get('fairness_score', 0), 'notes': assessment.get('fairness_notes', '')},
            'privacy': {'score': assessment.get('privacy_score', 0), 'notes': assessment.get('privacy_notes', '')},
            'transparency': {'score': assessment.get('transparency_score', 0), 'notes': assessment.get('transparency_notes', '')},
            'accountability': {'score': assessment.get('accountability_score', 0), 'notes': assessment.get('accountability_notes', '')},
            'safety': {'score': assessment.get('safety_score', 0), 'notes': assessment.get('safety_notes', '')},
        })
        
        # 요약 박스
        summary = assessment.get('summary', '해당 서비스의 요약 정보가 제공되지 않았습니다.')
        elements.append(Paragraph("요약", self.styles['heading2']))
        elements.append(Paragraph(summary, self.styles['body']))
        elements.append(Spacer(1, 0.2*cm))
        
        # 차원별 점수 표
        dim_table_data = [['차원', '점수 (5점 만점)', '주요 코멘트']]
        for dim_name, dim_info in dimensions.items():
            display_name = {
                'fairness': '공정성',
                'privacy': '프라이버시',
                'transparency': '투명성',
                'accountability': '책임성',
                'safety': '안전성'
            }.get(dim_name, dim_name)
            score = dim_info.get('score', 0) if isinstance(dim_info, dict) else 0
            notes = dim_info.get('notes', '') if isinstance(dim_info, dict) else ''
            dim_table_data.append([display_name, f"{score}/5", notes or '-'])
        
        dim_table = Table(dim_table_data, colWidths=[4.5*cm, 3*cm, 6*cm])
        dim_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.colors['primary']),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), self.korean_font),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ALIGN', (1,1), (1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, self.colors['gray_light']]),
            ('GRID', (0,0), (-1,-1), 1, self.colors['gray_medium']),
        ]))
        elements.append(dim_table)
        elements.append(Spacer(1, 0.3*cm))
        
        # 주요 취약점 및 권고
        elements.append(Paragraph("주요 취약점", self.styles['heading2']))
        weaknesses = assessment.get('weaknesses', ['구체적 취약점 정보 없음'])
        if isinstance(weaknesses, list):
            for w in weaknesses:
                elements.append(Paragraph(f"• {w}", self.styles['bullet']))
        else:
            elements.append(Paragraph(str(weaknesses), self.styles['body']))
        elements.append(Spacer(1, 0.2*cm))
        
        elements.append(Paragraph("권고사항 (우선순위 기준)", self.styles['heading2']))
        recs = assessment.get('recommendations', [
            '권고 사항이 제공되지 않았습니다.'
        ])
        if isinstance(recs, list):
            for r in recs:
                elements.append(Paragraph(f"• {r}", self.styles['bullet']))
        else:
            elements.append(Paragraph(str(recs), self.styles['body']))
        elements.append(Spacer(1, 0.5*cm))
        
        # 간단한 막대 차트 — 차원별 점수 시각화 (reportlab graphics)
        try:
            drawing = Drawing(400, 150)
            bc = VerticalBarChart()
            bc.x = 50
            bc.y = 15
            bc.height = 100
            bc.width = 300
            bc.data = [[
                dimensions.get('fairness', {}).get('score', 0),
                dimensions.get('privacy', {}).get('score', 0),
                dimensions.get('transparency', {}).get('score', 0),
                dimensions.get('accountability', {}).get('score', 0),
                dimensions.get('safety', {}).get('score', 0),
            ]]
            bc.categoryAxis.categoryNames = ['공정성','프라이버시','투명성','책임성','안전성']
            bc.valueAxis.valueMin = 0
            bc.valueAxis.valueMax = 5
            bc.valueAxis.valueStep = 1
            drawing.add(bc)
            elements.append(drawing)
            elements.append(Spacer(1, 0.3*cm))
        except Exception:
            # 실패 시 무시 (시각화는 보조 요소)
            pass
        
        return elements
    
    def _create_comparison_analysis(self, services: List[str], data: Dict) -> List:
        """여러 서비스 비교 분석(간단하게 표/평균/강점·약점 비교)"""
        elements = []
        elements.append(Paragraph("4. 비교 분석", self.styles['heading1']))
        elements.append(Spacer(1, 0.2*cm))
        
        # 비교용 표 생성: 서비스별 주요 점수(종합)
        header = ['서비스', '종합점수', '공정성', '프라이버시', '투명성', '책임성', '안전성']
        table_data = [header]
        for s in services:
            ass = data.get('risk_assessments', {}).get(s, {})
            row = [
                s,
                ass.get('overall_score', 0),
                ass.get('fairness_score', ass.get('dimensions', {}).get('fairness', {}).get('score', 0)),
                ass.get('privacy_score', ass.get('dimensions', {}).get('privacy', {}).get('score', 0)),
                ass.get('transparency_score', ass.get('dimensions', {}).get('transparency', {}).get('score', 0)),
                ass.get('accountability_score', ass.get('dimensions', {}).get('accountability', {}).get('score', 0)),
                ass.get('safety_score', ass.get('dimensions', {}).get('safety', {}).get('score', 0)),
            ]
            # 포맷팅: 숫자는 소수 1자리로
            row = [row[0]] + [f"{float(x):.1f}" if isinstance(x, (int, float, str)) and str(x).replace('.','',1).isdigit() else str(x) for x in row[1:]]
            table_data.append(row)
        
        comp_table = Table(table_data, colWidths=[4*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.colors['primary']),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), self.korean_font),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 1, self.colors['gray_medium']),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, self.colors['gray_light']]),
            ('ALIGN', (1,1), (-1,-1), 'CENTER')
        ]))
        elements.append(comp_table)
        elements.append(Spacer(1, 0.4*cm))
        
        # 요약 분석: 평균 및 공통 이슈
        elements.append(Paragraph("비교 요약", self.styles['heading2']))
        # 평균 계산
        avg_scores = {}
        count = max(len(services), 1)
        dims = ['overall_score', 'fairness_score', 'privacy_score', 'transparency_score', 'accountability_score', 'safety_score']
        for d in dims:
            ssum = 0.0
            for s in services:
                ssum += float(data.get('risk_assessments', {}).get(s, {}).get(d, 0) or 0)
            avg_scores[d] = ssum / count
        summary_lines = [
            f"• 전체 평균 종합점수: {avg_scores['overall_score']:.1f}/5",
            f"• 평균 공정성 점수: {avg_scores['fairness_score']:.1f}/5",
            f"• 평균 프라이버시 점수: {avg_scores['privacy_score']:.1f}/5",
            "• 공통 이슈: 편향성 테스트 미비, 책임성(거버넌스) 부재, 투명성 문서화 미흡"
        ]
        for l in summary_lines:
            elements.append(Paragraph(l, self.styles['body']))
        
        return elements
    
    def _create_comprehensive_recommendations(self, services: List[str], data: Dict) -> List:
        """종합 권고사항 (서비스 그룹 및 개별 권고 포함)"""
        elements = []
        elements.append(Paragraph("5. 종합 권고사항", self.styles['heading1']))
        elements.append(Spacer(1, 0.2*cm))
        
        # 공통 권고 — 그룹 레벨
        elements.append(Paragraph("5.1 공통 권고 (모든 서비스 대상)", self.styles['heading2']))
        common_recs = [
            "AI 윤리 정책 및 거버넌스 문서화 및 공개",
            "정기적인 편향성 테스트와 완화 절차 도입",
            "민감 데이터 취급에 대한 강화된 개인정보 보호 통제 적용",
            "투명성 보고서(모델 설명, 데이터 출처, 한계 등) 발행",
            "사후 책임 체계 및 사고 대응 프로세스 수립"
        ]
        for r in common_recs:
            elements.append(Paragraph(f"• {r}", self.styles['bullet']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 서비스별 우선 순위 권고
        elements.append(Paragraph("5.2 서비스별 우선 권고 (예시)", self.styles['heading2']))
        for s in services:
            ass = data.get('risk_assessments', {}).get(s, {})
            # 기본적으로 가장 낮은 차원에 포커스 권고
            dims = {
                '공정성': ass.get('fairness_score', ass.get('dimensions', {}).get('fairness', {}).get('score', 0)),
                '프라이버시': ass.get('privacy_score', ass.get('dimensions', {}).get('privacy', {}).get('score', 0)),
                '투명성': ass.get('transparency_score', ass.get('dimensions', {}).get('transparency', {}).get('score', 0)),
                '책임성': ass.get('accountability_score', ass.get('dimensions', {}).get('accountability', {}).get('score', 0)),
                '안전성': ass.get('safety_score', ass.get('dimensions', {}).get('safety', {}).get('score', 0)),
            }
            # 가장 낮은 값 찾기
            worst_dim = min(dims.items(), key=lambda x: float(x[1] or 0))[0]
            elements.append(Paragraph(f"{s} — 우선 개선 대상: {worst_dim}", self.styles['bullet_sub']))
            elements.append(Paragraph(f"권고: {s}는 {worst_dim} 향상을 위해 구체적으로 다음을 수행하십시오.", self.styles['body_indent']))
            elements.append(Paragraph("• 정책 및 절차 문서화\n• 기술적 통제(모델 모니터링, 로그, 테스트) 도입\n• 책임자 지정 및 정기 감사 계획 수립", self.styles['body_indent']))
            elements.append(Spacer(1, 0.2*cm))
        
        return elements
    
    def _create_references(self) -> List:
        """참고문헌(예시)"""
        elements = []
        elements.append(Paragraph("6. 참고문헌", self.styles['heading1']))
        elements.append(Spacer(1, 0.2*cm))
        
        refs = [
            "European Union. (2021). Proposal for a Regulation laying down harmonised rules on artificial intelligence (AI Act).",
            "UNESCO. (2021). Recommendation on the Ethics of Artificial Intelligence.",
            "OECD. (2019). OECD Principles on Artificial Intelligence.",
            "국내외 관련 가이드라인 및 공개 자료"
        ]
        for r in refs:
            elements.append(Paragraph(f"• {r}", self.styles['body']))
        
        return elements
    
    def _create_appendix(self) -> List:
        """부록(예: 체크리스트, 용어정의 등)"""
        elements = []
        elements.append(Paragraph("7. 부록", self.styles['heading1']))
        elements.append(Spacer(1, 0.2*cm))
        
        # 예시 체크리스트
        elements.append(Paragraph("7.1 평가 체크리스트 (예시)", self.styles['heading2']))
        checklist = [
            "• 개인정보 최소화 원칙 적용 여부",
            "• 편향성 테스트 및 결과 문서화 여부",
            "• 모델 변경 시 재평가 프로세스 존재 여부",
            "• 사용자 알림 및 동의 절차 구축 여부",
            "• 보안/침해사고 대응 계획 존재 여부"
        ]
        for c in checklist:
            elements.append(Paragraph(c, self.styles['bullet']))
        elements.append(Spacer(1, 0.3*cm))
        
        # 용어정의
        elements.append(Paragraph("7.2 용어정의", self.styles['heading2']))
        terms = [
            ("공정성", "알고리즘이 특정 그룹에 불이익을 주지 않도록 보장하는 원칙"),
            ("투명성", "시스템의 의사결정과 한계에 대해 설명 가능한 정도"),
            ("책임성", "시스템 운영 주체의 법적/윤리적 책임 소재"),
        ]
        for t, d in terms:
            elements.append(Paragraph(f"• {t}: {d}", self.styles['body']))
        
        return elements
    
    def _get_grade(self, score: float) -> str:
        """점수 -> 등급 변환 (예시)"""
        try:
            s = float(score)
        except Exception:
            s = 0.0
        if s >= 4.5:
            return "A+"
        elif s >= 4.0:
            return "A"
        elif s >= 3.5:
            return "B+"
        elif s >= 3.0:
            return "B"
        elif s >= 2.5:
            return "C"
        elif s >= 2.0:
            return "D"
        else:
            return "F"

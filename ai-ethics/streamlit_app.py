
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import sys
from typing import Dict, List
import pandas as pd
import traceback

# 절대 경로로 프로젝트 루트 설정
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# AIEthicsAssessmentSystem import
SYSTEM_AVAILABLE = False
try:
    from app import AIEthicsAssessmentSystem
    SYSTEM_AVAILABLE = True
    st.write("✅ AIEthicsAssessmentSystem 로드 성공")
except ImportError as e:
    st.error(f"⚠️ AIEthicsAssessmentSystem 로드 실패: {e}")
    st.info("데모 모드로 실행됩니다. 모든 기능을 시뮬레이션으로 체험할 수 있습니다.")

st.set_page_config(
    page_title="AI 윤리성 리스크 진단",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.set_page_config(
    page_title="AI 윤리성 리스크 진단",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0;
        letter-spacing: 1px;
    }
    
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #5a67d8;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card h3 {
        font-size: 0.9rem;
        margin: 0 0 10px 0;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 900;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-top: 5px;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .detail-card {
        border-left: 5px solid #667eea;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(to right, rgba(102, 126, 234, 0.05), transparent);
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .detail-card h4 {
        color: #667eea;
        margin-top: 0;
        font-weight: 700;
    }
    
    .evidence-item {
        background: linear-gradient(to right, #e3f2fd, #f5f5f5);
        padding: 12px 15px;
        margin: 8px 0;
        border-radius: 6px;
        border-left: 4px solid #2196f3;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .risk-item {
        background: linear-gradient(to right, #ffebee, #f5f5f5);
        padding: 12px 15px;
        margin: 8px 0;
        border-radius: 6px;
        border-left: 4px solid #f44336;
        font-size: 0.95rem;
    }
    
    .strength-item {
        background: linear-gradient(to right, #e8f5e9, #f5f5f5);
        padding: 12px 15px;
        margin: 8px 0;
        border-radius: 6px;
        border-left: 4px solid #4caf50;
        font-size: 0.95rem;
    }
    
    .progress-step {
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .progress-step.complete {
        background: #e8f5e9;
        border-left-color: #4caf50;
    }
    
    .progress-step.active {
        background: #fff3e0;
        border-left-color: #ff9800;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs > [data-baseweb="tab-list"] > button {
        font-weight: 600;
        font-size: 1rem;
    }
    
    .dataframe {
        font-size: 0.95rem !important;
    }
    
    .improvement-detail {
        background: linear-gradient(to right, #f0fff4, #f5f5f5);
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
    }
    
    .improvement-detail h5 {
        color: #28a745;
        margin-top: 0;
        font-weight: 700;
    }
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        font-size: 1.3rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


class EthicsDashboard:
    def __init__(self):
        self.dimensions = {
            "fairness": "공정성 및 편향성",
            "privacy": "프라이버시 보호",
            "transparency": "투명성 및 설명가능성",
            "accountability": "책임성 및 거버넌스",
            "safety": "안전성 및 보안"
        }
        
        self.initialize_session_state()
        
        if SYSTEM_AVAILABLE and 'system' not in st.session_state:
            with st.spinner("시스템 초기화 중..."):
                st.session_state.system = AIEthicsAssessmentSystem()
    
    def initialize_session_state(self):
        defaults = {
            'analysis_done': False,
            'results': None,
            'progress_logs': [],
            'pdf_generated': False,
            'pdf_content': None
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def generate_pdf_report(self, results: Dict) -> bytes:
        try:
            from tools.report_pdf_enhanced import EnhancedPDFReportGenerator
            import tempfile
            
            pdf_gen = EnhancedPDFReportGenerator()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                pdf_gen.generate_report(
                    output_path=tmp.name,
                    services=results['services'],
                    detailed_data=results['detailed_data'],
                    report_text=results['report']
                )
                
                with open(tmp.name, 'rb') as f:
                    pdf_bytes = f.read()
                
                os.unlink(tmp.name)
                return pdf_bytes
        
        except Exception as e:
            st.error(f"PDF 생성 오류: {e}")
            return None
    
    def run(self):
        st.markdown('<div class="main-header">⚖️ AI 윤리성 리스크 진단 시스템</div>', 
                   unsafe_allow_html=True)
        st.markdown('<div class="sub-header">전문적이고 종합적인 AI 서비스 윤리 평가</div>', 
                   unsafe_allow_html=True)
        
        if not SYSTEM_AVAILABLE:
            st.warning("AIEthicsAssessmentSystem을 불러올 수 없습니다. 데모 모드로 실행됩니다.")
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 설정")
            
            st.markdown("### 분석 서비스")
            services = st.multiselect(
                "분석할 AI 서비스를 선택하세요 (최대 3개)",
                ["ChatGPT", "Claude", "Google Gemini", "Copilot", "Midjourney", "DALL-E"],
                max_selections=3
            )
            
            st.markdown("---")
            
            st.markdown("### 평가 설정")
            st.info("""**적용 가이드라인**
- EU AI Act
- UNESCO AI Ethics
- OECD AI Principles""")
            
            st.markdown("---")
            
            if st.button("🚀 분석 시작", 
                        disabled=len(services)==0, 
                        use_container_width=True):
                self.start_analysis(services)
        
        if not st.session_state.analysis_done:
            self.render_welcome_page()
        else:
            self.render_results_page()
    
    def render_welcome_page(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
### 환영합니다

AI 서비스의 윤리적 리스크를 5개 차원에서 종합적으로 평가하고 개선 방향을 제시합니다.

#### 주요 기능
- ⚖️ **5개 차원 심층 평가**: 공정성, 프라이버시, 투명성, 책임성, 안전성
- 📊 **실시간 분석**: 진행 상황 모니터링
- 💡 **구체적 권고**: 실행 가능한 개선안
- 📈 **가이드라인 준수**: 국제 표준 기준 평가
- 🔍 **서비스 비교**: 여러 서비스 간 비교 분석

👈 **왼쪽 사이드바에서 시작하세요!**
            """)
    
    def start_analysis(self, services: List[str]):
        st.session_state.progress_logs = []
        
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### 분석 진행 중...")
            progress_area = st.empty()
            status_text = st.empty()
            progress_bar = st.progress(0)
        
        try:
            if SYSTEM_AVAILABLE:
                status_text.info("AI 윤리성 분석 시스템을 실행합니다...")
                
                output_dir = "outputs/streamlit_temp"
                os.makedirs(output_dir, exist_ok=True)
                
                report = st.session_state.system.analyze_services(
                    service_names=services,
                    output_dir=output_dir
                )
                
                latest_files = sorted([f for f in os.listdir(output_dir) 
                                     if f.endswith('_data.json')])
                if latest_files:
                    with open(os.path.join(output_dir, latest_files[-1]), 
                             'r', encoding='utf-8') as f:
                        detailed_data = json.load(f)
                    
                    st.session_state.results = {
                        'services': services,
                        'report': report['markdown_report'],
                        'detailed_data': detailed_data,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    progress_bar.progress(1.0)
                    status_text.success("분석 완료!")
                    st.session_state.analysis_done = True
                    st.rerun()
            else:
                self.run_demo_analysis(services, progress_area, progress_bar, status_text)
        
        except Exception as e:
            st.error(f"분석 중 오류: {e}")
            import traceback
            with st.expander("오류 상세"):
                st.code(traceback.format_exc())
    
    def run_demo_analysis(self, services, progress_area, progress_bar, status_text):
        import time
        
        steps = [
            "시스템 초기화 중...",
            f"서비스 분석 시작: {', '.join(services)}",
            "1단계: 서비스 정보 수집 및 분석 중...",
            "2단계: 윤리 리스크 상세 평가 중...",
            "3단계: 가이드라인 준수 여부 검증 중...",
            "4단계: 개선안 생성 중...",
            "5단계: 비교 분석 중..." if len(services) > 1 else "5단계: 건너뛰기...",
            "6단계: 최종 보고서 작성 중...",
        ]
        
        for idx, step in enumerate(steps):
            st.session_state.progress_logs.append({"step": step, "status": "active"})
            
            with progress_area:
                for i, log in enumerate(st.session_state.progress_logs):
                    status_class = "complete" if i < len(st.session_state.progress_logs) - 1 else "active"
                    icon = "✅" if status_class == "complete" else "⏳"
                    st.markdown(
                        f'<div class="progress-step {status_class}">{icon} {log["step"]}</div>',
                        unsafe_allow_html=True
                    )
            
            progress_bar.progress((idx + 1) / len(steps))
            time.sleep(0.8)
        
        detailed_data = self.generate_sample_data(services)
        
        st.session_state.results = {
            'services': services,
            'report': self.generate_sample_report(services, detailed_data),
            'detailed_data': detailed_data,
            'timestamp': datetime.now().isoformat()
        }
        
        status_text.success("분석 완료!")
        time.sleep(0.5)
        st.session_state.analysis_done = True
        st.rerun()
    
    def generate_sample_data(self, services: List[str]) -> Dict:
        import random
        
        sample_data = {
            'service_analyses': {},
            'risk_assessments': {},
            'improvement_suggestions': {}
        }
        
        for svc in services:
            sample_data['service_analyses'][svc] = {
                "service_overview": {
                    "description": f"{svc}는 고급 AI 기능을 제공하는 서비스입니다.",
                    "main_features": ["기능 1", "기능 2", "기능 3", "기능 4"],
                    "target_users": "일반 사용자, 기업",
                    "use_cases": ["콘텐츠 생성", "분석", "개발"]
                }
            }
            
            scores = {}
            dimension_details = {}
            
            for dim_key in self.dimensions.keys():
                score = round(random.uniform(2.8, 4.6), 1)
                scores[dim_key] = score
                
                dimension_details[dim_key] = {
                    'score': score,
                    'risk_level': '낮음' if score >= 4 else '중간' if score >= 3 else '높음',
                    'description': f"{self.dimensions[dim_key]} 평가 결과",
                    'evidence': [f"증거 {i}" for i in range(1, 4)],
                    'guideline_compliance': {
                        g: {"status": "준수", "requirement": "테스트"} 
                        for g in ["EU AI Act", "UNESCO AI Ethics", "OECD AI Principles"]
                    },
                    'reasoning': f"점수 {score}는 종합 평가 결과입니다.",
                    'risks_identified': [f"위험 {i}" for i in range(1, 3)],
                    'strengths': [f"강점 {i}" for i in range(1, 3)]
                }
            
            overall_score = round(sum(scores.values()) / len(scores), 1)
            
            sample_data['risk_assessments'][svc] = {
                'overall_score': overall_score,
                'overall_risk_level': '낮음' if overall_score >= 4 else '중간',
                **dimension_details
            }
            
            sample_data['improvement_suggestions'][svc] = [
                {
                    'dimension': self.dimensions[dim],
                    'priority': '상',
                    'current_score': scores[dim],
                    'target_score': min(5.0, scores[dim] + 1.0),
                    'current_issues': [f"이슈 {i}" for i in range(1, 3)],
                    'improvements': [{
                        'title': f'{self.dimensions[dim]} 개선',
                        'description': '개선 방안 설명',
                        'implementation_steps': [f'단계 {i}' for i in range(1, 5)],
                        'expected_impact': '30% 향상',
                        'timeline': '3-6개월'
                    }]
                }
                for dim in self.dimensions.keys() if scores[dim] < 4.5
            ]
        
        return sample_data
    
    def generate_sample_report(self, services: List[str], data: Dict) -> str:
        report = f"""# AI 윤리성 리스크 진단 보고서

**생성일**: {datetime.now().strftime('%Y년 %m월 %d일')}  
**분석 대상**: {', '.join(services)}  
**평가 기준**: EU AI Act, UNESCO AI Ethics, OECD AI Principles

## 1. 종합 평가

"""
        
        for svc in services:
            score = data['risk_assessments'][svc]['overall_score']
            report += f"- **{svc}**: {score}/5\n"
        
        report += "\n## 2. 차원별 평가\n\n"
        
        for svc in services:
            report += f"### {svc}\n\n"
            assessment = data['risk_assessments'][svc]
            
            for dim_key in self.dimensions.keys():
                dim_name = self.dimensions[dim_key]
                dim_data = assessment[dim_key]
                report += f"- {dim_name}: {dim_data['score']}/5\n"
            
            report += "\n"
        
        return report
    
    def render_results_page(self):
        results = st.session_state.results
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("📄 PDF 생성", use_container_width=True):
                with st.spinner("PDF 생성 중..."):
                    pdf_bytes = self.generate_pdf_report(results)
                    if pdf_bytes:
                        st.session_state.pdf_generated = True
                        st.session_state.pdf_content = pdf_bytes
        
        if st.session_state.pdf_generated and st.session_state.pdf_content:
            with col3:
                st.download_button(
                    "⬇️ 다운로드",
                    st.session_state.pdf_content,
                    file_name=f"ethics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 종합 대시보드",
            "📈 상세 평가",
            "💡 개선 권고안",
            "🔍 비교 분석",
            "📄 최종 보고서"
        ])
        
        with tab1:
            self.render_overview_tab(results)
        with tab2:
            self.render_detailed_tab(results)
        with tab3:
            self.render_improvement_tab(results)
        with tab4:
            self.render_comparison_tab(results)
        with tab5:
            self.render_report_tab(results)
    
    def render_overview_tab(self, results: Dict):
        st.markdown('<div class="section-header">📊 종합 평가 대시보드</div>', 
                   unsafe_allow_html=True)
        
        data = results['detailed_data']
        services = results['services']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
<div class="metric-card">
    <h3>분석 서비스</h3>
    <div class="metric-value">{len(services)}</div>
</div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_score = sum([svc['overall_score'] 
                           for svc in data['risk_assessments'].values()]) / len(services)
            color_class = "risk-low" if avg_score >= 4 else "risk-medium" if avg_score >= 3 else "risk-high"
            st.markdown(f"""
<div class="metric-card {color_class}">
    <h3>평균 점수</h3>
    <div class="metric-value">{avg_score:.1f}/5</div>
</div>
            """, unsafe_allow_html=True)
        
        with col3:
            risk_level = "낮음" if avg_score >= 4 else "중간" if avg_score >= 3 else "높음"
            st.markdown(f"""
<div class="metric-card {color_class}">
    <h3>종합 리스크</h3>
    <div class="metric-value">{risk_level}</div>
</div>
            """, unsafe_allow_html=True)
        
        with col4:
            improvement_count = sum([len(v) for v in data['improvement_suggestions'].values()])
            st.markdown(f"""
<div class="metric-card">
    <h3>개선 과제</h3>
    <div class="metric-value">{improvement_count}개</div>
</div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4>📡 차원별 평가 분포</h4>", unsafe_allow_html=True)
            fig = go.Figure()
            
            for service in services:
                scores = data['risk_assessments'][service]
                values = [scores[dim]['score'] for dim in self.dimensions.keys()]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=[self.dimensions[dim] for dim in self.dimensions.keys()],
                    fill='toself',
                    name=service,
                    opacity=0.7
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True,
                height=450,
                font=dict(size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<h4>📊 서비스별 종합 점수</h4>", unsafe_allow_html=True)
            
            df = pd.DataFrame([
                {
                    '서비스': svc,
                    '점수': data['risk_assessments'][svc]['overall_score']
                }
                for svc in services
            ])
            
            fig = px.bar(
                df,
                x='서비스',
                y='점수',
                color='점수',
                color_continuous_scale=['#f5576c', '#fee140', '#84fab0'],
                range_color=[0, 5],
                text='점수'
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                height=450,
                showlegend=False,
                yaxis_range=[0, 5]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("<h3>📋 서비스별 요약</h3>", unsafe_allow_html=True)
        
        summary_cols = st.columns(len(services))
        for idx, service in enumerate(services):
            with summary_cols[idx]:
                assessment = data['risk_assessments'][service]
                score = assessment['overall_score']
                
                if score >= 4:
                    status_emoji = "✅"
                    status_text = "우수"
                    color = "background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);"
                elif score >= 3:
                    status_emoji = "⚠️"
                    status_text = "개선필요"
                    color = "background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);"
                else:
                    status_emoji = "❌"
                    status_text = "위험"
                    color = "background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);"
                
                st.markdown(f"""
<div style="
    {color}
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
">
    <h3 style="margin: 0 0 10px 0;">{service}</h3>
    <h2 style="margin: 0;">{score}/5</h2>
    <p style="margin: 10px 0 0 0;"><strong>{status_emoji} {status_text}</strong></p>
</div>
                """, unsafe_allow_html=True)
    
    def render_detailed_tab(self, results: Dict):
        st.markdown('<div class="section-header">📈 상세 평가</div>', 
                   unsafe_allow_html=True)
        
        data = results['detailed_data']
        services = results['services']
        
        selected_service = st.selectbox("서비스 선택", services, key="detailed_select")
        
        if selected_service:
            assessment = data['risk_assessments'][selected_service]
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                score = assessment['overall_score']
                if score >= 4:
                    color = "🟢"
                elif score >= 3:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.markdown(f"""
<div class="detail-card">
    <h4>{selected_service} 평가 결과</h4>
    <p style="font-size: 1.5rem; font-weight: bold; margin: 10px 0;">
        {color} {score}/5
    </p>
    <p><strong>리스크 수준:</strong> {assessment['overall_risk_level']}</p>
</div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
<div class="detail-card">
    <h4>평가 설명</h4>
    <p>{assessment.get('description', 'N/A')}</p>
</div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown("<h3>📋 차원별 상세 평가</h3>", unsafe_allow_html=True)
            
            for dim_key in self.dimensions.keys():
                dim_name = self.dimensions[dim_key]
                dim_data = assessment[dim_key]
                
                with st.expander(
                    f"{'🟢' if dim_data['score'] >= 4 else '🟡' if dim_data['score'] >= 3 else '🔴'} "
                    f"{dim_name} - {dim_data['score']}/5"
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("점수", f"{dim_data['score']}/5")
                    
                    with col2:
                        st.metric("리스크", dim_data['risk_level'])
                    
                    with col3:
                        if isinstance(dim_data.get('guideline_compliance'), dict):
                            compliance_count = sum(
                                1 for c in dim_data['guideline_compliance'].values()
                                if isinstance(c, dict) and 
                                ('준수' in c.get('status', '') or 'Compliant' in c.get('status', ''))
                            )
                            st.metric("가이드라인 준수", f"{compliance_count}/3")
                    
                    st.markdown("---")
                    
                    st.markdown(f"""
<div class="detail-card">
    <h4>평가 설명</h4>
    <p>{dim_data.get('description', 'N/A')}</p>
</div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**📌 주요 증거**")
                    for evidence in dim_data.get('evidence', []):
                        st.markdown(f'<div class="evidence-item">✓ {evidence}</div>', 
                                   unsafe_allow_html=True)
                    
                    st.markdown("**⚖️ 가이드라인 준수 현황**")
                    
                    if isinstance(dim_data.get('guideline_compliance'), dict):
                        for guideline, compliance in dim_data['guideline_compliance'].items():
                            if isinstance(compliance, dict):
                                status = compliance.get('status', 'N/A')
                                emoji = "✅" if '준수' in status else "⚠️" if '부분' in status else "❌"
                                
                                st.markdown(f"{emoji} **{guideline}**: {status}")
                    
                    if dim_data.get('risks_identified'):
                        st.markdown("**⚠️ 발견된 리스크**")
                        for risk in dim_data['risks_identified']:
                            st.markdown(f'<div class="risk-item">⚠️ {risk}</div>', 
                                       unsafe_allow_html=True)
                    
                    if dim_data.get('strengths'):
                        st.markdown("**✅ 강점**")
                        for strength in dim_data['strengths']:
                            st.markdown(f'<div class="strength-item">✓ {strength}</div>', 
                                       unsafe_allow_html=True)
    
    def render_improvement_tab(self, results: Dict):
        st.markdown('<div class="section-header">💡 개선 권고안</div>', 
                   unsafe_allow_html=True)
        
        data = results['detailed_data']
        services = results['services']
        
        selected_service = st.selectbox("서비스 선택", services, key="improvement_select")
        
        if selected_service:
            improvements = data['improvement_suggestions'][selected_service]
            
            if not improvements:
                st.success("🎉 현재 모든 영역이 우수합니다!")
            else:
                priority_options = ["전체", "상", "중", "하"]
                priority_filter = st.radio("우선순위 필터", priority_options, 
                                          horizontal=True)
                
                filtered_improvements = improvements if priority_filter == "전체" else [
                    imp for imp in improvements if imp['priority'] == priority_filter
                ]
                
                for idx, imp in enumerate(filtered_improvements, 1):
                    priority_colors = {
                        "상": "🔴",
                        "중": "🟡",
                        "하": "🟢"
                    }
                    
                    priority_emoji = priority_colors.get(imp['priority'], "")
                    
                    with st.expander(
                        f"{priority_emoji} {idx}. {imp['dimension']} "
                        f"(우선순위: {imp['priority']})",
                        expanded=(idx == 1)
                    ):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("현재 점수", f"{imp['current_score']}/5")
                        
                        with col2:
                            st.metric("목표 점수", f"{imp['target_score']}/5")
                        
                        with col3:
                            improvement = imp['target_score'] - imp['current_score']
                            st.metric("개선 목표", f"+{improvement:.1f}")
                        
                        st.markdown("---")
                        
                        st.markdown(
                            '<div class="improvement-detail"><h5>현재 문제점</h5>',
                            unsafe_allow_html=True
                        )
                        for issue in imp['current_issues']:
                            st.markdown(f"• {issue}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.markdown("### 🎯 권장 개선 조치")
                        
                        for action_idx, action in enumerate(imp['improvements'], 1):
                            st.markdown(f"#### {action_idx}. {action['title']}")
                            st.write(action['description'])
                            
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown("**📋 구현 단계**")
                                for step in action['implementation_steps']:
                                    st.markdown(f"- {step}")
                            
                            with col2:
                                st.info(f"""
**📊 기대 효과**

{action['expected_impact']}

**⏱️ 소요 기간**

{action['timeline']}
                                """)
    
    def render_comparison_tab(self, results: Dict):
        st.markdown('<div class="section-header">🔍 서비스 비교 분석</div>', 
                   unsafe_allow_html=True)
        
        data = results['detailed_data']
        services = results['services']
        
        if len(services) < 2:
            st.info("비교 분석은 2개 이상의 서비스가 필요합니다.")
            return
        
        st.markdown("### 📊 차원별 점수 비교")
        
        comparison_data = []
        for dim_key in self.dimensions.keys():
            dim_name = self.dimensions[dim_key]
            row = {"차원": dim_name}
            for svc in services:
                row[svc] = data['risk_assessments'][svc][dim_key]['score']
            comparison_data.append(row)
        
        df_comparison = pd.DataFrame(comparison_data)
        
        def color_score(val):
            if isinstance(val, (int, float)):
                if val >= 4:
                    return 'background-color: #c8e6c9; color: #1b5e20; font-weight: bold;'
                elif val >= 3:
                    return 'background-color: #fff9c4; color: #f57f17; font-weight: bold;'
                else:
                    return 'background-color: #ffcdd2; color: #b71c1c; font-weight: bold;'
            return ''
        
        try:
            styled_df = df_comparison.style.map(color_score, subset=services)
        except:
            styled_df = df_comparison
        
        st.dataframe(styled_df, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### 🌡️ 점수 히트맵")
        
        heatmap_data = []
        for svc in services:
            row = [data['risk_assessments'][svc][dim]['score'] 
                  for dim in self.dimensions.keys()]
            heatmap_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=[self.dimensions[dim] for dim in self.dimensions.keys()],
            y=services,
            colorscale='RdYlGn',
            zmid=3,
            zmin=0,
            zmax=5,
            text=[[f"{val:.1f}" for val in row] for row in heatmap_data],
            texttemplate='%{text}',
            textfont={"size": 14},
            colorbar=dict(title="점수")
        ))
        
        fig.update_layout(
            height=300 + len(services) * 60,
            xaxis_title="평가 차원",
            yaxis_title="서비스"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### 🏆 종합 순위")
        
        rankings = []
        for service in services:
            score = data['risk_assessments'][service]['overall_score']
            rankings.append((service, score))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        
        rank_cols = st.columns(len(rankings))
        for idx, (service, score) in enumerate(rankings):
            medal_emoji = ["🥇", "🥈", "🥉"]
            medal = medal_emoji[idx] if idx < 3 else f"{idx+1}위"
            
            with rank_cols[idx]:
                st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
">
    <h1 style="margin: 0;">{medal}</h1>
    <h3 style="margin: 10px 0 0 0;">{service}</h3>
    <h2 style="margin: 10px 0 0 0;">{score}/5</h2>
</div>
                """, unsafe_allow_html=True)
    
    def render_report_tab(self, results: Dict):
        st.markdown('<div class="section-header">📄 최종 보고서</div>', 
                   unsafe_allow_html=True)
        
        report_md = results.get('report', '')
        
        st.markdown(report_md)
        
        st.markdown("---")
        st.markdown("### 💾 보고서 다운로드")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                "📥 마크다운",
                report_md,
                file_name=f"ethics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            json_data = json.dumps(results['detailed_data'], 
                                  ensure_ascii=False, indent=2)
            st.download_button(
                "📥 JSON",
                json_data,
                file_name=f"ethics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            services = results['services']
            data = results['detailed_data']
            
            csv_data = []
            for svc in services:
                row = {"서비스": svc}
                for dim_key in self.dimensions.keys():
                    dim_name = self.dimensions[dim_key]
                    row[dim_name] = data['risk_assessments'][svc][dim_key]['score']
                row["종합점수"] = data['risk_assessments'][svc]['overall_score']
                csv_data.append(row)
            
            df_csv = pd.DataFrame(csv_data)
            csv_string = df_csv.to_csv(index=False, encoding='utf-8-sig')
            
            st.download_button(
                "📥 CSV",
                csv_string,
                file_name=f"ethics_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )


if __name__ == "__main__":
    dashboard = EthicsDashboard()
    dashboard.run()
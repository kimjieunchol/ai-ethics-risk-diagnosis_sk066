import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import sys
from typing import Dict, List
import pandas as pd

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 실제 시스템 import
try:
    from app import AIEthicsAssessmentSystem
    SYSTEM_AVAILABLE = True
except ImportError:
    try:
        from main import AIEthicsAssessmentSystem
        SYSTEM_AVAILABLE = True
    except ImportError:
        SYSTEM_AVAILABLE = False

# 페이지 설정
st.set_page_config(
    page_title="AI 윤리성 리스크 진단",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header { 
        font-size: 2.5rem; 
        font-weight: bold; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-bottom: 2rem; 
    }
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 20px; 
        border-radius: 15px; 
        color: white; 
        text-align: center; 
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .risk-high { 
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
    }
    .risk-medium { 
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
        color: #333;
    }
    .risk-low { 
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
        color: #333;
    }
    .detail-card { 
        border-left: 4px solid #667eea; 
        padding: 20px; 
        margin: 15px 0; 
        background: #f8f9fa; 
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .evidence-item {
        background: #e3f2fd;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 3px solid #2196f3;
    }
    .risk-item {
        background: #ffebee;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 3px solid #f44336;
    }
    .strength-item {
        background: #e8f5e9;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 3px solid #4caf50;
    }
    .guideline-box {
        background: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    .progress-step {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        font-size: 14px;
    }
    .progress-step.complete {
        background: #e8f5e9;
        border-left-color: #4caf50;
    }
    .progress-step.active {
        background: #fff3e0;
        border-left-color: #ff9800;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .improvement-detail {
        background: #f0fff4;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border: 2px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)


class EthicsDashboard:
    """윤리성 평가 대시보드"""
    
    def __init__(self):
        self.dimensions = {
            "fairness": "공정성 및 편향성",
            "privacy": "프라이버시 보호",
            "transparency": "투명성 및 설명가능성",
            "accountability": "책임성 및 거버넌스",
            "safety": "안전성 및 보안"
        }
        
        self.dimensions_en = {
            "fairness": "Fairness & Bias",
            "privacy": "Privacy Protection",
            "transparency": "Transparency & Explainability",
            "accountability": "Accountability & Governance",
            "safety": "Safety & Security"
        }
        
        self.initialize_session_state()
        
        # 실제 시스템 초기화
        if SYSTEM_AVAILABLE and 'system' not in st.session_state:
            with st.spinner("시스템 초기화 중..." if self.is_korean() else "Initializing system..."):
                st.session_state.system = AIEthicsAssessmentSystem()
    
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if 'analysis_done' not in st.session_state:
            st.session_state.analysis_done = False
        if 'results' not in st.session_state:
            st.session_state.results = None
        if 'progress_logs' not in st.session_state:
            st.session_state.progress_logs = []
        if 'language' not in st.session_state:
            st.session_state.language = 'ko'
    
    def is_korean(self):
        """현재 언어가 한국어인지 확인"""
        return st.session_state.language == 'ko'
    
    def t(self, key: str) -> str:
        """번역 텍스트 반환"""
        texts = {
            'ko': {
                'main_title': '⚖️ AI 윤리성 리스크 진단 시스템',
                'settings': '🔧 설정',
                'language_setting': '🌐 언어 설정',
                'analysis_services': '📋 분석 서비스',
                'select_services': '분석할 AI 서비스를 선택하세요 (최대 3개)',
                'evaluation_settings': '⚙️ 평가 설정',
                'applied_guidelines': '적용 가이드라인',
                'start_analysis': '🚀 분석 시작',
                'previous_reports': '📂 이전 보고서',
                'load_report': '보고서 불러오기',
                'evaluation_dimensions': 'ℹ️ 평가 차원',
                'welcome_title': '환영합니다! 👋',
                'welcome_desc': '''AI 서비스의 윤리적 리스크를 종합적으로 진단하고 개선 방향을 제시합니다.

✨ **주요 기능**
- ⚖️ 5개 차원 심층 윤리 평가
- 📊 실시간 분석 진행 모니터링
- 💡 구체적인 개선 권고안
- 📈 가이드라인별 준수 현황
- 🔍 서비스 간 비교 분석

👈 **시작하기**: 왼쪽에서 분석할 서비스를 선택하세요!''',
                'analysis_in_progress': '🔄 분석 진행 중...',
                'analysis_complete': '✅ 분석 완료!',
                'tab_overview': '📊 종합 대시보드',
                'tab_detailed': '📈 상세 평가',
                'tab_improvement': '💡 개선 권고안',
                'tab_comparison': '🔍 비교 분석',
                'tab_report': '📄 최종 보고서',
                'new_analysis': '🔄 새로운 분석',
                'save_results': '💾 결과 저장',
                'download_report': '📥 보고서 다운로드',
                'analyzed_services': '분석 서비스',
                'avg_score': '평균 점수',
                'overall_risk': '종합 리스크',
                'improvements': '개선 권고',
                'low': '낮음',
                'medium': '중간',
                'high': '높음',
                'dimension_evaluation': '차원별 평가',
                'score_comparison': '종합 점수 비교',
                'service': '서비스',
                'overall_score': '종합점수',
                'detailed_evaluation': '상세 평가',
                'select_service': '서비스 선택',
                'risk': '리스크',
                'overall_assessment': '종합 평가',
                'excellent': '우수한 윤리성 수준을 보입니다',
                'good': '양호하나 개선이 필요합니다',
                'needs_improvement': '중대한 개선이 필요합니다',
                'dimension_details': '차원별 상세 평가',
                'score': '점수',
                'guideline_compliance': '가이드라인 준수',
                'evaluation_desc': '평가 설명',
                'key_evidence': '주요 증거',
                'no_evidence': '증거 정보가 없습니다',
                'identified_risks': '발견된 리스크',
                'strengths': '강점',
                'improvement_recommendations': '개선 권고안',
                'all_excellent': '🎉 현재 모든 영역이 우수합니다!',
                'priority_filter': '우선순위 필터',
                'all': '전체',
                'priority_high': '상',
                'priority_medium': '중',
                'priority_low': '하',
                'current_score': '현재 점수',
                'target_score': '목표 점수',
                'improvement_goal': '개선 목표',
                'current_issues': '현재 문제점',
                'recommended_actions': '권장 개선 조치',
                'implementation_steps': '구현 단계',
                'expected_impact': '기대 효과',
                'timeline': '소요 기간',
                'comparison_analysis': '비교 분석',
                'comparison_note': '비교 분석은 2개 이상의 서비스가 필요합니다',
                'dimension_comparison': '차원별 점수 비교',
                'dimension': '차원',
                'score_heatmap': '점수 히트맵',
                'final_report': '최종 보고서',
                'report_download': '보고서 다운로드',
                'report_saved': '보고서가 저장되었습니다',
                'no_saved_reports': '저장된 보고서가 없습니다',
                'select_report': '불러올 보고서 선택',
                'load': '불러오기',
                'report_loaded': '보고서를 불러왔습니다',
            },
            'en': {
                'main_title': '⚖️ AI Ethics Risk Assessment System',
                'settings': '🔧 Settings',
                'language_setting': '🌐 Language',
                'analysis_services': '📋 Analysis Services',
                'select_services': 'Select AI services to analyze (max 3)',
                'evaluation_settings': '⚙️ Evaluation Settings',
                'applied_guidelines': 'Applied Guidelines',
                'start_analysis': '🚀 Start Analysis',
                'previous_reports': '📂 Previous Reports',
                'load_report': 'Load Report',
                'evaluation_dimensions': 'ℹ️ Evaluation Dimensions',
                'welcome_title': 'Welcome! 👋',
                'welcome_desc': '''Comprehensively diagnose ethical risks of AI services and provide improvement directions.

✨ **Key Features**
- ⚖️ In-depth ethics evaluation across 5 dimensions
- 📊 Real-time analysis progress monitoring
- 💡 Specific improvement recommendations
- 📈 Guideline compliance status
- 🔍 Service comparison analysis

👈 **Get Started**: Select services to analyze from the left!''',
                'analysis_in_progress': '🔄 Analysis in Progress...',
                'analysis_complete': '✅ Analysis Complete!',
                'tab_overview': '📊 Overview',
                'tab_detailed': '📈 Detailed Assessment',
                'tab_improvement': '💡 Improvements',
                'tab_comparison': '🔍 Comparison',
                'tab_report': '📄 Report',
                'new_analysis': '🔄 New Analysis',
                'save_results': '💾 Save Results',
                'download_report': '📥 Download Report',
                'analyzed_services': 'Services',
                'avg_score': 'Avg Score',
                'overall_risk': 'Risk Level',
                'improvements': 'Improvements',
                'low': 'Low',
                'medium': 'Medium',
                'high': 'High',
                'dimension_evaluation': 'Dimension Evaluation',
                'score_comparison': 'Score Comparison',
                'service': 'Service',
                'overall_score': 'Overall Score',
                'detailed_evaluation': 'Detailed Assessment',
                'select_service': 'Select Service',
                'risk': 'Risk',
                'overall_assessment': 'Overall Assessment',
                'excellent': 'shows excellent ethics level',
                'good': 'is good but needs improvement',
                'needs_improvement': 'needs significant improvement',
                'dimension_details': 'Dimension Details',
                'score': 'Score',
                'guideline_compliance': 'Guideline Compliance',
                'evaluation_desc': 'Evaluation Description',
                'key_evidence': 'Key Evidence',
                'no_evidence': 'No evidence information available',
                'identified_risks': 'Identified Risks',
                'strengths': 'Strengths',
                'improvement_recommendations': 'Improvement Recommendations',
                'all_excellent': '🎉 All areas are currently excellent!',
                'priority_filter': 'Priority Filter',
                'all': 'All',
                'priority_high': 'High',
                'priority_medium': 'Medium',
                'priority_low': 'Low',
                'current_score': 'Current',
                'target_score': 'Target',
                'improvement_goal': 'Goal',
                'current_issues': 'Current Issues',
                'recommended_actions': 'Recommended Actions',
                'implementation_steps': 'Implementation Steps',
                'expected_impact': 'Expected Impact',
                'timeline': 'Timeline',
                'comparison_analysis': 'Comparison Analysis',
                'comparison_note': 'Comparison requires 2 or more services',
                'dimension_comparison': 'Dimension Score Comparison',
                'dimension': 'Dimension',
                'score_heatmap': 'Score Heatmap',
                'final_report': 'Final Report',
                'report_download': 'Download Report',
                'report_saved': 'Report has been saved',
                'no_saved_reports': 'No saved reports',
                'select_report': 'Select report to load',
                'load': 'Load',
                'report_loaded': 'Report loaded successfully',
            }
        }
        
        lang = 'ko' if self.is_korean() else 'en'
        return texts.get(lang, texts['ko']).get(key, key)
    
    def get_dimension_name(self, key: str) -> str:
        """차원 이름 반환 (언어별)"""
        if self.is_korean():
            return self.dimensions.get(key, key)
        else:
            return self.dimensions_en.get(key, key)
    
    def run(self):
        """대시보드 실행"""
        if not SYSTEM_AVAILABLE:
            warning_msg = "⚠️ AIEthicsAssessmentSystem을 불러올 수 없습니다. 데모 모드로 실행됩니다." if self.is_korean() else "⚠️ AIEthicsAssessmentSystem unavailable. Running in demo mode."
            st.warning(warning_msg)
        
        st.markdown(f'<div class="main-header">{self.t("main_title")}</div>', unsafe_allow_html=True)
        
        # 사이드바
        with st.sidebar:
            st.header(self.t('settings'))
            self.render_sidebar()
        
        # 메인 컨텐츠
        if not st.session_state.analysis_done:
            self.render_welcome_page()
        else:
            self.render_results_page()
    
    def render_sidebar(self):
        """사이드바 렌더링"""
        # 언어 선택
        st.markdown(f"### {self.t('language_setting')}")
        lang_options = ['한국어', 'English']
        current_idx = 0 if self.is_korean() else 1
        
        selected_lang = st.radio(
            "Language / 언어",
            options=lang_options,
            index=current_idx,
            horizontal=True,
            label_visibility="collapsed"
        )
        
        new_lang = 'ko' if selected_lang == '한국어' else 'en'
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()
        
        st.markdown("---")
        
        # 서비스 선택
        st.markdown(f"### {self.t('analysis_services')}")
        services = st.multiselect(
            self.t('select_services'),
            ["ChatGPT", "Claude", "Google Gemini", "Copilot", "Midjourney", "DALL-E"],
            max_selections=3
        )
        
        # 평가 설정
        st.markdown(f"### {self.t('evaluation_settings')}")
        guideline_text = f"**{self.t('applied_guidelines')}**\n- EU AI Act\n- UNESCO AI Ethics\n- OECD AI Principles"
        st.info(guideline_text)
        
        if st.button(self.t('start_analysis'), disabled=len(services)==0):
            self.start_analysis(services)
        
        st.markdown("---")
        
        # 이전 보고서
        st.markdown(f"### {self.t('previous_reports')}")
        if st.button(self.t('load_report')):
            self.load_previous_report()
        
        st.markdown("---")
        
        # 평가 차원
        st.markdown(f"### {self.t('evaluation_dimensions')}")
        dim_emojis = ["🎯", "🔒", "🔍", "⚖️", "🛡️"]
        for emoji, dim_key in zip(dim_emojis, self.dimensions.keys()):
            st.markdown(f"{emoji} {self.get_dimension_name(dim_key)}")
    
    def render_welcome_page(self):
        """환영 페이지"""
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f"## {self.t('welcome_title')}")
            st.markdown(self.t('welcome_desc'))
    
    def start_analysis(self, services: List[str]):
        """실제 시스템 분석 실행"""
        st.session_state.progress_logs = []
        
        # 진행 상황 표시 영역
        progress_container = st.container()
        
        with progress_container:
            st.markdown(f"### {self.t('analysis_in_progress')}")
            progress_area = st.empty()
            status_text = st.empty()
            progress_bar = st.progress(0)
        
        try:
            if SYSTEM_AVAILABLE:
                # 실제 시스템 실행
                msg = "실제 AI 윤리성 분석 시스템을 실행합니다..." if self.is_korean() else "Running real AI ethics analysis system..."
                status_text.info(msg)
                
                # 임시 출력 디렉토리
                output_dir = "outputs/streamlit_temp"
                os.makedirs(output_dir, exist_ok=True)
                
                # 분석 실행
                report = st.session_state.system.analyze_services(
                    service_names=services,
                    output_dir=output_dir
                )
                
                # 결과 로드
                latest_files = sorted([f for f in os.listdir(output_dir) if f.endswith('_data.json')])
                if latest_files:
                    with open(os.path.join(output_dir, latest_files[-1]), 'r', encoding='utf-8') as f:
                        detailed_data = json.load(f)
                    
                    st.session_state.results = {
                        'services': services,
                        'report': report,
                        'detailed_data': detailed_data,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    progress_bar.progress(1.0)
                    status_text.success(self.t('analysis_complete'))
                    st.session_state.analysis_done = True
                    st.rerun()
            else:
                # 데모 모드
                demo_msg = "⚠️ 데모 모드로 실행됩니다." if self.is_korean() else "⚠️ Running in demo mode."
                st.warning(demo_msg)
                self.run_demo_analysis(services, progress_area, progress_bar, status_text)
                
        except Exception as e:
            error_msg = f"❌ 분석 중 오류 발생: {e}" if self.is_korean() else f"❌ Error during analysis: {e}"
            st.error(error_msg)
            import traceback
            with st.expander("Error details" if not self.is_korean() else "오류 상세"):
                st.code(traceback.format_exc())
    
    def run_demo_analysis(self, services, progress_area, progress_bar, status_text):
        """데모 분석"""
        import time
        
        if self.is_korean():
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
        else:
            steps = [
                "Initializing system...",
                f"Starting analysis: {', '.join(services)}",
                "Step 1: Collecting service information...",
                "Step 2: Assessing ethical risks...",
                "Step 3: Verifying guideline compliance...",
                "Step 4: Generating improvements...",
                "Step 5: Comparing services..." if len(services) > 1 else "Step 5: Skipping...",
                "Step 6: Writing final report...",
            ]
        
        for idx, step in enumerate(steps):
            st.session_state.progress_logs.append({"step": step, "status": "active"})
            
            with progress_area:
                for i, log in enumerate(st.session_state.progress_logs):
                    if i == len(st.session_state.progress_logs) - 1:
                        st.markdown(f'<div class="progress-step active">⏳ {log["step"]}</div>', 
                                   unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="progress-step complete">✅ {log["step"]}</div>', 
                                   unsafe_allow_html=True)
            
            progress_bar.progress((idx + 1) / len(steps))
            time.sleep(1)
            st.session_state.progress_logs[-1]["status"] = "complete"
        
        # 상세한 샘플 결과 생성
        detailed_data = self.generate_detailed_sample_data(services)
        
        st.session_state.results = {
            'services': services,
            'report': self.generate_detailed_report(services, detailed_data),
            'detailed_data': detailed_data,
            'timestamp': datetime.now().isoformat()
        }
        
        status_text.success(self.t('analysis_complete'))
        time.sleep(1)
        st.session_state.analysis_done = True
        st.rerun()
    
    def generate_detailed_sample_data(self, services: List[str]) -> Dict:
        """상세한 샘플 데이터 생성"""
        import random
        
        if self.is_korean():
            guideline_requirements = {
                "EU AI Act": {
                    "fairness": "고위험 AI 시스템의 경우 편향성 테스트 및 완화 조치 필수",
                    "privacy": "GDPR 준수 및 데이터 최소화 원칙 적용",
                    "transparency": "AI 시스템 작동 방식에 대한 명확한 설명 제공",
                    "accountability": "책임자 지정 및 사고 보고 체계 구축",
                    "safety": "위험 관리 시스템 및 사전 적합성 평가 수행"
                },
                "UNESCO AI Ethics": {
                    "fairness": "다양성 존중 및 차별 방지",
                    "privacy": "개인정보 자기결정권 보장",
                    "transparency": "알고리즘의 이해가능성 확보",
                    "accountability": "인간 감독 및 개입 가능성 확보",
                    "safety": "인간 복지 및 안전 우선"
                },
                "OECD AI Principles": {
                    "fairness": "포용적 성장 및 지속가능한 발전",
                    "privacy": "인권과 민주적 가치 존중",
                    "transparency": "AI 시스템 투명성 및 책임있는 공개",
                    "accountability": "견고하고 안전한 AI",
                    "safety": "위험 기반 접근 및 지속적 모니터링"
                }
            }
        else:
            guideline_requirements = {
                "EU AI Act": {
                    "fairness": "Bias testing and mitigation required for high-risk AI systems",
                    "privacy": "GDPR compliance and data minimization principles",
                    "transparency": "Clear explanation of AI system operation",
                    "accountability": "Designated responsible person and incident reporting system",
                    "safety": "Risk management system and pre-conformity assessment"
                },
                "UNESCO AI Ethics": {
                    "fairness": "Respect for diversity and prevention of discrimination",
                    "privacy": "Guarantee of personal information self-determination",
                    "transparency": "Ensuring algorithm understandability",
                    "accountability": "Human oversight and intervention capability",
                    "safety": "Priority on human welfare and safety"
                },
                "OECD AI Principles": {
                    "fairness": "Inclusive growth and sustainable development",
                    "privacy": "Respect for human rights and democratic values",
                    "transparency": "AI system transparency and responsible disclosure",
                    "accountability": "Robust and secure AI",
                    "safety": "Risk-based approach and continuous monitoring"
                }
            }
        
        sample_data = {
            'service_analyses': {},
            'risk_assessments': {},
            'improvement_suggestions': {},
            'comparison_analysis': self.generate_comparison_text(services)
        }
        
        for svc in services:
            if self.is_korean():
                service_desc = f"{svc}는 대규모 언어 모델 기반 AI 서비스로, 다양한 텍스트 생성 및 대화 기능을 제공합니다."
                features = ["텍스트 생성", "대화형 인터페이스", "다국어 지원", "컨텍스트 이해"]
                target = "일반 사용자, 기업, 개발자"
                use_cases = ["콘텐츠 작성", "고객 서비스", "교육", "연구 지원"]
            else:
                service_desc = f"{svc} is a large language model-based AI service providing various text generation and conversational capabilities."
                features = ["Text generation", "Conversational interface", "Multilingual support", "Context understanding"]
                target = "General users, Enterprises, Developers"
                use_cases = ["Content creation", "Customer service", "Education", "Research support"]
            
            sample_data['service_analyses'][svc] = {
                "service_overview": {
                    "description": service_desc,
                    "main_features": features,
                    "target_users": target,
                    "use_cases": use_cases
                }
            }
            
            scores = {}
            dimension_details = {}
            
            for dim_key in self.dimensions.keys():
                dim_name = self.get_dimension_name(dim_key)
                score = round(random.uniform(2.8, 4.6), 1)
                
                if score >= 4.0:
                    risk_level = self.t('low')
                    description = f"{dim_name} 영역에서 우수한 수준을 보입니다." if self.is_korean() else f"Shows excellent level in {dim_name}."
                    risks = []
                    strengths = [f"명확한 {dim_name} 정책 수립", "정기적인 모니터링 및 평가"] if self.is_korean() else [f"Clear {dim_name} policy", "Regular monitoring"]
                    evidence = [f"공개된 {dim_name} 가이드라인 문서 확인", "독립적인 제3자 감사 수행"] if self.is_korean() else [f"Published {dim_name} guidelines", "Independent audit"]
                elif score >= 3.0:
                    risk_level = self.t('medium')
                    description = f"{dim_name} 영역에서 기본적인 요구사항은 충족하나 개선이 필요합니다." if self.is_korean() else f"Meets basic requirements in {dim_name} but needs improvement."
                    risks = [f"{dim_name} 관련 일부 정책 미흡"] if self.is_korean() else [f"Some {dim_name} policies inadequate"]
                    strengths = ["기본적인 요구사항 충족"] if self.is_korean() else ["Meets basic requirements"]
                    evidence = [f"기본적인 {dim_name} 정책 존재"] if self.is_korean() else [f"Basic {dim_name} policy exists"]
                else:
                    risk_level = self.t('high')
                    description = f"{dim_name} 영역에서 중대한 개선이 필요합니다." if self.is_korean() else f"Needs significant improvement in {dim_name}."
                    risks = [f"{dim_name} 정책 부재 또는 불명확", "가이드라인 미준수"] if self.is_korean() else [f"{dim_name} policy absent or unclear", "Non-compliance"]
                    strengths = ["개선 가능성 존재"] if self.is_korean() else ["Room for improvement"]
                    evidence = ["명확한 정책 문서 미발견"] if self.is_korean() else ["No clear policy found"]
                
                guideline_compliance = {}
                for guideline in ["EU AI Act", "UNESCO AI Ethics", "OECD AI Principles"]:
                    req = guideline_requirements[guideline][dim_key]
                    if score >= 4.0:
                        status = "준수" if self.is_korean() else "Compliant"
                        gap = "없음" if self.is_korean() else "None"
                        evidence_text = f"{guideline}의 요구사항 {status}" if self.is_korean() else f"{guideline} requirements {status}"
                    elif score >= 3.0:
                        status = "부분준수" if self.is_korean() else "Partial compliance"
                        gap_msg = "항목의 완전한 이행 필요" if self.is_korean() else "Full implementation needed"
                        gap = f"'{req}' {gap_msg}"
                        evidence_text = f"{guideline}의 요구사항 {status}" if self.is_korean() else f"{guideline} requirements {status}"
                    else:
                        status = "미준수" if self.is_korean() else "Non-compliant"
                        gap_msg = "항목의 즉각적인 개선 필요" if self.is_korean() else "Immediate improvement needed"
                        gap = f"'{req}' {gap_msg}"
                        evidence_text = f"{guideline}의 요구사항 {status}" if self.is_korean() else f"{guideline} requirements {status}"
                    
                    guideline_compliance[guideline] = {
                        "status": status,
                        "requirement": req,
                        "evidence": evidence_text,
                        "gap": gap
                    }
                
                scores[dim_key] = score
                dimension_details[dim_key] = {
                    'score': score,
                    'risk_level': risk_level,
                    'description': description,
                    'evidence': evidence,
                    'guideline_compliance': guideline_compliance,
                    'reasoning': f"점수 {score}는 정책 문서 분석, 가이드라인 준수 여부 등을 종합적으로 평가한 결과입니다." if self.is_korean() else f"Score {score} is based on comprehensive evaluation of policy analysis and guideline compliance.",
                    'risks_identified': risks,
                    'strengths': strengths
                }
            
            overall_score = round(sum(scores.values()) / len(scores), 1)
            
            sample_data['risk_assessments'][svc] = {
                'overall_score': overall_score,
                'overall_risk_level': self.t('low') if overall_score >= 4 else self.t('medium') if overall_score >= 3 else self.t('high'),
                **dimension_details
            }
            
            # 개선안 생성
            improvements = []
            for dim_key, score in scores.items():
                if score < 4.5:
                    dim_name = self.get_dimension_name(dim_key)
                    if score < 3.0:
                        priority = self.t('priority_high')
                    elif score < 4.0:
                        priority = self.t('priority_medium')
                    else:
                        priority = self.t('priority_low')
                    
                    improvements.append({
                        'dimension': dim_name,
                        'priority': priority,
                        'current_score': score,
                        'target_score': min(5.0, score + 1.0),
                        'current_issues': dimension_details[dim_key]['risks_identified'],
                        'improvements': [{
                            'title': f'{dim_name} 강화 프로그램' if self.is_korean() else f'{dim_name} Enhancement Program',
                            'description': f'{dim_name}을 개선하기 위한 체계적인 프로그램을 구축합니다.' if self.is_korean() else f'Build systematic program to improve {dim_name}.',
                            'implementation_steps': [
                                '1단계: 현황 분석 및 목표 설정' if self.is_korean() else 'Step 1: Analyze current state and set goals',
                                '2단계: 개선 방안 수립' if self.is_korean() else 'Step 2: Develop improvement plan',
                                '3단계: 실행 및 모니터링' if self.is_korean() else 'Step 3: Execute and monitor',
                                '4단계: 평가 및 개선' if self.is_korean() else 'Step 4: Evaluate and improve'
                            ],
                            'expected_impact': f'{dim_name} 30% 향상' if self.is_korean() else f'30% improvement in {dim_name}',
                            'success_metrics': ['개선 완료율', '만족도 점수'] if self.is_korean() else ['Completion rate', 'Satisfaction score'],
                            'timeline': '3-6개월' if self.is_korean() else '3-6 months',
                            'resources_needed': '전문가 2-3명' if self.is_korean() else '2-3 experts',
                            'guideline_reference': 'EU AI Act, UNESCO AI Ethics'
                        }]
                    })
            
            sample_data['improvement_suggestions'][svc] = improvements
        
        return sample_data
    
    def generate_detailed_report(self, services: List[str], data: Dict) -> str:
        """상세 보고서 생성"""
        if self.is_korean():
            report = f"""# AI 윤리성 리스크 진단 보고서

**생성일시**: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}  
**분석 대상**: {', '.join(services)}  
**평가 기준**: EU AI Act, UNESCO AI Ethics, OECD AI Principles

---

## 1. 개요

본 보고서는 {len(services)}개 AI 서비스의 윤리적 리스크를 평가한 결과입니다.

### 평가 대상 서비스
"""
        else:
            report = f"""# AI Ethics Risk Assessment Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Services Analyzed**: {', '.join(services)}  
**Evaluation Criteria**: EU AI Act, UNESCO AI Ethics, OECD AI Principles

---

## 1. Overview

This report presents the evaluation results of ethical risks for {len(services)} AI service(s).

### Services Evaluated
"""
        
        for svc in services:
            overall = data['risk_assessments'][svc]['overall_score']
            score_text = "점수" if self.is_korean() else "score"
            report += f"- **{svc}**: {self.t('overall_score')} {overall}/5{score_text}\n"
        
        report += "\n---\n\n"
        report += "## 2. " + ("서비스별 상세 분석" if self.is_korean() else "Detailed Analysis by Service") + "\n\n"
        
        for svc in services:
            assessment = data['risk_assessments'][svc]
            if self.is_korean():
                report += f"""### {svc}

#### 종합 평가
- **종합 점수**: {assessment['overall_score']}/5
- **리스크 수준**: {assessment['overall_risk_level']}

#### 차원별 평가
"""
            else:
                report += f"""### {svc}

#### Overall Assessment
- **Overall Score**: {assessment['overall_score']}/5
- **Risk Level**: {assessment['overall_risk_level']}

#### Dimension Evaluation
"""
            
            for dim_key in self.dimensions.keys():
                dim_name = self.get_dimension_name(dim_key)
                dim_data = assessment[dim_key]
                report += f"\n##### {dim_name}\n"
                report += f"- **{self.t('score')}**: {dim_data['score']}/5\n"
                report += f"- **{self.t('risk')}**: {dim_data['risk_level']}\n"
                report += f"- {dim_data['description']}\n\n"
            
            report += "\n---\n"
        
        if self.is_korean():
            report += f"""
## 3. 종합 권고사항

### 단기 조치 (1-3개월)
1. AI 윤리 정책 수립 및 공개
2. 투명성 보고서 발행

### 중기 조치 (3-6개월)
1. 편향성 테스트 프로그램 구축
2. AI 거버넌스 체계 구축

### 장기 조치 (6개월 이상)
1. 지속적인 모니터링 시스템 구축
2. 외부 감사 체계 확립

---

**보고서 생성**: AI 윤리성 리스크 진단 시스템  
**생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        else:
            report += f"""
## 3. Overall Recommendations

### Short-term Actions (1-3 months)
1. Establish and publish AI ethics policy
2. Issue transparency report

### Mid-term Actions (3-6 months)
1. Build bias testing program
2. Establish AI governance framework

### Long-term Actions (6+ months)
1. Build continuous monitoring system
2. Establish external audit framework

---

**Report Generated by**: AI Ethics Risk Assessment System  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report
    
    def generate_comparison_text(self, services: List[str]) -> str:
        """비교 분석 텍스트"""
        if len(services) < 2:
            return ""
        if self.is_korean():
            return f"분석 대상 {len(services)}개 서비스의 윤리 수준을 비교한 결과, 각 서비스마다 강점과 개선 영역이 다르게 나타났습니다."
        else:
            return f"Comparison of {len(services)} services shows different strengths and improvement areas for each service."
    
    def render_results_page(self):
        """결과 페이지"""
        results = st.session_state.results
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            self.t('tab_overview'), 
            self.t('tab_detailed'), 
            self.t('tab_improvement'), 
            self.t('tab_comparison'),
            self.t('tab_report')
        ])
        
        with tab1:
            self.render_overview_tab(results)
        with tab2:
            self.render_detailed_assessment_tab(results)
        with tab3:
            self.render_improvement_tab(results)
        with tab4:
            self.render_comparison_tab(results)
        with tab5:
            self.render_report_tab(results)
        
        # 하단 액션 버튼
        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button(self.t('new_analysis')):
                st.session_state.analysis_done = False
                st.session_state.results = None
                st.rerun()
        with col2:
            if st.button(self.t('save_results')):
                self.save_report(results)
        with col3:
            report_md = results.get('report', '')
            st.download_button(
                self.t('download_report'),
                report_md,
                file_name=f"ethics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    def render_overview_tab(self, results: Dict):
        """종합 대시보드"""
        st.header(f"📊 {self.t('tab_overview')}")
        
        data = results['detailed_data']
        services = results['services']
        
        # KPI 메트릭
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><h3>{self.t("analyzed_services")}</h3><h1>{len(services)}</h1></div>', 
                       unsafe_allow_html=True)
        
        with col2:
            avg_score = sum([svc['overall_score'] for svc in data['risk_assessments'].values()]) / len(services)
            color_class = "risk-low" if avg_score >= 4 else "risk-medium"
            st.markdown(f'<div class="metric-card {color_class}"><h3>{self.t("avg_score")}</h3><h1>{avg_score:.1f}/5</h1></div>', 
                       unsafe_allow_html=True)
        
        with col3:
            risk_level = self.t('low') if avg_score >= 4 else self.t('medium')
            color_class = "risk-low" if avg_score >= 4 else "risk-medium"
            st.markdown(f'<div class="metric-card {color_class}"><h3>{self.t("overall_risk")}</h3><h1>{risk_level}</h1></div>', 
                       unsafe_allow_html=True)
        
        with col4:
            improvement_count = sum([len(v) for v in data['improvement_suggestions'].values()])
            unit = "개" if self.is_korean() else ""
            st.markdown(f'<div class="metric-card"><h3>{self.t("improvements")}</h3><h1>{improvement_count}{unit}</h1></div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 레이더 차트와 바 차트
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"📡 {self.t('dimension_evaluation')}")
            fig = go.Figure()
            
            for service in services:
                scores = data['risk_assessments'][service]
                values = [scores[dim]['score'] for dim in self.dimensions.keys()]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=[self.get_dimension_name(dim) for dim in self.dimensions.keys()],
                    fill='toself',
                    name=service
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(f"📊 {self.t('score_comparison')}")
            
            df = pd.DataFrame([
                {self.t('service'): svc, self.t('overall_score'): data['risk_assessments'][svc]['overall_score']}
                for svc in services
            ])
            
            fig = px.bar(df, x=self.t('service'), y=self.t('overall_score'), 
                        color=self.t('overall_score'),
                        color_continuous_scale=['#f5576c', '#fcb69f', '#a8edea'],
                        range_color=[0, 5])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_detailed_assessment_tab(self, results: Dict):
        """상세 평가 탭"""
        st.header(f"📈 {self.t('detailed_evaluation')}")
        
        data = results['detailed_data']
        services = results['services']
        
        selected_service = st.selectbox(self.t('select_service'), services)
        
        if selected_service:
            assessment = data['risk_assessments'][selected_service]
            
            st.markdown(f"### {selected_service} {self.t('detailed_evaluation')}")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                score = assessment['overall_score']
                color = "🟢" if score >= 4 else "🟡" if score >= 3 else "🔴"
                st.markdown(f"## {color} {score}/5")
                st.markdown(f"**{self.t('risk')}**: {assessment['overall_risk_level']}")
            
            with col2:
                st.markdown(f"#### {self.t('overall_assessment')}")
                if score >= 4:
                    msg = f"{selected_service} {self.t('excellent')}"
                    st.success(msg)
                elif score >= 3:
                    msg = f"{selected_service} {self.t('good')}"
                    st.warning(msg)
                else:
                    msg = f"{selected_service} {self.t('needs_improvement')}"
                    st.error(msg)
            
            st.markdown("---")
            st.subheader(f"📋 {self.t('dimension_details')}")
            
            for dim_key in self.dimensions.keys():
                dim_name = self.get_dimension_name(dim_key)
                dim_data = assessment[dim_key]
                
                with st.expander(f"{'🟢' if dim_data['score'] >= 4 else '🟡' if dim_data['score'] >= 3 else '🔴'} {dim_name} - {dim_data['score']}/5", expanded=False):
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(self.t('score'), f"{dim_data['score']}/5")
                    with col2:
                        st.metric(self.t('risk'), dim_data['risk_level'])
                    with col3:
                        if isinstance(dim_data.get('guideline_compliance'), dict):
                            compliance_count = sum(
                                1 for c in dim_data['guideline_compliance'].values() 
                                if isinstance(c, dict) and ('준수' in c.get('status', '') or 'Compliant' in c.get('status', ''))
                            )
                            st.metric(self.t('guideline_compliance'), f"{compliance_count}/3")
                        else:
                            st.metric(self.t('guideline_compliance'), "N/A")
                    
                    st.markdown(f"#### 📝 {self.t('evaluation_desc')}")
                    st.markdown(f'<div class="detail-card">{dim_data["description"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"#### 📌 {self.t('key_evidence')}")
                    if isinstance(dim_data.get('evidence'), list):
                        for evidence in dim_data['evidence']:
                            st.markdown(f'<div class="evidence-item">✓ {evidence}</div>', unsafe_allow_html=True)
                    else:
                        st.info(self.t('no_evidence'))
                    
                    st.markdown(f"#### ⚖️ {self.t('guideline_compliance')}")
                    if isinstance(dim_data.get('guideline_compliance'), dict):
                        for guideline, compliance in dim_data['guideline_compliance'].items():
                            if isinstance(compliance, dict):
                                status = compliance.get('status', 'N/A')
                                if '준수' in status or 'Compliant' in status:
                                    status_emoji = "✅"
                                elif '부분' in status or 'Partial' in status:
                                    status_emoji = "⚠️"
                                else:
                                    status_emoji = "❌"
                                st.markdown(f"**{status_emoji} {guideline}**: {status}")
                            else:
                                st.markdown(f"**{guideline}**: {compliance}")
                    else:
                        st.info(self.t('no_evidence'))
                    
                    if dim_data.get('risks_identified'):
                        st.markdown(f"#### ⚠️ {self.t('identified_risks')}")
                        if isinstance(dim_data['risks_identified'], list):
                            for risk in dim_data['risks_identified']:
                                st.markdown(f'<div class="risk-item">⚠️ {risk}</div>', unsafe_allow_html=True)
                    
                    if dim_data.get('strengths'):
                        st.markdown(f"#### ✅ {self.t('strengths')}")
                        if isinstance(dim_data['strengths'], list):
                            for strength in dim_data['strengths']:
                                st.markdown(f'<div class="strength-item">✓ {strength}</div>', unsafe_allow_html=True)
    
    def render_improvement_tab(self, results: Dict):
        """개선 권고안 탭"""
        st.header(f"💡 {self.t('improvement_recommendations')}")
        
        data = results['detailed_data']
        services = results['services']
        
        selected_service = st.selectbox(self.t('select_service'), services, key="improvement_select")
        
        if selected_service:
            improvements = data['improvement_suggestions'][selected_service]
            
            st.markdown(f"### {selected_service} {self.t('improvement_recommendations')}")
            
            if not improvements:
                st.success(self.t('all_excellent'))
            else:
                priority_options = [self.t('all'), self.t('priority_high'), self.t('priority_medium'), self.t('priority_low')]
                priority_filter = st.radio(self.t('priority_filter'), priority_options, horizontal=True)
                
                filtered_improvements = improvements if priority_filter == self.t('all') else [
                    imp for imp in improvements if imp['priority'] == priority_filter
                ]
                
                for idx, imp in enumerate(filtered_improvements, 1):
                    if imp['priority'] == self.t('priority_high'):
                        priority_color = "🔴"
                    elif imp['priority'] == self.t('priority_medium'):
                        priority_color = "🟡"
                    else:
                        priority_color = "🟢"
                    
                    priority_label = "우선순위" if self.is_korean() else "Priority"
                    with st.expander(f"{priority_color} {imp['dimension']} ({priority_label}: {imp['priority']})", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(self.t('current_score'), f"{imp['current_score']}/5")
                        with col2:
                            st.metric(self.t('target_score'), f"{imp['target_score']}/5")
                        with col3:
                            improvement = imp['target_score'] - imp['current_score']
                            st.metric(self.t('improvement_goal'), f"+{improvement:.1f}")
                        
                        st.markdown(f"#### ⚠️ {self.t('current_issues')}")
                        for issue in imp['current_issues']:
                            st.markdown(f'<div class="risk-item">• {issue}</div>', unsafe_allow_html=True)
                        
                        st.markdown("---")
                        st.markdown(f"#### 🎯 {self.t('recommended_actions')}")
                        
                        for imp_idx, action in enumerate(imp['improvements'], 1):
                            st.markdown(f"##### {imp_idx}. {action['title']}")
                            st.write(action['description'])
                            
                            col1, col2 = st.columns([3, 2])
                            
                            with col1:
                                st.markdown(f"**📋 {self.t('implementation_steps')}**")
                                for step in action['implementation_steps']:
                                    st.markdown(f"- {step}")
                            
                            with col2:
                                st.markdown(f"**📊 {self.t('expected_impact')}**")
                                st.info(action['expected_impact'])
                                st.markdown(f"**⏱️ {self.t('timeline')}**")
                                st.code(action['timeline'])
    
    def render_comparison_tab(self, results: Dict):
        """비교 분석 탭"""
        st.header(f"🔍 {self.t('comparison_analysis')}")
        
        data = results['detailed_data']
        services = results['services']
        
        if len(services) < 2:
            st.info(self.t('comparison_note'))
            return
        
        if data.get('comparison_analysis'):
            st.markdown(data['comparison_analysis'])
        
        st.markdown("---")
        st.subheader(f"📊 {self.t('dimension_comparison')}")
        
        comparison_data = []
        for dim_key in self.dimensions.keys():
            dim_name = self.get_dimension_name(dim_key)
            row = {self.t('dimension'): dim_name}
            for svc in services:
                row[svc] = data['risk_assessments'][svc][dim_key]['score']
            comparison_data.append(row)
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # 스타일링된 테이블
        def color_score(val):
            if isinstance(val, (int, float)):
                if val >= 4:
                    return 'background-color: #c8e6c9; color: #1b5e20'
                elif val >= 3:
                    return 'background-color: #fff9c4; color: #f57f17'
                else:
                    return 'background-color: #ffcdd2; color: #b71c1c'
            return ''
        
        try:
            styled_df = df_comparison.style.map(color_score, subset=services)
        except AttributeError:
            styled_df = df_comparison.style.applymap(color_score, subset=services)
        
        st.dataframe(styled_df, use_container_width=True)
        
        # 히트맵
        st.markdown("---")
        st.subheader(f"🌡️ {self.t('score_heatmap')}")
        
        heatmap_data = []
        for svc in services:
            row = [data['risk_assessments'][svc][dim]['score'] for dim in self.dimensions.keys()]
            heatmap_data.append(row)
        
        score_label = "점수" if self.is_korean() else "Score"
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=[self.get_dimension_name(dim) for dim in self.dimensions.keys()],
            y=services,
            colorscale='RdYlGn',
            zmid=3,
            zmin=0,
            zmax=5,
            text=[[f"{val:.1f}" for val in row] for row in heatmap_data],
            texttemplate='%{text}',
            textfont={"size": 14},
            colorbar=dict(title=score_label)
        ))
        
        dim_label = "평가 차원" if self.is_korean() else "Dimensions"
        svc_label = "서비스" if self.is_korean() else "Services"
        fig.update_layout(
            height=300 + len(services) * 50,
            xaxis_title=dim_label,
            yaxis_title=svc_label
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_report_tab(self, results: Dict):
        """최종 보고서 탭"""
        st.header(f"📄 {self.t('final_report')}")
        
        report_md = results.get('report', '')
        st.markdown(report_md)
        
        st.markdown("---")
        st.subheader(f"💾 {self.t('report_download')}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                "📥 Markdown",
                report_md,
                file_name=f"ethics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        with col2:
            json_data = json.dumps(results['detailed_data'], ensure_ascii=False, indent=2)
            st.download_button(
                "📥 JSON",
                json_data,
                file_name=f"ethics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col3:
            services = results['services']
            data = results['detailed_data']
            
            csv_data = []
            for svc in services:
                row = {self.t('service'): svc}
                for dim_key in self.dimensions.keys():
                    dim_name = self.get_dimension_name(dim_key)
                    row[dim_name] = data['risk_assessments'][svc][dim_key]['score']
                row[self.t('overall_score')] = data['risk_assessments'][svc]['overall_score']
                csv_data.append(row)
            
            df_csv = pd.DataFrame(csv_data)
            csv_string = df_csv.to_csv(index=False, encoding='utf-8-sig')
            
            st.download_button(
                "📥 CSV",
                csv_string,
                file_name=f"ethics_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    def save_report(self, results: Dict):
        """보고서 저장"""
        try:
            save_dir = "saved_reports"
            os.makedirs(save_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            report_path = os.path.join(save_dir, f"report_{timestamp}.md")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(results['report'])
            
            data_path = os.path.join(save_dir, f"data_{timestamp}.json")
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            success_msg = f"✅ {self.t('report_saved')}!\n- {report_path}\n- {data_path}"
            st.success(success_msg)
            
        except Exception as e:
            error_msg = f"❌ 저장 중 오류: {e}" if self.is_korean() else f"❌ Error saving: {e}"
            st.error(error_msg)
    
    def load_previous_report(self):
        """이전 보고서 불러오기"""
        save_dir = "saved_reports"
        
        if not os.path.exists(save_dir):
            st.warning(self.t('no_saved_reports'))
            return
        
        json_files = [f for f in os.listdir(save_dir) if f.endswith('.json')]
        
        if not json_files:
            st.warning(self.t('no_saved_reports'))
            return
        
        json_files.sort(reverse=True)
        
        selected_file = st.selectbox(self.t('select_report'), json_files)
        
        if st.button(self.t('load')):
            try:
                file_path = os.path.join(save_dir, selected_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_results = json.load(f)
                
                st.session_state.results = loaded_results
                st.session_state.analysis_done = True
                st.success(f"✅ {self.t('report_loaded')}!")
                st.rerun()
                
            except Exception as e:
                error_msg = f"❌ 불러오기 실패: {e}" if self.is_korean() else f"❌ Load failed: {e}"
                st.error(error_msg)


# 메인 실행
if __name__ == "__main__":
    dashboard = EthicsDashboard()
    dashboard.run()
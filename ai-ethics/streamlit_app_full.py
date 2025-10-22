# ============================================
# streamlit_app_full_v3.py - 실제 분석 연동 버전
# ============================================
import streamlit as st
from datetime import datetime
from typing import List
from agents.aiengine import AIEthicsAssessmentSystem  # 실제 분석 시스템
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="AI 윤리성 리스크 진단",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .main-header { font-size: 3rem; font-weight: bold; color: #1f77b4; text-align: center; margin-bottom: 2rem; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: bold; }
    .improvement-card { border: 2px solid #28a745; padding: 15px; margin: 10px 0; border-radius: 8px; background: #f0fff4; }
    .log-container { background: #f8f9fa; padding: 10px; border-radius: 5px; height: 250px; overflow-y: scroll; font-family: monospace; }
</style>
""", unsafe_allow_html=True)


class EthicsDashboard:
    def __init__(self):
        if 'analysis_done' not in st.session_state:
            st.session_state.analysis_done = False
        if 'results' not in st.session_state:
            st.session_state.results = None

    def run(self):
        st.markdown('<div class="main-header">⚖️ AI 윤리성 리스크 진단 시스템</div>', unsafe_allow_html=True)

        with st.sidebar:
            self.render_sidebar()

        if not st.session_state.analysis_done:
            self.render_welcome_page()
        else:
            self.render_results_page()

    def render_sidebar(self):
        st.markdown("### 📋 분석 서비스")
        services = st.multiselect(
            "분석할 AI 서비스를 선택하세요 (최대 3개)",
            ["ChatGPT", "Claude", "Google Gemini", "Copilot", "Midjourney", "DALL-E"],
            max_selections=3
        )
        st.markdown("### ⚙️ 평가 가이드라인")
        guidelines = st.multiselect(
            "가이드라인 선택",
            ["EU AI Act", "UNESCO AI Ethics", "OECD AI Principles"],
            default=["EU AI Act", "UNESCO AI Ethics", "OECD AI Principles"]
        )

        if st.button("🚀 분석 시작", disabled=len(services)==0):
            self.start_analysis(services, guidelines)

    def render_welcome_page(self):
        st.markdown("## 환영합니다! 👋")
        st.markdown("왼쪽에서 분석할 서비스를 선택하고 시작하세요!")

    def start_analysis(self, services: List[str], guidelines: List[str]):
        st.session_state.results = None
        st.session_state.analysis_done = False

        log_container = st.empty()

        # Streamlit 실시간 로그 출력
        class StreamlitLogger:
            def __init__(self):
                self.text = ""
            def write(self, msg):
                if msg.strip():
                    self.text += msg + "\n"
                    log_container.markdown(f"<div class='log-container'>{self.text}</div>", unsafe_allow_html=True)

        import builtins
        builtins.print = StreamlitLogger().write

        try:
            st.info("🔄 실제 분석 진행 중...")
            system = AIEthicsAssessmentSystem()
            final_report = system.analyze_services(services)

            # 결과 세션 저장
            st.session_state.results = {
                'services': services,
                'guidelines': guidelines,
                'report': final_report,
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.analysis_done = True
            st.success("✅ 분석 완료!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ 분석 중 오류 발생: {e}")

    def render_results_page(self):
        results = st.session_state.results
        if not results:
            st.warning("결과가 없습니다.")
            return

        tab1, tab2 = st.tabs(["📊 대시보드", "📄 보고서"])

        with tab1:
            self.render_dashboard(results)
        with tab2:
            self.render_report(results)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 새로운 분석"):
                st.session_state.analysis_done = False
                st.rerun()

    def render_dashboard(self, results):
        st.header("📊 종합 대시보드")
        services = results['services']

        col1, col2 = st.columns(2)
        with col1:
            st.metric("분석 서비스", len(services))
        with col2:
            st.metric("분석 완료 시간", results['timestamp'].split("T")[1][:8])

        # 레이더 차트: 실제 분석 결과 연동 가능
        st.subheader("서비스별 레이더 차트")
        dimensions = ['fairness','privacy','transparency','accountability','safety']
        # 여기서는 샘플 데이터 표시 (실제 시스템에서 dimension별 점수 가져와서 연결)
        for svc in services:
            sample_scores = [3.5, 3.2, 4.0, 3.8, 3.6]
            fig = go.Figure(go.Scatterpolar(
                r=sample_scores,
                theta=dimensions,
                fill='toself',
                name=svc
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])), showlegend=True, height=350)
            st.plotly_chart(fig, use_container_width=True)

    def render_report(self, results):
        st.header("📄 최종 보고서")
        report_md = results.get('report', '')
        st.download_button("📥 보고서 다운로드 (Markdown)", report_md,
                           file_name=f"ethics_report_{datetime.now().strftime('%Y%m%d')}.md",
                           mime="text/markdown")
        st.markdown(report_md)


if __name__ == "__main__":
    dashboard = EthicsDashboard()
    dashboard.run()

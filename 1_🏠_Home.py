import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import (
    render_navbar, 
    render_footer, 
    render_page_header, 
    render_logout_button,
    render_expandable_footer
)
from utils.data_loader import load_data

st.set_page_config(
    page_title="Home - Global Inequality Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)

# Fixed navbar
render_navbar(current_page="Home", username=st.session_state.get('username', 'User'))

# Logout in sidebar
render_logout_button()

# Page header - no emoji
render_page_header(
    title="Welcome to Our Dashboard",
    subtitle="Explore global inequality data with powerful analytics and AI insights"
)

# Load data
df = load_data()

if df is not None:
    # Key metrics
    st.markdown("## Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center;'>
            <div style='font-size: 36px; font-weight: 700; background: linear-gradient(90deg, #00f5ff, #a162e8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                """ + str(len(df['country_name'].unique())) + """
            </div>
            <div style='color: #b4b8d4; font-size: 14px; margin-top: 8px;'>Countries Tracked</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center;'>
            <div style='font-size: 36px; font-weight: 700; background: linear-gradient(90deg, #00f5ff, #a162e8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                {df['gini_index'].mean():.1f}
            </div>
            <div style='color: #b4b8d4; font-size: 14px; margin-top: 8px;'>Average Gini Index</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center;'>
            <div style='font-size: 36px; font-weight: 700; background: linear-gradient(90deg, #00f5ff, #a162e8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                {int(df['year'].max())}
            </div>
            <div style='color: #b4b8d4; font-size: 14px; margin-top: 8px;'>Latest Year</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center;'>
            <div style='font-size: 36px; font-weight: 700; background: linear-gradient(90deg, #00f5ff, #a162e8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                {len(df):,}
            </div>
            <div style='color: #b4b8d4; font-size: 14px; margin-top: 8px;'>Total Records</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Quick Actions")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("View Dashboard", use_container_width=True, type="primary", key="qa1"):
            st.switch_page("pages/2_📊_Dashboard.py")
    
    with col2:
        if st.button("Compare Countries", use_container_width=True, key="qa2"):
            st.switch_page("pages/3_🔍_Country_Compare.py")
    
    with col3:
        if st.button("Trend Analysis", use_container_width=True, key="qa3"):
            st.switch_page("pages/4_📈_Trends.py")
    
    with col4:
        if st.button("AI Insights", use_container_width=True, key="qa4"):
            st.switch_page("pages/8_🤖_AI_Insights.py")
    
    with col5:
        if st.button("Generate Reports", use_container_width=True, key="qa5"):
            st.switch_page("pages/7_📧_Email_Reports.py")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## Platform Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(0, 245, 255, 0.1); border: 1px solid rgba(0, 245, 255, 0.3); border-radius: 12px; padding: 25px;'>
            <h3 style='color: #00f5ff; margin-top: 0;'>Latest Features</h3>
            <ul style='color: #b4b8d4; line-height: 1.8;'>
                <li>AI-powered country analysis</li>
                <li>Interactive trend forecasting</li>
                <li>Automated PDF report generation</li>
                <li>Enhanced global visualization</li>
                <li>Real-time data updates</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    

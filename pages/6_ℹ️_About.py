import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
render_navbar(current_page="About", username=st.session_state.get('username', 'User'))
render_logout_button()
st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



render_page_header(
    title="About Us",
    subtitle="Learn more about our mission and platform",
    icon="ℹ️"
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🌍 Our Mission
    
    The Global Inequality Platform is dedicated to making income inequality data accessible, understandable, and actionable for researchers, policymakers, and citizens worldwide.
    
    ### 📊 What We Do
    
    We provide comprehensive visualizations, AI-powered insights, and analytical tools to help you understand global income inequality patterns.
    
    ### 🎯 Our Values
    
    - **Transparency:** Open, accessible data for all
    - **Innovation:** Leveraging AI and modern technology
    - **Impact:** Supporting evidence-based policy decisions
    - **Accessibility:** Making complex data simple
    """)

with col2:
    st.info("""
    ### 📊 Platform Stats
    
    **195+** Countries  
    **50+** Years of Data  
    **10K+** Records  
    
    **Data Source:**  
    World Income Inequality Database (UNU-WIDER)
    """)
    
    st.success("""
    ### 📧 Contact
    
    **Email:** support@inequality-platform.com  
    **Phone:** +1 (555) 123-4567  
    **Address:** 123 Data Street, Analytics City
    """)

st.markdown("---")
st.markdown("### 👥 Our Team")

col1, col2, col3, col4 = st.columns(4)

team = [
    ("👨‍💻", "Dr. Alex Chen", "Data Scientist"),
    ("👩‍🎨", "Sarah Johnson", "UX Designer"),
    ("👨‍🔬", "Michael Rodriguez", "Research Lead"),
    ("👩‍💼", "Emily Watson", "Product Manager")
]

for col, (avatar, name, role) in zip([col1, col2, col3, col4], team):
    with col:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 48px; margin-bottom: 10px;">{avatar}</div>
            <h4 style="color: #00f5ff; margin-bottom: 5px;">{name}</h4>
            <p style="color: #b4b8d4; font-size: 14px;">{role}</p>
        </div>
        """, unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

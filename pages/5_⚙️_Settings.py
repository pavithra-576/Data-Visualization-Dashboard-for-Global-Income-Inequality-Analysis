import streamlit as st
from utils.auth import check_authentication, logout
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
render_navbar(current_page="Settings", username=st.session_state.get('username', 'User'))
render_logout_button()
st.set_page_config(
    page_title="Settings",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



render_page_header(
    title="User Settings",
    subtitle="Customize your experience and preferences",
)

tab1, tab2, tab3 = st.tabs([" Profile", " Preferences", " Security"])

with tab1:
    st.markdown("###  Profile Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Username", value=st.session_state.get('username', ''), disabled=True)
        st.text_input("Email", value="user@example.com", disabled=True)
    
    with col2:
        st.text_input("Member Since", value="2024", disabled=True)
        st.text_input("Account Type", value="Standard", disabled=True)

with tab2:
    st.markdown("###  Display Preferences")
    
    theme = st.selectbox("Theme", ["Dark (Default)", "Light", "Auto"])
    language = st.selectbox("Language", ["English", "Spanish", "French"])
    default_view = st.selectbox("Default Page", ["Home", "Dashboard", "Trends"])

    if st.button(" Save Preferences", type="primary"):
        st.success(" Preferences saved!")

with tab3:
    st.markdown("###  Change Password")
    
    with st.form("password_form"):
        current_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Update Password"):
            if new_pw == confirm_pw and len(new_pw) >= 6:
                st.success(" Password updated!")
            else:
                st.error(" Passwords don't match or too short")
st.markdown("<br><br>", unsafe_allow_html=True)
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

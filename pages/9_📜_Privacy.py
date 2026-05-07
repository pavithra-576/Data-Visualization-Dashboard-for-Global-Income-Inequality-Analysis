import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button
render_navbar(current_page="Privacy", username=st.session_state.get('username', 'User'))
render_logout_button()
st.set_page_config(
    page_title="Privacy Policy",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



render_page_header(
    title="Privacy Policy",
    subtitle="How we protect and use your data",
)

st.markdown("""
##  Privacy Policy

**Last Updated:** January 2025

### 1. Information We Collect

We collect information you provide directly to us when you:
- Create an account
- Use our services
- Contact us for support

### 2. How We Use Your Information

We use the information we collect to:
- Provide and maintain our services
- Improve user experience
- Communicate with you about updates
- Ensure platform security

### 3. Data Security

We implement industry-standard security measures to protect your personal information, including:
- Encrypted data storage
- Secure authentication
- Regular security audits
- Access controls

### 4. Your Rights

You have the right to:
-  Access your personal data
-  Request data deletion
-  Opt-out of communications
-  Export your data
-  Update your information

### 5. Data Sharing

We **never** sell your personal information. We only share data when:
- Required by law
- With your explicit consent
- To protect our rights and safety

### 6. Cookies and Tracking

We use cookies to:
- Remember your preferences
- Analyze site usage
- Improve functionality

You can control cookies through your browser settings.

### 7. Third-Party Services

Our platform integrates with:
- **Google Gemini AI** - For AI-powered insights
- **Power BI** - For data visualization
- **Analytics services** - For usage statistics

Each has their own privacy policy.

### 8. Children's Privacy

Our service is not intended for users under 13 years of age.

### 9. Changes to This Policy

We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page.

### 10. Contact Us

For privacy concerns or questions:

 **Email:** privacy@inequality-platform.com  
 **Phone:** +1 (555) 123-4567  
 **Address:** 123 Data Street, Analytics City, ST 12345

---

*This is a demo privacy policy for demonstration purposes.*
""")
st.markdown("<br><br>", unsafe_allow_html=True)
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

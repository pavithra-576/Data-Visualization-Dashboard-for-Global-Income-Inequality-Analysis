import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
from utils.data_loader import load_data
import re
# Fixed navbar with current page highlighted
render_navbar(current_page="Reports", username=st.session_state.get('username', 'User'))

# Fixed logout button
render_logout_button()
st.set_page_config(
    page_title="Email Reports",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



# Page header
render_page_header(
    title="Email Report Generator",
    subtitle="Generate custom reports and send them directly to your inbox",
)

# Load data
df = load_data()

if df is not None:
    # Create tabs
    tab1, tab2 = st.tabs([" Create Report", " Report History"])
    
    with tab1:
        st.markdown("###  Configure Your Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("####  Select Countries")
            countries = st.multiselect(
                "Choose countries to include",
                options=sorted(df['country_name'].unique()),
                default=['United States', 'China'],
                max_selections=10,
                help="Select up to 10 countries for analysis"
            )
            
            st.markdown("####  Time Period")
            year_min = int(df['year'].min())
            year_max = int(df['year'].max())
            year_range = st.slider(
                "Select year range",
                year_min, year_max,
                (2000, year_max)
            )
        
        with col2:
            st.markdown("####  Email Settings")
            recipient_email = st.text_input(
                "Recipient Email",
                placeholder="your.email@example.com",
                help="Email address where the report will be sent"
            )
            
            st.markdown("####  Report Type")
            report_type = st.selectbox(
                "Choose report format",
                ["Standard Report", "Executive Summary", "Detailed Analysis", "Data Export"]
            )
            
            st.markdown("####  Include Options")
            include_charts = st.checkbox("Include visualizations", value=True)
            include_stats = st.checkbox("Include statistics", value=True)
            include_recommendations = st.checkbox("Include policy recommendations", value=True)
        
        # Preview section
        if countries:
            st.markdown("---")
            st.markdown("###  Report Preview")
        
            filtered_df = df[
                (df['country_name'].isin(countries)) &
                (df['year'].between(year_range[0], year_range[1]))
            ]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Countries", len(countries))
            with col2:
                st.metric("Data Points", len(filtered_df))
            with col3:
                st.metric("Avg Gini", f"{filtered_df['gini_index'].mean():.2f}")
            with col4:
                st.metric("Year Span", f"{year_range[1] - year_range[0]} years")
            
            # Sample data
            st.markdown("####  Sample Data")
            st.dataframe(
                filtered_df.head(10)[['country_name', 'year', 'gini_index']],
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            generate_pdf = st.button(" Generate PDF", use_container_width=True, type="primary")
        
        with col2:
            send_email = st.button(" Generate & Email", use_container_width=True, type="primary")
        
        with col3:
            if st.button(" Reset", use_container_width=True):
                st.rerun()
        
        # Handle actions
        if generate_pdf and countries:
            st.success(f" PDF report would be generated for: {', '.join(countries)}")
            st.info(" Report includes: " + 
                   f"{'Charts, ' if include_charts else ''}" +
                   f"{'Statistics, ' if include_stats else ''}" +
                   f"{'Recommendations' if include_recommendations else ''}")
            st.balloons()
        
        if send_email:
            if not countries:
                st.warning(" Please select at least one country")
            elif not recipient_email:
                st.warning(" Please enter recipient email address")
            elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', recipient_email):
                st.error("Please enter a valid email address")
            else:
                st.success(f" Report generated for: {', '.join(countries)}")
                st.info(f" Report would be sent to: {recipient_email}")
                st.info(f" Report Type: {report_type}")
                st.balloons()
    
    with tab2:
        st.markdown("###  Recent Reports")
        
        st.info(" No reports generated yet. Create your first report in the 'Create Report' tab!")
        
        # Demo report history
        st.markdown("####  Demo Reports")
        
        demo_reports = [
            {"name": "Global Inequality Report 2023", "date": "2024-01-15", "countries": 5, "pages": 12},
            {"name": "US-China Comparison", "date": "2024-01-10", "countries": 2, "pages": 8},
            {"name": "European Trends Analysis", "date": "2024-01-05", "countries": 10, "pages": 15},
        ]
        
        for report in demo_reports:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"** {report['name']}**")
            with col2:
                st.caption(f" {report['date']}")
            with col3:
                st.caption(f" {report['countries']} countries")
            with col4:
                st.button(" Download", key=f"dl_{report['name']}", disabled=True, use_container_width=True)
            
            st.markdown("---")

else:
    st.error(" Unable to load data. Please check the file path in config.py")
st.markdown("<br><br>", unsafe_allow_html=True)
# Fixed footer
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

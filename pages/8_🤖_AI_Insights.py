import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
from utils.data_loader import load_data
# Fixed navbar with current page highlighted
render_navbar(current_page="AI", username=st.session_state.get('username', 'User'))

# Fixed logout button
render_logout_button()
# Try to import AI service
try:
    from utils.ai_service_gemini import AIInsightEngine
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

st.set_page_config(
    page_title="AI Insights",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



# Page header
render_page_header(
    title="AI-Powered Insights",
    subtitle="Unlock intelligent analysis and predictions with advanced AI",
)

# Load data
df = load_data()

if df is not None:
    if AI_AVAILABLE:
        # Initialize AI engine
        ai_engine = AIInsightEngine()
        
        # Create tabs for different AI features
        tab1, tab2, tab3, tab4 = st.tabs([
            " Country Analysis", 
            " Compare Countries", 
            " Trend Prediction",
            " AI Chat"
        ])
        
        with tab1:
            st.markdown("###  Deep Dive Country Analysis")
            st.markdown("Get AI-powered insights about any country's inequality patterns")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_country = st.selectbox(
                    "Select a country to analyze",
                    options=sorted(df['country_name'].unique()),
                    index=0
                )
            
            with col2:
                analyze_btn = st.button(" Generate AI Analysis", use_container_width=True, type="primary")
            
            if analyze_btn and selected_country:
                with st.spinner(" AI is analyzing the data..."):
                    # Get country data
                    country_data = df[df['country_name'] == selected_country].sort_values('year')
                    
                    # Display quick stats
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Latest Gini", f"{country_data['gini_index'].iloc[-1]:.2f}")
                    with col2:
                        st.metric("Average", f"{country_data['gini_index'].mean():.2f}")
                    with col3:
                        trend_emoji = "📈" if country_data['gini_index'].iloc[-1] > country_data['gini_index'].iloc[0] else "📉"
                        st.metric("Trend", trend_emoji)
                    with col4:
                        st.metric("Data Points", len(country_data))
                    
                    # Get AI insights
                    insights = ai_engine.analyze_country(df, selected_country)
                    
                    st.markdown("###  AI Analysis")
                    st.markdown(insights)
                    
                    # Visual trends
                    st.markdown("###  Visual Trends")
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=country_data['year'],
                        y=country_data['gini_index'],
                        mode='lines+markers',
                        name='Gini Index',
                        line=dict(color='#00f5ff', width=3),
                        marker=dict(size=8)
                    ))
                    
                    fig.update_layout(
                        title=f'Gini Index Trend for {selected_country}',
                        xaxis_title='Year',
                        yaxis_title='Gini Index',
                        template='plotly_dark',
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(26, 31, 58, 0.5)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("###  vs  AI-Powered Country Comparison")
            st.markdown("Compare multiple countries with intelligent analysis")
            
            comparison_countries = st.multiselect(
                "Select countries to compare (2-5 recommended)",
                options=sorted(df['country_name'].unique()),
                default=['United States', 'China'],
                max_selections=5
            )
            
            if st.button(" Generate Comparison Analysis", use_container_width=True, type="primary"):
                if len(comparison_countries) >= 2:
                    with st.spinner(" AI is comparing countries..."):
                        insights = ai_engine.compare_countries(df, comparison_countries)
                        
                        st.markdown("###  AI Comparative Analysis")
                        st.markdown(insights)
                else:
                    st.warning(" Please select at least 2 countries for comparison")
        
        with tab3:
            st.markdown("###  AI Trend Prediction & Forecasting")
            st.markdown("Predict future inequality trends using AI analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                prediction_country = st.selectbox(
                    "Select country for prediction",
                    options=sorted(df['country_name'].unique()),
                    key='prediction_country'
                )
            
            with col2:
                years_ahead = st.slider("Years to forecast", 1, 10, 5)
            
            if st.button(" Generate Predictions", use_container_width=True, type="primary"):
                with st.spinner(" AI is analyzing trends and making predictions..."):
                    prediction = ai_engine.predict_trends(df, prediction_country, years_ahead)
                    
                    st.markdown("###  AI Prediction Analysis")
                    st.markdown(prediction)
                    
                    st.info(" **Note:** These predictions are based on historical trends and AI analysis. Actual outcomes may vary.")
        
        with tab4:
            st.markdown("###  Chat with AI Assistant")
            st.markdown("Ask questions about the data and get intelligent responses")
            
            # Initialize chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="background: rgba(0, 245, 255, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 3px solid #00f5ff;">
                        <strong> You:</strong><br>{message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(161, 98, 232, 0.1); padding: 15px; border-radius: 12px; margin: 10px 0; border-left: 3px solid #a162e8;">
                        <strong> AI:</strong><br>{message['content']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Chat input
            user_question = st.text_input(
                "Ask anything about global inequality...",
                placeholder="e.g., Which region has the highest inequality?",
                key='chat_input'
            )
            
            col1, col2 = st.columns([1, 5])
            with col1:
                send_btn = st.button(" Send", use_container_width=True)
            with col2:
                if st.button(" Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            
            if send_btn and user_question:
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_question
                })
                
                # Get AI response
                with st.spinner(" Thinking..."):
                    response = ai_engine.answer_question(df, user_question)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                
                st.rerun()
            
            # Suggested questions
            if len(st.session_state.chat_history) == 0:
                st.markdown("###  Suggested Questions")
                
                suggestions = [
                    "What is the global trend in income inequality?",
                    "Which countries have reduced inequality the most?",
                    "What factors contribute to income inequality?",
                    "How does inequality affect economic growth?"
                ]
                
                cols = st.columns(2)
                for idx, suggestion in enumerate(suggestions):
                    with cols[idx % 2]:
                        if st.button(f" {suggestion}", key=f"suggest_{idx}", use_container_width=True):
                            st.session_state.chat_history.append({
                                'role': 'user',
                                'content': suggestion
                            })
                            response = ai_engine.answer_question(df, suggestion)
                            st.session_state.chat_history.append({
                                'role': 'assistant',
                                'content': response
                            })
                            st.rerun()
    
    else:
        # AI not available - show alternative
        st.warning("AI features require Google Gemini API key")
        
        st.markdown("""
        ### 🔧 How to Enable AI Features
        
        1. Get a **free** Gemini API key from: https://aistudio.google.com/app/apikey
        2. Add it to your `.env` file:
        ```
        GEMINI_API_KEY=your-api-key-here
        ```
        3. Restart the application
        
        ### 📊 Alternative Features
        
        While AI is being set up, you can:
        -  Explore the **Dashboard** for visualizations
        -  Use **Country Compare** for side-by-side analysis
        -  Check **Trends** for historical patterns
        -  Generate **Reports** (PDF export)
        """)
        
        if st.button(" Go to Dashboard", use_container_width=True, type="primary"):
            st.switch_page("pages/2_📊_Dashboard.py")

else:
    st.error(" Unable to load data. Please check the file path in config.py")
st.markdown("<br><br>", unsafe_allow_html=True)
# Fixed footer
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

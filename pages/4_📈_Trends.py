import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
from utils.data_loader import load_data
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
# Fixed navbar with current page highlighted
render_navbar(current_page="Trends", username=st.session_state.get('username', 'User'))

# Fixed logout button
render_logout_button()
st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



# Page header
render_page_header(
    title="Global Inequality Trends",
    subtitle="Analyze historical patterns and predict future trends",
)

# Load data
df = load_data()

if df is not None:
    # Analysis type selection
    analysis_type = st.radio(
        " Select Analysis Type:",
        ["Global Trends", "Regional Analysis", "Decade Comparison", "Country Forecasting"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if analysis_type == "Global Trends":
        st.markdown("###  Global Inequality Trends Over Time")
        
        # Calculate yearly averages
        yearly_avg = df.groupby('year')['gini_index'].agg(['mean', 'median', 'std']).reset_index()
        
        # Create multi-line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=yearly_avg['year'],
            y=yearly_avg['mean'],
            mode='lines+markers',
            name='Global Average',
            line=dict(color='#00f5ff', width=3),
            marker=dict(size=8),
            hovertemplate='Year: %{x}<br>Average: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=yearly_avg['year'],
            y=yearly_avg['median'],
            mode='lines+markers',
            name='Global Median',
            line=dict(color='#a162e8', width=3),
            marker=dict(size=8),
            hovertemplate='Year: %{x}<br>Median: %{y:.2f}<extra></extra>'
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=yearly_avg['year'].tolist() + yearly_avg['year'].tolist()[::-1],
            y=(yearly_avg['mean'] + yearly_avg['std']).tolist() + 
              (yearly_avg['mean'] - yearly_avg['std']).tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0, 245, 255, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='±1 Std Dev',
            showlegend=True
        ))
        
        fig.update_layout(
            title='Global Gini Index Trends with Standard Deviation',
            xaxis_title='Year',
            yaxis_title='Gini Index',
            template='plotly_dark',
            height=500,
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26, 31, 58, 0.5)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trend = "increasing" if yearly_avg['mean'].iloc[-1] > yearly_avg['mean'].iloc[0] else "decreasing"
            change = abs(yearly_avg['mean'].iloc[-1] - yearly_avg['mean'].iloc[0])
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; text-align: center;">
                <h4 style="color: #00f5ff;">Overall Trend</h4>
                <p style="font-size: 24px; font-weight: 700; color: {'#ff6b9d' if trend == 'increasing' else '#00ff88'};">
                {trend.upper()}
                </p>
                <p style="color: #b4b8d4;">Change: {change:.2f} points</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            highest_year = yearly_avg.loc[yearly_avg['mean'].idxmax(), 'year']
            highest_val = yearly_avg['mean'].max()
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; text-align: center;">
                <h4 style="color: #00f5ff;">Peak Year</h4>
                <p style="font-size: 24px; font-weight: 700; color: #ff6b9d;">
                {int(highest_year)}
                </p>
                <p style="color: #b4b8d4;">Gini: {highest_val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            lowest_year = yearly_avg.loc[yearly_avg['mean'].idxmin(), 'year']
            lowest_val = yearly_avg['mean'].min()
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; text-align: center;">
                <h4 style="color: #00f5ff;">Lowest Year</h4>
                <p style="font-size: 24px; font-weight: 700; color: #00ff88;">
                {int(lowest_year)}
                </p>
                <p style="color: #b4b8d4;">Gini: {lowest_val:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif analysis_type == "Regional Analysis":
        st.markdown("###  Regional Inequality Patterns")
        
        st.info(" Regional grouping based on major economic regions")
        
        # Simple region mapping
        region_map = {
            'United States': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
            'Brazil': 'South America', 'Argentina': 'South America', 'Chile': 'South America',
            'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia',
            'Germany': 'Europe', 'France': 'Europe', 'United Kingdom': 'Europe', 'Italy': 'Europe',
            'South Africa': 'Africa', 'Nigeria': 'Africa', 'Egypt': 'Africa'
        }
        
        df['region'] = df['country_name'].map(region_map).fillna('Other')
        
        # Regional average
        regional_avg = df.groupby('region')['gini_index'].mean().sort_values(ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=regional_avg.index,
                y=regional_avg.values,
                marker_color=['#00f5ff', '#a162e8', '#f093fb', '#4facfe', '#ff6b9d'],
                text=regional_avg.values.round(2),
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title='Average Gini Index by Region',
            xaxis_title='Region',
            yaxis_title='Average Gini Index',
            template='plotly_dark',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26, 31, 58, 0.5)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Regional statistics table
        st.markdown("####  Regional Statistics")
        regional_stats = df.groupby('region')['gini_index'].agg([
            ('Average', 'mean'),
            ('Median', 'median'),
            ('Min', 'min'),
            ('Max', 'max'),
            ('Countries', 'count')
        ]).round(2).sort_values('Average', ascending=False)
        
        st.dataframe(regional_stats, use_container_width=True)
    
    elif analysis_type == "Decade Comparison":
        st.markdown("###  Decade-by-Decade Comparison")
        
        # Create decade column
        df['decade'] = (df['year'] // 10) * 10
        
        # Box plot by decade
        fig = px.box(
            df,
            x='decade',
            y='gini_index',
            color='decade',
            title='Gini Index Distribution by Decade',
            labels={'decade': 'Decade', 'gini_index': 'Gini Index'}
        )
        
        fig.update_layout(
            template='plotly_dark',
            height=500,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26, 31, 58, 0.5)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Decade statistics
        st.markdown("####  Decade Statistics")
        decade_stats = df.groupby('decade')['gini_index'].agg([
            ('Average', 'mean'),
            ('Median', 'median'),
            ('Std Dev', 'std'),
            ('Data Points', 'count')
        ]).round(2)
        
        st.dataframe(decade_stats, use_container_width=True)
    
    else:  # Country Forecasting
        st.markdown("###  Simple Trend Forecasting")
        
        st.info(" Linear projection based on historical trends")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            country = st.selectbox(
                "Select a country to forecast:",
                sorted(df['country_name'].unique())
            )
        
        with col2:
            years_ahead = st.slider("Years to forecast", 1, 10, 5)
        
        country_data = df[df['country_name'] == country].sort_values('year')
        
        if len(country_data) > 5:
            years = country_data['year'].values
            gini = country_data['gini_index'].values
            
            # Simple linear regression
            z = np.polyfit(years, gini, 1)
            p = np.poly1d(z)
            
            # Forecast
            future_years = np.arange(years.max() + 1, years.max() + years_ahead + 1)
            forecast = p(future_years)
            
            # Create plot
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=years,
                y=gini,
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='#00f5ff', width=3),
                marker=dict(size=8)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=future_years,
                y=forecast,
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#a162e8', width=3, dash='dash'),
                marker=dict(size=8, symbol='diamond')
            ))
            
            # Trend line
            trend_line = p(years)
            fig.add_trace(go.Scatter(
                x=years,
                y=trend_line,
                mode='lines',
                name='Trend Line',
                line=dict(color='#ff6b9d', width=2, dash='dot'),
                opacity=0.7
            ))
            
            fig.update_layout(
                title=f'Gini Index Forecast for {country}',
                xaxis_title='Year',
                yaxis_title='Gini Index',
                template='plotly_dark',
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26, 31, 58, 0.5)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast table
            st.markdown("####  Forecast Details")
            forecast_df = pd.DataFrame({
                'Year': future_years.astype(int),
                'Predicted Gini': forecast.round(2),
                'Confidence': ['Medium'] * len(future_years)
            })
            
            st.dataframe(forecast_df, use_container_width=True, hide_index=True)
            
            st.warning(" **Note:** This is a simple linear projection. Actual values may vary due to policy changes and economic factors.")
        
        else:
            st.warning(" Not enough historical data for this country. At least 5 data points required.")

else:
    st.error(" Unable to load data. Please check the file path in config.py")
st.markdown("<br><br>", unsafe_allow_html=True)
# Fixed footer
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
from utils.data_loader import load_data
import plotly.graph_objects as go
import plotly.express as px
render_navbar(current_page="Compare", username=st.session_state.get('username', 'User'))
render_logout_button()
st.set_page_config(
    page_title="Country Comparison",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



render_page_header(
    title="Country Comparison Tool",
    subtitle="Compare income inequality metrics across multiple countries",
)

df = load_data()

if df is not None:
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        countries = st.multiselect(
            " Select Countries (max 6)",
            options=sorted(df['country_name'].unique()),
            default=['United States', 'China'],
            max_selections=6
        )
    
    with col2:
        year_min = int(df['year'].min())
        year_max = int(df['year'].max())
        year_range = st.slider(" Year Range", year_min, year_max, (2000, year_max))
    
    with col3:
        chart_type = st.selectbox(" View", ["Line", "Box", "Bar"])
    
    if countries:
        filtered_df = df[
            (df['country_name'].isin(countries)) &
            (df['year'].between(year_range[0], year_range[1]))
        ]
        
        if len(filtered_df) > 0:
            st.markdown("###  Comparative Analysis")
            
            if chart_type == "Line":
                fig = go.Figure()
                for country in countries:
                    country_data = filtered_df[filtered_df['country_name'] == country].sort_values('year')
                    fig.add_trace(go.Scatter(
                        x=country_data['year'],
                        y=country_data['gini_index'],
                        mode='lines+markers',
                        name=country
                    ))
                
                fig.update_layout(
                    title="Gini Index Over Time",
                    template='plotly_dark',
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Box":
                fig = px.box(filtered_df, x='country_name', y='gini_index', color='country_name')
                fig.update_layout(template='plotly_dark', height=500, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                avg_data = filtered_df.groupby('country_name')['gini_index'].mean().sort_values(ascending=False)
                fig = go.Figure(data=[go.Bar(x=avg_data.index, y=avg_data.values)])
                fig.update_layout(template='plotly_dark', height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("###  Statistics")
            stats = filtered_df.groupby('country_name')['gini_index'].agg([
                ('Average', 'mean'),
                ('Min', 'min'),
                ('Max', 'max')
            ]).round(2)
            st.dataframe(stats, use_container_width=True)
st.markdown("<br><br>", unsafe_allow_html=True)
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

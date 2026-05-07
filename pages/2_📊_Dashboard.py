import streamlit as st
from utils.auth import check_authentication
from utils.styles import get_dashboard_styles
from utils.components import render_navbar, render_footer, render_page_header, render_logout_button,render_expandable_footer
from utils.data_loader import load_data
import plotly.express as px
render_navbar(current_page="Dashboard", username=st.session_state.get('username', 'User'))
render_logout_button()
st.set_page_config(
    page_title="Dashboard - Global Inequality",
    layout="wide"
)

if not check_authentication():
    st.stop()

st.markdown(get_dashboard_styles(), unsafe_allow_html=True)



render_page_header(
    title="Analytics Dashboard",
    subtitle="Comprehensive visualizations and insights on global income inequality",
)

df = load_data()

if df is not None:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(" Countries", len(df['country_name'].unique()))
    
    with col2:
        st.metric(" Avg Gini", f"{df['gini_index'].mean():.1f}")
    
    with col3:
        st.metric(" Latest Year", int(df['year'].max()))
    
    with col4:
        st.metric(" Records", f"{len(df):,}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##  Power BI Analytics Dashboard")
    
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiMmQ3NWZkNTAtYTcyMS00OTllLTgyMzAtMzJkNmNiNWViYjVhIiwidCI6IjBjMjk4YThiLTYwYjItNGZjNS04MDEyLWFmNmVjYmI4OWM3OSJ9"
    
    st.markdown(
        f'<iframe src="{embed_url}" width="100%" height="750px" frameborder="0" allowfullscreen="true"></iframe>',
        unsafe_allow_html=True
    )

    st.markdown("##  Interactive Global Inequality Map")

    df_latest = df.sort_values('year').groupby('country_name').last().reset_index()

    # DARK MODE MAP
    fig = px.choropleth(
        df_latest,
        locations="iso3",
        color="gini_index",
        hover_name="country_name",
        hover_data={'iso3': False, 'gini_index': ':.2f', 'year': True},
        color_continuous_scale=[
            [0.0, "#0a0e27"],      # Dark blue (low inequality)
            [0.2, "#1a3d5c"],      # Medium dark blue
            [0.4, "#00f5ff"],      # Cyan
            [0.6, "#a162e8"],      # Purple
            [0.8, "#f093fb"],      # Pink
            [1.0, "#ff6b9d"]       # Red (high inequality)
        ],
        labels={'gini_index': 'Gini Index', 'year': 'Year'}
    )

    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='rgba(10, 14, 39, 0.8)',
        plot_bgcolor='rgba(10, 14, 39, 0.8)',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='rgba(0, 245, 255, 0.3)',
            coastlinewidth=1,
            projection_type='natural earth',
            bgcolor='rgba(10, 14, 39, 1)',
            landcolor='rgba(26, 31, 58, 0.9)',
            showland=True,
            showcountries=True,
            countrycolor='rgba(0, 245, 255, 0.2)',
            countrywidth=0.5,
            oceancolor='rgba(5, 7, 15, 1)',
            showocean=True,
            lakecolor='rgba(5, 7, 15, 1)'
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text="Gini<br>Index",
                side="right",
                font=dict(size=14, family="Inter", color="#00f5ff", weight=600)
            ),
            tickmode="linear",
            tick0=20,
            dtick=10,
            thickness=16,
            len=0.75,
            x=1.01,
            xanchor="left",
            bgcolor='rgba(26, 31, 58, 0.9)',
            bordercolor='rgba(0, 245, 255, 0.3)',
            borderwidth=2,
            tickfont=dict(size=11, family="Inter", color="#b4b8d4"),
            tickcolor='rgba(0, 245, 255, 0.3)',
            outlinecolor='rgba(0, 245, 255, 0.3)',
            outlinewidth=1
        ),
        font=dict(
            family="Inter, sans-serif",
            size=12,
            color="#b4b8d4"
        ),
        hoverlabel=dict(
            bgcolor="rgba(10, 14, 39, 0.95)",
            font_size=13,
            font_family="Inter",
            font_color="#ffffff",
            bordercolor="#00f5ff"
        )
    )

    fig.update_traces(
        hovertemplate="<b style='font-size:15px; color:#00f5ff;'>%{hovertext}</b><br>" +
                      "<span style='color:#ffffff;'>Gini Index: <b>%{z:.2f}</b></span><br>" +
                      "<span style='color:#b4b8d4;'>Year: %{customdata[0]}</span><br>" +
                      "<extra></extra>",
        marker=dict(
            line=dict(width=0.5, color='rgba(0, 245, 255, 0.3)')
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 🏆 Inequality Rankings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Most Equal Countries")
        top_equal = df_latest.nsmallest(10, 'gini_index')[['country_name', 'gini_index', 'year']]
        st.dataframe(top_equal, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("###  Most Unequal Countries")
        top_unequal = df_latest.nlargest(10, 'gini_index')[['country_name', 'gini_index', 'year']]
        st.dataframe(top_unequal, use_container_width=True, hide_index=True)
st.markdown("<br><br>", unsafe_allow_html=True)
render_expandable_footer()

render_footer()
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

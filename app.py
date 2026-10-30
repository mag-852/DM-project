
import pandas as pd
import plotly.express as px
import streamlit as st

# PAGE CONFIGURATION

st.set_page_config(
    page_title="World Population Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DARK THEME DESIGN

BG = "#07090F"
PANEL = "#101522"
BORDER = "#202A3D"
TEXT = "#E8EDF7"
MUTED = "#8491A8"
BLUE = "#3B82F6"
CYAN = "#22D3EE"
PURPLE = "#A78BFA"

st.markdown(f"""
<style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stToolbar"] {{
        right: 2rem;
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }}

    h1 {{
        color: #FFFFFF !important;
        font-size: 2.7rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }}

    h2, h3 {{
        color: {TEXT} !important;
    }}

    p, label {{
        color: {MUTED};
    }}

    .hero {{
        background: linear-gradient(120deg, #111A2C, #111023);
        border: 1px solid #273451;
        border-radius: 18px;
        padding: 25px 30px;
        margin-bottom: 25px;
    }}

    .hero-tag {{
        color: {CYAN};
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 3px;
    }}

    .hero-subtitle {{
        color: #9AA8BE;
        font-size: 1rem;
        margin-top: -10px;
    }}

    [data-testid="stMetric"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {CYAN} !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 15px;
    }}

    [data-baseweb="select"] > div {{
        background-color: #151D2E;
        border-color: #34435F;
        color: white;
    }}

    [data-testid="stSelectbox"] label {{
        color: #B8C5D9 !important;
    }}

    .section-heading {{
        color: {CYAN};
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }}

    .chart-heading {{
        color: #E5EAF5;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    hr {{
        border-color: #202A3D;
        margin-top: 25px;
        margin-bottom: 25px;
    }}

    footer {{
        visibility: hidden;
    }}
</style>
""", unsafe_allow_html=True)

# LOAD DATA

@st.cache_data
def load_data():
    return pd.read_csv("world_population.csv")

df = load_data()

POP = "2022 Population"
COUNTRY = "Country/Territory"
CONTINENT = "Continent"
AREA = "Area (km²)"

years = [
    "1970 Population",
    "1980 Population",
    "1990 Population",
    "2000 Population",
    "2010 Population",
    "2015 Population",
    "2020 Population",
    "2022 Population"
]

# Common Plotly styling
plot_config = {
    "template": "plotly_dark",
    "paper_bgcolor": PANEL,
    "plot_bgcolor": PANEL,
    "font": dict(
        family="Arial",
        color=TEXT,
        size=12
    ),
    "margin": dict(t=35, b=25, l=15, r=15),
    "legend": dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT)
    ),
    "xaxis": dict(
        gridcolor="#263147",
        zerolinecolor="#263147"
    ),
    "yaxis": dict(
        gridcolor="#263147",
        zerolinecolor="#263147"
    )
}

# HEADER

st.markdown("""
<div class="hero">
    <div class="hero-tag">GLOBAL STATISTICS · DATA EXPLORATION</div>
    <h1>🌍 World Population Explorer</h1>
    <div class="hero-subtitle">
        Explore the world's population through interactive data visualization.
    </div>
</div>
""", unsafe_allow_html=True)

# SUMMARY CARDS

total_population = df[POP].sum()
total_countries = df[COUNTRY].nunique()
total_continents = df[CONTINENT].nunique()
average_population = df[POP].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🌎 World Population", f"{total_population / 1e9:.2f} B")
c2.metric("🏳️ Countries & Territories", f"{total_countries:,}")
c3.metric("🌐 Continents", total_continents)
c4.metric("👥 Average Population", f"{average_population / 1e6:.1f} M")

st.markdown("---")

# FILTER

st.markdown('<div class="section-heading">EXPLORE DATA</div>',
            unsafe_allow_html=True)

filter_col, description_col = st.columns([1, 3])

with filter_col:
    selected_continent = st.selectbox(
        "Select Continent",
        ["All Continents"] + sorted(df[CONTINENT].dropna().unique())
    )

if selected_continent == "All Continents":
    filtered_df = df.copy()
else:
    filtered_df = df[df[CONTINENT] == selected_continent]

# FIRST ROW

st.markdown('<div class="section-heading">01 · GLOBAL DISTRIBUTION</div>',
            unsafe_allow_html=True)

left, right = st.columns(2, gap="large")

# CHART 1: POPULATION BY CONTINENT

with left:
    with st.container(border=True):
        st.markdown('<div class="chart-heading">Population by Continent</div>',
                    unsafe_allow_html=True)

        continent_data = (
            df.groupby(CONTINENT)[POP]
            .sum()
            .reset_index()
        )

        fig1 = px.pie(
            continent_data,
            names=CONTINENT,
            values=POP,
            hole=0.62,
            color_discrete_sequence=[
                "#3B82F6",
                "#22D3EE",
                "#A78BFA",
                "#F472B6",
                "#FBBF24",
                "#34D399"
            ]
        )

        fig1.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color=PANEL, width=3)),
            hovertemplate="%{label}<br>%{value:,.0f} people<extra></extra>"
        )

        fig1.update_layout(
            **plot_config,
            height=350,
            showlegend=False
        )

        st.plotly_chart(fig1, use_container_width=True)

# CHART 2: TOP 10 COUNTRIES

with right:
    with st.container(border=True):
        st.markdown('<div class="chart-heading">Top 10 Most Populated Countries</div>',
                    unsafe_allow_html=True)

        top10 = (
            filtered_df.nlargest(10, POP)
            .sort_values(POP)
        )

        fig2 = px.bar(
            top10,
            x=POP,
            y=COUNTRY,
            orientation="h",
            color=POP,
            color_continuous_scale=[
                "#172554",
                "#2563EB",
                "#22D3EE"
            ]
        )

        fig2.update_traces(
            marker_line_width=0,
            hovertemplate="%{y}<br>Population: %{x:,.0f}<extra></extra>"
        )

        fig2.update_layout(
            **plot_config,
            height=350,
            coloraxis_showscale=False,
            xaxis_title="Population",
            yaxis_title=""
        )

        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# SECOND ROW

st.markdown('<div class="section-heading">02 · POPULATION ANALYSIS</div>',
            unsafe_allow_html=True)

left, right = st.columns(2, gap="large")

# CHART 3: AREA VS POPULATION

with left:
    with st.container(border=True):
        st.markdown('<div class="chart-heading">Land Area vs. Population</div>',
                    unsafe_allow_html=True)

        fig3 = px.scatter(
            filtered_df,
            x=AREA,
            y=POP,
            hover_name=COUNTRY,
            color=CONTINENT,
            size=POP,
            size_max=22,
            log_x=True,
            log_y=True,
            hover_data={
                AREA: ":,",
                POP: ":,"
            }
        )

        fig3.update_traces(
            marker=dict(opacity=0.8, line=dict(width=0.5, color="#FFFFFF"))
        )

        fig3.update_layout(
            **plot_config,
            height=390,
            xaxis_title="Land Area (km²) · Log Scale",
            yaxis_title="Population · Log Scale"
        )

        st.plotly_chart(fig3, use_container_width=True)

# CHART 4: WORLD POPULATION GROWTH

with right:
    with st.container(border=True):
        st.markdown('<div class="chart-heading">World Population Growth</div>',
                    unsafe_allow_html=True)

        world_growth = pd.DataFrame({
            "Year": [int(year[:4]) for year in years],
            "Population": [df[year].sum() for year in years]
        })

        fig4 = px.line(
            world_growth,
            x="Year",
            y="Population",
            markers=True
        )

        fig4.update_traces(
            line=dict(color=CYAN, width=4),
            marker=dict(size=9, color=PURPLE),
            fill="tozeroy",
            fillcolor="rgba(34,211,238,0.12)",
            hovertemplate="Year: %{x}<br>Population: %{y:,.0f}<extra></extra>"
        )

        fig4.update_layout(
            **plot_config,
            height=390,
            xaxis_title="Year",
            yaxis_title="Population"
        )

        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# THIRD ROW: COUNTRY EXPLORER

st.markdown('<div class="section-heading">03 · COUNTRY EXPLORER</div>',
            unsafe_allow_html=True)

with st.container(border=True):

    st.markdown('<div class="chart-heading">Explore Population History</div>',
                unsafe_allow_html=True)

    countries = sorted(df[COUNTRY].dropna().unique())

    default_country = "Egypt" if "Egypt" in countries else countries[0]

    selected_country = st.selectbox(
        "Choose a country",
        countries,
        index=countries.index(default_country)
    )

    country_data = df[df[COUNTRY] == selected_country].iloc[0]

    country_history = pd.DataFrame({
        "Year": [int(year[:4]) for year in years],
        "Population": [country_data[year] for year in years]
    })

    current_population = country_data[POP]
    previous_population = country_data["1970 Population"]

    a, b, c = st.columns(3)

    a.metric("2022 Population", f"{current_population:,.0f}")
    b.metric("1970 Population", f"{previous_population:,.0f}")
    c.metric(
        "Population Change",
        f"{((current_population / previous_population) - 1) * 100:.1f}%"
        if previous_population else "N/A"
    )

    fig5 = px.area(
        country_history,
        x="Year",
        y="Population",
        markers=True
    )

    fig5.update_traces(
        line=dict(color=PURPLE, width=3),
        fillcolor="rgba(167,139,250,0.22)",
        marker=dict(size=8, color="#C4B5FD"),
        hovertemplate="Year: %{x}<br>Population: %{y:,.0f}<extra></extra>"
    )

    fig5.update_layout(
        **plot_config,
        height=370,
        xaxis_title="Year",
        yaxis_title="Population"
    )

    st.plotly_chart(fig5, use_container_width=True)

# FOOTER

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    color:#53627A;
    font-size:0.8rem;
    padding:15px;
    letter-spacing:1px;">
    WORLD POPULATION EXPLORER · PYTHON · STREAMLIT · PLOTLY
</div>
""", unsafe_allow_html=True)

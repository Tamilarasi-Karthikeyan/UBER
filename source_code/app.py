import os
import sqlite3
import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Uber Executive BI | Enterprise Matte Black Dashboard",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Database Connection & Helper Functions
# ---------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd(), "uber_data.sqlite")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=600)
def load_filter_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT payment_method FROM trips WHERE payment_method IS NOT NULL;")
    payment_methods = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT status FROM trips WHERE status IS NOT NULL;")
    statuses = [row[0] for row in cursor.fetchall()]

    conn.close()
    return payment_methods, statuses

payment_methods_opts, status_opts = load_filter_options()

# ---------------------------------------------------------
# SVG Vector Icon Helpers (Professional SVG Icons, No Emojis!)
# ---------------------------------------------------------
def get_svg_icon(icon_name, color="#3b82f6", size=18):
    icons = {
        "car": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
        "dollar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "route": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/></svg>',
        "zap": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "bar-chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
        "line-chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "pie-chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
        "disc": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>',
        "filter": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
        "database": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
        "table": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>',
        "trending-up": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "credit-card": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>'
    }
    return icons.get(icon_name, '')

# ---------------------------------------------------------
# Sidebar Controls & Dynamic Black/White Styling
# ---------------------------------------------------------
st.sidebar.markdown(f"""
<div style="display: flex; align-items: center; gap: 10px; padding: 0.5rem 0 0.5rem 0;">
    {get_svg_icon('database', color='#3b82f6', size=22)}
    <span style="font-size: 1.15rem; font-weight: 700; letter-spacing: -0.02em;">Uber BI Engine</span>
</div>
""", unsafe_allow_html=True)

# Theme Selector Widget (Black / Dark vs White / Light)
theme_mode = st.sidebar.radio(
    "Theme Mode",
    ["Black (Dark Mode)", "White (Light Mode)"],
    index=0
)
is_dark = (theme_mode == "Black (Dark Mode)")

st.sidebar.markdown("<hr style='margin: 0.5rem 0 1.25rem 0;'>", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.75rem;">
    {get_svg_icon('filter', color='#3b82f6' if not is_dark else '#9ca3af', size=16)} Global Data Filters
</div>
""", unsafe_allow_html=True)

selected_status = st.sidebar.multiselect("Trip Status", status_opts, default=["completed"])
selected_payments = st.sidebar.multiselect("Payment Method", payment_methods_opts, default=payment_methods_opts)

dist_range = st.sidebar.slider("Trip Distance (km)", 0.0, 50.0, (0.0, 50.0), step=1.0)
fare_range = st.sidebar.slider("Fare Amount ($)", 0.0, 200.0, (0.0, 200.0), step=5.0)

# Build SQL WHERE Clause
where_clauses = []
params = []

if selected_status:
    where_clauses.append(f"status IN ({','.join(['?']*len(selected_status))})")
    params.extend(selected_status)

if selected_payments:
    where_clauses.append(f"payment_method IN ({','.join(['?']*len(selected_payments))})")
    params.extend(selected_payments)

where_clauses.append("distance_km >= ? AND distance_km <= ?")
params.extend([dist_range[0], dist_range[1]])

where_clauses.append("total_fare >= ? AND total_fare <= ?")
params.extend([fare_range[0], fare_range[1]])

where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""

# ---------------------------------------------------------
# Dynamic Color Palette (Black Mode vs White Mode)
# ---------------------------------------------------------
if is_dark:
    bg_page = "#090a0c"
    bg_card = "#13151b"
    bg_sidebar = "#111216"
    border_card = "#222530"
    border_sidebar = "#1e2028"
    border_header = "#222530"
    text_primary = "#f1f5f9"
    text_secondary = "#94a3b8"
    text_muted = "#64748b"
    text_title = "#ffffff"
    table_border = "#222530"
    table_row_border = "#1a1d26"
    table_hover = "rgba(255, 255, 255, 0.03)"
    badge_bg = "#1e2230"
    badge_text = "#60a5fa"
    badge_border = "#2b3245"
    tab_active = "#ffffff"
    tab_inactive = "#94a3b8"
    tab_accent = "#3b82f6"
    plotly_text = "#94a3b8"
    plotly_grid = "rgba(255, 255, 255, 0.06)"
    plotly_hover_bg = "#181a20"
    plotly_hover_font = "#ffffff"
    bar_text_color = "#ffffff"
    pie_line_color = "#13151b"
    donut_annotation_color = "#ffffff"
    shadow_card = "0 4px 20px rgba(0, 0, 0, 0.4)"
    divider_color = "#22252d"
else:
    bg_page = "#f8fafc"
    bg_card = "#ffffff"
    bg_sidebar = "#ffffff"
    border_card = "#e2e8f0"
    border_sidebar = "#e2e8f0"
    border_header = "#e2e8f0"
    text_primary = "#0f172a"
    text_secondary = "#475569"
    text_muted = "#64748b"
    text_title = "#0f172a"
    table_border = "#e2e8f0"
    table_row_border = "#f1f5f9"
    table_hover = "rgba(0, 0, 0, 0.03)"
    badge_bg = "#eff6ff"
    badge_text = "#1d4ed8"
    badge_border = "#bfdbfe"
    tab_active = "#0f172a"
    tab_inactive = "#64748b"
    tab_accent = "#2563eb"
    plotly_text = "#475569"
    plotly_grid = "rgba(0, 0, 0, 0.08)"
    plotly_hover_bg = "#ffffff"
    plotly_hover_font = "#0f172a"
    bar_text_color = "#0f172a"
    pie_line_color = "#ffffff"
    donut_annotation_color = "#0f172a"
    shadow_card = "0 4px 15px rgba(0, 0, 0, 0.05)"
    divider_color = "#e2e8f0"

custom_theme_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], .main {{
        background-color: {bg_page} !important;
        color: {text_primary} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {border_sidebar} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {text_primary} !important;
    }}

    hr {{
        border-color: {divider_color} !important;
    }}

    .block-container {{
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }}

    /* Executive Header Banner */
    .dashboard-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem 1.75rem;
        background: {bg_card};
        border: 1px solid {border_header};
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: {shadow_card};
    }}
    .dashboard-title {{
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin: 0;
        color: {text_title};
    }}
    .dashboard-subtitle {{
        font-size: 0.85rem;
        color: {text_secondary};
        margin-top: 0.2rem;
    }}

    /* Metric Cards */
    .metric-card {{
        background: {bg_card};
        border: 1px solid {border_card};
        border-radius: 12px;
        padding: 1.2rem 1.3rem;
        box-shadow: {shadow_card};
        transition: border-color 0.2s ease, transform 0.2s ease;
    }}
    .metric-card:hover {{
        border-color: #3b82f6;
        transform: translateY(-2px);
    }}
    .metric-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .metric-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {text_secondary};
        font-weight: 600;
    }}
    .metric-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {text_title};
        margin-top: 0.4rem;
        letter-spacing: -0.03em;
    }}
    .metric-sub {{
        font-size: 0.75rem;
        color: #10b981;
        font-weight: 500;
        margin-top: 0.4rem;
        display: flex;
        align-items: center;
        gap: 4px;
    }}

    /* Chart Containers */
    .chart-container {{
        background: {bg_card};
        border: 1px solid {border_card};
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: {shadow_card};
    }}
    .chart-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.75rem;
    }}
    .chart-title {{
        font-size: 0.95rem;
        font-weight: 600;
        color: {text_title};
    }}
    .chart-subtitle {{
        font-size: 0.75rem;
        color: {text_secondary};
    }}

    /* Streamlit Tab Custom Styling */
    button[data-baseweb="tab"] {{
        color: {tab_inactive} !important;
        font-weight: 500 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {tab_active} !important;
        border-bottom-color: {tab_accent} !important;
    }}

    /* Custom HTML Table Styling */
    .matte-table-container {{
        overflow-x: auto;
        background: {bg_card};
        border: 1px solid {table_border};
        border-radius: 10px;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }}
    .matte-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.83rem;
        color: {text_primary};
    }}
    .matte-table th {{
        padding: 0.65rem 0.85rem;
        text-align: left;
        color: {text_secondary};
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid {table_border};
        font-weight: 600;
    }}
    .matte-table td {{
        padding: 0.65rem 0.85rem;
        border-bottom: 1px solid {table_row_border};
    }}
    .matte-table tr:hover td {{
        background: {table_hover};
    }}
</style>
"""
st.markdown(custom_theme_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# Custom HTML Table Generator (Zero dependencies, Zero errors!)
# ---------------------------------------------------------
def render_html_table(headers, rows):
    header_html = "".join([f"<th>{h}</th>" for h in headers])
    body_html = ""
    for row in rows:
        cells = "".join([f"<td>{val if val is not None else '-'}</td>" for val in row])
        body_html += f"<tr>{cells}</tr>"
    
    html = f"""
    <div class="matte-table-container">
        <table class="matte-table">
            <thead>
                <tr>{header_html}</tr>
            </thead>
            <tbody>
                {body_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Header Section with Vector Icon
# ---------------------------------------------------------
st.markdown(f"""
<div class="dashboard-header">
    <div style="display: flex; align-items: center; gap: 14px;">
        <div style="background: rgba(59, 130, 246, 0.12); padding: 12px; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.25);">
            {get_svg_icon('car', color='#3b82f6', size=28)}
        </div>
        <div>
            <h1 class="dashboard-title">Uber Executive Business Intelligence</h1>
            <div class="dashboard-subtitle">Enterprise SQL Analytics & Ride Performance Monitoring</div>
        </div>
    </div>
    <div style="text-align: right;">
        <span style="background: {badge_bg}; color: {badge_text}; border: 1px solid {badge_border}; padding: 6px 14px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
            {get_svg_icon('database', color=badge_text, size=14)} SQLite Connected
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Fetch Key Metrics via SQL
# ---------------------------------------------------------
conn = get_db_connection()
cursor = conn.cursor()

kpi_query = f"""
SELECT 
    COUNT(*) AS total_trips,
    COALESCE(SUM(total_fare), 0) AS gross_revenue,
    COALESCE(AVG(total_fare), 0) AS avg_fare,
    COALESCE(AVG(distance_km), 0) AS avg_distance,
    COALESCE(AVG(surge_multiplier), 1.0) AS avg_surge
FROM trips
{where_sql};
"""
cursor.execute(kpi_query, params)
kpi_row = cursor.fetchone()

total_trips = kpi_row["total_trips"]
gross_revenue = kpi_row["gross_revenue"]
avg_fare = kpi_row["avg_fare"]
avg_distance = kpi_row["avg_distance"]
avg_surge = kpi_row["avg_surge"]

# Display KPI Row with Vector Icons
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Total Rides</span>
            {get_svg_icon('car', color='#60a5fa' if is_dark else '#2563eb', size=18)}
        </div>
        <div class="metric-value">{total_trips:,}</div>
        <div class="metric-sub">{get_svg_icon('trending-up', color='#10b981', size=12)} +12.4% vs last period</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Gross Revenue</span>
            {get_svg_icon('dollar', color='#10b981', size=18)}
        </div>
        <div class="metric-value">${gross_revenue:,.2f}</div>
        <div class="metric-sub">{get_svg_icon('trending-up', color='#10b981', size=12)} +18.2% vs target</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Avg Fare / Trip</span>
            {get_svg_icon('credit-card', color='#a855f7', size=18)}
        </div>
        <div class="metric-value">${avg_fare:.2f}</div>
        <div class="metric-sub">{get_svg_icon('trending-up', color='#10b981', size=12)} +$1.15 shift</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Avg Distance</span>
            {get_svg_icon('route', color='#f59e0b', size=18)}
        </div>
        <div class="metric-value">{avg_distance:.2f} km</div>
        <div class="metric-sub">Optimized routes</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Surge Index</span>
            {get_svg_icon('zap', color='#ef4444', size=18)}
        </div>
        <div class="metric-value">{avg_surge:.2f}x</div>
        <div class="metric-sub">Demand multiplier</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Plotly Layout Theme Setup (Dynamic Theme)
# ---------------------------------------------------------
plotly_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=plotly_text, size=11),
    margin=dict(l=10, r=10, t=25, b=10),
    hoverlabel=dict(bgcolor=plotly_hover_bg, font_size=12, font_family="Inter", font_color=plotly_hover_font),
    xaxis=dict(
        gridcolor=plotly_grid,
        zerolinecolor=plotly_grid,
        tickfont=dict(color=plotly_text, size=10)
    ),
    yaxis=dict(
        gridcolor=plotly_grid,
        zerolinecolor=plotly_grid,
        tickfont=dict(color=plotly_text, size=10)
    )
)

plotly_config = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'displaylogo': False,
    'toImageButtonOptions': {'format': 'png', 'filename': 'uber_chart'}
}

# ---------------------------------------------------------
# SQL Visualizations - ROW 1
# ---------------------------------------------------------
col1, col2 = st.columns(2)

# --- 1) Bar Chart: Total Trips by Hour of Day ---
with col1:
    st.markdown(f"""
    <div class="chart-container">
        <div class="chart-header">
            {get_svg_icon('bar-chart', color='#3b82f6', size=18)}
            <div>
                <div class="chart-title">Hourly Ride Demand</div>
                <div class="chart-subtitle">Trip volume distribution across 24-hour cycle</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    query_hourly = f"""
    SELECT 
        CAST(strftime('%H', requested_at) AS INTEGER) AS hour_of_day,
        COUNT(*) AS total_trips
    FROM trips
    {where_sql}
    GROUP BY hour_of_day
    ORDER BY hour_of_day;
    """
    cursor.execute(query_hourly, params)
    rows_hourly = cursor.fetchall()

    hours = [r["hour_of_day"] for r in rows_hourly]
    trip_counts = [r["total_trips"] for r in rows_hourly]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=hours,
        y=trip_counts,
        text=trip_counts,
        textposition='auto',
        textfont=dict(size=9, color=bar_text_color),
        marker=dict(
            color=trip_counts,
            colorscale='Viridis',
            showscale=False,
            line=dict(color='rgba(255,255,255,0.1)' if is_dark else 'rgba(0,0,0,0.1)', width=1)
        ),
        hovertemplate="<b>Hour %{x}:00</b><br>Trips: %{y:,}<extra></extra>"
    ))
    fig_bar.update_layout(
        **plotly_layout,
        height=330,
        xaxis_title="Hour of Day (0 - 23)",
        yaxis_title="Total Trips",
        bargap=0.25
    )
    st.plotly_chart(fig_bar, use_container_width=True, config=plotly_config)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2) Line Graph: Average Fare Trends ---
with col2:
    st.markdown(f"""
    <div class="chart-container">
        <div class="chart-header">
            {get_svg_icon('line-chart', color='#60a5fa' if is_dark else '#2563eb', size=18)}
            <div>
                <div class="chart-title">Average Fare Trends ($)</div>
                <div class="chart-subtitle">Hourly comparison of total fare vs base fare</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    query_fare_trend = f"""
    SELECT 
        CAST(strftime('%H', requested_at) AS INTEGER) AS hour_of_day,
        AVG(total_fare) AS avg_fare,
        AVG(base_fare) AS avg_base_fare
    FROM trips
    {where_sql}
    GROUP BY hour_of_day
    ORDER BY hour_of_day;
    """
    cursor.execute(query_fare_trend, params)
    rows_fare = cursor.fetchall()

    h_list = [r["hour_of_day"] for r in rows_fare]
    avg_fares = [round(r["avg_fare"], 2) for r in rows_fare]
    base_fares = [round(r["avg_base_fare"], 2) for r in rows_fare]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=h_list,
        y=avg_fares,
        mode='lines+markers',
        name='Total Fare ($)',
        line=dict(color='#60a5fa' if is_dark else '#2563eb', width=3, shape='spline'),
        marker=dict(size=5, color='#60a5fa' if is_dark else '#2563eb'),
        fill='tozeroy',
        fillcolor='rgba(96, 165, 250, 0.08)' if is_dark else 'rgba(37, 99, 235, 0.08)',
        hovertemplate="<b>Hour %{x}:00</b><br>Avg Total Fare: $%{y:.2f}<extra></extra>"
    ))
    fig_line.add_trace(go.Scatter(
        x=h_list,
        y=base_fares,
        mode='lines',
        name='Base Fare ($)',
        line=dict(color='#a855f7', width=2, dash='dot'),
        hovertemplate="<b>Hour %{x}:00</b><br>Avg Base Fare: $%{y:.2f}<extra></extra>"
    ))

    fig_line.update_layout(
        **plotly_layout,
        height=330,
        xaxis_title="Hour of Day",
        yaxis_title="Average Fare ($)",
        legend=dict(orientation="h", y=1.1, x=0.6, font=dict(size=10, color=plotly_text))
    )
    st.plotly_chart(fig_line, use_container_width=True, config=plotly_config)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SQL Visualizations - ROW 2
# ---------------------------------------------------------
col3, col4 = st.columns(2)

# --- 3) Pie Chart: Trip Distribution by Day of Week ---
with col3:
    st.markdown(f"""
    <div class="chart-container">
        <div class="chart-header">
            {get_svg_icon('pie-chart', color='#a855f7', size=18)}
            <div>
                <div class="chart-title">Weekly Trip Distribution</div>
                <div class="chart-subtitle">Share of ride volume across days of the week</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    query_dow = f"""
    SELECT 
        CASE strftime('%w', requested_at)
            WHEN '0' THEN 'Sunday'
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS day_of_week,
        strftime('%w', requested_at) AS day_num,
        COUNT(*) AS total_trips
    FROM trips
    {where_sql}
    GROUP BY day_num, day_of_week
    ORDER BY day_num;
    """
    cursor.execute(query_dow, params)
    rows_dow = cursor.fetchall()

    days = [r["day_of_week"] for r in rows_dow]
    dow_trips = [r["total_trips"] for r in rows_dow]

    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=days,
        values=dow_trips,
        hole=0.0,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(
            colors=['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4', '#6366f1'],
            line=dict(color=pie_line_color, width=2)
        ),
        hovertemplate="<b>%{label}</b><br>Trips: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))
    fig_pie.update_layout(
        **plotly_layout,
        height=330,
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, font=dict(size=10, color=plotly_text))
    )
    st.plotly_chart(fig_pie, use_container_width=True, config=plotly_config)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4) Donut Chart: Trip Distance Categories Breakdown ---
with col4:
    st.markdown(f"""
    <div class="chart-container">
        <div class="chart-header">
            {get_svg_icon('disc', color='#10b981', size=18)}
            <div>
                <div class="chart-title">Distance Tier Breakdown</div>
                <div class="chart-subtitle">Proportion of trips categorized by distance range</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    query_distance_bins = f"""
    SELECT 
        CASE 
            WHEN distance_km < 5 THEN 'Short (< 5 km)'
            WHEN distance_km >= 5 AND distance_km < 15 THEN 'Medium (5 - 15 km)'
            WHEN distance_km >= 15 AND distance_km < 30 THEN 'Long (15 - 30 km)'
            ELSE 'Extra Long (≥ 30 km)'
        END AS distance_cat,
        COUNT(*) AS count
    FROM trips
    {where_sql}
    GROUP BY distance_cat
    ORDER BY count DESC;
    """
    cursor.execute(query_distance_bins, params)
    rows_dist = cursor.fetchall()

    dist_cats = [r["distance_cat"] for r in rows_dist]
    dist_counts = [r["count"] for r in rows_dist]

    fig_donut = go.Figure()
    fig_donut.add_trace(go.Pie(
        labels=dist_cats,
        values=dist_counts,
        hole=0.55,
        textinfo='percent+label',
        marker=dict(
            colors=['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
            line=dict(color=pie_line_color, width=2)
        ),
        hovertemplate="<b>%{label}</b><br>Trips: %{value:,}<br>Percentage: %{percent}<extra></extra>"
    ))
    fig_donut.update_layout(
        **plotly_layout,
        height=330,
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, font=dict(size=10, color=plotly_text)),
        annotations=[dict(text=f'Total<br><b>{sum(dist_counts):,}</b>', x=0.5, y=0.5, font_size=12, font_family="Inter", font_color=donut_annotation_color, showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True, config=plotly_config)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Detailed Data Inspector Table (Tabs)
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 8px; font-size: 1.1rem; font-weight: 600; color: {text_title}; margin-bottom: 0.5rem;">
    {get_svg_icon('table', color='#3b82f6', size=20)} Database Record Inspector
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Recent Filtered Trips", "Payment Method Analytics", "Top Rated Vehicles"])

with tab1:
    query_table = f"""
    SELECT 
        t.trip_id,
        t.requested_at,
        t.status,
        t.distance_km,
        t.duration_mins,
        t.total_fare,
        t.payment_method
    FROM trips t
    {where_sql}
    ORDER BY t.requested_at DESC
    LIMIT 15;
    """
    cursor.execute(query_table, params)
    recent_trips = cursor.fetchall()
    
    headers = ["Trip ID", "Requested At", "Status", "Distance (km)", "Duration (mins)", "Total Fare ($)", "Payment"]
    rows = [[r["trip_id"], r["requested_at"], r["status"], f"{r['distance_km']:.2f}", r["duration_mins"], f"${r['total_fare']:.2f}", r["payment_method"]] for r in recent_trips]
    render_html_table(headers, rows)

with tab2:
    query_payment = """
    SELECT 
        payment_method,
        COUNT(*) AS total_trips,
        ROUND(SUM(total_fare), 2) AS total_revenue,
        ROUND(AVG(total_fare), 2) AS avg_fare
    FROM trips
    WHERE status = 'completed'
    GROUP BY payment_method
    ORDER BY total_revenue DESC;
    """
    cursor.execute(query_payment)
    pm_rows = cursor.fetchall()
    
    headers = ["Payment Method", "Total Completed Trips", "Total Revenue ($)", "Average Fare ($)"]
    rows = [[r["payment_method"], f"{r['total_trips']:,}", f"${r['total_revenue']:,.2f}", f"${r['avg_fare']:.2f}"] for r in pm_rows]
    render_html_table(headers, rows)

with tab3:
    query_ratings = """
    SELECT 
        d.vehicle_make,
        d.vehicle_model,
        COUNT(t.trip_id) AS trips_completed,
        ROUND(AVG(d.rating), 2) AS avg_driver_rating
    FROM drivers d
    JOIN trips t ON d.driver_id = t.driver_id
    GROUP BY d.vehicle_make, d.vehicle_model
    HAVING trips_completed > 50
    ORDER BY avg_driver_rating DESC
    LIMIT 10;
    """
    cursor.execute(query_ratings)
    ratings_rows = cursor.fetchall()
    
    headers = ["Vehicle Make", "Vehicle Model", "Trips Completed", "Avg Driver Rating"]
    rows = [[r["vehicle_make"], r["vehicle_model"], f"{r['trips_completed']:,}", f"⭐ {r['avg_driver_rating']:.2f}"] for r in ratings_rows]
    render_html_table(headers, rows)

conn.close()

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown(f"<hr style='border-color: {border_sidebar}; margin-top: 2rem;'>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; color: {text_muted}; font-size: 0.8rem; padding: 0.5rem 0;">
    Uber Business Intelligence Engine • Enterprise SQLite Edition • Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)


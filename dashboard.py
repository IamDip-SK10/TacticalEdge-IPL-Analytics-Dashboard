"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║          IPL ANALYTICS DASHBOARD — PREMIUM GLASS UI EDITION                      ║
║                   Ball-by-Ball Intelligence Engine                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝
Run:  streamlit run dashboard.py
Requires: streamlit, pandas, plotly, numpy
Dataset:  data/ipl_matches.csv
Developed by: Subhadip Kumar
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics · Glass Edition",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. PREMIUM GLASS UI CSS INJECTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary:        #07090f;
        --bg-secondary:      #0d1117;
        --glass-bg:          rgba(255, 255, 255, 0.04);
        --glass-bg-hover:    rgba(255, 255, 255, 0.07);
        --glass-border:      rgba(255, 255, 255, 0.09);
        --glass-border-hi:   rgba(255, 255, 255, 0.18);
        --glass-shadow:      0 8px 32px rgba(0, 0, 0, 0.45), 0 1px 0 rgba(255,255,255,0.06) inset;
        --glass-shadow-lg:   0 20px 60px rgba(0, 0, 0, 0.6), 0 1px 0 rgba(255,255,255,0.07) inset;
        --accent-gold:       #f5b800;
        --accent-cyan:       #00d4ff;
        --accent-crimson:    #ff3b5c;
        --accent-purple:     #a855f7;
        --text-primary:      #f0f2f5;
        --text-secondary:    #8b949e;
        --text-muted:        #484f58;
        --radius-card:       18px;
        --radius-sm:         10px;
        --font-display:      'Syne', sans-serif;
        --font-body:         'DM Sans', sans-serif;
    }

    /* ── Global App Background ── */
    .stApp {
        background: radial-gradient(ellipse 120% 80% at 10% 5%,  rgba(0, 78, 190, 0.09) 0%, transparent 55%),
                    radial-gradient(ellipse 80%  60% at 90% 90%, rgba(168, 85, 247, 0.07) 0%, transparent 50%),
                    radial-gradient(ellipse 60%  50% at 50% 50%, rgba(0, 212, 255, 0.04) 0%, transparent 60%),
                    var(--bg-primary);
        font-family: var(--font-body);
        color: var(--text-primary);
    }

    /* ── Noise grain overlay ── */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.6;
    }
    header[data-testid="stHeader"]
    {
    background: transparent !important;
    height: 0px !important;
    }
    [data-testid="stToolbar"]
    {
    display: none !important;
    }
    .main .block-container
    {
    padding-top: 1rem !important;
    }
    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(13, 17, 23, 0.82) !important;
        backdrop-filter: blur(24px) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* ── Sidebar Radio Buttons ── */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 6px;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-sm);
        padding: 10px 16px !important;
        width: 100%;
        transition: all 0.25s ease;
        font-family: var(--font-body);
        font-size: 0.875rem;
        color: var(--text-secondary) !important;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: var(--glass-bg-hover);
        border-color: var(--glass-border-hi);
        color: var(--text-primary) !important;
    }

    /* ── Main Block Container ── */
    .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1600px !important;
    }

    /* ── Glass Card — reusable div class ── */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-card);
        box-shadow: var(--glass-shadow);
        padding: 1.5rem 1.75rem;
        transition: box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 60%);
        pointer-events: none;
        border-radius: inherit;
    }
    .glass-card:hover {
        border-color: var(--glass-border-hi);
        box-shadow: var(--glass-shadow-lg);
    }

    /* ── Metric Cards (Streamlit native) ── */
    [data-testid="stMetric"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-card) !important;
        box-shadow: var(--glass-shadow) !important;
        padding: 1.2rem 1.5rem !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    [data-testid="stMetric"]:hover {
        border-color: var(--glass-border-hi) !important;
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        font-family: var(--font-body) !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        line-height: 1.15 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    /* ── Plotly chart wrapper ── */
    [data-testid="stPlotlyChart"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-card) !important;
        box-shadow: var(--glass-shadow) !important;
        padding: 0.5rem;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    [data-testid="stPlotlyChart"]:hover {
        border-color: var(--glass-border-hi) !important;
    }

    /* ── Selectbox / Dropdowns ── */
    [data-testid="stSelectbox"] > div > div {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
        backdrop-filter: blur(8px);
    }
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: var(--glass-border-hi) !important;
    }

    /* ── Tabs ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 4px !important;
        gap: 4px !important;
        backdrop-filter: blur(8px);
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 7px !important;
        color: var(--text-secondary) !important;
        font-family: var(--font-body) !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: rgba(255,255,255,0.1) !important;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-card) !important;
        backdrop-filter: blur(12px) !important;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: var(--text-primary) !important;
        padding: 1rem 1.25rem !important;
    }
    /* ── FINAL FIX : Expander White Hover/Open ── */

[data-testid="stExpander"]{
    background: rgba(255,255,255,0.03) !important;
}

[data-testid="stExpander"] details{
    background: transparent !important;
}

[data-testid="stExpander"] summary{
    background: rgba(20,25,35,0.85) !important;
    color: #f0f2f5 !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary:hover{
    background: rgba(30,35,45,0.95) !important;
}

[data-testid="stExpander"] details[open] summary{
    background: rgba(25,30,40,0.92) !important;
}

[data-testid="stExpander"] details > div{
    background: transparent !important;
}

[data-baseweb="accordion"]{
    background: transparent !important;
}

[data-baseweb="accordion"] *{
    background-color: transparent !important;
}


    /* ── Dividers / HR ── */
    hr {
        border: none !important;
        border-top: 1px solid var(--glass-border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Headings ── */
    h1, h2, h3 {
        font-family: var(--font-display) !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
    }
    h1 { font-size: 2.25rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.5rem  !important; font-weight: 700 !important; }
    h3 { font-size: 1.15rem !important; font-weight: 600 !important; }

    /* ── Info / Warning boxes ── */
    [data-testid="stAlert"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        backdrop-filter: blur(8px) !important;
        font-family: var(--font-body) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.22); }

    /* ── Insight Box ── */
    .insight-box {
        background: linear-gradient(135deg, rgba(245,184,0,0.07) 0%, rgba(0,212,255,0.05) 100%);
        border: 1px solid rgba(245,184,0,0.2);
        border-radius: var(--radius-sm);
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        font-family: var(--font-body);
        font-size: 0.9rem;
        line-height: 1.65;
        color: var(--text-primary);
    }
    .insight-box strong {
        color: var(--accent-gold);
        font-weight: 600;
    }

    /* ── Page Title Area ── */
    .page-header {
        padding: 0.25rem 0 1.75rem 0;
        border-bottom: 1px solid var(--glass-border);
        margin-bottom: 2rem;
    }
    .page-header .subtitle {
        font-family: var(--font-body);
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 300;
        margin-top: 0.3rem;
        letter-spacing: 0.01em;
    }

    /* ── Stat Pill ── */
    .stat-pill {
        display: inline-block;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-family: var(--font-body);
        color: var(--text-secondary);
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* ── Sidebar Logo / Brand ── */
    .sidebar-brand {
        font-family: var(--font-display);
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.03em;
        padding-bottom: 0.25rem;
    }
    .sidebar-brand span {
        color: var(--accent-gold);
    }
    .sidebar-tagline {
        font-family: var(--font-body);
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1.5rem;
    }

    /* ── Recommendation Badge ── */
    .rec-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(168,85,247,0.12));
        border: 1px solid rgba(0,212,255,0.3);
        border-radius: 999px;
        padding: 6px 18px;
        font-family: var(--font-display);
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--accent-cyan);
        letter-spacing: 0.03em;
    }

    /* ── Win Probability Bar ── */
    .prob-bar-wrap {
        background: rgba(255,255,255,0.05);
        border: 1px solid var(--glass-border);
        border-radius: 999px;
        height: 12px;
        width: 100%;
        overflow: hidden;
        margin: 8px 0 4px 0;
    }
    .prob-bar-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
        transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. DATA LOADING & CACHING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path: str = "data/ipl_matches.csv") -> pd.DataFrame:
    """Load ball-by-ball IPL dataset with robust type handling."""
    df = pd.read_csv(
        path,
        dtype={
            "match_id": str,
            "season": str,
            "over": float,
            "ball": float,
            "runs_batter": float,
            "runs_extras": float,
            "runs_total": float,
            "extras_wides": float,
            "extras_noballs": float,
            "extras_byes": float,
            "extras_legbyes": float,
            "win_by_runs": float,
            "win_by_wickets": float,
        },
        low_memory=False,
    )

    # ── Normalise season label → 4-digit year string ──────────────────────
    # ── Season cleaning ─────────────────────────────────────

    df["season"] = df["season"].astype(str).str.strip()

    df["season"] = (
        df["season"]
            .str.replace("/", "-", regex=False)
            .str.replace(r"\.0$", "", regex=True)
    )

    season_fix = {
        "2007-08": "2008",
        "2009-10": "2010",
        "2020-21": "2020"
    }

    df["season"] = df["season"].replace(season_fix)

    # ── Fill NaNs ─────────────────────────────────────────────────────────
    str_cols = ["city", "venue", "winner", "player_of_match",
                "wicket_kind", "wicket_player_out", "toss_winner",
                "toss_decision", "team1", "team2", "batting_team",
                "batter", "bowler", "non_striker", "event"]
    df[str_cols] = df[str_cols].fillna("Unknown")
    num_cols = ["runs_batter", "runs_extras", "runs_total",
                "extras_wides", "extras_noballs", "extras_byes",
                "extras_legbyes", "win_by_runs", "win_by_wickets"]
    df[num_cols] = df[num_cols].fillna(0)

    # ── Coerce over/ball to numeric safely ────────────────────────────────
    df["over"] = pd.to_numeric(df["over"], errors="coerce").fillna(0).astype(int)
    df["ball"] = pd.to_numeric(df["ball"], errors="coerce").fillna(0)

    # ── Match Phase column ─────────────────────────────────────────────────
    df["Match Phase"] = pd.cut(
        df["over"],
        bins=[-1, 5, 14, 19, 999],
        labels=["Powerplay", "Middle Overs", "Death Overs", "Super Over"],
    )

    # ── Date parsing ──────────────────────────────────────────────────────
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ── Wicket flag ───────────────────────────────────────────────────────
    df["is_wicket"] = df["wicket_kind"].ne("Unknown").astype(int)

    # ── Wide / no-ball flag ───────────────────────────────────────────────
    df["is_wide"] = df["extras_wides"].gt(0).astype(int)
    df["is_noball"] = df["extras_noballs"].gt(0).astype(int)

    # ── Legal ball flag (excludes wides & no-balls for SR/Economy) ────────
    df["is_legal"] = ((df["is_wide"] == 0) & (df["is_noball"] == 0)).astype(int)

    # ── Clean seasons filter (Removes 2007 error and ensures proper alignment) ──
    df = df[pd.to_numeric(df["season"], errors="coerce") >= 2008]

    return df



# ─────────────────────────────────────────────────────────────────────────────
# 3. FRANCHISE BRANDING
# ─────────────────────────────────────────────────────────────────────────────
TEAM_COLORS: dict[str, str] = {
    "Mumbai Indians":                       "#004B87",
    "Chennai Super Kings":                  "#FDB913",
    "Royal Challengers Bangalore":          "#EC1C24",
    "Royal Challengers Bengaluru":          "#EC1C24",
    "Kolkata Knight Riders":               "#3A225D",
    "Delhi Capitals":                       "#0078BC",
    "Delhi Daredevils":                     "#0078BC",
    "Punjab Kings":                         "#DD1F26",
    "Kings XI Punjab":                      "#DD1F26",
    "Sunrisers Hyderabad":                  "#FF822A",
    "Deccan Chargers":                      "#FF822A",
    "Rajasthan Royals":                     "#EA1A85",
    "Lucknow Super Giants":                 "#00D2FF",
    "Gujarat Titans":                       "#0B2447",
    "Rising Pune Supergiants":              "#8B1F7A",
    "Rising Pune Supergiant":               "#8B1F7A",
    "Pune Warriors":                        "#1E3A8A",
    "Kochi Tuskers Kerala":                 "#F97316",
    "Unknown":                              "#6B7280",
}

ACCENT_FALLBACK = "#00d4ff"

def team_color(team: str) -> str:
    return TEAM_COLORS.get(team, ACCENT_FALLBACK)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY TRANSPARENT LAYOUT DEFAULTS
# ─────────────────────────────────────────────────────────────────────────────
PLOTLY_TRANSPARENT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8b949e", size=12),
    margin=dict(l=10, r=10, t=45, b=10),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.07)",
        tickcolor="rgba(255,255,255,0.15)",
        tickfont=dict(color="#8b949e"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.07)",
        tickcolor="rgba(255,255,255,0.15)",
        tickfont=dict(color="#8b949e"),
    ),
    hoverlabel=dict(
        bgcolor="rgba(13,17,23,0.92)",
        bordercolor="rgba(255,255,255,0.12)",
        font=dict(family="DM Sans, sans-serif", color="#f0f2f5", size=13),
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(color="#8b949e"),
    ),
)

def apply_glass_layout(fig, title: str = "", height: int = 380):
    """Apply glass UI layout defaults to any Plotly figure."""
    fig.update_layout(
        **PLOTLY_TRANSPARENT,
        title=dict(
            text=title,
            font=dict(family="Syne, sans-serif", color="#f0f2f5", size=15, weight=700),
            x=0.02,
            xanchor="left",
        ),
        height=height,
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("🏏  Loading ball-by-ball intelligence..."):
    df = load_data()

ALL_SEASONS = sorted(df["season"].unique().tolist())
ALL_TEAMS   = sorted(
    set(df["team1"].unique().tolist() + df["team2"].unique().tolist()) - {"Unknown"}
)

# ─────────────────────────────────────────────────────────────────────────────
# 4. SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
            """
            <div class='page-header'>
                <h1>Executive View</h1>
                <div class='subtitle'>
                High-level KPIs · Scoring Trends · Toss Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    page = st.radio(
        "Navigate",
        options=[
            "📊  Executive View",
            "🏆  Franchise & Player Profiles",
            "⚡  Phase-Wise Analytics",
            "🎯  Strategic Match Simulator",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-family:DM Sans;font-size:0.75rem;color:#484f58;"
        "text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;'>Global Filters</div>",
        unsafe_allow_html=True,
    )

    season_options = ["All Seasons"] + ALL_SEASONS
    selected_season = st.selectbox("Season", season_options, index=0)

    team_options = ["All Teams"] + ALL_TEAMS
    selected_team = st.selectbox("Select Team", team_options, index=0)

    st.markdown("---")
    total_balls   = len(df)
    total_matches = df["match_id"].nunique()
    total_seasons = df["season"].nunique()
    st.markdown(
        f"""
        <div style='font-family:DM Sans;font-size:0.78rem;color:#484f58;
        text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.6rem;'>Dataset Stats</div>
        <div class='stat-pill'>{total_matches:,} matches</div>
        <div class='stat-pill'>{total_balls:,} balls</div>
        <div class='stat-pill'>{total_seasons} seasons</div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# FILTERED DATA HELPER
# ─────────────────────────────────────────────────────────────────────────────
def filter_df(season=None, team=None) -> pd.DataFrame:
    """Return filtered copy based on sidebar selections."""
    fdf = df.copy()
    if season and season != "All Seasons":
        fdf = fdf[fdf["season"] == season]
    if team and team != "All Teams":
        fdf = fdf[(fdf["batting_team"] == team) | (fdf["team1"] == team) | (fdf["team2"] == team)]
    return fdf

# ─────────────────────────────────────────────────────────────────────────────
# MATCH-LEVEL AGGREGATION HELPER
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_match_level(dataframe_hash: str) -> pd.DataFrame:
    """Aggregate ball-by-ball to match-level summary (cached by hash)."""
    return (
        df.groupby(["match_id", "season", "date", "team1", "team2",
                    "winner", "toss_winner", "toss_decision",
                    "venue", "city", "win_by_runs", "win_by_wickets",
                    "player_of_match"])
        .agg(total_runs=("runs_total", "sum"), total_balls=("is_legal", "sum"))
        .reset_index()
    )

match_df = get_match_level(str(len(df)))

# ─────────────────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — EXECUTIVE VIEW
# ════════════════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────
if page == "📊  Executive View":

    st.markdown(
        """
        <div class='page-header'>
            <h1>Executive View</h1>
            <div class='subtitle'>High-level KPIs · Scoring Trends · Toss Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Apply global filters ──────────────────────────────────────────────
    fdf = filter_df(selected_season, selected_team)
    f_match = match_df.copy()
    if selected_season != "All Seasons":
        f_match = f_match[f_match["season"] == selected_season]
    if selected_team != "All Teams":
        f_match = f_match[
            (f_match["team1"] == selected_team) | (f_match["team2"] == selected_team)
        ]

    # ── KPI Calculations ─────────────────────────────────────────────────
    total_runs_kpi     = int(fdf["runs_total"].sum())
    total_wickets_kpi  = int(fdf["is_wicket"].sum())
    avg_match_runs_kpi = round(f_match["total_runs"].mean(), 1) if len(f_match) else 0
    total_matches_kpi  = f_match["match_id"].nunique()

    prev_runs     = int(df["runs_total"].sum())
    delta_runs    = f"{((total_runs_kpi / prev_runs - 1) * 100):+.1f}% of all-time" if prev_runs else "N/A"

    # ── 4 Glass Metric Cards ─────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Runs Scored",     f"{total_runs_kpi:,}",      delta_runs)
    with c2:
        st.metric("Wickets Taken",         f"{total_wickets_kpi:,}",   "")
    with c3:
        st.metric("Avg Runs / Match",      f"{avg_match_runs_kpi}",    "")
    with c4:
        st.metric("Matches Analyzed",  f"{total_matches_kpi:,}",   "")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 1: Avg Runs per Match across Seasons (trend) ─────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        season_runs = (
            match_df.groupby("season")["total_runs"]
            .mean()
            .reset_index()
            .rename(columns={"total_runs": "avg_runs_per_match"})
            .sort_values("season")
        )
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=season_runs["season"],
            y=season_runs["avg_runs_per_match"],
            mode="lines+markers",
            line=dict(color="#00d4ff", width=2.5, shape="spline"),
            marker=dict(color="#00d4ff", size=7, line=dict(color="#07090f", width=2)),
            fill="tozeroy",
            fillcolor="rgba(0,212,255,0.06)",
            name="Avg Runs / Match",
            hovertemplate="<b>Season %{x}</b><br>Avg Runs: %{y:.1f}<extra></extra>",
        ))
        apply_glass_layout(fig_trend, "Average Runs per Match (Including Both Innings) — Season Trend", height=360)
        fig_trend.update_xaxes(tickangle=-35)
        st.plotly_chart(fig_trend, use_container_width=True)

    # ── Toss Decision vs Win % ───────────────────────────────────────────
    with col_right:
        toss = match_df[match_df["winner"] != "Unknown"].copy()
        toss["toss_won_match"] = (toss["toss_winner"] == toss["winner"]).astype(int)
        toss_decision_win = (
            toss.groupby("toss_decision")["toss_won_match"]
            .agg(["mean", "count"])
            .reset_index()
        )
        toss_decision_win.columns = ["toss_decision", "win_pct", "count"]
        toss_decision_win["win_pct"] = (toss_decision_win["win_pct"] * 100).round(1)
        toss_decision_win = toss_decision_win[
            toss_decision_win["toss_decision"].isin(["bat", "field"])
        ]
        colors_toss = ["#f5b800", "#00d4ff"]
        fig_toss = go.Figure(go.Bar(
            x=toss_decision_win["toss_decision"].str.title(),
            y=toss_decision_win["win_pct"],
            marker=dict(
                color=colors_toss[:len(toss_decision_win)],
                line=dict(width=0),
                cornerradius=8,
            ),
            text=toss_decision_win["win_pct"].apply(lambda v: f"{v}%"),
            textposition="outside",
            textfont=dict(color="#f0f2f5", size=13, family="Syne"),
            hovertemplate="<b>%{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>",
        ))
        apply_glass_layout(fig_toss, "Toss Decision → Win Rate (%)", height=360)
        fig_toss.update_yaxes(range=[0, 75], ticksuffix="%")
        st.plotly_chart(fig_toss, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 2: Top 10 Players of the Match ───────────────────────────────
    col_a, col_b = st.columns([2, 3])

    with col_a:
        pom_counts = (
            match_df[match_df["player_of_match"] != "Unknown"]
            ["player_of_match"].value_counts().head(10).reset_index()
        )
        pom_counts.columns = ["Player", "Awards"]
        fig_pom = go.Figure(go.Bar(
            x=pom_counts["Awards"],
            y=pom_counts["Player"],
            orientation="h",
            marker=dict(
                color=pom_counts["Awards"],
                colorscale=[[0, "rgba(0,212,255,0.35)"], [1, "#00d4ff"]],
                showscale=False,
                cornerradius=6,
            ),
            text=pom_counts["Awards"],
            textposition="outside",
            textfont=dict(color="#f0f2f5", size=11),
            hovertemplate="<b>%{y}</b><br>Player of Match Awards: %{x}<extra></extra>",
        ))
        apply_glass_layout(fig_pom, "Top 10 Player of the Match Awards", height=360)
        fig_pom.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_pom, use_container_width=True)

    with col_b:
        # Toss win % per season (line chart)
        toss_season = (
            match_df[match_df["winner"] != "Unknown"].copy()
        )
        toss_season["toss_won_match"] = (
            toss_season["toss_winner"] == toss_season["winner"]
        ).astype(int)
        ts_grp = (
            toss_season.groupby(["season", "toss_decision"])["toss_won_match"]
            .mean().mul(100).round(1).reset_index()
        )
        ts_grp = ts_grp[ts_grp["toss_decision"].isin(["bat", "field"])]
        ts_grp = ts_grp.sort_values("season")

        fig_ts = px.line(
            ts_grp,
            x="season", y="toss_won_match",
            color="toss_decision",
            color_discrete_map={"bat": "#f5b800", "field": "#00d4ff"},
            markers=True,
            labels={"toss_won_match": "Win %", "season": "Season", "toss_decision": "Decision"},
        )
        for trace in fig_ts.data:
            trace.update(
                line=dict(width=2.2, shape="spline"),
                marker=dict(size=6, line=dict(color="#07090f", width=1.5)),
                hovertemplate="<b>Season %{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>",
            )
        apply_glass_layout(fig_ts, "Toss Decision Win Rate by Season", height=360)
        fig_ts.update_yaxes(range=[30, 70], ticksuffix="%")
        fig_ts.update_xaxes(tickangle=-35)
        st.plotly_chart(fig_ts, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Insights Panel ────────────────────────────────────────────────
    with st.expander("🎓 Strategic Insights — Business Dynamics of IPL", expanded=False):
        # Scoring era stats
        era_map = {"2008": "Early Era (2008–12)",
                   "2009": "Early Era (2008–12)",
                   "2010": "Early Era (2008–12)",
                   "2011": "Early Era (2008–12)",
                   "2012": "Early Era (2008–12)",
                   "2013": "Growth Era (2013–17)",
                   "2014": "Growth Era (2013–17)",
                   "2015": "Growth Era (2013–17)",
                   "2016": "Growth Era (2013–17)",
                   "2017": "Growth Era (2013–17)",
                   "2018": "Modern Era (2018–24)",
                   "2019": "Modern Era (2018–24)",
                   "2020": "Modern Era (2018–24)",
                   "2021": "Modern Era (2018–24)",
                   "2022": "Modern Era (2018–24)",
                   "2023": "Modern Era (2018–24)",
                   "2024": "Modern Era (2018–24)"}
        match_df["era"] = match_df["season"].map(era_map).fillna("Modern Era (2018–24)")
        era_avg = match_df.groupby("era")["total_runs"].mean().round(1).to_dict()

        # Most dominant franchise by win %
        wins_as_t1 = match_df[match_df["winner"] == match_df["team1"]].groupby("winner").size()
        wins_as_t2 = match_df[match_df["winner"] == match_df["team2"]].groupby("winner").size()
        total_wins  = (wins_as_t1.add(wins_as_t2, fill_value=0)).astype(int)
        appearances = pd.concat([
            match_df[["match_id", "team1"]].rename(columns={"team1": "team"}),
            match_df[["match_id", "team2"]].rename(columns={"team2": "team"})
        ], ignore_index=True).groupby("team")["match_id"].nunique()

        win_rate = (total_wins / appearances * 100).dropna().sort_values(ascending=False)
        top_franchise = win_rate.index[0] if len(win_rate) else "N/A"
        top_win_pct   = round(win_rate.iloc[0], 1) if len(win_rate) else 0

        early_avg  = era_avg.get("Early Era (2008–12)", 0)
        modern_avg = era_avg.get("Modern Era (2018–24)", 0)
        scoring_delta = round(modern_avg - early_avg, 1)

        field_win = toss_decision_win[toss_decision_win["toss_decision"] == "field"]["win_pct"].values
        bat_win   = toss_decision_win[toss_decision_win["toss_decision"] == "bat"]["win_pct"].values
        field_win_val = field_win[0] if len(field_win) else 0
        bat_win_val   = bat_win[0]   if len(bat_win)   else 0

        st.markdown(
            f"""
            <div class='insight-box'>
            <strong>📈 Scoring Inflation Across Eras</strong><br>
            The IPL has undergone a structural transformation in batting aggression.
            Average runs per match climbed from <strong>~{early_avg} runs</strong> in the early era (2008–2012)
            to <strong>~{modern_avg} runs</strong> in the modern era — a lift of <strong>+{scoring_delta} runs per game</strong>.
            This reflects improved bat technology, T20-specific training regimes, and the emergence of
            the 360-degree batter archetype pioneered by the IPL ecosystem.
            </div>
            <div class='insight-box'>
            <strong>🏆 Franchise Dominance & Competitive Moat</strong><br>
            <strong>{top_franchise}</strong> holds the highest historical win rate at <strong>{top_win_pct}%</strong>,
            underpinned by consistent talent acquisition, retention strategy, and strong coaching continuity.
            In a franchise sports context, this represents a durable competitive moat analogous to brand equity
            in consumer markets — achieved through repeatable operational excellence rather than one-season anomalies.
            </div>
            <div class='insight-box'>
            <strong>🎯 Toss Decision as a Strategic Lever</strong><br>
            Teams choosing to <strong>field first</strong> win <strong>{field_win_val}%</strong> of matches vs
            <strong>{bat_win_val}%</strong> for teams batting first. The marginal edge of fielding first (~
            {round(field_win_val - bat_win_val, 1)}pp) is statistically meaningful over a season but not decisive —
            suggesting match outcomes are driven more by execution than pre-match strategy. However, venue-specific
            toss analysis reveals heterogeneous outcomes: high-dew cities like Kolkata and Mumbai amplify the
            fielding advantage during knock-out stages.
            </div>
            <div class='insight-box'>
            <strong>💰 Business Model Insight: Why Ball-by-Ball Data Matters</strong><br>
            For broadcasters, each delivery represents a monetisable moment — a digital content micro-unit.
            With <strong>{total_balls:,} balls</strong> tracked across <strong>{total_matches:,} matches</strong>,
            the IPL generates a granularity of engagement data unmatched by any other cricket format.
            This drives hyper-targeted in-broadcast advertising, predictive fantasy sports algorithms,
            and real-time betting market liquidity — a multi-billion-dollar media rights and ad-tech flywheel.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — FRANCHISE & PLAYER PROFILES
# ════════════════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🏆  Franchise & Player Profiles":

    st.markdown(
        """
        <div class='page-header'>
            <h1>Franchise & Player Profiles</h1>
            <div class='subtitle'>Top Batsmen · Top Wicket-Takers · Franchise Color Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # If "All Teams" selected, default to first team for meaningful analysis
    active_team = selected_team if selected_team != "All Teams" else ALL_TEAMS[0]
    active_color = team_color(active_team)

    # Filter to selected team's batting data + season
    fdf_team = df.copy()
    if selected_season != "All Seasons":
        fdf_team = fdf_team[fdf_team["season"] == selected_season]
    team_batting = fdf_team[fdf_team["batting_team"] == active_team]

    # Franchise KPIs
    franchise_runs    = int(team_batting["runs_total"].sum())
    franchise_wickets = int(
        fdf_team[
            (fdf_team["batting_team"] != active_team) &
            (fdf_team["is_wicket"] == 1)
        ]["is_wicket"].sum()
    )
    franchise_matches = match_df.copy()
    if selected_season != "All Seasons":
        franchise_matches = franchise_matches[franchise_matches["season"] == selected_season]
    fm = franchise_matches[
        (franchise_matches["team1"] == active_team) | (franchise_matches["team2"] == active_team)
    ]
    franchise_wins = len(fm[fm["winner"] == active_team])
    franchise_total_m = len(fm)
    franchise_win_pct = round(franchise_wins / franchise_total_m * 100, 1) if franchise_total_m else 0

    # ── Franchise Identity Header ─────────────────────────────────────────
    st.markdown(
        f"""
        <div class='glass-card' style='
            border-left: 4px solid {active_color};
            margin-bottom: 1.5rem;
        '>
            <div style='font-family: Syne, sans-serif; font-size:1.6rem; font-weight:800;
                        color: {active_color}; letter-spacing:-0.02em;'>{active_team}</div>
            <div style='font-family: DM Sans, sans-serif; font-size:0.85rem; color:#8b949e; margin-top:4px;'>
                Season: <strong style='color:#f0f2f5;'>{selected_season}</strong> &nbsp;·&nbsp;
                Matches: <strong style='color:#f0f2f5;'>{franchise_total_m}</strong> &nbsp;·&nbsp;
                Wins: <strong style='color:#f0f2f5;'>{franchise_wins}</strong> &nbsp;·&nbsp;
                Win Rate: <strong style='color:{active_color};'>{franchise_win_pct}%</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Metric Cards Row ─────────────────────────────────────────────────
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.metric("Total Runs",        f"{franchise_runs:,}")
    with mc2:
        st.metric("Wickets Taken",     f"{franchise_wickets:,}")
    with mc3:
        st.metric("Matches Played",    f"{franchise_total_m}")
    with mc4:
        st.metric("Win Rate",          f"{franchise_win_pct}%")

    st.markdown("<br>", unsafe_allow_html=True)

    col_bat, col_bowl = st.columns(2)

    # ── Top 10 Batsmen ───────────────────────────────────────────────────
    with col_bat:
        top_batters = (
            team_batting.groupby("batter")["runs_batter"]
            .sum()
            .reset_index()
            .rename(columns={"runs_batter": "runs"})
            .sort_values("runs", ascending=False)
            .head(10)
        )
        top_batters = top_batters[top_batters["batter"] != "Unknown"]

        # Color gradient anchored to franchise color
        n = len(top_batters)
        bar_colors = [
            f"rgba({int(active_color[1:3],16)}, {int(active_color[3:5],16)}, {int(active_color[5:7],16)}, {0.45 + 0.55 * i/max(n-1,1):.2f})"
            for i in range(n)
        ]

        fig_bat = go.Figure(go.Bar(
            y=top_batters["batter"],
            x=top_batters["runs"],
            orientation="h",
            marker=dict(color=bar_colors, cornerradius=6),
            text=top_batters["runs"].apply(lambda v: f"{v:,}"),
            textposition="outside",
            textfont=dict(color="#f0f2f5", size=11),
            hovertemplate="<b>%{y}</b><br>Runs: %{x:,}<extra></extra>",
        ))
        apply_glass_layout(fig_bat, f"Top 10 Batsmen — {active_team}", height=400)
        fig_bat.update_layout(yaxis=dict(autorange="reversed"))
        fig_bat.update_xaxes(title_text="Runs Scored")
        st.plotly_chart(fig_bat, use_container_width=True)

    # ── Top 10 Wicket Takers (for this team as bowling side) ─────────────
    with col_bowl:
        bowling_side = fdf_team[
            (fdf_team["batting_team"] != active_team) &
            (fdf_team["is_wicket"] == 1)
        ]
        # Identify matches where active_team was playing
        active_match_ids = set(
            fdf_team[(fdf_team["team1"] == active_team) | (fdf_team["team2"] == active_team)]["match_id"].unique()
        )
        bowling_side = fdf_team[
            (fdf_team["match_id"].isin(active_match_ids)) &
            (fdf_team["batting_team"] != active_team) &
            (fdf_team["is_wicket"] == 1)
        ]
        top_bowlers = (
            bowling_side.groupby("bowler")["is_wicket"]
            .sum()
            .reset_index()
            .rename(columns={"is_wicket": "wickets"})
            .sort_values("wickets", ascending=False)
            .head(10)
        )
        top_bowlers = top_bowlers[top_bowlers["bowler"] != "Unknown"]

        n2 = len(top_bowlers)
        bowl_colors = [
            f"rgba({int(active_color[1:3],16)}, {int(active_color[3:5],16)}, {int(active_color[5:7],16)}, {0.4 + 0.6 * i/max(n2-1,1):.2f})"
            for i in range(n2)
        ]

        fig_bowl = go.Figure(go.Bar(
            y=top_bowlers["bowler"],
            x=top_bowlers["wickets"],
            orientation="h",
            marker=dict(color=bowl_colors, cornerradius=6),
            text=top_bowlers["wickets"],
            textposition="outside",
            textfont=dict(color="#f0f2f5", size=11),
            hovertemplate="<b>%{y}</b><br>Wickets: %{x}<extra></extra>",
        ))
        apply_glass_layout(fig_bowl, f"Top 10 Wicket Takers — {active_team}", height=400)
        fig_bowl.update_layout(yaxis=dict(autorange="reversed"))
        fig_bowl.update_xaxes(title_text="Wickets")
        st.plotly_chart(fig_bowl, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Season-by-Season Performance ─────────────────────────────────────
    st.markdown(
        "<h3 style='margin-bottom:1rem;'>Season-by-Season Performance Trajectory</h3>",
        unsafe_allow_html=True,
    )

    team_season_perf = []
    for ssn, grp in match_df.groupby("season"):
        ssn_team = grp[(grp["team1"] == active_team) | (grp["team2"] == active_team)]
        m_played = len(ssn_team)
        m_won    = len(ssn_team[ssn_team["winner"] == active_team])
        if m_played > 0:
            team_season_perf.append({
                "season":    ssn,
                "matches":   m_played,
                "wins":      m_won,
                "losses":    m_played - m_won,
                "win_rate":  round(m_won / m_played * 100, 1),
            })

    if team_season_perf:
        tsp_df = pd.DataFrame(team_season_perf).sort_values("season")

        fig_perf = make_subplots(specs=[[{"secondary_y": True}]])
        fig_perf.add_trace(go.Bar(
            x=tsp_df["season"],
            y=tsp_df["wins"],
            name="Wins",
            marker=dict(color=active_color, opacity=0.75, cornerradius=5),
            hovertemplate="Season %{x}<br>Wins: %{y}<extra></extra>",
        ), secondary_y=False)
        fig_perf.add_trace(go.Bar(
            x=tsp_df["season"],
            y=tsp_df["losses"],
            name="Losses",
            marker=dict(color="rgba(255,255,255,0.12)", cornerradius=5),
            hovertemplate="Season %{x}<br>Losses: %{y}<extra></extra>",
        ), secondary_y=False)
        fig_perf.add_trace(go.Scatter(
            x=tsp_df["season"],
            y=tsp_df["win_rate"],
            name="Win Rate %",
            mode="lines+markers",
            line=dict(color="#f5b800", width=2.2, shape="spline"),
            marker=dict(color="#f5b800", size=7, line=dict(color="#07090f", width=1.5)),
            hovertemplate="Season %{x}<br>Win Rate: %{y:.1f}%<extra></extra>",
        ), secondary_y=True)
        apply_glass_layout(fig_perf, "", height=320)
        fig_perf.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig_perf.update_yaxes(title_text="Matches",  secondary_y=False,
                               gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8b949e"))
        fig_perf.update_yaxes(title_text="Win Rate %", secondary_y=True,
                               range=[0, 100], ticksuffix="%",
                               tickfont=dict(color="#f5b800"))
        st.plotly_chart(fig_perf, use_container_width=True)
    else:
        st.info("No season-by-season data available for the selected team/season filters.")


# ─────────────────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — PHASE-WISE ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────
elif page == "⚡  Phase-Wise Analytics":

    st.markdown(
        """
        <div class='page-header'>
            <h1>Phase-Wise Analytics</h1>
            <div class='subtitle'>Powerplay · Middle Overs · Death Overs — Batter Strike Rate & Bowler Economy</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fdf_phase = filter_df(selected_season, selected_team)

    tab_pp, tab_mid, tab_death = st.tabs(["🟢  Powerplay (0–5)", "🟡  Middle Overs (6–14)", "🔴  Death Overs (15–19)"])

    def render_phase_tab(phase_name: str, phase_df: pd.DataFrame, accent: str):
        """Render batter SR + bowler economy charts for a given phase."""

        if phase_df.empty:
            st.warning(f"No data found for {phase_name} with the current filters.")
            return

        # ── Batter Strike Rate ────────────────────────────────────────────
        batter_phase = (
            phase_df.groupby("batter")
            .agg(
                runs=("runs_batter", "sum"),
                balls=("is_legal", "sum"),
            )
            .reset_index()
        )
        batter_phase = batter_phase[batter_phase["balls"] >= 30]
        batter_phase["strike_rate"] = (batter_phase["runs"] / batter_phase["balls"] * 100).round(1)
        top_sr = batter_phase.nlargest(5, "strike_rate")[["batter", "runs", "balls", "strike_rate"]]
        top_sr = top_sr[top_sr["batter"] != "Unknown"]

        # ── Bowler Economy Rate ───────────────────────────────────────────
        bowler_phase = (
            phase_df.groupby("bowler")
            .agg(
                runs_conceded=("runs_total", "sum"),
                balls_bowled=("is_legal", "sum"),
                wickets=("is_wicket", "sum"),
            )
            .reset_index()
        )
        bowler_phase = bowler_phase[bowler_phase["balls_bowled"] >= 24]
        bowler_phase["economy"] = (bowler_phase["runs_conceded"] / bowler_phase["balls_bowled"] * 6).round(2)
        top_econ = bowler_phase.nsmallest(5, "economy")[["bowler", "economy", "wickets", "balls_bowled"]]
        top_econ = top_econ[top_econ["bowler"] != "Unknown"]

        col_sr, col_econ = st.columns(2)

        with col_sr:
            if not top_sr.empty:
                sr_colors = [
                    f"rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},{0.4+0.6*i/max(len(top_sr)-1,1):.2f})"
                    for i in range(len(top_sr))
                ]
                fig_sr = go.Figure(go.Bar(
                    x=top_sr["strike_rate"],
                    y=top_sr["batter"],
                    orientation="h",
                    marker=dict(color=sr_colors, cornerradius=6),
                    text=top_sr["strike_rate"].apply(lambda v: f"{v:.1f}"),
                    textposition="outside",
                    textfont=dict(color="#f0f2f5", size=12),
                    customdata=top_sr[["runs", "balls"]].values,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Strike Rate: %{x:.1f}<br>"
                        "Runs: %{customdata[0]}<br>"
                        "Balls: %{customdata[1]}<extra></extra>"
                    ),
                ))
                apply_glass_layout(fig_sr, f"Top 5 Batters by Strike Rate — {phase_name}", height=320)
                fig_sr.update_layout(yaxis=dict(autorange="reversed"))
                fig_sr.update_xaxes(title_text="Strike Rate (min 30 balls)")
                st.plotly_chart(fig_sr, use_container_width=True)
            else:
                st.info(f"Insufficient data for batter strike rate in {phase_name}.")

        with col_econ:
            if not top_econ.empty:
                econ_colors = [
                    f"rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},{0.4+0.6*i/max(len(top_econ)-1,1):.2f})"
                    for i in range(len(top_econ))
                ]
                fig_econ = go.Figure(go.Bar(
                    x=top_econ["economy"],
                    y=top_econ["bowler"],
                    orientation="h",
                    marker=dict(color=econ_colors, cornerradius=6),
                    text=top_econ["economy"].apply(lambda v: f"{v:.2f}"),
                    textposition="outside",
                    textfont=dict(color="#f0f2f5", size=12),
                    customdata=top_econ[["wickets", "balls_bowled"]].values,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Economy: %{x:.2f}<br>"
                        "Wickets: %{customdata[0]}<br>"
                        "Balls: %{customdata[1]}<extra></extra>"
                    ),
                ))
                apply_glass_layout(fig_econ, f"Top 5 Bowlers by Economy — {phase_name}", height=320)
                fig_econ.update_layout(yaxis=dict(autorange="reversed"))
                fig_econ.update_xaxes(title_text="Economy Rate (min 24 balls)")
                st.plotly_chart(fig_econ, use_container_width=True)
            else:
                st.info(f"Insufficient data for bowler economy in {phase_name}.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Phase Run Distribution by Over ───────────────────────────────
        over_runs = (
            phase_df.groupby("over")["runs_total"]
            .mean().round(2).reset_index()
            .rename(columns={"runs_total": "avg_runs_per_over"})
        )
        if not over_runs.empty:
            fig_ov = go.Figure(go.Scatter(
                x=over_runs["over"],
                y=over_runs["avg_runs_per_over"],
                mode="lines+markers",
                fill="tozeroy",
                fillcolor=f"rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},0.08)",
                line=dict(color=accent, width=2.2, shape="spline"),
                marker=dict(color=accent, size=6, line=dict(color="#07090f", width=1.5)),
                hovertemplate="Over %{x}<br>Avg Runs: %{y:.2f}<extra></extra>",
            ))
            apply_glass_layout(fig_ov, f"Average Runs per Over — {phase_name}", height=280)
            fig_ov.update_xaxes(title_text="Over Number", dtick=1)
            fig_ov.update_yaxes(title_text="Avg Runs")
            st.plotly_chart(fig_ov, use_container_width=True)

    # ── Render each phase tab ──────────────────────────────────────────────
    with tab_pp:
        pp_df = fdf_phase[fdf_phase["Match Phase"] == "Powerplay"]
        render_phase_tab("Powerplay (Overs 0–5)", pp_df, "#00d4ff")

    with tab_mid:
        mid_df = fdf_phase[fdf_phase["Match Phase"] == "Middle Overs"]
        render_phase_tab("Middle Overs (6–14)", mid_df, "#f5b800")

    with tab_death:
        death_df = fdf_phase[fdf_phase["Match Phase"] == "Death Overs"]
        render_phase_tab("Death Overs (15–19)", death_df, "#ff3b5c")


# ─────────────────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — STRATEGIC MATCH SIMULATOR
# ════════════════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🎯  Strategic Match Simulator":

    st.markdown(
        """
        <div class='page-header'>
            <h1>Strategic Match Simulator</h1>
            <div class='subtitle'>Head-to-Head Intelligence · Venue Analytics · Toss Recommendation Engine</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    all_venues = sorted(
        df["venue"].dropna().unique().tolist()
    )
    all_venues = [v for v in all_venues if v != "Unknown"]

    # ── Selector Row ─────────────────────────────────────────────────────
    sel_col1, sel_col2, sel_col3 = st.columns(3)
    with sel_col1:
        team_a = st.selectbox("🏏  Team A", ALL_TEAMS, index=0)
    with sel_col2:
        remaining_teams = [t for t in ALL_TEAMS if t != team_a]
        team_b = st.selectbox("🏏  Team B", remaining_teams, index=0)
    with sel_col3:
        selected_venue = st.selectbox("📍  Select Venue", all_venues, index=0)

    if selected_season != "All Seasons":
        sim_match = match_df[match_df["season"] == selected_season].copy()
    else:
        sim_match = match_df.copy()

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # HEAD-TO-HEAD CALCULATIONS
    # ─────────────────────────────────────────────────────────────────────
    h2h = sim_match[
        ((sim_match["team1"] == team_a) & (sim_match["team2"] == team_b)) |
        ((sim_match["team1"] == team_b) & (sim_match["team2"] == team_a))
    ].copy()

    total_h2h    = len(h2h)
    wins_a       = len(h2h[h2h["winner"] == team_a])
    wins_b       = len(h2h[h2h["winner"] == team_b])
    no_result    = total_h2h - wins_a - wins_b
    win_pct_a    = round(wins_a / total_h2h * 100, 1) if total_h2h else 0
    win_pct_b    = round(wins_b / total_h2h * 100, 1) if total_h2h else 0

    # Venue-specific H2H
    venue_h2h    = h2h[h2h["venue"] == selected_venue]
    venue_total  = len(venue_h2h)
    venue_wins_a = len(venue_h2h[venue_h2h["winner"] == team_a])
    venue_wins_b = len(venue_h2h[venue_h2h["winner"] == team_b])
    venue_pct_a  = round(venue_wins_a / venue_total * 100, 1) if venue_total else 0
    venue_pct_b  = round(venue_wins_b / venue_total * 100, 1) if venue_total else 0

    # Overall venue stats (all teams)
    all_venue_matches = sim_match[sim_match["venue"] == selected_venue]
    av_total    = len(all_venue_matches)
    av_wins_bat = len(all_venue_matches[
        (all_venue_matches["toss_decision"] == "bat") &
        (all_venue_matches["toss_winner"] == all_venue_matches["winner"])
    ])
    av_wins_fld = len(all_venue_matches[
        (all_venue_matches["toss_decision"] == "field") &
        (all_venue_matches["toss_winner"] == all_venue_matches["winner"])
    ])
    av_bat_total = len(all_venue_matches[all_venue_matches["toss_decision"] == "bat"])
    av_fld_total = len(all_venue_matches[all_venue_matches["toss_decision"] == "field"])
    venue_bat_win_pct  = round(av_wins_bat / av_bat_total  * 100, 1) if av_bat_total  else 50.0
    venue_fld_win_pct  = round(av_wins_fld / av_fld_total  * 100, 1) if av_fld_total  else 50.0

    # Avg 1st & 2nd innings scores at venue
    venue_balls = df[df["venue"] == selected_venue]
    inn1_scores = (
        venue_balls[venue_balls["innings"] == 1]
        .groupby("match_id")["runs_total"].sum()
    )
    inn2_scores = (
        venue_balls[venue_balls["innings"] == 2]
        .groupby("match_id")["runs_total"].sum()
    )
    avg_inn1 = round(inn1_scores.mean(), 1) if len(inn1_scores) else 0
    avg_inn2 = round(inn2_scores.mean(), 1) if len(inn2_scores) else 0

    # Toss recommendation
    if venue_fld_win_pct > 55:
        toss_rec      = "Bowl First (Field)"
        toss_rec_icon = "🎯"
        toss_rec_color = "#00d4ff"
        toss_reason   = (
            f"Teams winning the toss and choosing to field win <strong>{venue_fld_win_pct}%</strong> "
            f"of matches at <em>{selected_venue}</em> — well above the 55% threshold. "
            f"Chasing teams benefit from pitch knowledge and dew factor."
        )
    elif venue_bat_win_pct > 55:
        toss_rec      = "Bat First"
        toss_rec_icon = "🏏"
        toss_rec_color = "#f5b800"
        toss_reason   = (
            f"Batting first wins <strong>{venue_bat_win_pct}%</strong> of matches at "
            f"<em>{selected_venue}</em>. Setting a target on this surface has proven advantageous — "
            f"likely a slow, low-bounce track where chasing is difficult."
        )
    else:
        toss_rec      = "Toss is a Coin Flip"
        toss_rec_icon = "🪙"
        toss_rec_color = "#a855f7"
        toss_reason   = (
            f"Venue data shows no significant bias at <em>{selected_venue}</em>. "
            f"Batting first wins {venue_bat_win_pct}%, fielding first wins {venue_fld_win_pct}%. "
            f"The toss advantage is negligible — focus on playing conditions on match day."
        )

    # ─────────────────────────────────────────────────────────────────────
    # DISPLAY: H2H Overview Cards
    # ─────────────────────────────────────────────────────────────────────
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.metric("H2H Matches Played", f"{total_h2h}")
    with mc2:
        st.metric(f"{team_a[:18]} Wins", f"{wins_a}",  f"{win_pct_a}% win rate")
    with mc3:
        st.metric(f"{team_b[:18]} Wins", f"{wins_b}",  f"{win_pct_b}% win rate")
    with mc4:
        st.metric("No Result / Tie",     f"{no_result}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # CHARTS ROW
    # ─────────────────────────────────────────────────────────────────────
    col_pie, col_venue, col_innings = st.columns([2, 2, 2])

    # ── H2H Donut ────────────────────────────────────────────────────────
    with col_pie:
        if total_h2h > 0:
            pie_labels  = [team_a, team_b]
            pie_values  = [wins_a, wins_b]
            pie_colors_ = [team_color(team_a), team_color(team_b)]
            if no_result > 0:
                pie_labels.append("No Result")
                pie_values.append(no_result)
                pie_colors_.append("rgba(255,255,255,0.12)")
            fig_pie = go.Figure(go.Pie(
                labels=pie_labels,
                values=pie_values,
                hole=0.6,
                marker=dict(
                    colors=pie_colors_,
                    line=dict(color="rgba(0,0,0,0.3)", width=2),
                ),
                textfont=dict(family="DM Sans, sans-serif", color="#f0f2f5", size=12),
                hovertemplate="<b>%{label}</b><br>Wins: %{value}<br>Share: %{percent}<extra></extra>",
            ))
            fig_pie.update_layout(
                **PLOTLY_TRANSPARENT,
                title=dict(
                    text="Overall H2H Win Share",
                    font=dict(family="Syne, sans-serif", color="#f0f2f5", size=14, weight=700),
                    x=0.02,
                ),
                height=320,
                showlegend=True,
                annotations=[dict(
                    text=f"{total_h2h}<br><span style='font-size:11px'>matches</span>",
                    x=0.5, y=0.5,
                    font=dict(family="Syne, sans-serif", color="#f0f2f5", size=18),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No head-to-head data found for this matchup in the selected season.")

    # ── Venue-specific H2H ───────────────────────────────────────────────
    with col_venue:
        if venue_total > 0:
            fig_venue_bar = go.Figure()
            fig_venue_bar.add_trace(go.Bar(
                x=[team_a, team_b],
                y=[venue_wins_a, venue_wins_b],
                marker=dict(
                    color=[team_color(team_a), team_color(team_b)],
                    cornerradius=8,
                ),
                text=[f"{venue_pct_a}%", f"{venue_pct_b}%"],
                textposition="outside",
                textfont=dict(color="#f0f2f5", size=13, family="Syne"),
                hovertemplate="<b>%{x}</b><br>Venue Wins: %{y}<extra></extra>",
            ))
            apply_glass_layout(fig_venue_bar, f"Venue H2H — {selected_venue[:30]}", height=320)
            fig_venue_bar.update_yaxes(title_text="Wins at Venue")
            st.plotly_chart(fig_venue_bar, use_container_width=True)
        else:
            st.markdown(
                f"""
                <div class='glass-card' style='height:260px;display:flex;align-items:center;
                justify-content:center;flex-direction:column;gap:8px;'>
                    <div style='font-size:2rem;'>📍</div>
                    <div style='font-family:DM Sans;color:#8b949e;font-size:0.9rem;text-align:center;'>
                        No H2H data at<br><strong style='color:#f0f2f5;'>{selected_venue}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Avg Innings Scores at Venue ───────────────────────────────────────
    with col_innings:
        fig_inn = go.Figure()
        fig_inn.add_trace(go.Bar(
            x=["1st Innings", "2nd Innings"],
            y=[avg_inn1, avg_inn2],
            marker=dict(
                color=["rgba(245,184,0,0.7)", "rgba(0,212,255,0.7)"],
                cornerradius=8,
            ),
            text=[f"{avg_inn1:.0f}", f"{avg_inn2:.0f}"],
            textposition="outside",
            textfont=dict(color="#f0f2f5", size=14, family="Syne"),
            hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.1f}<extra></extra>",
        ))
        apply_glass_layout(fig_inn, f"Avg Innings Score — {selected_venue[:30]}", height=320)
        fig_inn.update_yaxes(title_text="Average Runs", range=[0, max(avg_inn1, avg_inn2) * 1.25 + 10])
        st.plotly_chart(fig_inn, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # TOSS RECOMMENDATION ENGINE
    # ─────────────────────────────────────────────────────────────────────
    st.markdown("<h2 style='margin-bottom:1rem;'>🧠  Toss Recommendation Engine</h2>", unsafe_allow_html=True)

    rec_col, detail_col = st.columns([2, 3])

    with rec_col:
        win_prob_a = win_pct_a if total_h2h else 50.0
        win_prob_b = win_pct_b if total_h2h else 50.0
        # Adjust by venue if data exists
        if venue_total > 0:
            weight = min(venue_total / 10, 0.35)
            win_prob_a = round(win_prob_a * (1 - weight) + venue_pct_a * weight, 1)
            win_prob_b = round(100 - win_prob_a, 1)

        st.markdown(
            f"""
            <div class='glass-card' style='
                border-top: 3px solid {toss_rec_color};
                text-align: center;
                padding: 2rem;
            '>
                <div style='font-family:DM Sans;font-size:0.75rem;color:#8b949e;
                text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem;'>
                    Toss Recommendation
                </div>
                <div style='font-size:3rem;margin-bottom:0.5rem;'>{toss_rec_icon}</div>
                <div class='rec-badge' style='
                    background:rgba({int(toss_rec_color[1:3],16)},{int(toss_rec_color[3:5],16)},{int(toss_rec_color[5:7],16)},0.12);
                    border-color:rgba({int(toss_rec_color[1:3],16)},{int(toss_rec_color[3:5],16)},{int(toss_rec_color[5:7],16)},0.35);
                    color:{toss_rec_color};
                    font-size:1rem;
                    padding:10px 28px;
                    display:inline-block;
                    margin-bottom:1.25rem;
                '>{toss_rec}</div>
                <hr style='margin:1rem 0;border-color:rgba(255,255,255,0.07);'>
                <div style='font-family:DM Sans;font-size:0.8rem;color:#8b949e;margin-bottom:0.4rem;'>
                    Batting-first win rate at venue
                </div>
                <div style='font-family:Syne;font-size:1.3rem;font-weight:700;color:#f5b800;'>
                    {venue_bat_win_pct}%
                </div>
                <div style='font-family:DM Sans;font-size:0.8rem;color:#8b949e;margin:0.6rem 0 0.4rem;'>
                    Fielding-first win rate at venue
                </div>
                <div style='font-family:Syne;font-size:1.3rem;font-weight:700;color:#00d4ff;'>
                    {venue_fld_win_pct}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with detail_col:
        st.markdown(
            f"""
            <div class='glass-card'>
                <div style='font-family:Syne;font-size:1rem;font-weight:700;
                color:#f0f2f5;margin-bottom:1rem;'>Win Probability Estimate</div>

                <div style='font-family:DM Sans;font-size:0.85rem;color:#8b949e;
                margin-bottom:4px;'>{team_a}</div>
                <div style='font-family:Syne;font-size:1.5rem;font-weight:700;
                color:{team_color(team_a)};margin-bottom:6px;'>{win_prob_a:.1f}%</div>
                <div class='prob-bar-wrap'>
                    <div class='prob-bar-fill' style='
                        width:{win_prob_a:.1f}%;
                        background:linear-gradient(90deg,{team_color(team_a)},{team_color(team_a)}88);
                    '></div>
                </div>

                <div style='margin-top:1.1rem;font-family:DM Sans;font-size:0.85rem;
                color:#8b949e;margin-bottom:4px;'>{team_b}</div>
                <div style='font-family:Syne;font-size:1.5rem;font-weight:700;
                color:{team_color(team_b)};margin-bottom:6px;'>{win_prob_b:.1f}%</div>
                <div class='prob-bar-wrap'>
                    <div class='prob-bar-fill' style='
                        width:{win_prob_b:.1f}%;
                        background:linear-gradient(90deg,{team_color(team_b)},{team_color(team_b)}88);
                    '></div>
                </div>

                <hr style='margin:1.25rem 0;border-color:rgba(255,255,255,0.07);'>

                <div style='font-family:Syne;font-size:0.95rem;font-weight:600;
                color:#f0f2f5;margin-bottom:0.6rem;'>Strategic Rationale</div>
                <div style='font-family:DM Sans;font-size:0.88rem;color:#8b949e;line-height:1.65;'>
                    {toss_reason}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── H2H Season Trend ─────────────────────────────────────────────────
    if total_h2h > 0:
        st.markdown("<h3 style='margin-bottom:1rem;'>Head-to-Head Win Trend by Season</h3>", unsafe_allow_html=True)
        h2h_season = []
        for ssn, grp in h2h.groupby("season"):
            g_total  = len(grp)
            g_wins_a = len(grp[grp["winner"] == team_a])
            g_wins_b = len(grp[grp["winner"] == team_b])
            if g_total > 0:
                h2h_season.append({
                    "season":   ssn,
                    "wins_a":   g_wins_a,
                    "wins_b":   g_wins_b,
                    "total":    g_total,
                })
        if h2h_season:
            h2h_s_df = pd.DataFrame(h2h_season).sort_values("season")
            fig_h2h = go.Figure()
            fig_h2h.add_trace(go.Bar(
                x=h2h_s_df["season"],
                y=h2h_s_df["wins_a"],
                name=team_a,
                marker=dict(color=team_color(team_a), cornerradius=5, opacity=0.85),
                hovertemplate=f"<b>{team_a}</b><br>Season %{{x}}<br>Wins: %{{y}}<extra></extra>",
            ))
            fig_h2h.add_trace(go.Bar(
                x=h2h_s_df["season"],
                y=h2h_s_df["wins_b"],
                name=team_b,
                marker=dict(color=team_color(team_b), cornerradius=5, opacity=0.85),
                hovertemplate=f"<b>{team_b}</b><br>Season %{{x}}<br>Wins: %{{y}}<extra></extra>",
            ))
            apply_glass_layout(fig_h2h, f"{team_a} vs {team_b} — Season-by-Season H2H", height=300)
            fig_h2h.update_layout(barmode="group")
            fig_h2h.update_xaxes(tickangle=-35)
            fig_h2h.update_yaxes(title_text="Wins", dtick=1)
            st.plotly_chart(fig_h2h, use_container_width=True)

    # ── Venue Toss Decision Breakdown ────────────────────────────────────
    if av_total > 0:
        st.markdown("<h3 style='margin-bottom:1rem;'>Venue Toss Decision Breakdown</h3>", unsafe_allow_html=True)
        toss_breakdown_df = (
            all_venue_matches[all_venue_matches["toss_decision"].isin(["bat", "field"])]
            .groupby("toss_decision")
            .agg(
                total_matches=("match_id", "count"),
                toss_winner_won=(
                    "winner",
                    lambda x: (x == all_venue_matches.loc[x.index, "toss_winner"]).sum()
                ),
            )
            .reset_index()
        )
        toss_breakdown_df["win_pct"] = (
            toss_breakdown_df["toss_winner_won"] / toss_breakdown_df["total_matches"] * 100
        ).round(1)

        fig_td = go.Figure()
        fig_td.add_trace(go.Bar(
            x=toss_breakdown_df["toss_decision"].str.title(),
            y=toss_breakdown_df["total_matches"],
            name="Times Chosen",
            marker=dict(color="rgba(255,255,255,0.1)", cornerradius=8),
            hovertemplate="<b>%{x}</b><br>Times chosen: %{y}<extra></extra>",
        ))
        fig_td.add_trace(go.Bar(
            x=toss_breakdown_df["toss_decision"].str.title(),
            y=toss_breakdown_df["toss_winner_won"],
            name="Toss Winner Also Won Match",
            marker=dict(color=["#f5b800", "#00d4ff"], cornerradius=8),
            text=toss_breakdown_df["win_pct"].apply(lambda v: f"{v}%"),
            textposition="outside",
            textfont=dict(color="#f0f2f5", size=13, family="Syne"),
            hovertemplate="<b>%{x}</b><br>Toss + Match wins: %{y}<br>Rate: %{text}<extra></extra>",
        ))
        apply_glass_layout(fig_td, f"Toss Decision Analysis at {selected_venue[:40]}", height=320)
        fig_td.update_layout(barmode="group")
        fig_td.update_yaxes(title_text="Number of Matches")
        st.plotly_chart(fig_td, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([5, 1, 5])

with col2:
    st.image("assets/logoipl.jpg", width=60)

st.markdown(
    """
    <div style='
        text-align:center;
        font-family:DM Sans, sans-serif;
        font-size:0.76rem;
        color:#484f58;
        padding-top:2px;
        padding-bottom:1rem;
        letter-spacing:0.04em;
        line-height:1.6;
    '>
        IPL Analytics Dashboard · Glass Edition <br>
        Built with Streamlit + Plotly · Ball-by-Ball Intelligence Engine <br>
        Developed by Subhadip Kumar
    </div>
    """,
    unsafe_allow_html=True,
)

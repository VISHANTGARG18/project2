"""
Custom Theme, Glassmorphism Styling, and Full Light/Dark Mode CSS for Lumina Platform.
"""

import streamlit as st

def apply_custom_css(theme_mode: str = "Dark Mode 🌙"):
    """Injects comprehensive Light/Dark executive custom CSS styles into Streamlit app."""
    is_light = "Light" in theme_mode

    # Set Plotly template in session state
    st.session_state['plotly_template'] = "plotly_white" if is_light else "plotly_dark"

    if is_light:
        bg_main = "#F8FAFC"
        bg_sidebar = "#F1F5F9"
        card_bg = "#FFFFFF"
        card_border = "rgba(0, 0, 0, 0.08)"
        card_shadow = "0 4px 20px 0 rgba(0, 0, 0, 0.05)"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        status_bg = "#E2E8F0"
        status_border = "rgba(0, 0, 0, 0.1)"
        tab_active = "#311B92"
    else:
        bg_main = "#0F172A"
        bg_sidebar = "#0B0F19"
        card_bg = "rgba(30, 41, 59, 0.75)"
        card_border = "rgba(255, 255, 255, 0.12)"
        card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.25)"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        status_bg = "rgba(15, 23, 42, 0.8)"
        status_border = "rgba(255, 255, 255, 0.08)"
        tab_active = "#FFB300"

    css = f"""
    <style>
        /* Global Page Background & Text Overrides */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
        }}

        /* Headings & Text Color */
        h1, h2, h3, h4, h5, h6, .stMarkdown p {{
            color: {text_primary} !important;
        }}

        /* Tabs Styling */
        .stTabs [data-baseweb="tab"] {{
            color: {text_secondary} !important;
            font-weight: 600;
        }}

        .stTabs [aria-selected="true"] {{
            color: {tab_active} !important;
            border-bottom-color: {tab_active} !important;
        }}

        /* Glassmorphism Metric Cards */
        .glass-card {{
            background: {card_bg};
            border-radius: 12px;
            padding: 20px;
            border: 1px solid {card_border};
            box-shadow: {card_shadow};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 15px;
        }}

        .glass-card:hover {{
            transform: translateY(-2px);
        }}

        .kpi-title {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {text_secondary};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {text_primary};
            margin: 5px 0;
        }}

        .kpi-delta-positive {{
            font-size: 0.9rem;
            font-weight: 600;
            color: #10B981;
        }}

        .kpi-delta-negative {{
            font-size: 0.9rem;
            font-weight: 600;
            color: #EF4444;
        }}

        /* Executive Alert Banner */
        .alert-banner-danger {{
            background: rgba(239, 68, 68, 0.12);
            border-left: 4px solid #EF4444;
            padding: 12px 18px;
            border-radius: 6px;
            color: {text_primary};
            margin-bottom: 12px;
            font-weight: 500;
        }}

        .alert-banner-warning {{
            background: rgba(245, 158, 11, 0.12);
            border-left: 4px solid #F59E0B;
            padding: 12px 18px;
            border-radius: 6px;
            color: {text_primary};
            margin-bottom: 12px;
            font-weight: 500;
        }}

        .alert-banner-success {{
            background: rgba(16, 185, 129, 0.12);
            border-left: 4px solid #10B981;
            padding: 12px 18px;
            border-radius: 6px;
            color: {text_primary};
            margin-bottom: 12px;
            font-weight: 500;
        }}

        /* System Status Panel */
        .status-panel {{
            background: {status_bg};
            border: 1px solid {status_border};
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 0.85rem;
            color: {text_secondary};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

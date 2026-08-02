"""
Groww / Stripe Premium Aesthetic Theme & Dynamic CSS & Plotly Theme Helper for Lumina Platform.
"""

import streamlit as st

def get_plotly_theme_dict(theme_mode: str = "Dark Mode 🌙"):
    """Returns exact Plotly layout configuration matching Light or Dark mode."""
    is_light = "Light" in theme_mode
    template = "plotly_white" if is_light else "plotly_dark"
    font_color = "#0F172A" if is_light else "#F8FAFC"
    sub_color = "#475569" if is_light else "#94A3B8"
    grid_color = "#E2E8F0" if is_light else "rgba(255, 255, 255, 0.08)"

    return {
        "template": template,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": dict(color=font_color, family="Inter, sans-serif"),
        "xaxis": dict(gridcolor=grid_color, tickfont=dict(color=sub_color), title_font=dict(color=font_color)),
        "yaxis": dict(gridcolor=grid_color, tickfont=dict(color=sub_color), title_font=dict(color=font_color))
    }

def apply_custom_css(theme_mode: str = "Dark Mode 🌙"):
    """Injects high-end Groww / Stripe inspired CSS aesthetics into Streamlit app."""
    is_light = "Light" in theme_mode

    st.session_state['theme_mode'] = theme_mode
    st.session_state['plotly_template'] = "plotly_white" if is_light else "plotly_dark"

    if is_light:
        bg_main = "#F4F7FA"
        bg_sidebar = "#FFFFFF"
        card_bg = "linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)"
        card_border = "1px solid rgba(0, 208, 156, 0.2)"
        card_shadow = "0 10px 30px -5px rgba(0, 208, 156, 0.08), 0 4px 12px -2px rgba(0, 0, 0, 0.04)"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        status_bg = "#FFFFFF"
        status_border = "1px solid rgba(0, 208, 156, 0.25)"
        accent_color = "#00D09C"
        sidebar_text = "#0F172A"
        input_bg = "#FFFFFF"
        input_border = "#CBD5E1"
    else:
        bg_main = "#0B0F17"
        bg_sidebar = "#111622"
        card_bg = "linear-gradient(135deg, rgba(18, 24, 38, 0.85) 0%, rgba(15, 20, 32, 0.85) 100%)"
        card_border = "1px solid rgba(0, 208, 156, 0.15)"
        card_shadow = "0 12px 35px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.05)"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        status_bg = "rgba(18, 24, 38, 0.9)"
        status_border = "1px solid rgba(0, 208, 156, 0.2)"
        accent_color = "#00D09C"
        sidebar_text = "#F8FAFC"
        input_bg = "#1A202C"
        input_border = "rgba(255, 255, 255, 0.15)"

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

        /* Global Font & Background Overrides */
        html, body, [class*="css"], .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
            background-image: radial-gradient(circle at 50% 0%, rgba(0, 208, 156, 0.04), transparent 60%);
        }}

        [data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            border-right: 1px solid rgba(0, 208, 156, 0.15) !important;
        }}

        /* Sidebar Text & Label Overrides */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {sidebar_text} !important;
        }}

        /* Streamlit Input Controls Override */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div, 
        .stDateInput input, 
        .stTextInput input {{
            background-color: {input_bg} !important;
            color: {text_primary} !important;
            border: 1px solid {input_border} !important;
            border-radius: 8px !important;
        }}

        div[data-baseweb="select"] span, 
        div[data-baseweb="select"] div,
        div[data-baseweb="popover"] div {{
            color: {text_primary} !important;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            color: {text_primary} !important;
            letter-spacing: -0.02em !important;
        }}

        /* Groww Premium Metric Card */
        .groww-card {{
            background: {card_bg};
            border-radius: 16px;
            padding: 22px 20px;
            border: {card_border};
            box-shadow: {card_shadow};
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
        }}

        .groww-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(0, 208, 156, 0.4);
            box-shadow: 0 20px 40px -10px rgba(0, 208, 156, 0.15);
        }}

        .groww-title {{
            font-size: 0.78rem;
            font-weight: 700;
            color: {text_secondary};
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
        }}

        .groww-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.95rem;
            font-weight: 800;
            color: {text_primary};
            letter-spacing: -0.03em;
            margin: 4px 0 8px 0;
        }}

        .groww-badge-pos {{
            display: inline-flex;
            align-items: center;
            background: rgba(0, 208, 156, 0.12);
            color: #00D09C;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            border: 1px solid rgba(0, 208, 156, 0.25);
        }}

        .groww-badge-neg {{
            display: inline-flex;
            align-items: center;
            background: rgba(239, 68, 68, 0.12);
            color: #FF5252;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            border: 1px solid rgba(239, 68, 68, 0.25);
        }}

        /* System Status Panel */
        .status-panel {{
            background: {status_bg};
            border: {status_border};
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 0.85rem;
            color: {text_secondary};
            box-shadow: {card_shadow};
        }}

        /* Tab Buttons Styling */
        .stTabs [data-baseweb="tab"] {{
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: {text_secondary} !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
        }}

        .stTabs [aria-selected="true"] {{
            color: {accent_color} !important;
            background: rgba(0, 208, 156, 0.08) !important;
            border-bottom: 3px solid {accent_color} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

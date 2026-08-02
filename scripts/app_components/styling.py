"""
Custom Theme, Glassmorphism Styling, and Dynamic Light/Dark Mode CSS for Lumina Platform.
"""

import streamlit as st

def apply_custom_css(theme_mode: str = "Dark Mode 🌙"):
    """Injects dynamic Light/Dark executive custom CSS styles into Streamlit app."""
    is_light = "Light" in theme_mode

    # Set Plotly template in session state
    st.session_state['plotly_template'] = "plotly_white" if is_light else "plotly_dark"

    if is_light:
        card_bg = "rgba(255, 255, 255, 0.88)"
        card_border = "rgba(0, 0, 0, 0.12)"
        card_shadow = "0 8px 30px 0 rgba(0, 0, 0, 0.08)"
        kpi_title_color = "#475569"
        kpi_val_color = "#0F172A"
        text_color = "#1E293B"
        status_bg = "rgba(241, 245, 249, 0.9)"
        status_border = "rgba(0, 0, 0, 0.1)"
    else:
        card_bg = "rgba(30, 41, 59, 0.75)"
        card_border = "rgba(255, 255, 255, 0.12)"
        card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.25)"
        kpi_title_color = "#94A3B8"
        kpi_val_color = "#F8FAFC"
        text_color = "#E2E8F0"
        status_bg = "rgba(15, 23, 42, 0.8)"
        status_border = "rgba(255, 255, 255, 0.08)"

    css = f"""
    <style>
        /* Glassmorphism Metric Cards */
        .glass-card {{
            background: {card_bg};
            backdrop-filter: blur(10px);
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
            color: {kpi_title_color};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {kpi_val_color};
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
            background: rgba(239, 68, 68, 0.15);
            border-left: 4px solid #EF4444;
            padding: 12px 18px;
            border-radius: 6px;
            color: {text_color};
            margin-bottom: 12px;
            font-weight: 500;
        }}

        .alert-banner-warning {{
            background: rgba(245, 158, 11, 0.15);
            border-left: 4px solid #F59E0B;
            padding: 12px 18px;
            border-radius: 6px;
            color: {text_color};
            margin-bottom: 12px;
            font-weight: 500;
        }}

        .alert-banner-success {{
            background: rgba(16, 185, 129, 0.15);
            border-left: 4px solid #10B981;
            padding: 12px 18px;
            border-radius: 6px;
            color: {text_color};
            margin-bottom: 12px;
            font-weight: 500;
        }}

        /* System Status Panel */
        .status-panel {{
            background: {status_bg};
            border: 1px solid {status_border};
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 0.8rem;
            color: {kpi_title_color};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

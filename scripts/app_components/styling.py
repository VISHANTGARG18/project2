"""
Custom Theme, Glassmorphism Styling, and CSS Injection for Lumina Platform.
"""

import streamlit as st

def apply_custom_css():
    """Injects executive custom CSS styles into Streamlit app."""
    css = """
    <style>
        /* Modern Typography & Root Colors */
        :root {
            --primary-indigo: #311B92;
            --accent-teal: #00897B;
            --warm-gold: #FFB300;
            --slate-gray: #455A64;
            --card-bg-dark: rgba(30, 41, 59, 0.7);
            --card-border-dark: rgba(255, 255, 255, 0.1);
        }

        /* Glassmorphism Metric Cards */
        .glass-card {
            background: rgba(30, 41, 59, 0.75);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 15px;
        }

        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.35);
        }

        .kpi-title {
            font-size: 0.85rem;
            font-weight: 600;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #F8FAFC;
            margin: 5px 0;
        }

        .kpi-delta-positive {
            font-size: 0.9rem;
            font-weight: 600;
            color: #10B981;
        }

        .kpi-delta-negative {
            font-size: 0.9rem;
            font-weight: 600;
            color: #EF4444;
        }

        /* Executive Alert Banner */
        .alert-banner-danger {
            background: rgba(239, 68, 68, 0.15);
            border-left: 4px solid #EF4444;
            padding: 12px 18px;
            border-radius: 6px;
            color: #FCA5A5;
            margin-bottom: 12px;
            font-weight: 500;
        }

        .alert-banner-warning {
            background: rgba(245, 158, 11, 0.15);
            border-left: 4px solid #F59E0B;
            padding: 12px 18px;
            border-radius: 6px;
            color: #FDE68A;
            margin-bottom: 12px;
            font-weight: 500;
        }

        .alert-banner-success {
            background: rgba(16, 185, 129, 0.15);
            border-left: 4px solid #10B981;
            padding: 12px 18px;
            border-radius: 6px;
            color: #6EE7B7;
            margin-bottom: 12px;
            font-weight: 500;
        }

        /* System Status Panel */
        .status-panel {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 0.8rem;
            color: #64748B;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

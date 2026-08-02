#!/usr/bin/env python3
"""
PDF Generator Script for Lumina Analytics Platform Interview Prep Guide.
Generates docs/Lumina_Retail_Analytics_Interview_Prep_Guide.pdf using ReportLab.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def create_interview_prep_pdf():
    pdf_path = os.path.join("docs", "Lumina_Retail_Analytics_Interview_Prep_Guide.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#00897B")     # Deep Teal / Emerald
    SECONDARY = colors.HexColor("#311B92")   # Deep Indigo
    DARK_TEXT = colors.HexColor("#0F172A")   # Dark Slate
    MUTED_TEXT = colors.HexColor("#475569")  # Muted Slate
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Card Light Background
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Custom Typography Styles
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=6
    )

    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=MUTED_TEXT,
        spaceAfter=15
    )

    style_h1 = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=SECONDARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    style_code = ParagraphStyle(
        'CodeCustom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=6
    )

    story = []

    # Title Banner
    story.append(Paragraph("💎 Lumina Executive Analytics Platform", style_title))
    story.append(Paragraph("Comprehensive Technical Architecture, SQL Analytics, & Interview Preparation Guide", style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    # Section 1: Executive Framing
    story.append(Paragraph("1. Executive Business Framing & Problem Statement", style_h1))
    story.append(Paragraph(
        "<b>Business Context:</b> Leadership at Lumina Lifestyle & Living (an omnichannel retailer selling Premium Home Goods, Smart Electronics, and Outdoor Living across North America, Europe, and Asia Pacific) needs visibility into why net profit margins vary significantly across geographical regions and fulfillment channels (Online E-Commerce vs. Retail Flagship Stores). Management requires clear data to identify which products and customer cohorts drive true bottom-line profitability, where promotional discounting is eroding profit margins, and how to optimize customer acquisition and retention budgets.",
        style_body
    ))

    # Section 2: Technical Architecture
    story.append(Paragraph("2. High-Level Technical Architecture", style_h1))
    arch_data = [
        ["Component", "Technology / Pattern", "Key Responsibilities"],
        ["Relational Database", "SQLite3 (ANSI SQL)", "Stores 16,832 order items, PK/FK constraints, CHECK validations"],
        ["Data View", "vw_sales_analytics", "Single source of truth pre-computing Revenue, Discounts, COGS, Profit, Margins"],
        ["Advanced SQL Suite", "SQL Window Functions & CTEs", "MoM/YoY growth (LAG), Category rankings (DENSE_RANK), 5-Stage RFM"],
        ["Web Platform", "Streamlit & Plotly Express", "Obsidian Dark UI, 9 global filters, 6 specialized analytics tabs"],
        ["Security Validator", "Python Regex Engine", "SELECT-only query validator blocking DROP, DELETE, ALTER, TRUNCATE"]
    ]
    t_arch = Table(arch_data, colWidths=[110, 150, 280])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (-1,-1), DARK_TEXT),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # Section 3: Data Modeling & Schema
    story.append(Paragraph("3. Relational Schema & Single-Source-of-Truth View", style_h1))
    story.append(Paragraph(
        "The project consists of 5 normalized relational tables (<b>STORES, PRODUCTS, CUSTOMERS, ORDERS, ORDER_ITEMS</b>). Schema constraints enforce <code>ON DELETE RESTRICT</code> on foreign keys and strict <code>CHECK</code> validations (e.g. <code>discount_percent BETWEEN 0.0 AND 0.50</code>). Stores include updated <code>country</code> (USA, Canada, UK, Germany, Japan) and <code>state</code> columns.",
        style_body
    ))
    story.append(Paragraph("Single-Source-of-Truth View Calculations (vw_sales_analytics):", style_h2))
    story.append(Paragraph("• <b>Gross Revenue:</b> quantity * unit_price", style_body))
    story.append(Paragraph("• <b>Discount Amount:</b> quantity * unit_price * discount_percent", style_body))
    story.append(Paragraph("• <b>Net Revenue:</b> gross_revenue - discount_amount", style_body))
    story.append(Paragraph("• <b>Net Profit:</b> net_revenue - total_cogs - allocated_shipping_cost", style_body))
    story.append(Paragraph("• <b>Profit Margin %:</b> (net_profit / net_revenue) * 100.0", style_body))

    story.append(Spacer(1, 10))

    # Section 4: Advanced SQL Suite
    story.append(Paragraph("4. Advanced SQL Analytics Suite", style_h1))
    
    sql_summary = [
        ["SQL Script", "Core Functionality", "Key SQL Techniques Used"],
        ["01_monthly_trends_mom_yoy.sql", "MoM & YoY Growth Trends", "LAG(net_revenue, 1) OVER (ORDER BY order_year_month)"],
        ["02_product_performance_rankings.sql", "Product Category Rankings", "DENSE_RANK(), RANK(), ROW_NUMBER() PARTITION BY category"],
        ["03_cohort_retention_analysis.sql", "24-Month Cohort Retention", "Pivot matrix tracking active buyers by signup cohort month"],
        ["04_rfm_segmentation.sql", "5-Stage Customer RFM", "5-level CTE chain with NTILE(5) scoring Recency/Freq/Monetary"],
        ["05_regional_channel_margins.sql", "Channel Margin Comparison", "Grouped margin aggregation comparing Online vs Retail Stores"],
        ["06_moving_averages_running_totals.sql", "Moving Averages & YTD", "SUM() OVER (ORDER BY order_date ROWS BETWEEN 29 PRECEDING)"]
    ]
    t_sql = Table(sql_summary, colWidths=[140, 160, 240])
    t_sql.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (-1,-1), DARK_TEXT),
    ]))
    story.append(t_sql)

    story.append(Spacer(1, 12))

    # Section 5: Web Platform Tabs & Groww Design System
    story.append(Paragraph("5. Streamlit Web Platform & Groww Aesthetics", style_h1))
    story.append(Paragraph(
        "The application is built under <code>scripts/app.py</code> with 11 modular components under <code>scripts/app_components/</code> and 9 backend utility engines under <code>scripts/utils/</code>. It is styled with an Obsidian Midnight Dark theme (<code>#0B0F17</code>) and Groww Electric Emerald (<code>#00D09C</code>) accents.",
        style_body
    ))

    tab_data = [
        ["Platform Tab", "Interactive Features & Capabilities"],
        ["🏠 Executive Overview", "8 Groww KPI cards, prior-period Deltas, Alert banners, 5 AI Insights, Plotly smooth splines"],
        ["📦 Product Intelligence", "Searchable catalog, ABC classification, Pareto 80/20 chart, Real-Time Discount Scenario Simulator"],
        ["👥 Customer Analytics", "Customer 360 Individual Lookup (lifetime spend, loyalty score 1-100, timeline), Cohort Heatmap"],
        ["🛒 Market Basket Explorer", "Support/Confidence/Lift sliders, automated Product Bundle Cross-Sell Recommender"],
        ["📈 Forecasting Studio", "YoY growth, confidence bounds, inflation sliders driving Optimistic, Base, Pessimistic curves"],
        ["🧠 SQL Analytics Lab", "Interactive editor, SELECT-only security engine, CSV/Excel/Markdown/HTML report exporters"]
    ]
    t_tab = Table(tab_data, colWidths=[130, 410])
    t_tab.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BACKGROUND', (0,1), (-1,-1), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (-1,-1), DARK_TEXT),
    ]))
    story.append(t_tab)

    story.append(Spacer(1, 12))

    # Section 6: Key Findings
    story.append(Paragraph("6. Key Business Findings to Memorize for Interviews", style_h1))
    story.append(Paragraph("• <b>Online Channel Margin Erosion (3.96% Drag):</b> Online E-Commerce achieved a 56.53% net margin vs 60.49%–60.88% in flagship stores, driven by 8.62% avg discounts and absorbed shipping costs ($85K annual profit erosion).", style_body))
    story.append(Paragraph("• <b>RFM Champions Concentration (61.3% Profit):</b> 28.98% of customers (364 Champions) contribute $1.77M in net profit with an average spend of $8,178.02.", style_body))
    story.append(Paragraph("• <b>Q4 Seasonal Revenue Surge:</b> November and December generate 35.8% of annual net profit, surging 85.3% MoM in November due to holiday electronics and gifts.", style_body))
    story.append(Paragraph("• <b>Outdoor Living Profit Efficiency:</b> Outdoor Living leads category profitability at a 61.19% net margin.", style_body))

    story.append(Spacer(1, 12))

    # Section 7: Behavioral Q&A
    story.append(Paragraph("7. STAR Method Interview Q&A", style_h1))
    story.append(Paragraph("<b>Q1: Can you walk me through an end-to-end analytics project you built from scratch?</b>", style_h2))
    story.append(Paragraph("<b>Situation:</b> Omnichannel retailers often struggle to understand why net profit margins vary between online e-commerce and flagship store locations.<br/><b>Task:</b> I designed and built an end-to-end executive analytics platform for Lumina Lifestyle & Living querying 16,832 transaction line items over 2024–2025.<br/><b>Action:</b> I engineered a normalized SQLite database schema, created a single-source-of-truth analytical view (<code>vw_sales_analytics</code>), authored an advanced SQL suite using window functions (<code>LAG</code>, <code>DENSE_RANK</code>) and a 5-stage CTE RFM customer segmentation model, and built a flagship Streamlit web application with 6 specialized tabs and a SELECT-only SQL sandbox.<br/><b>Result:</b> Uncovered that online discounting eroded $85K in profit margin and identified that 28.98% of customers ('Champions') drive 61.3% of total net profit.", style_body))

    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Q2: How did you enforce security in your interactive SQL Sandbox?</b>", style_h2))
    story.append(Paragraph("I built a custom Python security validator engine (<code>sql_runner.py</code>) using upper-case regex word-boundary matching (<code>r'\\b' + kw + r'\\b'</code>) to strictly enforce SELECT-only query execution, blocking any DDL or DML mutation commands (<code>DROP, DELETE, UPDATE, ALTER, TRUNCATE, INSERT, REPLACE</code>).", style_body))

    doc.build(story)
    print(f"Successfully generated PDF: {pdf_path}")

if __name__ == "__main__":
    create_interview_prep_pdf()

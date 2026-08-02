"""
Multi-Format Report Export Utility for Lumina Analytics Platform.
"""

import io
import pandas as pd
from datetime import datetime

def export_df_to_csv(df: pd.DataFrame) -> bytes:
    """Converts a DataFrame to UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode('utf-8')

def export_df_to_excel(df: pd.DataFrame) -> bytes:
    """Converts a DataFrame to Excel binary bytes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Lumina Export')
    return output.getvalue()

def generate_markdown_report(kpis: dict, top_products: pd.DataFrame, insights: list) -> str:
    """Generates an executive summary markdown report."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"""# Lumina Lifestyle & Living - Executive Performance Report

**Generated**: {now_str}

---

## 1. Key Performance Indicators (KPIs)

- **Total Net Revenue**: ${kpis.get('net_revenue', 0):,.2f}
- **Total Net Profit**: ${kpis.get('net_profit', 0):,.2f}
- **Net Profit Margin %**: {kpis.get('margin_pct', 0):.2f}%
- **Completed Orders**: {kpis.get('total_orders', 0):,}
- **Average Order Value**: ${kpis.get('aov', 0):,.2f}
- **Repeat Buyer Rate**: {kpis.get('repeat_rate_pct', 0):.2f}%

---

## 2. Top Performing Products

| Category | Product Name | Net Revenue | Net Profit | Margin % |
| :--- | :--- | :--- | :--- | :--- |
"""

    if not top_products.empty:
        for r in top_products.head(5).itertuples():
            md += f"| {getattr(r, 'category', 'N/A')} | {getattr(r, 'product_name', 'N/A')} | ${getattr(r, 'net_revenue', 0):,.2f} | ${getattr(r, 'net_profit', 0):,.2f} | {getattr(r, 'net_profit_margin_pct', 0):.2f}% |\n"

    md += "\n---\n\n## 3. Executive Insights & Directives\n\n"
    for idx, ins in enumerate(insights, 1):
        md += f"{idx}. {ins}\n"

    return md

def generate_html_report(kpis: dict, top_products: pd.DataFrame, insights: list) -> str:
    """Generates an executive summary HTML document."""
    md_content = generate_markdown_report(kpis, top_products, insights)
    # Simple clean HTML wrap
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Lumina Executive Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; padding: 30px; background: #0F172A; color: #F8FAFC; }}
        h1 {{ color: #FFB300; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        h2 {{ color: #38BDF8; margin-top: 30px; }}
        ul {{ line-height: 1.6; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 15px; background: #1E293B; }}
        th, td {{ border: 1px solid #334155; padding: 12px; text-align: left; }}
        th {{ background: #311B92; color: white; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap; font-family: inherit;">{md_content}</pre>
</body>
</html>"""
    return html

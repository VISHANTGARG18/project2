"""
Formatting and utility helper functions for Lumina Executive Analytics Platform.
"""

def fmt_currency(val: float) -> str:
    """Format float as currency string ($#,##0.00)."""
    if val is None or val != val:
        return "$0.00"
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:,.2f}M"
    if abs(val) >= 1_000:
        return f"${val / 1_000:,.2f}K"
    return f"${val:,.2f}"

def fmt_currency_exact(val: float) -> str:
    """Format float as exact dollar amount ($#,##0.00)."""
    if val is None or val != val:
        return "$0.00"
    return f"${val:,.2f}"

def fmt_percent(val: float) -> str:
    """Format float as percentage string (0.00%)."""
    if val is None or val != val:
        return "0.00%"
    return f"{val:.2f}%"

def fmt_number(val: int) -> str:
    """Format integer with thousands separator (#,##0)."""
    if val is None or val != val:
        return "0"
    return f"{int(val):,}"

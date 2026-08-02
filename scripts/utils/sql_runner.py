"""
Secure SQL Query Validator & Execution Utility for Lumina Analytics Lab.
Permits SELECT operations and blocks dangerous DDL/DML statements.
"""

import time
import re
import pandas as pd
from .database import execute_query

DANGEROUS_KEYWORDS = ["DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE", "INSERT", "REPLACE", "CREATE", "ATTACH", "DETACH"]

def validate_and_run_sql(query: str):
    """
    Validates that the SQL query is a safe SELECT statement, executes it,
    and measures query duration and row count.
    """
    cleaned_query = query.strip()
    
    if not cleaned_query:
        return None, "Empty query provided.", 0.0, 0

    # Check for forbidden keywords
    upper_query = cleaned_query.upper()
    for kw in DANGEROUS_KEYWORDS:
        # Match whole word keyword
        if re.search(r'\b' + kw + r'\b', upper_query):
            return None, f"Security Violation: '{kw}' statement is strictly prohibited. Only SELECT queries are permitted.", 0.0, 0

    # Ensure query starts with SELECT or WITH
    if not (upper_query.startswith("SELECT") or upper_query.startswith("WITH")):
        return None, "Security Violation: Query must begin with SELECT or WITH.", 0.0, 0

    start_time = time.time()
    try:
        df = execute_query(cleaned_query)
        duration = time.time() - start_time
        return df, None, duration, len(df)
    except Exception as e:
        duration = time.time() - start_time
        return None, f"Database Error: {str(e)}", duration, 0

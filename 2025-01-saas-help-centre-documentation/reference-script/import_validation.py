# ============================================================
# File: import_validation.py
# Purpose: Validate imported trading data before it is accepted
# Context: Help Centre reference (non-production example)
# ============================================================

import csv
from typing import List, Dict


REQUIRED_HEADERS = [
    "trade_id",
    "instrument",
    "entry_price",
    "exit_price",
    "direction",
    "timestamp"
]


class ImportValidationError(Exception):
    """Raised when imported trading data fails validation."""
    pass


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and returns a list of rows as dictionaries.
    """
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def validate_headers(headers: List[str]) -> None:
    """
    Ensures all required headers are present.
    """
    missing = [h for h in REQUIRED_HEADERS if h not in headers]
    if missing:
        raise ImportValidationError(
            f"Missing required columns: {', '.join(missing)}"
        )


def validate_row(row: Dict[str, str], row_number: int) -> None:
    """
    Validates a single row of imported trade data.
    """
    if not row.get("trade_id"):
        raise ImportValidationError(f"Row {row_number}: trade_id is empty")

    if row.get("direction") not in ["buy", "sell"]:
        raise ImportValidationError(
            f"Row {row_number}: direction must be 'buy' or 'sell'"
        )

    try:
        float(row.get("entry_price", ""))
        float(row.get("exit_price", ""))
    except ValueError:
        raise ImportValidationError(
            f"Row {row_number}: entry_price or exit_price is not numeric"
        )


def validate_import(file_path: str) -> List[Dict[str, str]]:
    """
    Full validation workflow for imported CSV data.
    """
    rows = read_csv(file_path)

    if not rows:
        raise ImportValidationError("Import file is empty")

    validate_headers(list(rows[0].keys()))

    for index, row in enumerate(rows, start=1):
        validate_row(row, index)

    return rows


# ============================================================
# File: export_cleanup.py
# Purpose: Prepare exported trading data for external use
# ============================================================

def remove_empty_rows(rows: List[List[str]]) -> List[List[str]]:
    """
    Removes fully empty rows from exported data.
    """
    return [row for row in rows if any(cell.strip() for cell in row)]


def normalize_numeric_fields(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Normalizes numeric fields as strings with consistent formatting.
    """
    normalized = []

    for row in rows:
        row_copy = dict(row)
        row_copy["entry_price"] = f"{float(row['entry_price']):.2f}"
        row_copy["exit_price"] = f"{float(row['exit_price']):.2f}"
        normalized.append(row_copy)

    return normalized


def prepare_export(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Complete export preparation workflow.
    """
    rows = normalize_numeric_fields(rows)
    return rows


# ============================================================
# File: insight_calculation_example.py
# Purpose: Demonstrate how basic behavioural insights are derived
# ============================================================

from statistics import mean


def calculate_profit(trade: Dict[str, str]) -> float:
    """
    Calculates profit or loss for a single trade.
    """
    entry = float(trade["entry_price"])
    exit_price = float(trade["exit_price"])

    if trade["direction"] == "buy":
        return exit_price - entry
    return entry - exit_price


def calculate_win_rate(trades: List[Dict[str, str]]) -> float:
    """
    Calculates win rate based on trade outcomes.
    """
    profits = [calculate_profit(t) for t in trades]
    wins = [p for p in profits if p > 0]

    if not profits:
        return 0.0

    return round(len(wins) / len(profits), 2)


def calculate_average_profit(trades: List[Dict[str, str]]) -> float:
    """
    Calculates average profit per trade.
    """
    profits = [calculate_profit(t) for t in trades]
    return round(mean(profits), 2) if profits else 0.0


def calculate_overtrading_indicator(trades: List[Dict[str, str]], threshold: int = 5) -> bool:
    """
    Simple heuristic to flag potential overtrading behavior.
    """
    return len(trades) > threshold


def summarize_insights(trades: List[Dict[str, str]]) -> Dict[str, float]:
    """
    Produces a basic insight summary from trading data.
    """
    return {
        "win_rate": calculate_win_rate(trades),
        "average_profit": calculate_average_profit(trades),
        "overtrading_flag": calculate_overtrading_indicator(trades)
    }


# ============================================================
# File: support_diagnostics.py
# Purpose: Help identify common issues reported by users
# ============================================================

def detect_missing_fields(trades: List[Dict[str, str]]) -> List[str]:
    """
    Detects missing required fields in trade records.
    """
    issues = []

    for index, trade in enumerate(trades, start=1):
        for field in REQUIRED_HEADERS:
            if not trade.get(field):
                issues.append(f"Trade {index}: missing {field}")

    return issues


def detect_invalid_prices(trades: List[Dict[str, str]]) -> List[str]:
    """
    Detects invalid price values in trade data.
    """
    issues = []

    for index, trade in enumerate(trades, start=1):
        try:
            float(trade["entry_price"])
            float(trade["exit_price"])
        except ValueError:
            issues.append(f"Trade {index}: invalid price format")

    return issues


def run_diagnostics(trades: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Runs all diagnostic checks and returns a summary.
    """
    return {
        "missing_fields": detect_missing_fields(trades),
        "invalid_prices": detect_invalid_prices(trades)
    }

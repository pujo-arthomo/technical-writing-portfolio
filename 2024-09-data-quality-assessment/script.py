```python
import csv
import os
from collections import Counter

# Configuration
INPUT_FILE = "input_data.csv"      # Change to your input file name
REPORT_FILE = "quality_report.txt" # Output report file

def load_csv(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

def run_quality_checks(rows):
    if not rows:
        return ["No data loaded."]
    
    issues = []
    header = rows[0]
    data_rows = rows[1:]
    
    # 1. Empty rows
    empty_count = sum(1 for row in data_rows if not any(row))
    if empty_count:
        issues.append(f"Found {empty_count} completely empty rows.")
    
    # 2. Missing values
    missing_count = sum(1 for row in data_rows if '' in row)
    if missing_count:
        issues.append(f"Found {missing_count} rows with missing values.")
    
    # 3. Exact duplicates
    row_counts = Counter(tuple(row) for row in data_rows)
    duplicates = {row: count for row, count in row_counts.items() if count > 1}
    if duplicates:
        issues.append(f"Found {len(duplicates)} exact duplicate row(s).")
    
    # 4. Column consistency
    expected_cols = len(header)
    inconsistent = [i+2 for i, row in enumerate(data_rows) if len(row) != expected_cols]
    if inconsistent:
        issues.append(f"Found {len(inconsistent)} row(s) with inconsistent column count (expected {expected_cols}).")
    
    if not issues:
        issues.append("No obvious quality issues detected.")
    
    return issues

def write_report(issues, report_path):
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Data Quality Assessment Report\n")
        f.write("="*40 + "\n\n")
        for issue in issues:
            f.write(f"- {issue}\n")
    print(f"Report written to {report_path}")

# Main execution
if __name__ == "__main__":
    print(f"Running quality check on {INPUT_FILE}...")
    rows = load_csv(INPUT_FILE)
    if rows is not None:
        issues = run_quality_checks(rows)
        write_report(issues, REPORT_FILE)

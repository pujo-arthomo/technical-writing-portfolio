import csv
import os

INPUT_FILE = "input.csv"
OUTPUT_FILE = "prepared_output.csv"
LOG_FILE = "preparation_log.txt"


def load_csv(file_path):
    rows = []
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    return rows


def normalize_whitespace(rows):
    cleaned_rows = []
    for row in rows:
        cleaned_row = []
        for cell in row:
            cleaned_row.append(cell.strip())
        cleaned_rows.append(cleaned_row)
    return cleaned_rows


def remove_empty_rows(rows):
    filtered_rows = []
    for row in rows:
        if any(cell for cell in row):
            filtered_rows.append(row)
    return filtered_rows


def check_column_consistency(rows, log_messages):
    if not rows:
        log_messages.append("Warning: CSV file is empty.")
        return

    expected_length = len(rows[0])

    for index, row in enumerate(rows, start=1):
        if len(row) != expected_length:
            log_messages.append(
                f"Warning: Row {index} has {len(row)} columns (expected {expected_length})."
            )


def write_output(rows, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def write_log(messages, log_path):
    if not messages:
        return

    with open(log_path, "w", encoding="utf-8") as file:
        for message in messages:
            file.write(message + "\n")


def prepare_csv(input_path, output_path, log_path):
    log_messages = []

    if not os.path.exists(input_path):
        log_messages.append("Error: Input file not found.")
        write_log(log_messages, log_path)
        return

    rows = load_csv(input_path)
    rows = normalize_whitespace(rows)
    rows = remove_empty_rows(rows)
    check_column_consistency(rows, log_messages)

    write_output(rows, output_path)
    write_log(log_messages, log_path)


if __name__ == "__main__":
    prepare_csv(INPUT_FILE, OUTPUT_FILE, LOG_FILE)

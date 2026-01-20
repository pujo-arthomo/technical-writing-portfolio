import csv

INPUT_FILE = "exported_data.csv"
OUTPUT_FILE = "filtered_output.csv"


def read_data(file_path):
    with open(file_path, newline="", encoding="utf-8") as file:
        return list(csv.reader(file))


def filter_empty_rows(rows):
    header, *data = rows
    filtered = [row for row in data if any(cell.strip() for cell in row)]
    return [header] + filtered


def write_data(file_path, rows):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def process_export():
    rows = read_data(INPUT_FILE)
    cleaned_rows = filter_empty_rows(rows)
    write_data(OUTPUT_FILE, cleaned_rows)


if __name__ == "__main__":
    process_export()

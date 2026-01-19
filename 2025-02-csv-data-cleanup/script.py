import csv

input_file = "input.csv"
output_file = "cleaned_output.csv"

with open(input_file, newline="", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    rows = [
        [cell.strip() for cell in row]
        for row in reader
        if any(cell.strip() for cell in row)
    ]

with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

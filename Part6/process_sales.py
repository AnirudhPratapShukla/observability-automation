import csv
import statistics

INPUT_FILE = "Part6/sales-data.csv"
OUTPUT_FILE = "Part6/filtered_sales.csv"

# Read the sales data
with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Calculate average price per square foot
price_per_sqft = [
    float(row["price_per_sqft"])
    for row in rows
    if row["price_per_sqft"]
]

average_price_per_sqft = statistics.mean(price_per_sqft)

# Filter properties below the average
filtered_rows = [
    row for row in rows
    if float(row["price_per_sqft"]) < average_price_per_sqft
]

# Write filtered data while keeping all original columns
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(filtered_rows)

print(f"Total properties processed: {len(rows)}")
print(f"Average price per sqft: ${average_price_per_sqft:.2f}")
print(f"Properties below average: {len(filtered_rows)}")
print(f"Output file created: {OUTPUT_FILE}")

# Part 6 — Data Processing

## Python CSV Data Processing

This task processes real estate sales data using Python.

### Input

- File: `sales-data.csv`
- Records processed: 1,000
- Key field used: `price_per_sqft`

### Processing

The `process_sales.py` script:

1. Reads `sales-data.csv`.
2. Calculates the average `price_per_sqft` across all properties.
3. Selects properties with a `price_per_sqft` below the average.
4. Writes the filtered records to `filtered_sales.csv`.
5. Retains all original columns.

### Results

- Total properties processed: 1,000
- Average price per square foot: $520.87
- Properties below average: 485
- Output file: `filtered_sales.csv`

### How to Run

From the repository root:

```bash
python3 Part6/process_sales.py

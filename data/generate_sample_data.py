import csv
import random

headers = ["Date", "Product", "Sales"]
rows = []

for i in range(50):
    row = [
        f"2023-04-{random.randint(1, 30)}", # generate random date between 2023-04-01 and 2023-04-30
        f"Product {random.randint(1, 5)}", # generate random product name
        random.randint(100, 1000)          # generate random sales value
    ]
    rows.append(row)

with open("sales_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(rows)

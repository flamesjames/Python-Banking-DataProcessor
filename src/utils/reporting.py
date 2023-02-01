import csv
import pandas as pd
import numpy as np
from datetime import datetime
import os


# Capture the transaction data file location
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
file_name = ROOT_DIR + "\\data\\test_transaction_data.xlsx"

# Read the excel file (turn into Pandas dataframe)
transactions = pd.read_excel(file_name)

# Get the initial count of rows and columns from the input sheet
initial_row_total = len(transactions)
initial_col_total = len(transactions.columns)

# Drop "Value Date" column
transactions.drop(columns=["VALUE DATE"], axis=1, inplace=True)

# Drop rows where both "Withdrawal Amount" and "Deposit Amount" are empty
transactions = transactions.dropna(subset=["WITHDRAWAL AMT", "DEPOSIT AMT"], how='all')

# Remove duplicate rows
transactions = transactions.drop_duplicates()

# Capture and print the statistics of the cleaned dataset (only taking into account numeric values).
data_stats = transactions.describe(include = [np.number])
print(data_stats)

# Get the number of rows and columns removed due to missing inputs
removed_rows = initial_row_total - len(transactions)
removed_cols = initial_col_total - len(transactions.columns)

# Initialize variables
final_balance = 0
total_withdrawals = 0
total_deposits = 0

# Iterate through transactions
for index, transaction in transactions.iterrows():
    if not pd.isnull(transaction["DEPOSIT AMT"]):
        total_deposits += transaction["DEPOSIT AMT"]
    if not pd.isnull(transaction["WITHDRAWAL AMT"]):
        total_withdrawals += transaction["WITHDRAWAL AMT"]

# Capture the final balance (last transaction within the sheet)
last_row = transactions.iloc[-1]
final_balance = last_row["BALANCE AMT"]

# Get the current date and time
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

data_summary = f"""
DATA PROCESSED ON: {current_time}\n
NUMBER OF ROWS REMOVED: {removed_rows}\n
NUMBER OF COLUMNS REMOVED: {removed_cols}\n
DATA STATS:\n{data_stats}\n
"""

print(data_summary)

# Ask user for output format
output_format = input("Enter the output format (csv/excel): ")

if output_format == "csv":
    # Write results to CSV file
    with open("transactions.csv", "w") as csvfile:
        fieldnames = ["Info", "Description", "Summary", "Final Balance", "Total Withdrawals", "Total Deposits"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "Info": "Transaction Report",
            "Description": "This report shows the final balance, total withdrawals, and total deposits.",
            "Summary": data_summary,
            "Final Balance": final_balance,
            "Total Withdrawals": total_withdrawals,
            "Total Deposits": total_deposits
        })
    print(f"Data exported to {output_format} successfully!")

elif output_format == "excel":
    # Write results to excel file
    data = {
        "Info": ["Transaction Report"],
        "Description": ["This report shows the final balance, total withdrawals, and total deposits."],
        "Summary": [data_summary],
        "Final Balance": [final_balance],
        "Total Withdrawals": [total_withdrawals],
        "Total Deposits": [total_deposits]
    }
    df = pd.DataFrame(data)
    df.to_excel("transactions.xlsx", index=False)
    print(f"Data exported to {output_format} successfully!")
else:
    print("Invalid output format. Please enter either 'csv' or 'excel'.")
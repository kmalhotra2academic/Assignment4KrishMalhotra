"""
Description: A program that reads through transaction records and reports the results.
Author: ACE Faculty
Edited by: Krish Malhotra
Date: October 14, 2024
Usage: This program will read transaction data from a .csv file, summarize and 
report the results.
"""

import csv
import os

valid_transaction_types = ['deposit', 'withdraw']
customer_data = {}
rejected_records = []
transaction_count = 0
transaction_counter = 0
total_transaction_amount = 0

# Clears console
os.system('cls' if os.name == 'nt' else 'clear')

# Read the CSV file
try:
    with open('bank_data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # Skip the header row
        
        for row in reader:
            # Reset valid record and error message for each iteration
            valid_record = True
            error_message = ''

            # Check if the row has the correct number of columns
            if len(row) != 3:
                valid_record = False
                error_message = 'Row does not have exactly three columns.'
            
            # Extract the customer ID from the first column
            customer_id = row[0]
            
            # Extract the transaction type from the second column
            transaction_type = row[1]

            ### VALIDATION 1 ###
            if transaction_type not in valid_transaction_types:
                valid_record = False
                error_message += 'Not a valid transaction type. '

            # Extract the transaction amount from the third column
            try:
                transaction_amount = float(row[2])
            except ValueError:
                valid_record = False
                error_message += 'Non-numeric transaction amount.'

            if valid_record:
                # Initialize the customer's account balance if it doesn't already exist
                if customer_id not in customer_data:
                    customer_data[customer_id] = {'balance': 0, 'transactions': []}

                # Update the customer's account balance based on the transaction type
                if transaction_type == 'deposit':
                    customer_data[customer_id]['balance'] += transaction_amount
                    transaction_count += 1
                    total_transaction_amount += transaction_amount
                elif transaction_type == 'withdraw':
                    customer_data[customer_id]['balance'] -= transaction_amount
                    transaction_count += 1
                    total_transaction_amount += transaction_amount
                
                # Record transactions in the customer's transaction history
                customer_data[customer_id]['transactions'].append((transaction_amount, transaction_type))
            else:
                ### COLLECT INVALID RECORDS ###
                rejected_records.append((row, error_message))
except FileNotFoundError as e:
    print(f"ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")

# Print the final account balances for each customer
print("PiXELL River Transaction Report\n===============================\n")
for customer_id, data in customer_data.items():
    balance = data['balance']
    print(f"\nCustomer {customer_id} has a balance of ${balance:,.2f}.")
    
    # Print the transaction history for the customer
    print("Transaction History:")
    for transaction in data['transactions']:
        amount, type = transaction
        print(f"\t{type.capitalize()}: ${amount:,.2f}")

# Calculate and print the average transaction amount
if transaction_count > 0:
    average_transaction_amount = total_transaction_amount / transaction_count
    print(f"\nAVERAGE TRANSACTION AMOUNT: ${average_transaction_amount:,.2f}")
else:
    print("\nNo valid transactions to calculate an average.")

# Print rejected records
if rejected_records:
    print("\nREJECTED RECORDS\n================")
    for record in rejected_records:
        print("REJECTED:", record)
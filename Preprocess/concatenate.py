"""
此檔將原本提供之training data以及後來公布private testing data的答案合併成新的training data
讀入2個檔案train.csv與private_1.csv後，會輸出新的training檔案，名為train2.csv
PS. train.csv為上一個github repo我輸出的檔案
"""
import pandas as pd

# Read the CSV files
public_data = pd.read_csv('train.csv')
private_data = pd.read_csv('private_1.csv')

# Concatenate the dataframes
combined_data = pd.concat([public_data, private_data], ignore_index=True)

# Write the concatenated data to a new CSV file
combined_data.to_csv('train2.csv', index=False)

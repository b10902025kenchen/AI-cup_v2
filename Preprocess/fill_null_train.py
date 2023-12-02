"""
此檔會填入training data的null value，如果是類別型，我們把null視為新的類別；如果是數值型，我們填入平均值
讀入一個檔案train_time_myf_cano_moref_conam.csv，輸出新的檔案train_time_myf_cano_moref_conam_null.csv
"""

import pandas as pd

# Read the CSV file into a DataFrame
file_path = "train_time_myf_cano_moref_conam.csv"  # Replace with the actual file path
df = pd.read_csv(file_path)

# Fill null values in the specified columns with the provided values
df['etymd'].fillna(77, inplace=True)
df['mcc'].fillna(777, inplace=True)
df['stocn'].fillna(777, inplace=True)
df['scity'].fillna(77777, inplace=True)
df['stscd'].fillna(7.0, inplace=True)
df['hcefg'].fillna(7, inplace=True)
df['csmcu'].fillna(777, inplace=True)

# Calculate the average value for 'cano_locdt_sigma'
cano_locdt_sigma_mean = df['cano_locdt_sigma'].mean()
# Fill null values in 'cano_locdt_sigma' column with its average value
df['cano_locdt_sigma'].fillna(cano_locdt_sigma_mean, inplace=True)

# Write the modified DataFrame to a new CSV file
output_file_path = "train_time_myf_cano_moref_conam_null.csv"
df.to_csv(output_file_path, index=False)

print(f"The modified data has been written to {output_file_path}.")

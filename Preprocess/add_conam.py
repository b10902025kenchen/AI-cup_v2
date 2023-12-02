"""
此檔為新增feature的第五個檔案，要新增額度相關feature，我們新增同卡號同天消費金額最大與最小值
讀入兩個檔案train_time_myf_cano_moref.csv與test_time_myf_cano_moref.csv，輸出新的檔案train_time_myf_cano_moref_conam.csv與test_time_myf_cano_moref_conam.csv
"""

import pandas as pd

# Read the filled CSV files
train_file = "train_time_myf_cano_moref.csv"
test_file = "test_time_myf_cano_moref.csv"

# Read the CSV files into DataFrames
train_data = pd.read_csv(train_file)
test_data = pd.read_csv(test_file)

# Calculate 'cano_locdt_conam_max' and 'cano_locdt_conam_min' columns
print("cano_locdt_conam_max")
train_data['cano_locdt_conam_max'] = train_data.groupby(['cano', 'locdt'])['conam'].transform('max')
train_data['cano_locdt_conam_min'] = train_data.groupby(['cano', 'locdt'])['conam'].transform('min')

print("cano_locdt_conam_max2")
test_data['cano_locdt_conam_max'] = test_data.groupby(['cano', 'locdt'])['conam'].transform('max')
test_data['cano_locdt_conam_min'] = test_data.groupby(['cano', 'locdt'])['conam'].transform('min')

# Save the updated DataFrames to new CSV files
train_data.to_csv("train_time_myf_cano_moref_conam.csv", index=False)
test_data.to_csv("test_time_myf_cano_moref_conam.csv", index=False)

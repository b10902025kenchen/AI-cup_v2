"""
此檔為新增feature的第三個檔案，要卡號相關的feature，我們新增卡號在train和test data的總出現次數，5天內出現次數，與20天內出現次數，皆為數值型資料
讀入兩個檔案train_time_myf.csv與test_time_myf.csv，輸出新的檔案train_time_myf_cano.csv與test_time_myf_cano.csv
"""

import pandas as pd

# Read the training and testing CSV files
train_data = pd.read_csv("train_time_myf.csv")
test_data = pd.read_csv("test_time_myf.csv")

# Combine both datasets for 'cano' occurrences
combined_data = pd.concat([train_data, test_data])

# Calculate 'cano' occurrences in combined data for 'cano_all'
combined_cano_counts = combined_data['cano'].value_counts().reset_index()
combined_cano_counts.columns = ['cano', 'cano_all_combined']

# Merge 'cano_all_combined' counts back to both datasets
train_data = pd.merge(train_data, combined_cano_counts, on='cano', how='left')
test_data = pd.merge(test_data, combined_cano_counts, on='cano', how='left')

# Define a function to count 'cano' occurrences based on locdt differences
def count_cano_occurrences(data, locdt_threshold):
    """
    此函式計算一卡號在threshold天內出現次數
    """
    grouped = data.groupby('cano').apply(lambda x: (x['locdt'].diff() <= locdt_threshold).sum()).reset_index()
    grouped.columns = ['cano', f'cano_{locdt_threshold}']
    return grouped

# Calculate occurrences of 'cano' within locdt threshold for cano_5 and cano_20
cano_5_combined = count_cano_occurrences(combined_data, 5)
cano_20_combined = count_cano_occurrences(combined_data, 20)

# Merge 'cano_5_combined' and 'cano_20_combined' counts back to both datasets
train_data = pd.merge(train_data, cano_5_combined, on='cano', how='left')
train_data = pd.merge(train_data, cano_20_combined, on='cano', how='left')

test_data = pd.merge(test_data, cano_5_combined, on='cano', how='left')
test_data = pd.merge(test_data, cano_20_combined, on='cano', how='left')

# Save the modified training and testing datasets to new CSV files
train_data.to_csv("train_time_myf_cano.csv", index=False)
test_data.to_csv("test_time_myf_cano.csv", index=False)

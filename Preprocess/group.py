"""
此檔會用來處理類別型資料，我們使用target encoding的作法，將所有類別型資料，用相同值當中被盜刷的比例取代，這也是我們處理類別型資料的關鍵
讀入兩個檔案train_time_myf_cano_moref_conam_null.csv與test_time_myf_cano_moref_conam_null.csv，
輸出train_time_myf_cano_moref_conam_null_group.csv與test_time_myf_cano_moref_conam_null_group.csv
"""

import pandas as pd

# Read the first CSV file
print("Read the first CSV file")
df = pd.read_csv('train_time_myf_cano_moref_conam_null.csv')

# Columns to modify
columns_to_modify = [
    'chid', 'cano', 'contp', 'etymd', 'mchno', 'acqic', 'mcc',
    'ecfg', 'insfg', 'bnsfg', 'stocn', 'scity', 'stscd', 'ovrlt',
    'flbmk', 'hcefg', 'csmcu', 'flg_3dsmk', 'fequc', 'fequ0', 'hour'
]

print("Calculate mean")
# Create a dictionary to store mean_per_category DataFrames for each column
mean_per_category_dict = {}

# Calculate mean of "label" for each category in specified columns
for column in columns_to_modify:
    # Calculate mean and count for each category
    mean_per_category_dict[column] = df.groupby(column)['label'].agg(['mean', 'count'])

    # Replace values according to the given rules
    df[column] = df[column].apply(lambda x: mean_per_category_dict[column].at[x, 'mean'] if mean_per_category_dict[column].at[x, 'count'] >= 5 else 0.003686356)

print("Read the second CSV file")
# Read the second CSV file without the "label" column
df2 = pd.read_csv('test_time_myf_cano_moref_conam_null.csv')

print("Replace values in the second dataframe using the same rules")
# Replace values in the second dataframe using the same rules
for column in columns_to_modify:
    df2[column] = df2[column].apply(lambda x: mean_per_category_dict[column].at[x, 'mean'] if x in mean_per_category_dict[column].index and mean_per_category_dict[column].at[x, 'count'] >= 5 else 0.003686356)

print("Save")
# Save the modified dataframes to new CSV files
df.to_csv('train_time_myf_cano_moref_conam_null_group.csv', index=False)
df2.to_csv('test_time_myf_cano_moref_conam_null_group.csv', index=False)

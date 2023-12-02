"""
此檔為新增feature的第四個檔案，要新增3個features，其一為一卡號有交易的天數，其二為一卡號一天平均交易次數，其三為卡號交易日期的標準差
讀入兩個檔案train_time_myf_cano.csv與test_time_myf_cano.csv，輸出新的檔案train_time_myf_cano_moref.csv與test_time_myf_cano_moref.csv
"""

import pandas as pd

# Read the training and testing CSV files
train_file = "train_time_myf_cano.csv"
test_file = "test_time_myf_cano.csv"

train_data = pd.read_csv(train_file)
test_data = pd.read_csv(test_file)

# Concatenate training and testing data
combined_data = pd.concat([train_data, test_data])

# Calculate the number of unique days each card has transactions
print("cano_locdt")
combined_data['cano_locdt'] = combined_data.groupby('cano')['locdt'].transform('nunique')

print("cano_locdt_freq")
# Calculate the cano_locdt_freq feature
combined_data['cano_locdt_freq'] = combined_data['cano_all_combined'] / combined_data['cano_locdt']

print("cano_locdt_sigma")
# Calculate the standard deviation of locdt for each card (training + testing) by 'cano'
combined_data['cano_locdt_sigma'] = combined_data.groupby('cano')['locdt'].transform('std')

print("chid_mchno")
# Calculate the chid_mchno feature
combined_data['chid_mchno'] = combined_data.groupby(['chid', 'mchno'])['locdt'].transform('count')

print("cano_locdt2")
# Split back into train and test data
train_data['cano_locdt'] = combined_data[:len(train_data)].cano_locdt
test_data['cano_locdt'] = combined_data[len(train_data):].cano_locdt

print("cano_locdt_freq2")
train_data['cano_locdt_freq'] = combined_data[:len(train_data)].cano_locdt_freq
test_data['cano_locdt_freq'] = combined_data[len(train_data):].cano_locdt_freq

print("cano_locdt_sigma2")
train_data['cano_locdt_sigma'] = combined_data[:len(train_data)].cano_locdt_sigma
test_data['cano_locdt_sigma'] = combined_data[len(train_data):].cano_locdt_sigma

print("chid_mchno2")
train_data['chid_mchno'] = combined_data[:len(train_data)].chid_mchno
test_data['chid_mchno'] = combined_data[len(train_data):].chid_mchno

# Save the updated data to new CSV files
train_add_file = "train_time_myf_cano_moref.csv"
test_add_file = "test_time_myf_cano_moref.csv"

train_data.to_csv(train_add_file, index=False)
test_data.to_csv(test_add_file, index=False)

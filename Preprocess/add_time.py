"""
此檔為新增feature的第一個檔案，要加時間相關的feature，由原本的locdt與loctm計算出新的hour,minute,second與累積時間time
讀入兩個檔案train.csv與private_1_processed.csv，輸出新的檔案train_time.csv與test_time.csv
"""
import pandas as pd

# Read the filled CSV files
train_file = "train2.csv"
test_file = "private_2_processed.csv"

# Read the CSV files into DataFrames
train_data = pd.read_csv(train_file)
test_data = pd.read_csv(test_file)

# Define a function to extract hour, minute, and second from 'loctm'
def extract_time_components(loctm):
    """
    此函式將loctm切成hour, minute與second
    """
    loctm_str = str(loctm).zfill(6)  # Ensure it's 6 digits, filling zeros if needed
    hour = int(loctm_str[:2])
    minute = int(loctm_str[2:4])
    second = int(loctm_str[4:])
    return hour, minute, second

# Extract hour, minute, and second from 'loctm' and create columns for each
train_data['hour'], train_data['minute'], train_data['second'] = zip(*train_data['loctm'].apply(extract_time_components))
test_data['hour'], test_data['minute'], test_data['second'] = zip(*test_data['loctm'].apply(extract_time_components))

# Calculate 'time' column as specified
train_data['time'] = train_data['locdt'] * 86400 + train_data['hour'] * 3600 + train_data['minute'] * 60 + train_data['second']
test_data['time'] = test_data['locdt'] * 86400 + test_data['hour'] * 3600 + test_data['minute'] * 60 + test_data['second']

# Save the updated DataFrames to new CSV files
train_data.to_csv("train_time.csv", index=False)
test_data.to_csv("test_time.csv", index=False)

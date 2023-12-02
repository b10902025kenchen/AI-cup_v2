"""
此檔為新增feature的第二個檔案，要新增2個features，其一為實付金額是否等於消費地金額，其二為實付金額是否等於0，皆為類別型資料
讀入兩個檔案train_time.csv與test_time.csv，輸出新的檔案train_time_myf.csv與test_time_myf.csv
"""
import pandas as pd

# Read the CSV files
train_data = pd.read_csv('train_time.csv')
test_data = pd.read_csv('test_time.csv')

# Define the function to create the new columns
def create_new_columns(data):
    """
    此函式增加兩個新的column，fequc與fequ0
    """
    data['fequc'] = (data['flam1'] == data['csmam']).astype(int)
    data['fequ0'] = (data['flam1'] == 0).astype(int)
    return data

# Add new columns to both train and test data
train_data = create_new_columns(train_data)
test_data = create_new_columns(test_data)

# Write the modified data to new CSV files
train_data.to_csv('train_time_myf.csv', index=False)
test_data.to_csv('test_time_myf.csv', index=False)

import pandas as pd

# Read the original CSV file
file_path = 'train_time_myf_cano_moref_conam_null_group.csv'  # Replace this with your CSV file path
df = pd.read_csv(file_path)

# Get the rows from 9297568 to 10098331
rows_to_copy = df.iloc[8688527:10098330]

# Append the selected rows 800764 times
appended_rows = pd.concat([rows_to_copy] * 1, ignore_index=True)

# Combine the original dataframe with the appended rows
new_df = pd.concat([df, appended_rows], ignore_index=True)

# Write the new dataframe to a new CSV file
output_file_path = 'train_time_myf_cano_moref_conam_null_group_dup.csv'  # Replace this with your desired output file path
new_df.to_csv(output_file_path, index=False)

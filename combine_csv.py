import pandas as pd
import os

# Generate file paths
file_paths = [f'checkpoint_{i}.csv' for i in range(1, 199)]  # Adjust the range as needed

# Create an empty DataFrame to store the concatenated columns
combined_column = pd.DataFrame()

for file_path in file_paths:
    if os.path.exists(file_path):
        # Read the CSV file
        df = pd.read_csv(file_path, header=None)

        # Check if the file has the correct format
        if df.shape[1] >= 2 and df.shape[0] == 23:
            # Extract the second column
            combined_column = pd.concat([combined_column, df.iloc[:, 1]], ignore_index=True, axis=1)
        else:
            print(f"File {file_path} does not have the expected format.")
    else:
        print(f"File {file_path} not found.")

# Save the combined column to a new CSV file
combined_column.to_csv('combined_column.csv', index=False, header=False)
print("Combined column saved to 'combined_column.csv'")

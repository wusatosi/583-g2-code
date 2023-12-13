import argparse
import pandas as pd

def convert_to_dataframe(file_path, modifications=None, sort=False, ascending=True):
    """
    Reads data from a file, converts it into a pandas DataFrame, applies multiple modifications if given,
    and sorts the DataFrame if requested.
    
    Parameters:
    file_path (str): Path to the file containing the data.
    modifications (list of tuples, optional): List of tuples where each tuple contains an operation and its value change.
    sort (bool, optional): Whether to sort the DataFrame.
    ascending (bool, optional): Sort in ascending order if True, else in descending order.
    
    Returns:
    pd.DataFrame: A DataFrame with two columns - 'Operation' and 'Value'.
    """
    with open(file_path, 'r') as file:
        data_str = file.read()

    # Splitting the data into rows and then into columns
    rows = data_str.strip().split('\n')
    split_rows = [row.split(',') for row in rows]

    # Creating a DataFrame
    df = pd.DataFrame(split_rows, columns=["Operation", "Value"])
    df["Value"] = df["Value"].astype(float)

    # Applying modifications
    if modifications:
        for operation, change in modifications:
            df.loc[df['Operation'] == operation, 'Value'] += change

    # Sorting the DataFrame, if requested
    if sort:
        df = df.sort_values(by="Value", ascending=ascending)

    return df

def parse_modifications(modification_args):
    """ Parses modification arguments into a list of tuples. """
    modifications = []
    for mod in modification_args:
        operation, change = mod.split(',')
        modifications.append((operation, float(change)))
    return modifications

def main():
    parser = argparse.ArgumentParser(description='Convert data to DataFrame, modify values, and sort the DataFrame.')
    parser.add_argument('file_path', type=str, help='Path to the file containing the data')
    parser.add_argument('--modify', nargs='*', help='List of operations and value changes, e.g., ADD_FIX,0.1 SUB_FIX,-0.2')
    parser.add_argument('--sort', action='store_true', help='Sort the DataFrame by value')
    parser.add_argument('--ascending', action='store_true', help='Sort in ascending order (default is descending)')

    args = parser.parse_args()

    modifications = None
    if args.modify:
        modifications = parse_modifications(args.modify)

    df = convert_to_dataframe(args.file_path, modifications, args.sort, args.ascending)
    print(df)

if __name__ == "__main__":
    main()

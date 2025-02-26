import pandas as pd
import numpy as np

def load_data(file_path):    # 1. File Loading
    """Loads a CSV file and returns a DataFrame."""
    try:
        data = pd.read_csv(file_path)
        print(f"{file_path} loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def clean_data(data):    # 2. Data Cleaning
    """Fixes missing values."""
    if data is not None:
        # Fill missing values with the column average
        data.fillna(data.mean(), inplace=True)
        print("Missing values filled successfully.")
        return data
    else:
        return None

def compute_statistics(data, column_name):    # 3. Statistics Calculation
    """Shows basic stats for a column."""
    if data is not None and column_name in data.columns:
        minimum = data[column_name].min()
        maximum = data[column_name].max()
        mean = data[column_name].mean()
        median = data[column_name].median()
        std_dev = data[column_name].std()
        
        print(f"Statistics for {column_name}:")
        print(f"Minimum: {minimum}")
        print(f"Maximum: {maximum}")
        print(f"Mean: {mean}")
        print(f"Median: {median}")
        print(f"Standard Deviation: {std_dev}")
        
        return {
            'min': minimum,
            'max': maximum,
            'mean': mean,
            'median': median,
            'std_dev': std_dev
        }
    else:
        print(f"Column {column_name} not found in the data.")
        return None

def export_to_csv(stats, filename='statistics_output.csv'):
    """Exports statistics to a CSV file."""
    output_path = 'labs/lab2/' + filename  # Output dosyasının tam yolu
    stats_df = pd.DataFrame(stats).T  # .T transposes the dictionary so stats are in rows
    stats_df.to_csv(output_path, index=True)  # Save to CSV with stats as rows
    print(f"Exported statistics to {output_path}")


def main():    # Main Function
    file_path = 'datasets/soil_test.csv'    # 4. Set the file path
    data = load_data(file_path)    # 5. Load the data
    cleaned_data = clean_data(data)    # 6. Clean the data
    if cleaned_data is not None:    # 7. Calculate statistics
        if x == 'a':
            stats_all = {}
            for i in columnss:
                stats_all[i] = compute_statistics(cleaned_data, i)  # You can choose a column like soil_ph
            # Export the results to CSV when x is 'a' and y is 'y'
            if y == 'y':
                export_to_csv(stats_all)  # Export all statistics
        elif x == 's':
            selected_column = columnss[int(y)-1]  # Select the column based on user input
            stats = compute_statistics(cleaned_data, selected_column)
            if stats is not None and y == 'y':
                export_to_csv({selected_column: stats})  # Export only the selected column's stats
            

columnss = ['soil_ph', 'nitrogen', 'phosphorus', 'moisture']
x = str(input('Do you want a specific column or all columns [enter(s/a)]='))

if x == 's':
    y = str(input('Which data do you need [soil_ph, nitrogen, phosphorus, moisture](1, 2, 3, 4)?='))
    if y != '1' and y != '2' and y != '3' and y != '4':
        print('You must write 1, 2, 3, or 4; your entry is wrong!!!')
        exit()
elif x == 'a':
    y = str(input('Do you want to export the result in a CSV file? (y/n)='))
    if y != 'y' and y != 'n':
        print('You must write y or n, your entry is wrong!!!')
        exit()
else:
    print('You must write a or s, your entry is wrong!!!')
    exit()

main()

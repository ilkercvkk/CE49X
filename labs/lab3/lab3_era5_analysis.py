import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path):
    """Loads a CSV file into a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path, parse_dates=['timestamp'])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found: {file_path}")

def calculate_wind_speed(df):
    """Calculates wind speed from u10m and v10m components."""
    df['wind_speed'] = np.sqrt(df['u10m']**2 + df['v10m']**2)
    return df

def compute_monthly_averages(df):
    """Computes monthly average wind speed."""
    df['month'] = df['timestamp'].dt.month
    monthly_avg = df.groupby('month')['wind_speed'].mean()
    return monthly_avg

def compute_seasonal_averages(df):
    """Computes seasonal average wind speed."""
    seasons = {12: 'Winter', 1: 'Winter', 2: 'Winter',
               3: 'Spring', 4: 'Spring', 5: 'Spring',
               6: 'Summer', 7: 'Summer', 8: 'Summer',
               9: 'Fall', 10: 'Fall', 11: 'Fall'}
    df['season'] = df['timestamp'].dt.month.map(seasons)
    seasonal_avg = df.groupby('season')['wind_speed'].mean()
    return seasonal_avg

def plot_wind_speed(monthly_avg_berlin, monthly_avg_munich):
    """Plots monthly average wind speeds for Berlin and Munich."""
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_avg_berlin.index, monthly_avg_berlin, label='Berlin', marker='o')
    plt.plot(monthly_avg_munich.index, monthly_avg_munich, label='Munich', marker='s')
    plt.xlabel('Month')
    plt.ylabel('Average Wind Speed (m/s)')
    plt.title('Monthly Average Wind Speed')
    plt.legend()
    plt.grid()
    plt.show()

def pref():  
    x = input("Berlin, Munich, or Both? (b/m/both): ")
    if x not in ['b','m','both']:
        print('You must write b, m, both ; your entry is wrong!!!')
        exit()
    y = input("Monthly, Seasonal, or Both? (m/s/b): ")
    if y not in ['m','s','b']:
        print('You must write m, s, b ; your entry is wrong!!!')
        exit()
    if x == 'both' and y in ['m', 'b']:
        z = input("Do you want to plot the monthly graph? (y/n): ")
        if z not in ['y','n']:
            print('You must write y or n ; your entry is wrong!!!')
            exit()
    else:
        z = None
    return x,y,z

def main():
    city, period, graph = pref()

    berlin_file = '../../datasets/berlin_era5_wind_20241231_20241231.csv'
    munich_file = '../../datasets/munich_era5_wind_20241231_20241231.csv'

    if city == 'b':
        berlin_df = load_data(berlin_file)
        berlin_df = calculate_wind_speed(berlin_df)
        if period == 'm':
            monthly_avg_berlin = compute_monthly_averages(berlin_df)
            print("Monthly Averages (Berlin):\n", monthly_avg_berlin)
        elif period == 's':
            seasonal_avg_berlin = compute_seasonal_averages(berlin_df)
            print("Seasonal Averages (Berlin):\n", seasonal_avg_berlin)
        elif period == 'b':
            monthly_avg_berlin = compute_monthly_averages(berlin_df)
            print("Monthly Averages (Berlin):\n", monthly_avg_berlin)
            seasonal_avg_berlin = compute_seasonal_averages(berlin_df)
            print("Seasonal Averages (Berlin):\n", seasonal_avg_berlin)

    elif city == 'm':
        munich_df = load_data(munich_file)
        munich_df = calculate_wind_speed(munich_df)        
        if period == 'm':
            monthly_avg_munich = compute_monthly_averages(munich_df)
            print("Monthly Averages (Munich):\n", monthly_avg_munich)
        elif period == 's':
            seasonal_avg_munich = compute_seasonal_averages(munich_df)
            print("Seasonal Averages (Munich):\n", seasonal_avg_munich) 
        elif period == 'b':
            monthly_avg_munich = compute_monthly_averages(munich_df)
            print("Monthly Averages (Munich):\n", monthly_avg_munich)
            seasonal_avg_munich = compute_seasonal_averages(munich_df)
            print("Seasonal Averages (Munich):\n", seasonal_avg_munich)

    elif city == 'both':
        berlin_df = load_data(berlin_file)
        munich_df = load_data(munich_file)
        berlin_df = calculate_wind_speed(berlin_df)
        munich_df = calculate_wind_speed(munich_df)
        if period == 'm':
            monthly_avg_berlin = compute_monthly_averages(berlin_df)
            monthly_avg_munich = compute_monthly_averages(munich_df)
            print("Monthly Averages (Berlin):\n", monthly_avg_berlin)
            print("Monthly Averages (Munich):\n", monthly_avg_munich)
        elif period == 's':
            seasonal_avg_berlin = compute_seasonal_averages(berlin_df)
            seasonal_avg_munich = compute_seasonal_averages(munich_df)
            print("Seasonal Averages (Berlin):\n", seasonal_avg_berlin)
            print("Seasonal Averages (Munich):\n", seasonal_avg_munich)
        elif period == 'b':
            monthly_avg_berlin = compute_monthly_averages(berlin_df)
            monthly_avg_munich = compute_monthly_averages(munich_df)
            print("Monthly Averages (Berlin):\n", monthly_avg_berlin)
            print("Monthly Averages (Munich):\n", monthly_avg_munich)
            seasonal_avg_berlin = compute_seasonal_averages(berlin_df)
            seasonal_avg_munich = compute_seasonal_averages(munich_df)
            print("Seasonal Averages (Berlin):\n", seasonal_avg_berlin)
            print("Seasonal Averages (Munich):\n", seasonal_avg_munich)
    
    if graph == 'y':
        plot_wind_speed(monthly_avg_berlin, monthly_avg_munich)
        
main()
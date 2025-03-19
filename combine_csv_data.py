# CTA Tracker - CSV Combiner
# This script combines all the CSV files in the CTA tracker project into a single comprehensive dataset

import pandas as pd
import os

# File paths
data_dir = os.path.dirname(os.path.abspath(__file__))
lines_file = os.path.join(data_dir, 'Lines.csv')
stations_file = os.path.join(data_dir, 'Stations.csv')
stops_file = os.path.join(data_dir, 'Stops.csv')
stop_details_file = os.path.join(data_dir, 'StopDetails.csv')
ridership_file = os.path.join(data_dir, 'Ridership.csv')

# Output file
combined_file = os.path.join(data_dir, 'CTA_Combined_Data.csv')

def combine_csv_files():
    """Combine all CSV files into a single comprehensive dataset"""
    print("Loading CSV files...")
    
    try:
        # Load each CSV file
        lines_df = pd.read_csv(lines_file)
        stations_df = pd.read_csv(stations_file)
        stops_df = pd.read_csv(stops_file)
        stop_details_df = pd.read_csv(stop_details_file)
        
        # Check if ridership file exists and load it
        ridership_exists = os.path.exists(ridership_file)
        if ridership_exists:
            ridership_df = pd.read_csv(ridership_file)
        
        print("All files loaded successfully!")
        
        # Convert IDs to string to ensure proper joining
        for df in [lines_df, stations_df, stops_df, stop_details_df]:
            id_columns = [col for col in df.columns if 'ID' in col or 'Id' in col]
            for col in id_columns:
                df[col] = df[col].astype(str)
        
        if ridership_exists:
            id_columns = [col for col in ridership_df.columns if 'ID' in col or 'Id' in col]
            for col in id_columns:
                ridership_df[col] = ridership_df[col].astype(str)
        
        # Combine the data
        print("Combining data...")
        
        # First, join stops with stations to get station names
        combined_df = pd.merge(stops_df, stations_df, on='Station_ID', how='left')
        
        # Then, join with stop_details to get line information
        combined_df = pd.merge(combined_df, stop_details_df, on='Stop_ID', how='left')
        
        # Finally, join with lines to get line colors
        combined_df = pd.merge(combined_df, lines_df, on='Line_ID', how='left')
        
        # If ridership data exists, join it as well
        if ridership_exists:
            # Convert date column if it exists
            if 'Ride_Date' in ridership_df.columns:
                ridership_df['Ride_Date'] = pd.to_datetime(ridership_df['Ride_Date'], errors='coerce')
            
            # Join ridership data
            combined_df = pd.merge(combined_df, ridership_df, on='Station_ID', how='left')
        
        # Save the combined data to a CSV file
        print(f"Saving combined data to {combined_file}...")
        combined_df.to_csv(combined_file, index=False)
        
        print(f"Combined data saved successfully! Total rows: {len(combined_df)}")
        print(f"Columns in combined dataset: {', '.join(combined_df.columns)}")
        
        return True
    
    except Exception as e:
        print(f"Error combining CSV files: {e}")
        return False

def main():
    """Main function to run the CSV combiner"""
    print("CTA Tracker - CSV Combiner")
    print("==========================")
    
    success = combine_csv_files()
    
    if success:
        print("\nAll CSV files have been successfully combined into a single dataset!")
        print(f"The combined file is located at: {combined_file}")
    else:
        print("\nFailed to combine CSV files. Please check the error messages above.")

if __name__ == "__main__":
    main()
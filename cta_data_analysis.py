# CTA Tracker Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Create output directory for saving plots
output_dir = 'output_plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")
else:
    print(f"Output directory already exists: {output_dir}")

# Set plot style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

# File path
data_file = 'CTA_Combined_Data.csv'

# Check if file exists
if not os.path.exists(data_file):
    print(f"Error: {data_file} not found.")
    exit(1)

print(f"Loading data from {data_file}...")

#############################################################
# 1. Data Understanding
#############################################################

def examine_data_structure(df):
    """Examine the structure of the dataset"""
    print("\n1. Data Structure:")
    print(f"\nDataset shape: {df.shape} (rows, columns)")
    print("\nColumn names:")
    for col in df.columns:
        print(f"  - {col}")
    
    print("\nData types:")
    print(df.dtypes)
    
    print("\nSample data (first 5 rows):")
    print(df.head())

def check_missing_values(df):
    """Check for missing values in the dataset"""
    print("\n2. Missing Values:")
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    
    missing_data = pd.DataFrame({
        'Missing Values': missing,
        'Percentage': missing_percent
    })
    
    print(missing_data[missing_data['Missing Values'] > 0])
    
    if missing.sum() == 0:
        print("No missing values found.")

def understand_variables(df):
    """Understand the variables in the dataset"""
    print("\n3. Variable Summary:")
    
    # Numeric variables
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    print("\nNumeric variables summary:")
    print(df[numeric_cols].describe())
    
    # Categorical variables
    cat_cols = df.select_dtypes(include=['object']).columns
    print("\nCategorical variables summary:")
    for col in cat_cols:
        unique_values = df[col].nunique()
        print(f"  - {col}: {unique_values} unique values")
        if unique_values < 10:  # Only show if there are few unique values
            print(f"    Values: {df[col].unique()}")

#############################################################
# 2. Data Cleaning
#############################################################

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    print("\n1. Handling Missing Values:")
    
    # Check if there are any missing values
    if df.isnull().sum().sum() == 0:
        print("No missing values to handle.")
        return df
    
    # For numeric columns, fill with median
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            print(f"  - Filled missing values in {col} with median: {median_value}")
    
    # For categorical columns, fill with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            mode_value = df[col].mode()[0]
            df[col] = df[col].fillna(mode_value)
            print(f"  - Filled missing values in {col} with mode: {mode_value}")
    
    return df

def fix_data_types(df):
    """Fix data types in the dataset"""
    print("\n2. Fixing Data Types:")
    
    # Convert ID columns to string if they're not already
    id_columns = [col for col in df.columns if 'ID' in col or 'Id' in col]
    for col in id_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
            print(f"  - Converted {col} to string type")
    
    # Convert geographic coordinates to float
    geo_columns = ['Latitude', 'Longitude']
    for col in geo_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"  - Converted {col} to numeric type")
    
    # Convert ADA indicator to boolean
    if 'ADA' in df.columns:
        df['ADA'] = df['ADA'].astype(bool)
        print("  - Converted ADA to boolean type")
    
    # Convert date columns to datetime
    date_columns = [col for col in df.columns if 'Date' in col]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            print(f"  - Converted {col} to datetime type")
    
    return df

def remove_unnecessary_columns(df):
    """Remove unnecessary columns and create derived variables"""
    print("\n3. Column Management:")
    
    # List all columns
    print("Available columns:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    # For this analysis, we'll keep all columns but create some derived ones
    
    # Create derived variables if date column exists
    if 'Ride_Date' in df.columns:
        # Extract year, month, day, day of week
        df['Year'] = df['Ride_Date'].dt.year
        df['Month'] = df['Ride_Date'].dt.month
        df['Day'] = df['Ride_Date'].dt.day
        df['DayOfWeek'] = df['Ride_Date'].dt.dayofweek
        print("  - Created date-based derived variables (Year, Month, Day, DayOfWeek)")
    
    return df

#############################################################
# 3. Exploratory Analysis
#############################################################

# 3.1 Univariate Analysis
def univariate_analysis(df):
    """Perform univariate analysis on the dataset"""
    print("\n3.1 Univariate Analysis:")
    
    # Analyze numeric variables
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    print("\nNumeric Variables Distribution:")
    
    for col in numeric_cols:
        if col == 'Num_Riders' or 'ID' not in col:
            print(f"\n  - {col} statistics:")
            print(df[col].describe())
            
            # Plot histogram
            plt.figure()
            sns.histplot(df[col], kde=True)
            plt.title(f'Distribution of {col}')
            plt.tight_layout()
            # Save figure to file
            filename = f"{output_dir}/univariate_numeric_{col}.png"
            plt.savefig(filename)
            print(f"Saved plot to {filename}")
            plt.close()
    
    # Analyze categorical variables
    cat_cols = df.select_dtypes(include=['object', 'bool']).columns
    print("\nCategorical Variables Distribution:")
    
    for col in cat_cols:
        if df[col].nunique() < 30:  # Only plot if there aren't too many categories
            print(f"\n  - {col} value counts:")
            value_counts = df[col].value_counts()
            print(value_counts)
            
            # Plot bar chart
            plt.figure()
            sns.countplot(y=col, data=df, order=value_counts.index)
            plt.title(f'Distribution of {col}')
            plt.tight_layout()
            # Save figure to file
            filename = f"{output_dir}/univariate_categorical_{col}.png"
            plt.savefig(filename)
            print(f"Saved plot to {filename}")
            plt.close()

# 3.2 Bivariate Analysis
def bivariate_analysis(df):
    """Perform bivariate analysis on the dataset"""
    print("\n3.2 Bivariate Analysis:")
    
    # Ridership by station
    if 'Station_Name' in df.columns and 'Num_Riders' in df.columns:
        print("\nRidership by Station:")
        station_ridership = df.groupby('Station_Name')['Num_Riders'].sum().sort_values(ascending=False)
        print(station_ridership.head(10))
        
        # Plot top 10 stations by ridership
        plt.figure(figsize=(12, 8))
        station_ridership.head(10).sort_values().plot(kind='barh')
        plt.title('Top 10 Stations by Ridership')
        plt.xlabel('Number of Riders')
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/bivariate_top10_stations.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()
    
    # Ridership by day type
    if 'Type_of_Day' in df.columns and 'Num_Riders' in df.columns:
        print("\nRidership by Day Type:")
        day_type_ridership = df.groupby('Type_of_Day')['Num_Riders'].sum()
        print(day_type_ridership)
        
        # Plot ridership by day type
        plt.figure()
        day_type_ridership.plot(kind='bar')
        plt.title('Ridership by Day Type')
        plt.xlabel('Day Type (W=Weekday, A=Saturday, U=Sunday/Holiday)')
        plt.ylabel('Number of Riders')
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/bivariate_day_type.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()
    
    # Ridership by month
    if 'Month' in df.columns and 'Num_Riders' in df.columns:
        print("\nRidership by Month:")
        month_ridership = df.groupby('Month')['Num_Riders'].sum()
        print(month_ridership)
        
        # Plot ridership by month
        plt.figure()
        month_ridership.plot(kind='line', marker='o')
        plt.title('Ridership by Month')
        plt.xlabel('Month')
        plt.ylabel('Number of Riders')
        plt.xticks(range(1, 13))
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/bivariate_month_ridership.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()

# 3.3 Multivariate Analysis
def multivariate_analysis(df):
    """Perform multivariate analysis on the dataset"""
    print("\n3.3 Multivariate Analysis:")
    
    # Ridership by station and day type
    if all(col in df.columns for col in ['Station_Name', 'Type_of_Day', 'Num_Riders']):
        print("\nRidership by Station and Day Type:")
        station_day_ridership = df.groupby(['Station_Name', 'Type_of_Day'])['Num_Riders'].sum().unstack()
        print(station_day_ridership.head(10))
        
        # Plot heatmap of top 10 stations by day type
        plt.figure(figsize=(12, 8))
        top_stations = df.groupby('Station_Name')['Num_Riders'].sum().nlargest(10).index
        heatmap_data = df[df['Station_Name'].isin(top_stations)].pivot_table(
            index='Station_Name', 
            columns='Type_of_Day', 
            values='Num_Riders', 
            aggfunc='sum'
        )
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='viridis')
        plt.title('Ridership by Station and Day Type (Top 10 Stations)')
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/multivariate_station_day_type.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()
    
    # Ridership by year and month (if date columns exist)
    if all(col in df.columns for col in ['Year', 'Month', 'Num_Riders']):
        print("\nRidership by Year and Month:")
        year_month_ridership = df.groupby(['Year', 'Month'])['Num_Riders'].sum().unstack()
        print(year_month_ridership)
        
        # Plot heatmap of ridership by year and month
        plt.figure(figsize=(12, 8))
        year_month_pivot = df.pivot_table(
            index='Year', 
            columns='Month', 
            values='Num_Riders', 
            aggfunc='sum'
        )
        sns.heatmap(year_month_pivot, annot=True, fmt='.0f', cmap='viridis')
        plt.title('Ridership by Year and Month')
        plt.xlabel('Month')
        plt.ylabel('Year')
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/multivariate_year_month.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()

# 3.4 Domain-Specific Analysis
def domain_specific_analysis(df):
    """Perform domain-specific analysis on the dataset"""
    print("\n3.4 Domain-Specific Analysis:")
    
    # Accessibility analysis
    if 'ADA' in df.columns:
        print("\nAccessibility Analysis:")
        ada_counts = df['ADA'].value_counts()
        print(f"Accessible stops: {ada_counts.get(True, 0)}")
        print(f"Non-accessible stops: {ada_counts.get(False, 0)}")
        
        # Plot pie chart of accessibility
        plt.figure()
        ada_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Proportion of ADA Accessible Stops')
        plt.ylabel('')  # Hide the ylabel
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/domain_ada_accessibility.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()
    
    # Line color analysis
    if 'Color' in df.columns and 'Num_Riders' in df.columns:
        print("\nLine Color Analysis:")
        color_ridership = df.groupby('Color')['Num_Riders'].sum().sort_values(ascending=False)
        print(color_ridership)
        
        # Plot bar chart of ridership by line color
        plt.figure()
        # Create a color map for CTA lines, handling special cases like Purple-Express
        color_map = {
            'Red': 'red',
            'Blue': 'blue',
            'Brown': 'brown',
            'Green': 'green',
            'Orange': 'orange',
            'Pink': 'pink',
            'Purple': 'purple',
            'Purple-Express': 'purple',
            'Yellow': 'yellow'
        }
        # Get colors for each bar based on line name
        bar_colors = [color_map.get(color, 'gray') for color in color_ridership.index]
        
        color_ridership.plot(kind='bar', color=bar_colors)
        plt.title('Ridership by Line Color')
        plt.xlabel('Line Color')
        plt.ylabel('Number of Riders')
        plt.tight_layout()
        # Save figure to file
        filename = f"{output_dir}/domain_line_color.png"
        plt.savefig(filename)
        print(f"Saved plot to {filename}")
        plt.close()

#############################################################
# Main Execution
#############################################################

def main():
    """Main function to execute the analysis"""
    try:
        # Load the data
        df = pd.read_csv(data_file)
        print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
        
        # 1. Data Understanding
        print("\n=== DATA UNDERSTANDING ===")
        examine_data_structure(df)
        check_missing_values(df)
        understand_variables(df)
        
        # 2. Data Cleaning
        print("\n=== DATA CLEANING ===")
        df = handle_missing_values(df)
        df = fix_data_types(df)
        df = remove_unnecessary_columns(df)
        
        # 3. Exploratory Analysis
        print("\n=== EXPLORATORY ANALYSIS ===")
        
        # Ask user which analyses to run
        print("\nSelect analyses to run:")
        print("1. Univariate Analysis")
        print("2. Bivariate Analysis")
        print("3. Multivariate Analysis")
        print("4. Domain-Specific Analysis")
        print("5. All Analyses")
        print("0. Exit")
        
        choice = input("Enter your choice (0-5): ")
        
        if choice == '1' or choice == '5':
            univariate_analysis(df)
        
        if choice == '2' or choice == '5':
            bivariate_analysis(df)
        
        if choice == '3' or choice == '5':
            multivariate_analysis(df)
        
        if choice == '4' or choice == '5':
            domain_specific_analysis(df)
        
        if choice == '0':
            print("Exiting analysis.")
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()

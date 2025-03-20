# CTA Train Tracker

A comprehensive data analysis tool for Chicago Transit Authority (CTA) train ridership data. This project provides tools to combine, analyze, and visualize CTA train data to understand ridership patterns across stations, time periods, and train lines.

## Project Overview

The CTA Train Tracker project consists of several components:

1. **Data Combination**: Combines multiple CSV files containing CTA data into a single comprehensive dataset
2. **Data Analysis**: Performs various analyses on the combined data to extract insights
3. **Visualization**: Creates informative visualizations to help understand ridership patterns

## Features

- Combines data from multiple CTA data sources (Lines, Stations, Stops, StopDetails, Ridership)
- Performs data cleaning and preprocessing
- Conducts four types of analysis:
  - Univariate Analysis: Examines distributions of individual variables
  - Bivariate Analysis: Explores relationships between pairs of variables
  - Multivariate Analysis: Analyzes complex relationships between multiple variables
  - Domain-Specific Analysis: Focuses on transit-specific aspects like accessibility and line performance
- Generates visualizations for all analyses
- Interactive menu for selecting which analyses to run

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cta-train-tracker.git
   cd cta-train-tracker
   ```

2. Install required dependencies:
   ```
   pip install pandas numpy matplotlib seaborn
   ```

## Usage

### Combining CSV Data

To combine the CSV files into a single dataset:

```
python combine_csv_data.py
```

This will create a `CTA_Combined_Data.csv` file containing the combined dataset.

### Running Analysis

To run the analysis on the combined data:

```
python cta_data_analysis.py
```

This will display an interactive menu where you can select which analyses to run:
1. Univariate Analysis
2. Bivariate Analysis
3. Multivariate Analysis
4. Domain-Specific Analysis
5. All Analyses
0. Exit

### Main Program

To run the main program which includes database queries and additional analysis:

```
python main.py
```

## Visualizations

All visualizations are saved to the `output_plots` directory with the following naming conventions:

- Univariate plots: `univariate_[type]_[variable].png`
- Bivariate plots: `bivariate_[focus].png`
- Multivariate plots: `multivariate_[focus].png`
- Domain-specific plots: `domain_[focus].png`

Key visualizations include:
- Top 10 stations by ridership
- Ridership by day type (weekday, Saturday, Sunday/holiday)
- Monthly ridership patterns
- Station and day type heatmap
- Year and month heatmap
- ADA accessibility pie chart
- Ridership by train line color

## Key Insights

The analysis helps understand:
- Which stations have the highest ridership
- How ridership varies by day of the week and month of the year
- Patterns across different train lines
- Accessibility of the CTA system

These insights can help with planning service improvements, understanding passenger behavior, and making data-driven decisions about the CTA system.

## Project Structure

- `combine_csv_data.py`: Script to combine multiple CSV files into a single dataset
- `cta_data_analysis.py`: Main analysis script with interactive menu
- `main.py`: Additional analysis and database queries
- `CTA_Combined_Data.csv`: Combined dataset created by the combine script
- `CTA_Tracker_Analysis_Plan.md`: Detailed plan for the data analysis
- `CTA_Analysis_Summary.md`: Summary of the analysis and key findings
- `output_plots/`: Directory containing all generated visualizations
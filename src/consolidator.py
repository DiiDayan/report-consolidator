import pandas as pd
import os
from pathlib import Path

def consolidate_reports(input_folder='data/input', output_folder='output'):
    """
    Reads all CSV files from a folder and consolidates them into a single file.
    Works with any CSV structure.
    """
    # Get all CSV files
    csv_files = list(Path(input_folder).glob('*.csv'))
    print(f"Files found: {len(csv_files)}")
    
    if len(csv_files) == 0:
        print("No CSV files found in the input folder.")
        return None
    
    # Read all files and store them in a list
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)
        print(f"Reading: {file.name} - Columns: {list(df.columns)}")
        dataframes.append(df)
    
    # Consolidate all into one
    consolidated_df = pd.concat(dataframes, ignore_index=True)
    print(f"\nTotal rows consolidated: {len(consolidated_df)}")
    print(f"Columns in consolidated file: {list(consolidated_df.columns)}")
    
    # Save consolidated file
    output_file = Path(output_folder) / 'consolidated_report.csv'
    consolidated_df.to_csv(output_file, index=False)
    print(f"File saved at: {output_file}")
    
    return consolidated_df

def calculate_statistics(df, numeric_columns=None):
    """
    Calculates basic statistics from the consolidated dataframe.
    If numeric_columns not specified, auto-detects numeric columns.
    """
    if df is None or len(df) == 0:
        print("No data to analyze.")
        return
    
    # Auto-detect numeric columns if not specified
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_columns) == 0:
        print("No numeric columns found for statistics.")
        return
    
    print("\n=== STATISTICS ===")
    for col in numeric_columns:
        print(f"\n{col.upper()}:")
        print(f"  Total: {df[col].sum():,.2f}")
        print(f"  Average: {df[col].mean():,.2f}")
        print(f"  Min: {df[col].min():,.2f}")
        print(f"  Max: {df[col].max():,.2f}")

def create_chart(df, x_column=None, y_columns=None, output_folder='output'):
    """
    Creates a chart with flexible column selection.
    If columns not specified, tries to auto-detect.
    """
    import matplotlib.pyplot as plt
    
    if df is None or len(df) == 0:
        print("No data to visualize.")
        return
    
    # Auto-detect columns if not specified
    if x_column is None:
        # Try to find a text/category column for X axis
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        if len(text_cols) > 0:
            x_column = text_cols[0]
        else:
            print("No suitable column found for X axis.")
            return
    
    if y_columns is None:
        # Use all numeric columns for Y axis
        y_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(y_columns) == 0:
        print("No numeric columns found for chart.")
        return
    
    # Create chart
    plt.figure(figsize=(12, 6))
    
    for col in y_columns:
        plt.plot(df[x_column], df[col], marker='o', label=col.capitalize(), linewidth=2)
    
    plt.xlabel(x_column.capitalize())
    plt.ylabel('Value')
    plt.title(f'{x_column.capitalize()} Analysis')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    
    # Save chart
    chart_file = Path(output_folder) / 'data_visualization.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"\nChart saved at: {chart_file}")

if __name__ == "__main__":
    # Consolidate reports
    df = consolidate_reports()
    
    if df is not None:
        # Calculate statistics (auto-detects numeric columns)
        calculate_statistics(df)
        
        # Create visualization (auto-detects suitable columns)
        create_chart(df)
        
        print("\n✓ Consolidation completed!")
        print("\nPreview of consolidated data:")
        print(df.head(10))
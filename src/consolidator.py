import pandas as pd
import os
from pathlib import Path

def consolidate_reports(input_folder='data/input', output_folder='output'):
    """
    Reads all CSV files from a folder and consolidates them into a single file.
    """
    # Get all CSV files
    csv_files = list(Path(input_folder).glob('*.csv'))
    print(f"Files found: {len(csv_files)}")
    
    # Read all files and store them in a list
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)
        print(f"Reading: {file.name}")
        dataframes.append(df)
    
    # Consolidate all into one
    consolidated_df = pd.concat(dataframes, ignore_index=True)
    print(f"\nTotal rows consolidated: {len(consolidated_df)}")
    
    # Save consolidated file
    output_file = Path(output_folder) / 'consolidated_report.csv'
    consolidated_df.to_csv(output_file, index=False)
    print(f"File saved at: {output_file}")
    
    return consolidated_df

def calculate_statistics(df):
    """
    Calculates basic statistics from the consolidated dataframe.
    """
    print("\n=== STATISTICS ===")
    print(f"Total sales: ${df['sales'].sum():,.0f}")
    print(f"Total expenses: ${df['expenses'].sum():,.0f}")
    print(f"Net profit: ${(df['sales'] - df['expenses']).sum():,.0f}")
    print(f"Average sales: ${df['sales'].mean():,.0f}")
    print(f"Average expenses: ${df['expenses'].mean():,.0f}")

def create_chart(df, output_folder='output'):
    """
    Creates a chart comparing sales vs expenses by month.
    """
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['month'], df['sales'], marker='o', label='Sales', linewidth=2)
    plt.plot(df['month'], df['expenses'], marker='s', label='Expenses', linewidth=2)
    plt.xlabel('Month')
    plt.ylabel('Amount ($)')
    plt.title('Sales vs Expenses by Month')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    
    # Save chart
    chart_file = Path(output_folder) / 'sales_expenses_chart.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"\nChart saved at: {chart_file}")

if __name__ == "__main__":
    df = consolidate_reports()
    calculate_statistics(df)
    create_chart(df)
    print("\n✓ Consolidation completed!")
    print(df)
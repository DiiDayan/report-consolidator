import pandas as pd
import os
from pathlib import Path
from metrics_calculator import calculate_marketing_metrics, get_platform_summary, get_performance_insights

def consolidate_reports(input_folder='data/input', output_folder='output'):
    """
    Reads all CSV files from a folder and consolidates them into a single file.
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
    
    # Calculate marketing metrics
    print("\nCalculating marketing KPIs...")
    consolidated_df = calculate_marketing_metrics(consolidated_df)
    
    # Save consolidated file with metrics
    output_file = Path(output_folder) / 'consolidated_report_with_metrics.csv'
    consolidated_df.to_csv(output_file, index=False)
    print(f"File saved at: {output_file}")
    
    return consolidated_df

def show_marketing_summary(df):
    """
    Display marketing performance summary by platform.
    """
    if df is None or len(df) == 0:
        print("No data to analyze.")
        return
    
    print("\n" + "="*60)
    print("MARKETING PERFORMANCE SUMMARY")
    print("="*60)
    
    # Get platform summary
    summary = get_platform_summary(df)
    
    if summary is not None:
        print("\nPlatform Performance:")
        print(summary.to_string())
        
        # Get insights
        insights = get_performance_insights(summary)
        if insights:
            print("\n" + "-"*60)
            print("KEY INSIGHTS:")
            print("-"*60)
            for insight in insights:
                print(insight)
    else:
        print("No platform data available for summary.")

def create_marketing_charts(df, output_folder='output'):
    """
    Creates marketing-focused visualizations.
    """
    import matplotlib.pyplot as plt
    
    if df is None or len(df) == 0:
        print("No data to visualize.")
        return
    
    if 'platform' not in df.columns:
        print("No platform column found for visualization.")
        return
    
    # Get aggregated data by platform
    summary = get_platform_summary(df)
    
    if summary is None:
        return
    
    # Determine which metrics we can visualize
    kpi_cols = ['ctr', 'cpc', 'cpm', 'cpa', 'conversion_rate']
    available_kpis = [col for col in kpi_cols if col in summary.columns]
    
    if len(available_kpis) == 0:
        print("No KPIs available for visualization.")
        return
    
    # Create subplots based on available KPIs
    n_plots = len(available_kpis)
    n_cols = 2
    n_rows = (n_plots + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 5 * n_rows))
    fig.suptitle('Marketing KPIs by Platform', fontsize=16, fontweight='bold')
    
    # Flatten axes for easy iteration
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
    
    for idx, kpi in enumerate(available_kpis):
        ax = axes[idx]
        summary[kpi].plot(kind='bar', ax=ax, color=colors[:len(summary)])
        
        # Format title
        kpi_title = kpi.upper().replace('_', ' ')
        ax.set_title(kpi_title, fontsize=12, fontweight='bold')
        ax.set_ylabel(kpi_title)
        ax.grid(True, alpha=0.3, axis='y')
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f')
    
    # Hide extra subplots
    for idx in range(len(available_kpis), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    # Save chart
    chart_file = Path(output_folder) / 'marketing_performance.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"\nChart saved at: {chart_file}")
    plt.close()

if __name__ == "__main__":
    # Consolidate reports and calculate metrics
    df = consolidate_reports()
    
    if df is not None:
        # Show marketing summary
        show_marketing_summary(df)
        
        # Create visualizations
        create_marketing_charts(df)
        
        print("\n✓ Marketing analysis completed!")
        
        # Show campaign-level summary if multiple campaigns exist
        if 'campaign' in df.columns:
            print("\nPerformance by Campaign:")
            campaign_summary = df.groupby('campaign')[['impressions', 'clicks', 'spend', 'conversions']].sum()
            
            # Recalculate KPIs for campaigns
            campaign_summary['ctr'] = (campaign_summary['clicks'] / campaign_summary['impressions'] * 100).round(2)
            campaign_summary['cpc'] = (campaign_summary['spend'] / campaign_summary['clicks']).round(2)
            campaign_summary['cpa'] = (campaign_summary['spend'] / campaign_summary['conversions']).round(2)
            campaign_summary['conversion_rate'] = (campaign_summary['conversions'] / campaign_summary['clicks'] * 100).round(2)
            
            print(campaign_summary.to_string())
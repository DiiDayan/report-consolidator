"""
Marketing Metrics Calculator
Calculates standard marketing KPIs from campaign data
"""

import pandas as pd
import numpy as np

def calculate_marketing_metrics(df):
    """
    Calculate marketing KPIs based on available columns.
    
    Returns:
        DataFrame with original data plus calculated metrics
    """
    df = df.copy()
    
    # Normalize column names (lowercase, strip spaces)
    df.columns = df.columns.str.lower().str.strip()
    
    # Map common variations to standard names
    column_mapping = {
        'cost': 'spend',
        'amount': 'spend',
        'impress': 'impressions',
        'views': 'impressions',
        'conv': 'conversions',
        'sales': 'conversions'
    }
    
    for old, new in column_mapping.items():
        for col in df.columns:
            if old in col and new not in df.columns:
                df.rename(columns={col: new}, inplace=True)
    
    # Calculate CTR (Click-Through Rate)
    if 'clicks' in df.columns and 'impressions' in df.columns:
        df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
    
    # Calculate CPC (Cost Per Click)
    if 'spend' in df.columns and 'clicks' in df.columns:
        df['cpc'] = (df['spend'] / df['clicks']).round(2)
        df['cpc'] = df['cpc'].replace([np.inf, -np.inf], np.nan)
    
    # Calculate CPM (Cost Per Mille/Thousand Impressions)
    if 'spend' in df.columns and 'impressions' in df.columns:
        df['cpm'] = (df['spend'] / df['impressions'] * 1000).round(2)
    
    # Calculate CPA (Cost Per Acquisition)
    if 'spend' in df.columns and 'conversions' in df.columns:
        df['cpa'] = (df['spend'] / df['conversions']).round(2)
        df['cpa'] = df['cpa'].replace([np.inf, -np.inf], np.nan)
    
    # Calculate Conversion Rate
    if 'conversions' in df.columns and 'clicks' in df.columns:
        df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(2)
        df['conversion_rate'] = df['conversion_rate'].replace([np.inf, -np.inf], np.nan)
    
    # Calculate ROAS (Return on Ad Spend)
    if 'revenue' in df.columns and 'spend' in df.columns:
        df['roas'] = (df['revenue'] / df['spend']).round(2)
        df['roas'] = df['roas'].replace([np.inf, -np.inf], np.nan)
    
    return df


def get_platform_summary(df):
    """
    Generate summary statistics by platform.
    
    Returns:
        DataFrame with aggregated metrics by platform
    """
    if 'platform' not in df.columns:
        return None
    
    # Columns to sum
    sum_cols = ['impressions', 'clicks', 'spend', 'conversions']
    sum_cols = [col for col in sum_cols if col in df.columns]
    
    # Group and aggregate
    summary = df.groupby('platform')[sum_cols].sum()
    
    # Recalculate KPIs on aggregated data
    if 'clicks' in summary.columns and 'impressions' in summary.columns:
        summary['ctr'] = (summary['clicks'] / summary['impressions'] * 100).round(2)
    
    if 'spend' in summary.columns and 'clicks' in summary.columns:
        summary['cpc'] = (summary['spend'] / summary['clicks']).round(2)
    
    if 'spend' in summary.columns and 'impressions' in summary.columns:
        summary['cpm'] = (summary['spend'] / summary['impressions'] * 1000).round(2)
    
    if 'spend' in summary.columns and 'conversions' in summary.columns:
        summary['cpa'] = (summary['spend'] / summary['conversions']).round(2)
    
    if 'conversions' in summary.columns and 'clicks' in summary.columns:
        summary['conversion_rate'] = (summary['conversions'] / summary['clicks'] * 100).round(2)
    
    return summary


def get_performance_insights(summary_df):
    """
    Generate actionable insights from platform summary.
    
    Returns:
        List of insight strings
    """
    insights = []
    
    if summary_df is None or len(summary_df) == 0:
        return insights
    
    # Best CTR
    if 'ctr' in summary_df.columns:
        best_ctr = summary_df['ctr'].idxmax()
        insights.append(f"✓ {best_ctr} has the highest CTR ({summary_df.loc[best_ctr, 'ctr']:.2f}%)")
    
    # Lowest CPC
    if 'cpc' in summary_df.columns:
        best_cpc = summary_df['cpc'].idxmin()
        insights.append(f"✓ {best_cpc} has the lowest CPC (${summary_df.loc[best_cpc, 'cpc']:.2f})")
    
    # Best conversion rate
    if 'conversion_rate' in summary_df.columns:
        best_conv = summary_df['conversion_rate'].idxmax()
        insights.append(f"✓ {best_conv} has the best conversion rate ({summary_df.loc[best_conv, 'conversion_rate']:.2f}%)")
    
    # Lowest CPA
    if 'cpa' in summary_df.columns:
        best_cpa = summary_df['cpa'].idxmin()
        insights.append(f"✓ {best_cpa} has the lowest CPA (${summary_df.loc[best_cpa, 'cpa']:.2f})")
    
    # Total spend distribution
    if 'spend' in summary_df.columns:
        total_spend = summary_df['spend'].sum()
        for platform in summary_df.index:
            pct = (summary_df.loc[platform, 'spend'] / total_spend * 100)
            insights.append(f"• {platform} represents {pct:.1f}% of total ad spend")
    
    return insights
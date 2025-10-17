"""
Marketing Statistics Analyzer
Provides statistically robust analysis of marketing campaign performance
Addresses the aggregate CTR limitation by showing both volume-weighted metrics
and campaign-level statistical distributions
"""

import pandas as pd
import numpy as np

def analyze_platform_statistics(df):
    """
    Analyzes marketing performance at both aggregate and campaign levels.
    
    This function addresses the statistical limitation of simple aggregation
    by showing:
    1. Aggregate metrics (volume-weighted) - useful for budget decisions
    2. Campaign-level statistics (mean, median, std) - useful for optimization
    3. Performance ranges - identifies best/worst performers
    
    Args:
        df: DataFrame with calculated marketing metrics (must include CTR, CPC, etc.)
    
    Returns:
        dict: Statistical summary by platform
    """
    
    if df.empty:
        print("⚠️  No data available for statistical analysis")
        return {}
    
    print("\n" + "="*70)
    print("📊 MARKETING PERFORMANCE STATISTICS")
    print("="*70)
    print("\nNote: Aggregate metrics are volume-weighted (useful for budget allocation)")
    print("      Campaign metrics show actual performance variability (useful for optimization)")
    print("="*70)
    
    stats_summary = {}
    
    for platform in sorted(df['platform'].unique()):
        platform_data = df[df['platform'] == platform]
        
        print(f"\n{'='*70}")
        print(f"🎯 {platform.upper()}")
        print(f"{'='*70}")
        
        # Basic counts
        n_campaigns = len(platform_data['campaign'].unique())
        n_days = len(platform_data)
        
        print(f"\n📈 Dataset Overview:")
        print(f"  • Number of campaigns: {n_campaigns}")
        print(f"  • Number of data points: {n_days}")
        
        # Aggregate metrics (volume-weighted)
        total_impressions = platform_data['impressions'].sum()
        total_clicks = platform_data['clicks'].sum()
        total_spend = platform_data['spend'].sum()
        total_conversions = platform_data['conversions'].sum()
        
        agg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        agg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        agg_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        agg_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
        
        print(f"\n💰 Volume Totals:")
        print(f"  • Total impressions: {total_impressions:,.0f}")
        print(f"  • Total clicks: {total_clicks:,.0f}")
        print(f"  • Total spend: ${total_spend:,.2f}")
        print(f"  • Total conversions: {total_conversions:,.0f}")
        
        # Campaign-level statistics for each metric
        print(f"\n📊 CTR (Click-Through Rate)")
        print(f"  • Aggregate CTR: {agg_ctr:.2f}% (volume-weighted)")
        if n_campaigns > 1:
            campaign_ctr_mean = platform_data['ctr'].mean()
            campaign_ctr_median = platform_data['ctr'].median()
            campaign_ctr_std = platform_data['ctr'].std()
            campaign_ctr_min = platform_data['ctr'].min()
            campaign_ctr_max = platform_data['ctr'].max()
            
            print(f"  • Campaign average: {campaign_ctr_mean:.2f}%")
            print(f"  • Campaign median: {campaign_ctr_median:.2f}%")
            print(f"  • Std deviation: {campaign_ctr_std:.2f}%")
            print(f"  • Range: {campaign_ctr_min:.2f}% - {campaign_ctr_max:.2f}%")
            
            if campaign_ctr_std > campaign_ctr_mean * 0.5:
                print(f"  ⚠️  High variability detected - review individual campaigns")
        
        print(f"\n💵 CPC (Cost Per Click)")
        print(f"  • Aggregate CPC: ${agg_cpc:.2f} (volume-weighted)")
        if n_campaigns > 1:
            campaign_cpc_mean = platform_data['cpc'].mean()
            campaign_cpc_median = platform_data['cpc'].median()
            campaign_cpc_std = platform_data['cpc'].std()
            campaign_cpc_min = platform_data['cpc'].min()
            campaign_cpc_max = platform_data['cpc'].max()
            
            print(f"  • Campaign average: ${campaign_cpc_mean:.2f}")
            print(f"  • Campaign median: ${campaign_cpc_median:.2f}")
            print(f"  • Std deviation: ${campaign_cpc_std:.2f}")
            print(f"  • Range: ${campaign_cpc_min:.2f} - ${campaign_cpc_max:.2f}")
        
        print(f"\n🎯 Conversion Rate")
        print(f"  • Aggregate conversion rate: {agg_conversion_rate:.2f}% (volume-weighted)")
        if n_campaigns > 1 and 'conversion_rate' in platform_data.columns:
            campaign_conv_mean = platform_data['conversion_rate'].mean()
            campaign_conv_median = platform_data['conversion_rate'].median()
            campaign_conv_std = platform_data['conversion_rate'].std()
            campaign_conv_min = platform_data['conversion_rate'].min()
            campaign_conv_max = platform_data['conversion_rate'].max()
            
            print(f"  • Campaign average: {campaign_conv_mean:.2f}%")
            print(f"  • Campaign median: {campaign_conv_median:.2f}%")
            print(f"  • Std deviation: {campaign_conv_std:.2f}%")
            print(f"  • Range: {campaign_conv_min:.2f}% - {campaign_conv_max:.2f}%")
        
        print(f"\n💰 CPA (Cost Per Acquisition)")
        print(f"  • Aggregate CPA: ${agg_cpa:.2f} (volume-weighted)")
        if n_campaigns > 1 and 'cpa' in platform_data.columns:
            campaign_cpa_mean = platform_data['cpa'].mean()
            campaign_cpa_median = platform_data['cpa'].median()
            campaign_cpa_std = platform_data['cpa'].std()
            campaign_cpa_min = platform_data['cpa'].min()
            campaign_cpa_max = platform_data['cpa'].max()
            
            print(f"  • Campaign average: ${campaign_cpa_mean:.2f}")
            print(f"  • Campaign median: ${campaign_cpa_median:.2f}")
            print(f"  • Std deviation: ${campaign_cpa_std:.2f}")
            print(f"  • Range: ${campaign_cpa_min:.2f} - ${campaign_cpa_max:.2f}")
        
        # Identify best and worst performing campaigns
        if n_campaigns > 1:
            print(f"\n🏆 Campaign Performance Highlights:")
            
            # Best CTR
            best_ctr_idx = platform_data['ctr'].idxmax()
            best_ctr_campaign = platform_data.loc[best_ctr_idx, 'campaign']
            best_ctr_value = platform_data.loc[best_ctr_idx, 'ctr']
            print(f"  • Best CTR: {best_ctr_campaign} ({best_ctr_value:.2f}%)")
            
            # Lowest CPC
            lowest_cpc_idx = platform_data['cpc'].idxmin()
            lowest_cpc_campaign = platform_data.loc[lowest_cpc_idx, 'campaign']
            lowest_cpc_value = platform_data.loc[lowest_cpc_idx, 'cpc']
            print(f"  • Lowest CPC: {lowest_cpc_campaign} (${lowest_cpc_value:.2f})")
            
            # Best conversion rate
            if 'conversion_rate' in platform_data.columns:
                best_conv_idx = platform_data['conversion_rate'].idxmax()
                best_conv_campaign = platform_data.loc[best_conv_idx, 'campaign']
                best_conv_value = platform_data.loc[best_conv_idx, 'conversion_rate']
                print(f"  • Best conversion rate: {best_conv_campaign} ({best_conv_value:.2f}%)")
        
        # Store summary for programmatic access
        stats_summary[platform] = {
            'n_campaigns': n_campaigns,
            'aggregate_ctr': agg_ctr,
            'aggregate_cpc': agg_cpc,
            'aggregate_conversion_rate': agg_conversion_rate,
            'aggregate_cpa': agg_cpa,
            'total_spend': total_spend
        }
        
        if n_campaigns > 1:
            stats_summary[platform].update({
                'campaign_ctr_mean': campaign_ctr_mean,
                'campaign_ctr_std': campaign_ctr_std,
                'campaign_cpc_mean': campaign_cpc_mean,
                'campaign_cpc_std': campaign_cpc_std
            })
    
    print("\n" + "="*70)
    print("📝 Statistical Notes:")
    print("="*70)
    print("""
• Aggregate metrics: Calculated from total impressions/clicks/spend
  - Useful for: Platform budget allocation decisions
  - Limitation: Large campaigns dominate, hiding variability
  
• Campaign metrics: Statistical distribution of daily/campaign performance
  - Useful for: Campaign optimization and identifying outliers
  - More robust: Shows true performance variation
  
• High std deviation (>50% of mean): Indicates inconsistent performance
  - Review individual campaigns for optimization opportunities
    """)
    
    return stats_summary


def compare_platforms(df):
    """
    Generates cross-platform comparison for strategic decisions.
    
    Args:
        df: DataFrame with calculated marketing metrics
    
    Returns:
        pd.DataFrame: Platform comparison table
    """
    
    print("\n" + "="*70)
    print("🔄 CROSS-PLATFORM COMPARISON")
    print("="*70)
    
    comparison = []
    
    for platform in df['platform'].unique():
        platform_data = df[df['platform'] == platform]
        
        total_impressions = platform_data['impressions'].sum()
        total_clicks = platform_data['clicks'].sum()
        total_spend = platform_data['spend'].sum()
        total_conversions = platform_data['conversions'].sum()
        
        agg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        agg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        agg_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
        
        comparison.append({
            'Platform': platform,
            'Total Spend': f"${total_spend:,.2f}",
            'Impressions': f"{total_impressions:,.0f}",
            'CTR': f"{agg_ctr:.2f}%",
            'CPC': f"${agg_cpc:.2f}",
            'CPA': f"${agg_cpa:.2f}",
            'Conversions': int(total_conversions)
        })
    
    comparison_df = pd.DataFrame(comparison)
    print("\n" + comparison_df.to_string(index=False))
    
    # Budget allocation insights
    total_budget = df['spend'].sum()
    print(f"\n💰 Budget Allocation:")
    for platform in df['platform'].unique():
        platform_spend = df[df['platform'] == platform]['spend'].sum()
        percentage = (platform_spend / total_budget * 100)
        print(f"  • {platform}: ${platform_spend:,.2f} ({percentage:.1f}%)")
    
    return comparison_df


def export_statistics_report(df, output_path='output/statistics_report.txt'):
    """
    Exports detailed statistics report to a text file.
    
    Args:
        df: DataFrame with marketing metrics
        output_path: Path to save the report
    """
    import sys
    from io import StringIO
    
    # Capture print output
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    analyze_platform_statistics(df)
    compare_platforms(df)
    
    report_content = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write(report_content)
    
    print(f"\n✅ Statistics report exported to: {output_path}")
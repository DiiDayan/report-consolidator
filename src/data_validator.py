"""
Data Quality Validator
Checks for common data quality issues in marketing campaign data
"""

import pandas as pd
import numpy as np

def validate_data(df):
    """
    Validates data quality and returns a report of issues found.
    
    Returns:
        dict: Validation report with issues found
    """
    report = {
        'empty_columns': [],
        'duplicate_rows': 0,
        'missing_values': {},
        'inconsistencies': [],
        'has_issues': False
    }
    
    # Check for empty columns
    for col in df.columns:
        if df[col].isna().all():
            report['empty_columns'].append(col)
            report['has_issues'] = True
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        report['duplicate_rows'] = duplicates
        report['has_issues'] = True
    
    # Check for missing values
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            missing_pct = (missing / len(df) * 100)
            report['missing_values'][col] = {
                'count': missing,
                'percentage': round(missing_pct, 2)
            }
            if missing_pct > 5:  # Flag if >5% missing
                report['has_issues'] = True
    
    # Check for inconsistencies in numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        # Check for negative values where they shouldn't exist
        if col in ['impressions', 'clicks', 'spend', 'conversions']:
            negatives = (df[col] < 0).sum()
            if negatives > 0:
                report['inconsistencies'].append(
                    f"{col} has {negatives} negative values"
                )
                report['has_issues'] = True
    
    # Check for zero spend with conversions (OUTSIDE the loop)
    if 'spend' in df.columns and 'conversions' in df.columns:
        zero_spend_conv = ((df['spend'] == 0) & (df['conversions'] > 0)).sum()
        if zero_spend_conv > 0:
            report['inconsistencies'].append(
                f"{zero_spend_conv} rows have conversions but zero spend"
            )
            report['has_issues'] = True
    
    return report

def print_validation_report(report):
    """
    Prints a formatted validation report.
    """
    print("\n" + "="*60)
    print("DATA QUALITY REPORT")
    print("="*60)
    
    if not report['has_issues']:
        print("\n✓ No significant data quality issues found!")
        return
    
    # Empty columns
    if report['empty_columns']:
        print("\n⚠️  Empty Columns:")
        for col in report['empty_columns']:
            print(f"  - {col}")
    
    # Duplicate rows
    if report['duplicate_rows'] > 0:
        print(f"\n⚠️  Duplicate Rows: {report['duplicate_rows']}")
    
    # Missing values
    if report['missing_values']:
        print("\n⚠️  Missing Values:")
        for col, info in report['missing_values'].items():
            if info['percentage'] > 5:
                print(f"  - {col}: {info['count']} ({info['percentage']}%)")
    
    # Inconsistencies
    if report['inconsistencies']:
        print("\n⚠️  Data Inconsistencies:")
        for issue in report['inconsistencies']:
            print(f"  - {issue}")
    
    print("\n" + "-"*60)
    print("Recommendation: Review flagged issues before analysis")
    print("-"*60)

def clean_data(df, remove_duplicates=True, fill_missing=False):
    """
    Cleans data based on validation findings.
    
    Args:
        df: DataFrame to clean
        remove_duplicates: Whether to remove duplicate rows
        fill_missing: Whether to fill missing numeric values with 0
    
    Returns:
        Cleaned DataFrame
    """
    df_clean = df.copy()
    
    # Remove empty columns
    empty_cols = [col for col in df_clean.columns if df_clean[col].isna().all()]
    if empty_cols:
        df_clean = df_clean.drop(columns=empty_cols)
        print(f"Removed {len(empty_cols)} empty columns")
    
    # Remove duplicates
    if remove_duplicates:
        before = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        removed = before - len(df_clean)
        if removed > 0:
            print(f"Removed {removed} duplicate rows")
    
    # Fill missing values
    if fill_missing:
        numeric_cols = df_clean.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if df_clean[col].isna().any():
                df_clean[col] = df_clean[col].fillna(0)
                print(f"Filled missing values in {col} with 0")
    
    return df_clean
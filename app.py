import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import sys
from io import StringIO

# Import from src directory
from src.metrics_calculator import calculate_marketing_metrics
from src.consolidator import get_platform_summary, get_performance_insights
from src.statistics_analyzer import analyze_platform_statistics, compare_platforms, export_statistics_report

st.set_page_config(
    page_title="Marketing Performance Consolidator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Marketing Performance Consolidator")
st.markdown("Upload CSV/Excel files with marketing campaign data to consolidate and analyze performance.")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Campaign Files")
    uploaded_files = st.file_uploader(
        "Choose CSV or Excel files",
        type=['csv', 'xlsx'],
        accept_multiple_files=True
    )
    
    st.markdown("---")
    st.markdown("### 📋 Expected Columns:")
    st.code("""
date
campaign
impressions
clicks
spend
conversions
platform
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ How it works:")
    st.markdown("""
1. Upload campaign data files
2. Files are consolidated automatically
3. KPIs calculated (CTR, CPC, CPA, etc.)
4. View detailed statistics
5. Download results
    """)

# Main content
if uploaded_files:
    st.success(f"✓ {len(uploaded_files)} file(s) uploaded successfully")
    
    # Consolidate button
    if st.button("🚀 Analyze Campaign Data", type="primary", use_container_width=True):
        with st.spinner("Consolidating and calculating KPIs..."):
            # Read and consolidate
            dataframes = []
            for file in uploaded_files:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:  # .xlsx
                    df = pd.read_excel(file, engine='openpyxl')
                dataframes.append(df)
                file.seek(0)
            
            consolidated_df = pd.concat(dataframes, ignore_index=True)
            
            # Calculate marketing metrics
            consolidated_df = calculate_marketing_metrics(consolidated_df)
            
            # Store in session state
            st.session_state['consolidated_df'] = consolidated_df
            
            st.success("✓ Analysis completed!")
    
    # Display results if available
    if 'consolidated_df' in st.session_state:
        df = st.session_state['consolidated_df']
        
        st.markdown("---")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Statistics", "📋 Data Table", "📈 Visualizations"])
        
        with tab1:
            st.header("📊 Campaign Performance Statistics")
            
            # Capture the output from statistics_analyzer
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Call the statistics functions
            analyze_platform_statistics(df)
            
            # Get the output
            stats_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Display in a code block for better formatting
            st.text(stats_output)
            
            # Also show the comparison table
            st.markdown("---")
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            compare_platforms(df)
            
            comparison_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            st.text(comparison_output)
        
        with tab2:
            st.subheader("📋 Consolidated Data")
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total rows: {len(df)} | Columns: {', '.join(df.columns)}")
            
            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Consolidated CSV",
                data=csv,
                file_name="consolidated_report_with_metrics.csv",
                mime="text/csv",
            )
        
        with tab3:
            st.subheader("📈 Performance Visualizations")
            
            # Check if we have platform data
            if 'platform' in df.columns:
                summary = get_platform_summary(df)
                
                if summary is not None:
                    # Let user select KPIs to visualize
                    kpi_cols = ['ctr', 'cpc', 'cpm', 'cpa', 'conversion_rate']
                    available_kpis = [col for col in kpi_cols if col in summary.columns]
                    
                    selected_kpis = st.multiselect(
                        "Select KPIs to visualize",
                        available_kpis,
                        default=available_kpis[:3] if len(available_kpis) >= 3 else available_kpis
                    )
                    
                    if selected_kpis:
                        # Create charts
                        n_plots = len(selected_kpis)
                        cols = st.columns(min(n_plots, 2))
                        
                        colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
                        
                        for idx, kpi in enumerate(selected_kpis):
                            with cols[idx % 2]:
                                fig, ax = plt.subplots(figsize=(6, 4))
                                summary.reset_index()[[kpi]].plot(
                                    kind='bar',
                                    ax=ax,
                                    color=colors[idx % len(colors)],
                                    legend=False
                                )
                                ax.set_title(f'{kpi.upper()} by Platform', fontsize=12, fontweight='bold')
                                ax.set_xlabel('Platform')
                                ax.set_ylabel(kpi.upper())
                                plt.xticks(rotation=45)
                                plt.tight_layout()
                                st.pyplot(fig)
                                plt.close()
            else:
                st.info("No platform column found for visualizations")

else:
    st.info("👈 Upload campaign files to get started")
    
    # Show example format
    st.markdown("### 📄 Example Data Format")
    example_data = {
        'date': ['2025-01-15', '2025-01-16'],
        'campaign': ['Winter_Sale', 'Winter_Sale'],
        'impressions': [32000, 30500],
        'clicks': [850, 820],
        'spend': [320, 310],
        'conversions': [22, 20],
        'platform': ['Google', 'Google']
    }
    st.dataframe(pd.DataFrame(example_data))
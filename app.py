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

# Custom CSS for better tab styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        font-size: 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

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
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Detailed Statistics", "📋 Data Table", "🎨 Visualizations"])
        
        with tab1:
            st.header("🎯 Platform Performance Summary")
            
            # Check if we have platform data
            if 'platform' in df.columns:
                summary = get_platform_summary(df)
                
                if summary is not None:
                    # Display summary table
                    st.dataframe(summary.style.format("{:.2f}"), use_container_width=True)
                    
                    # Key Insights
                    insights = get_performance_insights(summary)
                    if insights:
                        st.markdown("### 💡 Key Insights")
                        col1, col2 = st.columns(2)
                        
                        for idx, insight in enumerate(insights):
                            with col1 if idx % 2 == 0 else col2:
                                if "✓" in insight:
                                    st.success(insight)
                                else:
                                    st.info(insight)
            
            # Download buttons
            st.markdown("---")
            st.subheader("📥 Downloads")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Consolidated CSV",
                    data=csv,
                    file_name="consolidated_report_with_metrics.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Statistics report download
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                analyze_platform_statistics(df)
                compare_platforms(df)
                
                report_content = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                st.download_button(
                    label="📄 Download Statistics Report",
                    data=report_content,
                    file_name="statistics_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with tab2:
            st.header("📊 Campaign Performance Statistics")
            st.markdown("Detailed statistical analysis showing both aggregate (volume-weighted) and campaign-level metrics.")
            
            # Show statistics for each platform
            platforms = df['platform'].unique() if 'platform' in df.columns else []
            
            for platform in sorted(platforms):
                platform_data = df[df['platform'] == platform]
                
                with st.expander(f"🎯 {platform.upper()} - Detailed Metrics", expanded=True):
                    # Calculate metrics
                    n_campaigns = len(platform_data['campaign'].unique())
                    total_impressions = platform_data['impressions'].sum()
                    total_clicks = platform_data['clicks'].sum()
                    total_spend = platform_data['spend'].sum()
                    total_conversions = platform_data['conversions'].sum()
                    
                    # Aggregate metrics
                    agg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                    agg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
                    agg_conv_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
                    agg_cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
                    
                    # Display metrics in columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Impressions", f"{total_impressions:,.0f}")
                        st.metric("Aggregate CTR", f"{agg_ctr:.2f}%")
                    
                    with col2:
                        st.metric("Total Clicks", f"{total_clicks:,.0f}")
                        st.metric("Aggregate CPC", f"${agg_cpc:.2f}")
                    
                    with col3:
                        st.metric("Total Spend", f"${total_spend:,.2f}")
                        st.metric("Aggregate CPA", f"${agg_cpa:.2f}")
                    
                    with col4:
                        st.metric("Total Conversions", f"{total_conversions:,.0f}")
                        st.metric("Conversion Rate", f"{agg_conv_rate:.2f}%")
                    
                    # Campaign-level statistics if multiple campaigns
                    if n_campaigns > 1:
                        st.markdown("---")
                        st.markdown("**📊 Campaign-Level Statistics**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**CTR Distribution**")
                            st.write(f"• Mean: {platform_data['ctr'].mean():.2f}%")
                            st.write(f"• Median: {platform_data['ctr'].median():.2f}%")
                            st.write(f"• Std Dev: {platform_data['ctr'].std():.2f}%")
                            st.write(f"• Range: {platform_data['ctr'].min():.2f}% - {platform_data['ctr'].max():.2f}%")
                            
                            if platform_data['ctr'].std() > platform_data['ctr'].mean() * 0.5:
                                st.warning("⚠️ High variability - review individual campaigns")
                        
                        with col2:
                            st.markdown("**CPC Distribution**")
                            st.write(f"• Mean: ${platform_data['cpc'].mean():.2f}")
                            st.write(f"• Median: ${platform_data['cpc'].median():.2f}")
                            st.write(f"• Std Dev: ${platform_data['cpc'].std():.2f}")
                            st.write(f"• Range: ${platform_data['cpc'].min():.2f} - ${platform_data['cpc'].max():.2f}")
                        
                        st.markdown("---")
                        st.markdown("**🏆 Best Performers**")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            best_ctr_idx = platform_data['ctr'].idxmax()
                            st.success(f"**Best CTR:** {platform_data.loc[best_ctr_idx, 'campaign']}")
                            st.write(f"{platform_data.loc[best_ctr_idx, 'ctr']:.2f}%")
                        
                        with col2:
                            best_cpc_idx = platform_data['cpc'].idxmin()
                            st.success(f"**Lowest CPC:** {platform_data.loc[best_cpc_idx, 'campaign']}")
                            st.write(f"${platform_data.loc[best_cpc_idx, 'cpc']:.2f}")
                        
                        with col3:
                            if 'conversion_rate' in platform_data.columns:
                                best_conv_idx = platform_data['conversion_rate'].idxmax()
                                st.success(f"**Best Conv. Rate:** {platform_data.loc[best_conv_idx, 'campaign']}")
                                st.write(f"{platform_data.loc[best_conv_idx, 'conversion_rate']:.2f}%")
            
            # Show comparison table
            st.markdown("---")
            st.subheader("🔄 Cross-Platform Comparison")
            
            summary = get_platform_summary(df)
            if summary is not None:
                st.dataframe(summary.style.format("{:.2f}"), use_container_width=True)
                
                # Budget allocation
                st.markdown("**💰 Budget Allocation:**")
                total_budget = df['spend'].sum()
                for platform in sorted(platforms):
                    platform_spend = df[df['platform'] == platform]['spend'].sum()
                    percentage = (platform_spend / total_budget * 100)
                    st.write(f"• {platform}: ${platform_spend:,.2f} ({percentage:.1f}%)")
        
        with tab3:
            st.subheader("📋 Consolidated Data")
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total rows: {len(df)} | Columns: {', '.join(df.columns)}")
        
        with tab4:
            st.subheader("🎨 Performance Visualizations")
            
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
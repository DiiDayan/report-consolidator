import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import sys
from pathlib import Path

# Add src to path to import our modules
sys.path.append(str(Path(__file__).parent / 'src'))
from metrics_calculator import calculate_marketing_metrics, get_platform_summary, get_performance_insights

st.set_page_config(
    page_title="Marketing Performance Consolidator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Marketing Performance Consolidator")
st.markdown("**Unified analytics for multi-platform ad campaigns**")
st.markdown("Upload your campaign data from Facebook, Google, LinkedIn, and other platforms to get instant KPI analysis.")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Campaign Data")
    uploaded_files = st.file_uploader(
    "Choose CSV or Excel files",
    type=['csv', 'xlsx'],
    accept_multiple_files=True,
    help="Upload campaign reports from different ad platforms"
    )   
    
    st.markdown("---")
    st.markdown("### 📈 What you'll get:")
    st.markdown("✓ Automatic KPI calculation (CTR, CPC, CPA)")
    st.markdown("✓ Cross-platform comparison")
    st.markdown("✓ Actionable insights")
    st.markdown("✓ Downloadable reports")
    
    st.markdown("---")
    st.markdown("### 🎯 Supported metrics:")
    st.caption("Impressions • Clicks • Spend • Conversions")

# Main content
if uploaded_files:
    st.success(f"✓ {len(uploaded_files)} file(s) uploaded successfully")
    
    # Preview section
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
    
    # Consolidate button
    if st.button("🚀 Analyze Campaign Data", type="primary", use_container_width=True):
        with st.spinner("Consolidating and calculating KPIs..."):
            # Read and consolidate
            dataframes = []
            for file in uploaded_files:
                df = pd.read_csv(file)
                dataframes.append(df)
                file.seek(0)
            
            consolidated_df = pd.concat(dataframes, ignore_index=True)
            
            # Calculate marketing metrics
            consolidated_df = calculate_marketing_metrics(consolidated_df)
            
            # Store in session state
            st.session_state['consolidated_df'] = consolidated_df
            st.success("✓ Analysis completed!")
    
    # Display results
    if 'consolidated_df' in st.session_state:
        df = st.session_state['consolidated_df']
        
        st.markdown("---")
        
        # Check if we have platform data
        has_platform = 'platform' in df.columns
        
        if has_platform:
            # Platform Performance Section
            st.header("🎯 Platform Performance")
            
            summary = get_platform_summary(df)
            
            if summary is not None:
                # Display summary table
                st.dataframe(summary.style.format("{:.2f}"), use_container_width=True)
                
                # Key Insights
                insights = get_performance_insights(summary)
                if insights:
                    st.markdown("### 💡 Key Insights")
                    for insight in insights:
                        if "✓" in insight:
                            st.success(insight)
                        else:
                            st.info(insight)
                
                # Visualizations
                st.markdown("### 📊 KPI Comparison")
                
                kpi_cols = ['ctr', 'cpc', 'cpm', 'cpa', 'conversion_rate']
                available_kpis = [col for col in kpi_cols if col in summary.columns]
                
                if available_kpis:
                    # Let user select which KPIs to visualize
                    selected_kpis = st.multiselect(
                        "Select KPIs to visualize",
                        available_kpis,
                        default=available_kpis[:3]
                    )
                    
                    if selected_kpis:
                        n_plots = len(selected_kpis)
                        cols = st.columns(min(n_plots, 2))
                        
                        colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
                        
                        for idx, kpi in enumerate(selected_kpis):
                            with cols[idx % 2]:
                                fig, ax = plt.subplots(figsize=(6, 4))
                                summary[kpi].plot(kind='bar', ax=ax, color=colors[:len(summary)])
                                
                                kpi_title = kpi.upper().replace('_', ' ')
                                ax.set_title(kpi_title, fontsize=12, fontweight='bold')
                                ax.set_ylabel(kpi_title)
                                ax.grid(True, alpha=0.3, axis='y')
                                ax.tick_params(axis='x', rotation=45)
                                
                                # Add value labels
                                for container in ax.containers:
                                    ax.bar_label(container, fmt='%.2f')
                                
                                plt.tight_layout()
                                st.pyplot(fig)
                                plt.close()
        
        # Campaign Performance (if available)
        if 'campaign' in df.columns:
            st.markdown("---")
            st.header("🎬 Campaign Performance")
            
            campaign_cols = ['impressions', 'clicks', 'spend', 'conversions']
            campaign_cols = [col for col in campaign_cols if col in df.columns]
            
            if campaign_cols:
                campaign_summary = df.groupby('campaign')[campaign_cols].sum()
                
                # Calculate KPIs
                if 'clicks' in campaign_summary.columns and 'impressions' in campaign_summary.columns:
                    campaign_summary['ctr'] = (campaign_summary['clicks'] / campaign_summary['impressions'] * 100).round(2)
                
                if 'spend' in campaign_summary.columns and 'clicks' in campaign_summary.columns:
                    campaign_summary['cpc'] = (campaign_summary['spend'] / campaign_summary['clicks']).round(2)
                
                if 'spend' in campaign_summary.columns and 'conversions' in campaign_summary.columns:
                    campaign_summary['cpa'] = (campaign_summary['spend'] / campaign_summary['conversions']).round(2)
                
                if 'conversions' in campaign_summary.columns and 'clicks' in campaign_summary.columns:
                    campaign_summary['conversion_rate'] = (campaign_summary['conversions'] / campaign_summary['clicks'] * 100).round(2)
                
                st.dataframe(campaign_summary.style.format("{:.2f}"), use_container_width=True)
        
        # Download Section
        st.markdown("---")
        st.header("⬇️ Download Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download consolidated data with metrics
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Full Report (CSV)",
                data=csv,
                file_name="marketing_report_with_kpis.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Download platform summary
            if has_platform and summary is not None:
                summary_csv = summary.to_csv().encode('utf-8')
                st.download_button(
                    label="📊 Download Platform Summary (CSV)",
                    data=summary_csv,
                    file_name="platform_summary.csv",
                    mime="text/csv",
                    use_container_width=True
                )

else:
    # Welcome screen
    st.info("👈 Upload your campaign CSV files to get started")
    
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        ### What this tool does:
        
        1. **Upload** campaign data from multiple platforms (Facebook Ads, Google Ads, LinkedIn Ads, etc.)
        2. **Consolidate** all data into a single view
        3. **Calculate** essential marketing KPIs automatically:
           - **CTR** (Click-Through Rate): How engaging are your ads?
           - **CPC** (Cost Per Click): How much are you paying per click?
           - **CPM** (Cost Per Mille): Cost per 1,000 impressions
           - **CPA** (Cost Per Acquisition): How much does each conversion cost?
           - **Conversion Rate**: What % of clicks convert?
        4. **Compare** performance across platforms
        5. **Download** reports with all calculated metrics
        
        ### Example use case:
        
        You're running a campaign on Facebook, Google, and LinkedIn. Each platform gives you a CSV export.
        Upload all three files here, and instantly see:
        - Which platform has the best CTR
        - Where your CPC is lowest
        - Which platform delivers the best conversion rate
        - How your budget is distributed
        
        **No more spreadsheet juggling. Just insights.**
        """)
    
    with st.expander("📋 Required data format"):
        st.markdown("""
        Your CSV files should include some combination of these columns:
        
        **Essential:**
        - `impressions` (or `views`)
        - `clicks`
        - `spend` (or `cost`)
        - `conversions` (or `sales`)
        
        **Optional but recommended:**
        - `platform` (Facebook, Google, LinkedIn, etc.)
        - `campaign` (campaign name)
        - `date`
        
        The tool automatically detects and normalizes column names, so slight variations are OK.
        """)

# Footer
st.markdown("---")
st.caption("Built with Python • Pandas • Streamlit | Focused on practical marketing analytics")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
    page_title="CSV Report Consolidator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV Report Consolidator")
st.markdown("Upload multiple CSV files to consolidate, analyze, and visualize your data.")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Choose CSV files",
        type=['csv'],
        accept_multiple_files=True
    )
    
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("1. Upload one or more CSV files")
    st.markdown("2. Review the data preview")
    st.markdown("3. Click 'Consolidate' to combine files")
    st.markdown("4. View statistics and charts")
    st.markdown("5. Download consolidated report")

# Main content
if uploaded_files:
    st.success(f"✓ {len(uploaded_files)} file(s) uploaded")
    
    # Preview section
    with st.expander("📄 Preview uploaded files", expanded=True):
        for file in uploaded_files:
            st.subheader(f"📁 {file.name}")
            df_preview = pd.read_csv(file)
            st.dataframe(df_preview.head(), use_container_width=True)
            st.caption(f"Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")
            file.seek(0)  # Reset file pointer
    
    # Consolidate button
    if st.button("🔄 Consolidate Data", type="primary"):
        with st.spinner("Consolidating files..."):
            # Read and consolidate all files
            dataframes = []
            for file in uploaded_files:
                df = pd.read_csv(file)
                dataframes.append(df)
                file.seek(0)
            
            consolidated_df = pd.concat(dataframes, ignore_index=True)
            
            # Store in session state
            st.session_state['consolidated_df'] = consolidated_df
            st.success("✓ Files consolidated successfully!")
    
    # Display results if consolidated
    if 'consolidated_df' in st.session_state:
        df = st.session_state['consolidated_df']
        
        st.markdown("---")
        st.header("📊 Consolidated Data")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Data", "📈 Statistics", "📊 Visualizations"])
        
        with tab1:
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total rows: {len(df)} | Columns: {', '.join(df.columns)}")
            
            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Consolidated CSV",
                data=csv,
                file_name="consolidated_report.csv",
                mime="text/csv",
            )
        
        with tab2:
            st.subheader("Statistical Summary")
            
            # Numeric columns statistics
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) > 0:
                col1, col2 = st.columns(2)
                
                for idx, col in enumerate(numeric_cols):
                    with col1 if idx % 2 == 0 else col2:
                        st.metric(
                            label=f"{col.upper()} - Total",
                            value=f"${df[col].sum():,.2f}"
                        )
                        st.metric(
                            label=f"{col.upper()} - Average",
                            value=f"${df[col].mean():,.2f}"
                        )
                        with st.expander(f"More details for {col}"):
                            st.write(f"**Min:** ${df[col].min():,.2f}")
                            st.write(f"**Max:** ${df[col].max():,.2f}")
                            st.write(f"**Median:** ${df[col].median():,.2f}")
                            st.write(f"**Std Dev:** ${df[col].std():,.2f}")
            else:
                st.info("No numeric columns found for statistical analysis.")
        
        with tab3:
            st.subheader("Data Visualizations")
            
            # Auto-detect columns for visualization
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(text_cols) > 0 and len(numeric_cols) > 0:
                # Column selection
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis (Category)", text_cols, index=0)
                with col2:
                    y_cols = st.multiselect("Y-axis (Values)", numeric_cols, default=numeric_cols)
                
                if y_cols:
                    # Create chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    for col in y_cols:
                        ax.plot(df[x_col], df[col], marker='o', label=col.capitalize(), linewidth=2)
                    
                    ax.set_xlabel(x_col.capitalize())
                    ax.set_ylabel('Value')
                    ax.set_title(f'{x_col.capitalize()} Analysis')
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    st.pyplot(fig)
                    
                    # Download chart
                    buf = BytesIO()
                    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                    buf.seek(0)
                    st.download_button(
                        label="⬇️ Download Chart",
                        data=buf,
                        file_name="data_visualization.png",
                        mime="image/png"
                    )
            else:
                st.info("Need both text and numeric columns for visualization.")

else:
    st.info("👈 Upload CSV files using the sidebar to get started")
    
    # Example/demo section
    with st.expander("ℹ️ What can this tool do?"):
        st.markdown("""
        **This tool helps you:**
        - 📁 Consolidate multiple CSV files into one
        - 📊 Automatically analyze numeric data
        - 📈 Generate visualizations
        - ⬇️ Download consolidated reports
        
        **Perfect for:**
        - Monthly sales reports
        - Multi-source data combination
        - Quick data analysis
        - Executive reporting
        """)

# Footer
st.markdown("---")
st.caption("Created with Python, Pandas, Matplotlib, and Streamlit")
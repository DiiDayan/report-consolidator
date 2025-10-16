# 📊 Marketing Performance Consolidator

**Unified analytics for multi-platform ad campaigns**

Stop juggling spreadsheets from Facebook, Google, and LinkedIn. Consolidate your ad data, calculate essential KPIs automatically, and make informed budget decisions—all in one tool.

---

## ✨ Key Features

### **Automatic KPI Calculation**
- **CTR** (Click-Through Rate) - Ad engagement metric
- **CPC** (Cost Per Click) - Click efficiency
- **CPM** (Cost Per Mille) - Impression cost
- **CPA** (Cost Per Acquisition) - Conversion cost
- **Conversion Rate** - Click-to-conversion efficiency

### **Cross-Platform Analysis**
- Consolidate data from Facebook Ads, Google Ads, LinkedIn Ads, and more
- Compare performance metrics across platforms
- Identify best-performing channels instantly

### **Actionable Insights**
- Automatic detection of best/worst performers
- Budget distribution analysis
- Performance recommendations

### **Two Interfaces**
- **Web App**: Drag-and-drop interface for non-technical users
- **CLI**: Command-line tool for automation and scripting

---

## 🎯 Who Is This For?

- **Marketing Managers** running multi-platform campaigns
- **Growth Marketers** optimizing ad spend
- **Digital Marketing Freelancers** managing client campaigns
- **Small Marketing Agencies** needing quick reporting

---

## 🚀 Quick Start

### Web Interface (Recommended)

```bash
# Clone and setup
git clone https://github.com/DiiDayan/report-consolidator.git
cd report-consolidator
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Launch web app
streamlit run app.py
```

Open your browser, upload your CSV files, and get instant insights.

### Command Line

```bash
# Place CSV files in data/input/
python3 src/consolidator.py

# Find results in output/
# - consolidated_report_with_metrics.csv
# - marketing_performance.png
```

---

## 📊 Example Output

### Platform Performance Summary
```
Platform Performance:
          impressions  clicks  spend  conversions   ctr   cpc    cpm    cpa  conversion_rate
platform                                                                                    
Facebook       254600    2546   1025           60  1.00  0.40   4.03  17.08             2.36
Google         161600    4250   1605          111  2.63  0.38   9.93  14.46             2.61
LinkedIn        60000     904    756           42  1.51  0.84  12.60  18.00             4.65
```

### Key Insights (Auto-Generated)
- ✓ Google has the highest CTR (2.63%)
- ✓ Google has the lowest CPC ($0.38)
- ✓ LinkedIn has the best conversion rate (4.65%)
- ✓ Google has the lowest CPA ($14.46)

### Visual KPI Comparison
Interactive charts showing CTR, CPC, CPA, and conversion rate across all platforms.

---

## 📸 Screenshots

### Welcome Screen
![Welcome Screen](docs/screenshots/1_welcome.png)

### Platform Performance Analysis
![Platform Performance](docs/screenshots/2_platform_performance.png)

### KPI Visualizations
![KPI Charts](docs/screenshots/3_kpi_charts.png)

### Campaign Performance
![Campaign Summary](docs/screenshots/4_campaign_summary.png)

### Export Options
![Download Reports](docs/screenshots/5_download.png)

---

## 📁 Data Format

Your CSV files should include these columns (common variations are auto-detected):

**Essential:**
- `impressions` (or `views`, `impress`)
- `clicks`
- `spend` (or `cost`, `amount`)
- `conversions` (or `sales`, `conv`)

**Recommended:**
- `platform` (Facebook, Google, LinkedIn, etc.) - for cross-platform comparison
- `campaign` - for campaign-level analysis
- `date` - for time-series analysis

**The tool automatically:**
- Normalizes column names (handles variations)
- Detects and groups by platform
- Calculates all relevant KPIs
- Generates insights

---

## 🛠️ Technologies

- **Python 3.8+** - Core language
- **Pandas** - Data manipulation and KPI calculation
- **Matplotlib** - Visualization
- **Streamlit** - Interactive web interface
- **NumPy** - Numerical operations

---

## 📈 Use Case Example

### The Problem
You run a Winter Sale campaign across three platforms:
- Facebook Ads → `facebook_ads_jan.csv`
- Google Ads → `google_ads_jan.csv`
- LinkedIn Ads → `linkedin_ads_jan.csv`

Each platform gives you different CSV formats. You need to:
- See total performance across all platforms
- Compare which platform is most cost-effective
- Decide where to allocate more budget

### The Solution
1. Upload all three CSV files to the tool
2. Get instant consolidated view with calculated KPIs
3. See insights like "Google has lowest CPC but LinkedIn has best conversion rate"
4. Make data-driven budget decisions

**Time saved:** From hours of spreadsheet work to seconds.

---

## Roadmap

Planned enhancements tracked in [GitHub Issues](https://github.com/DiiDayan/report-consolidator/issues):

- [ ] Excel file support (.xlsx)
- [ ] Advanced data validation and quality checks
- [ ] Intelligent merge for related datasets
- [ ] Additional chart types and visualizations
- [ ] More platform integrations (TikTok, Twitter Ads)
- [ ] Anomaly detection (performance spikes/drops)
- [ ] Budget optimization suggestions

---

## Background

This tool was built to solve a real problem: marketing teams waste hours consolidating data from different ad platforms and manually calculating KPIs in spreadsheets.

By automating the consolidation and calculation process, marketers can focus on strategy and optimization rather than data wrangling.

---

## License

MIT License - feel free to use and modify for your needs.

---

## 🤝 Contributing

Found a bug? Have a feature request? Open an [issue](https://github.com/DiiDayan/report-consolidator/issues) or submit a pull request.

---

## Author

Built with practical marketing analytics in mind.

**Skills demonstrated:**
- Python development
- Data analysis and KPI calculation
- Web application development (Streamlit)
- Marketing domain knowledge
- Clean code and documentation

---

**Ready to simplify your marketing analytics?** [Get started](#-quick-start) now.
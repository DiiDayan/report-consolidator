# Marketing Performance Consolidator

Consolidate ad data from Facebook, Google, LinkedIn (and others) into one place. Automatic KPI calculation + campaign-level statistics included.

## What it does

Takes multiple CSV files from different ad platforms and:

- Merges them into one dataset
- Calculates standard marketing KPIs (CTR, CPC, CPA, conversion rate, CPM)
- Shows campaign-level statistics (mean, median, std dev, ranges)
- Identifies best/worst performing campaigns
- Generates performance comparisons across platforms
- Points out what's working and what isn't

Two ways to use it:
- **Web interface**: Upload files, see results, download reports
- **Command line**: Drop CSVs in a folder, run script

## Why this exists

Marketers running campaigns on multiple platforms waste time:
- Downloading CSVs from each platform
- Copy-pasting into spreadsheets
- Manually calculating KPIs
- Making comparison charts
- Figuring out which campaigns actually perform well

This automates it. Upload → Get analysis → Done.

## Setup

```bash
git clone https://github.com/DiiDayan/report-consolidator.git
cd report-consolidator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Web interface
```bash
streamlit run app.py
```

Upload your files and explore results in tabs:
- **Overview**: Platform summary + key insights
- **Detailed Statistics**: Campaign-level metrics with distribution analysis
- **Data Table**: Full consolidated data
- **Visualizations**: KPI charts

Download buttons for:
- Consolidated CSV with all metrics
- Statistics report (TXT file with full analysis)

### Command line
```bash
# Put your CSVs in data/input/
python3 src/consolidator.py
# Results in output/
```

## What you get

Platform comparison:
```
Platform Performance:
          impressions  clicks  spend  conversions   ctr   cpc    cpa  conversion_rate
Facebook       254600    2546   1025           60  1.00  0.40  17.08             2.36
Google         161600    4250   1605          111  2.63  0.38  14.46             2.61
LinkedIn        60000     904    756           42  1.51  0.84  18.00             4.65
```

Campaign-level statistics (new):
```
📊 CTR (Click-Through Rate)
  • Aggregate CTR: 1.21% (volume-weighted)
  • Campaign average: 1.22%
  • Campaign median: 1.03%
  • Std deviation: 0.72%
  • Range: 0.42% - 2.25%
  ⚠️  High variability detected - review individual campaigns

🏆 Campaign Performance Highlights:
  • Best CTR: Retargeting (2.25%)
  • Lowest CPC: Cold_Audience ($0.44)
  • Best conversion rate: Winter_Sale (2.67%)
```

Automatic insights:
- Google has lowest CPC ($0.38)
- LinkedIn has best conversion rate (4.65%)
- Facebook represents 30% of total spend
- Retargeting campaign outperforms by 2x

Charts comparing KPIs across platforms.

## Expected data format

Your CSVs or Excel files need these columns (tool auto-detects variations):

**Required:**
- `impressions` (or `views`)
- `clicks`
- `spend` (or `cost`)
- `conversions` (or `sales`)

**Optional:**
- `platform` - for cross-platform comparison
- `campaign` - for campaign-level analysis
- `date` - for time analysis

Column names are flexible. The tool handles common variations automatically.

## Metrics calculated

- **CTR** (Click-Through Rate): `(clicks / impressions) × 100`
- **CPC** (Cost Per Click): `spend / clicks`
- **CPM** (Cost Per Mille): `(spend / impressions) × 1000`
- **CPA** (Cost Per Acquisition): `spend / conversions`
- **Conversion Rate**: `(conversions / clicks) × 100`
- **ROAS** (if revenue data): `revenue / spend`

Plus statistical distribution (mean, median, std dev, min/max) for each metric when multiple campaigns exist.

## Tech stack

Python • Pandas • Matplotlib • Streamlit

## Roadmap

See [Issues](https://github.com/DiiDayan/report-consolidator/issues) for planned features:
- ~~Excel file support~~ ✅ Done
- ~~Data validation~~ ✅ Done
- ~~Campaign-level statistics~~ ✅ Done
- Industry benchmarks for context
- Better chart design + downloadable visualizations
- Smart merge for related datasets

## License

MIT

Built to solve a real workflow problem. If it helps you, use it.
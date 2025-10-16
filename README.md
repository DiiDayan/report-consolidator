# 📊 CSV Report Consolidator

Python automation tool that consolidates multiple CSV files into a single report, calculates key statistics, and generates automatic visualizations. Available as both a command-line tool and an interactive web interface.

## ✨ Features

- **Automatic consolidation**: Reads all CSV files from a folder and combines them into one
- **Flexible column detection**: Works with any CSV structure - no fixed column names required
- **Real-time statistics**: Calculates totals, averages, min, max, and more
- **Data visualization**: Generates comparative charts automatically
- **Two interfaces**: Use via command line or interactive web app
- **Easy to use**: Execute a single command and get all results

## 🚀 Use Cases

- Consolidate monthly sales reports
- Combine data from multiple sources
- Generate executive reports quickly
- Automate repetitive analysis
- Interactive data exploration

## 📋 Requirements

- Python 3.8 or higher
- pandas
- matplotlib
- openpyxl
- streamlit

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/DiiDayan/report-consolidator.git
cd report-consolidator
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Option 1: Web Interface (Recommended)

Launch the interactive Streamlit app:

```bash
streamlit run app.py
```

This opens a web interface where you can:
- 📁 Drag and drop CSV files
- 👀 Preview data before consolidation
- 📊 View interactive statistics and charts
- ⬇️ Download consolidated reports
- 🎨 Customize visualizations

### Option 2: Command Line

1. Place your CSV files in the `data/input/` folder

2. Run the script:
```bash
python3 src/consolidator.py
```

3. Find the results in the `output/` folder:
   - `consolidated_report.csv` - Consolidated data
   - `data_visualization.png` - Visualization

## 📁 Project Structure

```
report-consolidator/
├── app.py                   # Streamlit web interface
├── src/
│   └── consolidator.py      # Command-line script
├── data/
│   └── input/               # Place your CSVs here (CLI mode)
├── output/                  # Generated results (CLI mode)
├── requirements.txt         # Dependencies
└── README.md
```

## 📊 Sample Output

The tool generates:

**Statistics:**
```
=== STATISTICS ===

SALES:
  Total: 17,400.00
  Average: 1,933.33
  Min: 1,200.00
  Max: 2,400.00

EXPENSES:
  Total: 9,750.00
  Average: 1,083.33
  Min: 800.00
  Max: 1,300.00
```

**Interactive charts** with customizable axes and download options

## 🎯 Key Features

### Flexible Column Detection
- No hardcoded column names required
- Automatically detects numeric and text columns
- Works with any CSV structure

### Comprehensive Statistics
- Totals, averages, min, max, median, standard deviation
- Automatic detection of numeric columns
- Clear, formatted output

### Interactive Visualizations
- Choose which columns to visualize
- Multiple chart types
- High-resolution export (300 DPI)

## 🛠️ Technologies

- **Python 3.13** - Core language
- **pandas** - Data manipulation
- **matplotlib** - Visualization
- **openpyxl** - Excel file reading
- **streamlit** - Web interface

## 📸 Screenshots

### Web Interface
- Clean, intuitive design
- Real-time data preview
- Interactive charts
- One-click downloads

## License

MIT License

## Author

Created as part of my data analysis and automation portfolio.

**Skills demonstrated:**
- Python development
- Data analysis and visualization
- Web application development
- Git workflow and version control
- Clean code and documentation

## Contributing

Suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

## Roadmap

- [ ] Support for Excel (.xlsx) files
- [ ] Custom column mapping interface
- [ ] Export to multiple formats (PDF, Excel)
- [ ] Scheduled automation
- [ ] API integration
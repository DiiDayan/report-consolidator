# 📊 CSV Report Consolidator

Python automation tool that consolidates multiple CSV files into a single report, calculates key statistics, and generates automatic visualizations.

## ✨ Features

- **Automatic consolidation**: Reads all CSV files from a folder and combines them into one
- **Real-time statistics**: Calculates totals, averages, and key metrics
- **Data visualization**: Generates comparative charts automatically
- **Easy to use**: Execute a single command and get all results

## 🚀 Use Cases

- Consolidate monthly sales reports
- Combine data from multiple sources
- Generate executive reports quickly
- Automate repetitive analysis

## 📋 Requirements

- Python 3.8 or higher
- pandas
- matplotlib
- openpyxl

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

1. Place your CSV files in the `data/input/` folder

2. Run the script:
```bash
python3 src/consolidator.py
```

3. Find the results in the `output/` folder:
   - `consolidated_report.csv` - Consolidated data
   - `sales_expenses_chart.png` - Visualization

## 📁 Project Structure

```
report-consolidator/
├── src/
│   └── consolidator.py      # Main script
├── data/
│   └── input/               # Place your CSVs here
├── output/                  # Generated results
├── examples/                # Sample files
├── requirements.txt         # Dependencies
└── README.md
```

## 📊 Sample Output

The script generates:

**Statistics:**
```
=== STATISTICS ===
Total sales: $17,400
Total expenses: $9,750
Net profit: $7,650
Average sales: $1,933
Average expenses: $1,083
```

**Comparative chart** of sales vs expenses by month

## 🛠️ Technologies

- Python 3.13
- pandas - Data manipulation
- matplotlib - Visualization
- openpyxl - Excel file reading

## 🔄 Future Enhancements

- Flexible column mapping for different CSV structures
- Interactive web interface with Streamlit
- Support for multiple data formats (Excel, JSON)
- Custom visualization options

## 📝 License

MIT License

## Author

Created as part of my data analysis and automation portfolio.

## 🤝 Contributing

Suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.
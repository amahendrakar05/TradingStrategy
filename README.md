# Yahoo Finance Trading Analysis

A Python project for fetching and analyzing live and historical stock market data from Yahoo Finance API, with both desktop and web interfaces.

**🌐 Try the Web App:** [Live on Streamlit Cloud](https://streamlit.io/cloud) (deploy instructions below)

## Features

- 📊 **Fetch Historical Data**: Download historical stock data for any date range
- 🔴 **Live Data**: Get real-time stock price updates
- 📈 **Technical Analysis**: Calculate SMA, EMA, RSI, MACD, Bollinger Bands, ATR
- 🎯 **Support & Resistance**: Calculate 4 different S/R methods (Pivot Points, Fibonacci, Recent Levels, Dynamic Levels)
- 📉 **Statistics**: Comprehensive statistical analysis including mean, median, standard deviation
- 💾 **CSV Export**: Export analysis results to CSV files
- 🔍 **Stock Information**: Fetch detailed company information, market cap, P/E ratios, etc.
- **NEW:** 🎯 **Options Strategies**: Black-Scholes pricing, Greeks calculations, Probability of Profit
- **NEW:** 🌐 **Web App**: Browser-based interface with interactive charts

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. Clone or navigate to the project directory:
```bash
cd m:\Trading
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
Trading/
├── streamlit_app.py         # Web application (Streamlit) - NEW
├── src/
│   ├── yahoo_finance.py      # Yahoo Finance API connector
│   ├── analysis.py           # Technical & Options analysis
│   ├── gui_analysis.py       # Desktop GUI application (tkinter)
│   ├── run_gui.py            # GUI launcher script
│   ├── main.py               # Example usage script (comprehensive)
│   └── quickstart.py         # Quick start example (console)
├── data/                     # Output data directory
├── notebooks/                # Jupyter notebooks for analysis
├── requirements.txt          # Python dependencies
├── DEPLOYMENT_GUIDE.md       # GitHub & Streamlit Cloud deployment
├── OPTIONS_FEATURE_STATUS.md # Options features documentation
└── README.md                 # This file
```

## Usage

### 🌐 Web App (Browser)

Run locally:
```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

Or deploy to Streamlit Cloud for free - [See Deployment Guide](DEPLOYMENT_GUIDE.md)

### 🖥️ Desktop App (GUI)

Run the interactive GUI:
```bash
cd src
python run_gui.py
```

Features:
- Select stock symbol and date range
- View technical analysis with 6 indicators
- See support/resistance levels
- View options strategies and Greeks
- Color-coded analysis results

### 📝 Command Line Examples

#### Basic Example: Fetch Historical Data

```python
from yahoo_finance import YahooFinanceConnector
from datetime import datetime, timedelta

connector = YahooFinanceConnector()

# Define date range
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

# Fetch historical data
df = connector.fetch_historical_data('AAPL', start_date, end_date)
print(df.head())
```

### Example: Fetch Live Data

```python
connector = YahooFinanceConnector()

# Fetch live data for multiple stocks
symbols = ['AAPL', 'MSFT', 'GOOGL']
data = connector.fetch_live_data(symbols)
print(data)
```

### Example: Technical Analysis

```python
from analysis import TechnicalAnalysis

# Add technical indicators to dataframe
df_analysis = TechnicalAnalysis.add_indicators(df)

# View indicators
print(df_analysis[['Close', 'SMA_20', 'EMA_12', 'RSI_14', 'MACD']])
```

### Example: Stock Information

```python
connector = YahooFinanceConnector()

# Get stock info
info = connector.fetch_stock_info('AAPL')
print(info)
```

### Launch Interactive GUI

The easiest way to analyze stocks! Run the GUI application:

```bash
cd src
python run_gui.py
```

**Features:**
- 📅 Date range picker (calendar widget)
- 📊 Stock symbol input
- ⏱️ Configurable time intervals (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)
- 🎯 One-click analysis
- 📈 Complete technical indicators display
- 💾 Scrollable results view
- 🔄 Real-time status updates

### Run All Examples

Navigate to the `src` directory and run:
```bash
cd src
python main.py
```

## API Methods

### YahooFinanceConnector

#### `fetch_historical_data(symbol, start_date, end_date, interval='1d')`
Fetch historical stock data

**Parameters:**
- `symbol` (str): Stock ticker (e.g., 'AAPL')
- `start_date` (str): Format 'YYYY-MM-DD'
- `end_date` (str): Format 'YYYY-MM-DD'
- `interval` (str): '1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'

**Returns:** pd.DataFrame with OHLCV data

#### `fetch_live_data(symbols)`
Fetch latest/live stock data

**Parameters:**
- `symbols` (list or str): Single or list of ticker symbols

**Returns:** pd.DataFrame with latest data

#### `fetch_stock_info(symbol)`
Fetch detailed stock information

**Parameters:**
- `symbol` (str): Stock ticker

**Returns:** dict with company info, market cap, P/E ratio, etc.

#### `fetch_multiple_stocks(symbols, start_date, end_date, interval='1d')`
Fetch historical data for multiple stocks

**Parameters:**
- `symbols` (list): List of ticker symbols
- `start_date` (str): Start date
- `end_date` (str): End date
- `interval` (str): Data interval

**Returns:** dict with symbol as key and DataFrame as value

#### `get_price_change(symbol, start_date, end_date)`
Calculate price change over a period

**Returns:** dict with start price, end price, change amount, and change percentage

### TechnicalAnalysis

#### Available Indicators
- `calculate_sma(df, window=20)` - Simple Moving Average
- `calculate_ema(df, window=12)` - Exponential Moving Average
- `calculate_rsi(df, window=14)` - Relative Strength Index
- `calculate_macd(df, fast=12, slow=26, signal=9)` - MACD
- `calculate_bollinger_bands(df, window=20, num_std=2)` - Bollinger Bands
- `calculate_atr(df, window=14)` - Average True Range
- `add_indicators(df, sma_window=20, ema_window=12, rsi_window=14)` - Add all indicators

### DataAnalyzer

- `calculate_statistics(df)` - Get mean, median, std dev, min, max
- `calculate_returns(df, period=1)` - Calculate periodic returns
- `export_to_csv(df, filename)` - Export DataFrame to CSV

## Common Stock Symbols

| Symbol | Company | Symbol | Company |
|--------|---------|--------|---------|
| AAPL | Apple | MSFT | Microsoft |
| GOOGL | Google | AMZN | Amazon |
| TSLA | Tesla | NVDA | NVIDIA |
| META | Meta | NFLX | Netflix |
| AMD | AMD | INTC | Intel |

## GUI User Guide

### Opening the Application

```bash
python run_gui.py
```

### How to Use

1. **Enter Stock Symbol**
   - Type the stock ticker (e.g., AAPL, MSFT, GOOGL)
   - Case-insensitive (automatically converted to uppercase)

2. **Select Date Range**
   - Click on "Start Date" calendar button to pick start date
   - Click on "End Date" calendar button to pick end date
   - Default: 1 year of data

3. **Choose Time Interval**
   - **1m**: 1 minute (for intraday analysis)
   - **5m, 15m, 30m**: Short-term intervals
   - **1h**: Hourly data
   - **1d**: Daily data (most common)
   - **1wk**: Weekly data
   - **1mo**: Monthly data

4. **Click "Fetch Data & Analyze"**
   - Application fetches data from Yahoo Finance
   - Calculates all technical indicators
   - Displays comprehensive analysis in results pane

### Results Displayed

**Company Information Section:**
- Company name
- Sector and industry
- Current stock price
- Market capitalization
- P/E ratio
- 52-week high/low

**Price Statistics Section:**
- Mean price over period
- Median price
- Standard deviation (volatility)
- Minimum and maximum prices
- Price range

**Support & Resistance Section:**
The GUI displays four different S/R calculation methods:

1. **Pivot Points (Daily)**
   - Resistance 2 & 1 (upper targets)
   - Pivot Point (midpoint)
   - Support 1 & 2 (lower targets)
   - Best for: Day traders

2. **Recent Price Levels (20-day)**
   - Recent Resistance (highest price in 20 days)
   - Recent Support (lowest price in 20 days)
   - Best for: Swing traders

3. **Fibonacci Retracement Levels**
   - 100.0%, 61.8%, 50.0%, 38.2%, 23.6%, 0.0%
   - Identifies likely pullback/resistance zones
   - Best for: Position traders

4. **Dynamic Levels (Moving Averages)**
   - Upper/Lower Bollinger Bands
   - SMA (20-day trend line)
   - Best for: Trend following

**Technical Indicators (Latest Data):**
- Current close price with change
- Trading volume
- **Moving Averages**: SMA (20), EMA (12)
- **Momentum Indicators**: RSI (14), MACD, MACD Signal
- **Bollinger Bands**: Upper, Middle, Lower bands
- **Volatility**: ATR (Average True Range)

**Recent Data Table:**
- Last 10 days of OHLCV data
- Open, High, Low, Close prices
- Trading volume

## 🚀 Deployment & Publishing

### Publish to GitHub

Share your project on GitHub so others can use it:

1. **Install Git** - Download from https://git-scm.com/download/win
2. **Create GitHub Account** - Sign up at https://github.com
3. **Push Code** - See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions

### Deploy Web App to Streamlit Cloud (Free)

Make your app accessible online with zero cost:

1. Push code to GitHub (see above)
2. Create Streamlit Cloud account at https://streamlit.io/cloud
3. Connect to GitHub and deploy `streamlit_app.py`

Your app will be live at: `https://your-username.streamlit.app`

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions**

## Support & Resistance Analysis

### What is Support & Resistance?

- **Support**: Price level where stock tends to STOP FALLING (floor)
- **Resistance**: Price level where stock tends to STOP RISING (ceiling)

### Four Calculation Methods

1. **Pivot Points**
   - Traditional method using yesterday's High, Low, Close
   - Recalculated daily
   - Formula: `Pivot = (H + L + C) / 3`
   - Usage: Day traders, entry/exit planning

2. **Recent Levels**
   - Highest and lowest prices from last 20 days
   - Represents actual price extremes
   - Usage: Swing traders, breakout signals

3. **Fibonacci Retracement**
   - Based on golden ratio (0.618, 0.382)
   - Identifies likely pullback levels
   - Levels: 23.6%, 38.2%, 50.0%, 61.8%
   - Usage: Trend reversal prediction

4. **Dynamic Levels**
   - Moving averages and Bollinger Bands
   - Changes as new data arrives
   - Usage: Trend confirmation

### Interpretation Tips

- **At Resistance**: Watch for rejection or breakout
- **At Support**: Watch for bounce or breakdown
- **Multiple Levels**: Stronger when multiple methods align
- **With Trend**: Higher probability when aligned with trend direction
- **Volume Confirmation**: Valid when volume increases at these levels

### Quick Reference

| Method | Best For | Accuracy | Update |
|--------|----------|----------|--------|
| Pivot Points | Day Trading | 65-70% | Daily |
| Recent Levels | Swing Trading | 70-75% | Real-time |
| Fibonacci | Position Trading | 60-65% | Fixed |
| Dynamic Levels | Trend Following | 65-70% | Real-time |

For detailed interpretation guide, see `SUPPORT_RESISTANCE_GUIDE.py`

### Tips

- Use **1d** interval for most stock analysis
- Use **1m or 5m** for day trading analysis
- Use **1wk or 1mo** for long-term trends
- Check **RSI**: < 30 (oversold), > 70 (overbought)
- Use **Bollinger Bands** to identify price extremes
- Use **MACD** to identify trend changes

## Data Output

Analysis results are exported to the `data/` folder in CSV format:
- `aapl_historical.csv` - Historical data
- `aapl_technical_analysis.csv` - Data with technical indicators
- Additional CSV files based on your analysis

## Error Handling

All methods include error handling and logging. Check the console output for:
- Connection errors
- Invalid symbols
- Date range issues
- Data retrieval failures

## Troubleshooting

### No data returned
- Verify the stock symbol is correct
- Check the date range (Yahoo Finance may not have data for some future dates)
- Ensure your internet connection is active

### Import errors
- Verify all packages are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.10+)

### Performance optimization
- For large date ranges, consider using a longer interval ('1wk' or '1mo')
- For multiple stocks, process them in batches

## Dependencies

- **yfinance** - Yahoo Finance API integration
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **matplotlib** - Data visualization
- **seaborn** - Statistical data visualization
- **python-dotenv** - Environment variable management
- **requests** - HTTP library

## License

This project is open source and available for educational and personal use.

## References

- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Technical Analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp)

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review example code in `src/main.py`
3. Check error logs in console output

---

**Created:** May 2026
**Last Updated:** May 2026

"""
GUI Application - Quick Reference Guide
Interactive Stock Analysis Tool
"""

GUI_QUICK_START = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    YAHOO FINANCE - GUI QUICK START                          ║
║                  Interactive Technical Analysis Application                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 LAUNCHING THE APPLICATION
═════════════════════════════════════════════════════════════════════════════

  From command line, in the 'src' directory:
  
    python run_gui.py
  
  Or using the full Python path:
  
    m:/Trading/.venv/Scripts/python.exe run_gui.py


📋 APPLICATION FEATURES
═════════════════════════════════════════════════════════════════════════════

  ✓ Interactive Stock Selection
    - Enter any stock symbol (AAPL, MSFT, GOOGL, TSLA, etc.)
    - Auto-case conversion
  
  ✓ Calendar Date Picker
    - Visual calendar for easy date selection
    - Default: Last 365 days
    - Customizable start and end dates
  
  ✓ Multiple Time Intervals
    - 1m, 5m, 15m, 30m - Intraday trading
    - 1h - Hourly analysis
    - 1d - Daily analysis (recommended)
    - 1wk - Weekly trends
    - 1mo - Long-term analysis
  
  ✓ One-Click Analysis
    - "Fetch Data & Analyze" button
    - Real-time status updates
    - Threaded processing (no UI freezing)
  
  ✓ Comprehensive Results Display
    - Company Information
    - Price Statistics
    - Technical Indicators
    - Recent Data Table
    - Scrollable results window


📊 TECHNICAL INDICATORS CALCULATED
═════════════════════════════════════════════════════════════════════════════

  Moving Averages:
  └─ SMA (20)  - Simple Moving Average over 20 periods
  └─ EMA (12)  - Exponential Moving Average over 12 periods

  Momentum Indicators:
  └─ RSI (14)  - Relative Strength Index (0-100 scale)
                 < 30 = Oversold, > 70 = Overbought
  └─ MACD      - Moving Average Convergence Divergence
  └─ Signal    - MACD signal line

  Volatility:
  └─ ATR (14)  - Average True Range (volatility measure)
  
  Support/Resistance:
  └─ Bollinger Bands - Upper, Middle (SMA), Lower bands


📈 INTERPRETATION TIPS
═════════════════════════════════════════════════════════════════════════════

  RSI Indicator:
  • RSI < 30      → Stock may be oversold (potential buy signal)
  • RSI > 70      → Stock may be overbought (potential sell signal)
  • 30-70         → Neutral zone

  Moving Averages:
  • Price > SMA   → Uptrend
  • Price < SMA   → Downtrend
  • EMA crossover → Potential trend reversal

  Bollinger Bands:
  • Price touches upper band  → Resistance/overbought
  • Price touches lower band  → Support/oversold
  • Band width               → Volatility measure

  MACD:
  • MACD > Signal → Bullish signal
  • MACD < Signal → Bearish signal
  • Zero crossing → Trend change


🔍 EXAMPLE WORKFLOWS
═════════════════════════════════════════════════════════════════════════════

  Workflow 1: Day Trading Analysis
  ────────────────────────────────
  1. Symbol: TSLA
  2. Date Range: Today ± 5 days
  3. Interval: 15m or 30m
  4. Look at: RSI, MACD, ATR for entry/exit signals

  Workflow 2: Swing Trading
  ────────────────────────────────
  1. Symbol: MSFT
  2. Date Range: Last 30-90 days
  3. Interval: 1d
  4. Look at: Moving averages, Bollinger Bands, RSI

  Workflow 3: Long-term Investing
  ────────────────────────────────
  1. Symbol: AAPL
  2. Date Range: Last 1-2 years
  3. Interval: 1wk or 1mo
  4. Look at: Trend direction, overall price range


💾 RESULTS OUTPUT
═════════════════════════════════════════════════════════════════════════════

  The GUI displays:
  
  Company Information
  ├─ Name, Sector, Industry
  ├─ Current Price, Market Cap
  └─ P/E Ratio, 52-week High/Low

  Price Statistics
  ├─ Mean, Median prices
  ├─ Standard Deviation (volatility)
  └─ Min/Max prices and range

  Latest Technical Indicators
  ├─ Moving Averages
  ├─ Momentum Indicators
  ├─ Bollinger Bands
  └─ ATR Volatility

  Recent Data Table
  ├─ Last 10 trading days
  └─ OHLCV (Open, High, Low, Close, Volume) data


⚙️ TROUBLESHOOTING
═════════════════════════════════════════════════════════════════════════════

  Issue: "No data found"
  Solution: Verify stock symbol is correct, check date range

  Issue: "Connection error"
  Solution: Check internet connection, Yahoo Finance may be temporarily unavailable

  Issue: GUI not launching
  Solution: Ensure tkcalendar is installed: pip install tkcalendar

  Issue: Slow performance
  Solution: Use larger time intervals (1d, 1wk) instead of 1m


📚 EXAMPLES OF STOCK SYMBOLS
═════════════════════════════════════════════════════════════════════════════

  Technology:     AAPL, MSFT, GOOGL, META, NVDA, INTC
  E-Commerce:     AMZN, EBAY, SHOP
  Automotive:     TSLA, F, GM, TM
  Finance:        JPM, BAC, GS, WFC
  Healthcare:     JNJ, PFE, MRNA, UNH
  Energy:         XOM, CVX, COP, MPC
  Retail:         WMT, TGT, COST, HD
  Telecom:        T, VZ, TMUS, CMCSA
  Airlines:       AAL, DAL, UAL, ALK
  Crypto (ETF):   GBTC, IBIT, FBTC


🔗 QUICK LINKS
═════════════════════════════════════════════════════════════════════════════

  Project Repository: m:/Trading/
  Source Code:       m:/Trading/src/
  GUI Code:         m:/Trading/src/gui_analysis.py
  Documentation:     m:/Trading/README.md


═════════════════════════════════════════════════════════════════════════════
For more information, see README.md in the project root directory.
═════════════════════════════════════════════════════════════════════════════
"""

if __name__ == '__main__':
    print(GUI_QUICK_START)

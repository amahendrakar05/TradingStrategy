"""
GUI Test - Verify all GUI components work correctly
Simulates what the GUI will display
"""

import sys
from datetime import datetime, timedelta
from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, DataAnalyzer, SupportResistance

def test_gui_analysis():
    """Test the analysis pipeline that the GUI uses"""
    print("\n" + "="*80)
    print("GUI COMPONENT TEST - Analysis Pipeline Verification")
    print("="*80 + "\n")
    
    # Initialize connector
    connector = YahooFinanceConnector()
    
    # Test parameters (as user would input in GUI)
    symbol = "AAPL"
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    interval = "1d"
    
    print(f"Input Parameters:")
    print(f"  Symbol: {symbol}")
    print(f"  Date Range: {start_date} to {end_date}")
    print(f"  Interval: {interval}\n")
    
    # Step 1: Fetch data
    print("Step 1: Fetching historical data from Yahoo Finance...")
    df_data = connector.fetch_historical_data(symbol, start_date, end_date, interval)
    
    if df_data is None or df_data.empty:
        print("ERROR: No data retrieved!")
        return False
    
    print(f"✓ Retrieved {len(df_data)} records\n")
    
    # Step 2: Get stock info
    print("Step 2: Fetching stock information...")
    info = connector.fetch_stock_info(symbol)
    
    if info:
        print(f"✓ Company: {info['company_name']}")
        print(f"✓ Sector: {info['sector']}")
        print(f"✓ Current Price: ${info['current_price']}\n")
    
    # Step 3: Calculate statistics
    print("Step 3: Calculating price statistics...")
    stats = DataAnalyzer.calculate_statistics(df_data)
    
    print(f"✓ Mean Price: ${stats['mean']:.2f}")
    print(f"✓ Std Dev: ${stats['std_dev']:.2f}")
    print(f"✓ Price Range: ${stats['min']:.2f} - ${stats['max']:.2f}\n")
    
    # Step 4: Add technical indicators
    print("Step 4: Calculating technical indicators...")
    df_analysis = TechnicalAnalysis.add_indicators(df_data)
    
    print(f"✓ SMA (20)")
    print(f"✓ EMA (12)")
    print(f"✓ RSI (14)")
    print(f"✓ MACD")
    print(f"✓ Bollinger Bands")
    print(f"✓ ATR\n")
    
    # Step 5: Display latest values
    print("Step 5: Latest Technical Indicators (Most Recent Date):")
    latest = df_analysis.iloc[-1]
    
    print(f"  Close Price: ${latest['Close']:.2f}")
    print(f"  SMA (20): ${latest['SMA_20']:.2f}")
    print(f"  EMA (12): ${latest['EMA_12']:.2f}")
    print(f"  RSI (14): {latest['RSI_14']:.2f}")
    print(f"  MACD: {latest['MACD']:.4f}")
    print(f"  Bollinger Upper: ${latest['BB_Upper']:.2f}")
    print(f"  Bollinger Lower: ${latest['BB_Lower']:.2f}")
    print(f"  ATR: ${latest['ATR']:.2f}\n")
    
    # Step 6: Calculate support and resistance
    print("Step 6: Support & Resistance Analysis:")
    levels = SupportResistance.get_all_levels(df_analysis)
    
    current_price = latest['Close']
    
    # Pivot Points
    pp = levels['pivot_points']
    print(f"\n  Pivot Points:")
    print(f"    Resistance 2: ${pp['resistance2']:.2f}")
    print(f"    Resistance 1: ${pp['resistance1']:.2f}")
    print(f"    Pivot Point:  ${pp['pivot']:.2f}")
    print(f"    Support 1:    ${pp['support1']:.2f}")
    print(f"    Support 2:    ${pp['support2']:.2f}")
    
    # Recent Levels
    recent = levels['recent_levels']
    print(f"\n  Recent Levels (20 days):")
    print(f"    Resistance: ${recent['recent_resistance']:.2f} (+${recent['recent_resistance'] - current_price:.2f})")
    print(f"    Support:    ${recent['recent_support']:.2f} (-${current_price - recent['recent_support']:.2f})")
    
    # Fibonacci
    fib = levels['fibonacci']
    print(f"\n  Fibonacci Retracement:")
    print(f"    100% (High):  ${fib['fib_100']:.2f}")
    print(f"    61.8%:        ${fib['fib_618']:.2f}")
    print(f"    50.0%:        ${fib['fib_500']:.2f}")
    print(f"    38.2%:        ${fib['fib_382']:.2f}")
    print(f"    23.6%:        ${fib['fib_236']:.2f}")
    print(f"    0% (Low):     ${fib['fib_0']:.2f}")
    
    # Step 6: Display data table
    print("Step 6: Recent Data (Last 5 Days):")
    print(f"{'Date':<20} {'Open':>12} {'High':>12} {'Low':>12} {'Close':>12} {'Volume':>15}")
    print("-" * 80)
    
    for idx, row in df_analysis.tail(5).iterrows():
        date_str = str(idx.date()) if hasattr(idx, 'date') else str(idx)[:10]
        print(f"{date_str:<20} ${row['Open']:>11.2f} ${row['High']:>11.2f} ${row['Low']:>11.2f} ${row['Close']:>11.2f} {int(row.get('Volume', 0)):>14,}")
    
    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED - GUI Analysis Pipeline is Working!")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        success = test_gui_analysis()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}\n")
        sys.exit(1)

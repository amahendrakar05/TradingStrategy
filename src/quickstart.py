"""
Quick Start Example - Yahoo Finance Data Fetching
Simple script to demonstrate basic usage
"""

from datetime import datetime, timedelta
from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, SupportResistance

def main():
    print("\n" + "="*60)
    print("Yahoo Finance - Quick Start Example")
    print("="*60 + "\n")
    
    # Initialize connector
    connector = YahooFinanceConnector()
    
    # Initialize
    df_with_indicators = None
    
    # Example 1: Get stock information
    print("📊 Example 1: Fetching Stock Information\n")
    symbol = 'AAPL'
    info = connector.fetch_stock_info(symbol)
    if info:
        print(f"Symbol: {info['symbol']}")
        print(f"Company: {info['company_name']}")
        print(f"Sector: {info['sector']}")
        print(f"Current Price: ${info['current_price']}")
        print(f"Market Cap: ${info['market_cap']}\n")
    
    # Example 2: Fetch historical data
    print("📈 Example 2: Fetching 30 Days of Historical Data\n")
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    df = connector.fetch_historical_data(symbol, start_date, end_date)
    if df is not None:
        print(f"Retrieved {len(df)} records\n")
        print("Recent data (last 5 days):")
        print(df[['Open', 'High', 'Low', 'Close', 'Volume']].tail())
        print()
    
    # Example 3: Technical analysis
    print("🔧 Example 3: Adding Technical Indicators\n")
    if df is not None:
        df_with_indicators = TechnicalAnalysis.add_indicators(df)
        print("Latest data with technical indicators:")
        print(df_with_indicators[['Close', 'SMA_20', 'RSI_14']].tail(3))
        print()
    
    # Example 4: Support and Resistance
    print("📊 Example 4: Support & Resistance Levels\n")
    if df_with_indicators is not None:
        levels = SupportResistance.get_all_levels(df_with_indicators)
        current = df_with_indicators.iloc[-1]['Close']
        
        pp = levels['pivot_points']
        print(f"Pivot Points (Daily):")
        print(f"  Resistance 2: ${pp['resistance2']:.2f}")
        print(f"  Resistance 1: ${pp['resistance1']:.2f}")
        print(f"  Pivot Point:  ${pp['pivot']:.2f}")
        print(f"  Support 1:    ${pp['support1']:.2f}")
        print(f"  Support 2:    ${pp['support2']:.2f}")
        
        recent = levels['recent_levels']
        print(f"\nRecent Levels (20 days):")
        print(f"  Resistance: ${recent['recent_resistance']:.2f}")
        print(f"  Support:    ${recent['recent_support']:.2f}")
        
        fib = levels['fibonacci']
        print(f"\nFibonacci Retracement:")
        print(f"  61.8%: ${fib['fib_618']:.2f}")
        print(f"  50.0%: ${fib['fib_500']:.2f}")
        print(f"  38.2%: ${fib['fib_382']:.2f}")
        print()
    
    # Example 5: Price change calculation
    print("📉 Example 5: Price Change Analysis (Last 30 Days)\n")
    change = connector.get_price_change(symbol, start_date, end_date)
    if change:
        print(f"Symbol: {change['symbol']}")
        print(f"Start Price: ${change['start_price']}")
        print(f"End Price: ${change['end_price']}")
        print(f"Change: ${change['change']} ({change['change_percent']:.2f}%)")
        print()
    
    print("="*60)
    print("✓ Quick start example completed!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

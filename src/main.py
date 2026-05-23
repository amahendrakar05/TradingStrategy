"""
Main Script - Yahoo Finance Data Fetch and Analysis
Example usage of Yahoo Finance connector and analysis tools
"""

import sys
from datetime import datetime, timedelta
import pandas as pd
from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, DataAnalyzer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_fetch_historical_data():
    """Example: Fetch historical stock data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Fetch Historical Stock Data")
    print("="*60)
    
    connector = YahooFinanceConnector()
    
    # Define date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Fetch data
    df = connector.fetch_historical_data('AAPL', start_date, end_date, interval='1d')
    
    if df is not None:
        print(f"\nData retrieved: {len(df)} records")
        print("\nFirst 5 records:")
        print(df.head())
        print("\nLast 5 records:")
        print(df.tail())
        
        # Export to CSV
        connector_instance = connector
        df.to_csv('../data/aapl_historical.csv')
        print("\n✓ Data exported to data/aapl_historical.csv")


def example_fetch_live_data():
    """Example: Fetch live stock data"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Fetch Live Stock Data")
    print("="*60)
    
    connector = YahooFinanceConnector()
    
    # Fetch live data for multiple stocks
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    data = connector.fetch_live_data(symbols)
    
    if data is not None:
        print(f"\nLive data for {', '.join(symbols)}:")
        print(data)


def example_stock_info():
    """Example: Fetch stock information"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Fetch Stock Information")
    print("="*60)
    
    connector = YahooFinanceConnector()
    
    symbol = 'AAPL'
    info = connector.fetch_stock_info(symbol)
    
    if info:
        print(f"\nStock Information for {symbol}:")
        for key, value in info.items():
            print(f"  {key}: {value}")


def example_technical_analysis():
    """Example: Perform technical analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Technical Analysis")
    print("="*60)
    
    connector = YahooFinanceConnector()
    
    # Fetch data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    
    df = connector.fetch_historical_data('AAPL', start_date, end_date)
    
    if df is not None:
        # Add technical indicators
        df_analysis = TechnicalAnalysis.add_indicators(df)
        
        print("\nData with Technical Indicators:")
        print(df_analysis[['Close', 'SMA_20', 'EMA_12', 'RSI_14', 'MACD']].tail(10))
        
        # Export analysis
        df_analysis.to_csv('../data/aapl_technical_analysis.csv')
        print("\n✓ Analysis exported to data/aapl_technical_analysis.csv")


def example_statistics():
    """Example: Calculate statistics"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Statistics Analysis")
    print("="*60)
    
    connector = YahooFinanceConnector()
    
    # Fetch data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    df = connector.fetch_historical_data('MSFT', start_date, end_date)
    
    if df is not None:
        stats = DataAnalyzer.calculate_statistics(df)
        
        print("\nMicrosoft (MSFT) - 1 Year Statistics:")
        for key, value in stats.items():
            print(f"  {key}: ${value:.2f}")
        
        # Calculate returns
        returns = DataAnalyzer.calculate_returns(df, period=1)
        print(f"\n  Daily Return (Mean): {returns.mean():.4f}")
        print(f"  Daily Return (Std Dev): {returns.std():.4f}")


def example_price_change():
    """Example: Calculate price changes"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Price Change Analysis")
    print("="*60)
    
    connector = YahooFinanceConnector()
    
    # Calculate price changes for multiple stocks
    stocks = ['AAPL', 'MSFT', 'GOOGL']
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    print(f"\nPrice changes from {start_date} to {end_date}:")
    
    for stock in stocks:
        change = connector.get_price_change(stock, start_date, end_date)
        if change:
            print(f"\n  {change['symbol']}:")
            print(f"    Start Price: ${change['start_price']}")
            print(f"    End Price: ${change['end_price']}")
            print(f"    Change: ${change['change']} ({change['change_percent']:.2f}%)")


def main():
    """Run all examples"""
    logger.info("Starting Yahoo Finance Data Analysis Examples")
    
    try:
        # Run examples
        example_fetch_historical_data()
        example_fetch_live_data()
        example_stock_info()
        example_technical_analysis()
        example_statistics()
        example_price_change()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error running examples: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

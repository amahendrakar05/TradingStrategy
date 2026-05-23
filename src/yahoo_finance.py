"""
Yahoo Finance API Integration Module
Handles fetching live and historical stock data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class YahooFinanceConnector:
    """
    Connector class for Yahoo Finance API
    Provides methods to fetch historical and live stock data
    """
    
    def __init__(self):
        """Initialize the Yahoo Finance connector"""
        logger.info("Initializing Yahoo Finance Connector")
    
    def fetch_historical_data(self, symbol, start_date, end_date, interval='1d'):
        """
        Fetch historical stock data from Yahoo Finance
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
            interval (str): Data interval - '1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'
        
        Returns:
            pd.DataFrame: Historical data with columns [Open, High, Low, Close, Volume]
        """
        try:
            logger.info(f"Fetching historical data for {symbol} from {start_date} to {end_date}")
            
            # Create Ticker object
            ticker = yf.Ticker(symbol)
            
            # Fetch historical data
            df = ticker.history(start=start_date, end=end_date, interval=interval)
            
            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                return None
            
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return None
    
    def fetch_live_data(self, symbols):
        """
        Fetch live/latest stock data from Yahoo Finance
        
        Args:
            symbols (list or str): Single symbol or list of symbols (e.g., ['AAPL', 'MSFT', 'GOOGL'])
        
        Returns:
            pd.DataFrame: Live data with current price information
        """
        try:
            if isinstance(symbols, str):
                symbols = [symbols]
            
            logger.info(f"Fetching live data for {', '.join(symbols)}")
            
            # Fetch data
            data = yf.download(tickers=symbols, period='1d', interval='1m', progress=False)
            
            if data.empty:
                logger.warning("No live data returned")
                return None
            
            logger.info(f"Successfully fetched live data for {len(symbols)} symbol(s)")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching live data: {str(e)}")
            return None
    
    def fetch_stock_info(self, symbol):
        """
        Fetch detailed stock information from Yahoo Finance
        
        Args:
            symbol (str): Stock ticker symbol
        
        Returns:
            dict: Stock information including company name, sector, market cap, etc.
        """
        try:
            logger.info(f"Fetching stock info for {symbol}")
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract key information
            stock_info = {
                'symbol': symbol,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'current_price': info.get('currentPrice', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            }
            
            return stock_info
            
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
            return None
    
    def fetch_multiple_stocks(self, symbols, start_date, end_date, interval='1d'):
        """
        Fetch historical data for multiple stocks
        
        Args:
            symbols (list): List of stock ticker symbols
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
            interval (str): Data interval
        
        Returns:
            dict: Dictionary with symbol as key and DataFrame as value
        """
        results = {}
        
        for symbol in symbols:
            df = self.fetch_historical_data(symbol, start_date, end_date, interval)
            if df is not None:
                results[symbol] = df
        
        return results
    
    def get_price_change(self, symbol, start_date, end_date):
        """
        Calculate price change for a stock over a period
        
        Args:
            symbol (str): Stock ticker symbol
            start_date (str): Start date
            end_date (str): End date
        
        Returns:
            dict: Price change metrics
        """
        try:
            df = self.fetch_historical_data(symbol, start_date, end_date)
            
            if df is None or df.empty:
                return None
            
            start_price = df['Close'].iloc[0]
            end_price = df['Close'].iloc[-1]
            change = end_price - start_price
            change_pct = (change / start_price) * 100
            
            return {
                'symbol': symbol,
                'start_price': round(start_price, 2),
                'end_price': round(end_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_pct, 2)
            }
            
        except Exception as e:
            logger.error(f"Error calculating price change for {symbol}: {str(e)}")
            return None

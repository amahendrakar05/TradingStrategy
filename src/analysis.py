"""
Data Analysis Module
Provides technical analysis indicators and data analysis functions
"""

import pandas as pd
import numpy as np
import logging
from scipy.stats import norm
from datetime import datetime

logger = logging.getLogger(__name__)


class OptionsAnalysis:
    """
    Calculate Options Greeks and trading strategies
    """
    
    @staticmethod
    def black_scholes_call(S, K, T, r, sigma):
        """
        Calculate Black-Scholes call option price
        
        Args:
            S: Current stock price
            K: Strike price
            T: Time to expiration (years)
            r: Risk-free rate
            sigma: Volatility (annualized)
        
        Returns:
            Call price
        """
        if T <= 0 or sigma <= 0:
            return max(S - K, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    
    @staticmethod
    def black_scholes_put(S, K, T, r, sigma):
        """
        Calculate Black-Scholes put option price
        """
        if T <= 0 or sigma <= 0:
            return max(K - S, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return put_price
    
    @staticmethod
    def calculate_greeks(S, K, T, r, sigma, option_type='call'):
        """
        Calculate all Greeks for an option
        
        Args:
            S: Current stock price
            K: Strike price
            T: Time to expiration (years)
            r: Risk-free rate
            sigma: Volatility
            option_type: 'call' or 'put'
        
        Returns:
            dict: Delta, Gamma, Theta, Vega, Rho
        """
        if T <= 0 or sigma <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        # Delta
        if option_type.lower() == 'call':
            delta = norm.cdf(d1)
        else:
            delta = norm.cdf(d1) - 1
        
        # Gamma
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        
        # Theta (per day)
        if option_type.lower() == 'call':
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                    r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        else:
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + 
                    r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        
        # Vega (per 1% change in volatility)
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100
        
        # Rho (per 1% change in interest rate)
        if option_type.lower() == 'call':
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
    
    @staticmethod
    def calculate_probability_of_profit(S, K, T, r, sigma, option_type='call', debit=0):
        """
        Calculate probability of profit (POP)
        
        Args:
            S: Current stock price
            K: Strike price
            T: Time to expiration (years)
            r: Risk-free rate
            sigma: Volatility
            option_type: 'call' or 'put'
            debit: Premium paid (for debit spreads)
        
        Returns:
            Probability of profit (0-100)
        """
        if T <= 0:
            if option_type.lower() == 'call':
                return 100 if S > K else 0
            else:
                return 100 if S < K else 0
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
        if option_type.lower() == 'call':
            # Probability of finishing ITM
            pop = norm.cdf(d1) * 100
        else:
            pop = norm.cdf(-d1) * 100
        
        return pop
    
    @staticmethod
    def get_strategy_recommendation(df, stock_info, rsi_14, macd, current_price):
        """
        Get options strategy recommendation based on technical analysis
        
        Args:
            df: Price data
            stock_info: Stock information
            rsi_14: RSI value
            macd: MACD value
            current_price: Current stock price
        
        Returns:
            dict: Strategy recommendation
        """
        recommendation = {
            'strategy': None,
            'direction': None,
            'type': None,
            'rationale': None,
            'confidence': None
        }
        
        # Determine trend and momentum
        sma_20 = df['Close'].rolling(20).mean().iloc[-1]
        current_above_sma = current_price > sma_20
        
        # Strong bullish signals
        if rsi_14 < 70 and current_above_sma and macd > 0:
            recommendation['strategy'] = 'CALL SPREAD'
            recommendation['direction'] = 'BULLISH'
            recommendation['type'] = 'buy_call'
            recommendation['rationale'] = 'Uptrend with momentum, not overbought'
            recommendation['confidence'] = 'HIGH'
        
        # Strong bearish signals
        elif rsi_14 > 30 and not current_above_sma and macd < 0:
            recommendation['strategy'] = 'PUT SPREAD'
            recommendation['direction'] = 'BEARISH'
            recommendation['type'] = 'buy_put'
            recommendation['rationale'] = 'Downtrend with momentum, not oversold'
            recommendation['confidence'] = 'HIGH'
        
        # Neutral/consolidation
        elif 40 < rsi_14 < 60 and abs(current_price - sma_20) < (sma_20 * 0.02):
            recommendation['strategy'] = 'IRON CONDOR'
            recommendation['direction'] = 'NEUTRAL'
            recommendation['type'] = 'iron_condor'
            recommendation['rationale'] = 'Price consolidating, low volatility expected'
            recommendation['confidence'] = 'MEDIUM'
        
        # Overbought
        elif rsi_14 > 70:
            recommendation['strategy'] = 'PUT SPREAD'
            recommendation['direction'] = 'BEARISH'
            recommendation['type'] = 'buy_put'
            recommendation['rationale'] = 'Overbought condition, pullback likely'
            recommendation['confidence'] = 'MEDIUM'
        
        # Oversold
        elif rsi_14 < 30:
            recommendation['strategy'] = 'CALL SPREAD'
            recommendation['direction'] = 'BULLISH'
            recommendation['type'] = 'buy_call'
            recommendation['rationale'] = 'Oversold condition, bounce likely'
            recommendation['confidence'] = 'MEDIUM'
        
        else:
            recommendation['strategy'] = 'STRADDLE'
            recommendation['direction'] = 'NEUTRAL'
            recommendation['type'] = 'straddle'
            recommendation['rationale'] = 'Mixed signals, expect volatility'
            recommendation['confidence'] = 'LOW'
        
        return recommendation
    
    @staticmethod
    def analyze_option_chain(current_price, option_chain, days_to_expiration, 
                           volatility=0.25, risk_free_rate=0.05):
        """
        Analyze option chain and calculate Greeks for key strikes
        
        Args:
            current_price: Current stock price
            option_chain: DataFrame with option chain data
            days_to_expiration: Days until expiration
            volatility: Historical volatility
            risk_free_rate: Risk-free rate
        
        Returns:
            dict: Analysis results
        """
        T = days_to_expiration / 365
        
        results = []
        
        for idx, row in option_chain.iterrows():
            try:
                strike = row['strike']
                
                # Calculate Greeks
                call_greeks = OptionsAnalysis.calculate_greeks(
                    current_price, strike, T, risk_free_rate, volatility, 'call'
                )
                put_greeks = OptionsAnalysis.calculate_greeks(
                    current_price, strike, T, risk_free_rate, volatility, 'put'
                )
                
                # Calculate POP
                call_pop = OptionsAnalysis.calculate_probability_of_profit(
                    current_price, strike, T, risk_free_rate, volatility, 'call'
                )
                put_pop = OptionsAnalysis.calculate_probability_of_profit(
                    current_price, strike, T, risk_free_rate, volatility, 'put'
                )
                
                results.append({
                    'strike': strike,
                    'moneyness': (strike - current_price) / current_price,
                    'call_delta': call_greeks['delta'],
                    'call_gamma': call_greeks['gamma'],
                    'call_theta': call_greeks['theta'],
                    'call_pop': call_pop,
                    'put_delta': put_greeks['delta'],
                    'put_gamma': put_greeks['gamma'],
                    'put_theta': put_greeks['theta'],
                    'put_pop': put_pop,
                    'call_price': row.get('lastPrice', 0),
                    'put_price': row.get('lastPrice', 0)
                })
            except Exception as e:
                logger.warning(f"Error processing option {row.get('strike', 'N/A')}: {e}")
                continue
        
        return pd.DataFrame(results)





class TechnicalAnalysis:
    """
    Technical Analysis indicators for stock data
    """
    
    @staticmethod
    def calculate_sma(df, window=20):
        """
        Calculate Simple Moving Average (SMA)
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            window (int): Number of periods for SMA
        
        Returns:
            pd.Series: SMA values
        """
        return df['Close'].rolling(window=window).mean()
    
    @staticmethod
    def calculate_ema(df, window=12):
        """
        Calculate Exponential Moving Average (EMA)
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            window (int): Number of periods for EMA
        
        Returns:
            pd.Series: EMA values
        """
        return df['Close'].ewm(span=window, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(df, window=14):
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            window (int): Number of periods for RSI
        
        Returns:
            pd.Series: RSI values (0-100)
        """
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(df, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            fast (int): Fast EMA period
            slow (int): Slow EMA period
            signal (int): Signal line period
        
        Returns:
            tuple: (MACD line, Signal line, Histogram)
        """
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(df, window=20, num_std=2):
        """
        Calculate Bollinger Bands
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            window (int): Number of periods for SMA
            num_std (float): Number of standard deviations
        
        Returns:
            tuple: (Upper band, Middle band, Lower band)
        """
        middle_band = df['Close'].rolling(window=window).mean()
        std_dev = df['Close'].rolling(window=window).std()
        
        upper_band = middle_band + (std_dev * num_std)
        lower_band = middle_band - (std_dev * num_std)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def calculate_atr(df, window=14):
        """
        Calculate Average True Range (ATR)
        
        Args:
            df (pd.DataFrame): DataFrame with OHLC columns
            window (int): Number of periods for ATR
        
        Returns:
            pd.Series: ATR values
        """
        high_low = df['High'] - df['Low']
        high_close = abs(df['High'] - df['Close'].shift())
        low_close = abs(df['Low'] - df['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=window).mean()
        
        return atr
    
    @staticmethod
    def add_indicators(df, sma_window=20, ema_window=12, rsi_window=14):
        """
        Add multiple technical indicators to DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame with OHLC data
            sma_window (int): Window for SMA
            ema_window (int): Window for EMA
            rsi_window (int): Window for RSI
        
        Returns:
            pd.DataFrame: DataFrame with added indicators
        """
        df_copy = df.copy()
        
        # Add indicators
        df_copy['SMA_20'] = TechnicalAnalysis.calculate_sma(df, sma_window)
        df_copy['EMA_12'] = TechnicalAnalysis.calculate_ema(df, ema_window)
        df_copy['RSI_14'] = TechnicalAnalysis.calculate_rsi(df, rsi_window)
        
        # MACD
        macd, signal, hist = TechnicalAnalysis.calculate_macd(df)
        df_copy['MACD'] = macd
        df_copy['MACD_Signal'] = signal
        df_copy['MACD_Hist'] = hist
        
        # Bollinger Bands
        upper, middle, lower = TechnicalAnalysis.calculate_bollinger_bands(df)
        df_copy['BB_Upper'] = upper
        df_copy['BB_Middle'] = middle
        df_copy['BB_Lower'] = lower
        
        # ATR
        df_copy['ATR'] = TechnicalAnalysis.calculate_atr(df)
        
        return df_copy


class SupportResistance:
    """
    Calculate support and resistance levels using multiple methods
    """
    
    @staticmethod
    def calculate_pivot_points(df):
        """
        Calculate traditional pivot points
        
        Args:
            df (pd.DataFrame): DataFrame with OHLC data
        
        Returns:
            dict: Pivot levels
        """
        # Get the last row
        last = df.iloc[-1]
        
        high = last['High']
        low = last['Low']
        close = last['Close']
        
        pivot = (high + low + close) / 3
        resistance1 = (2 * pivot) - low
        support1 = (2 * pivot) - high
        resistance2 = pivot + (high - low)
        support2 = pivot - (high - low)
        
        return {
            'pivot': pivot,
            'resistance1': resistance1,
            'resistance2': resistance2,
            'support1': support1,
            'support2': support2
        }
    
    @staticmethod
    def calculate_fibonacci_levels(df):
        """
        Calculate Fibonacci retracement levels
        
        Args:
            df (pd.DataFrame): DataFrame with price data
        
        Returns:
            dict: Fibonacci levels
        """
        # Use 52-week high/low
        high = df['High'].max()
        low = df['Low'].min()
        
        diff = high - low
        
        # Fibonacci levels
        level_0 = low  # 0%
        level_236 = low + (diff * 0.236)  # 23.6%
        level_382 = low + (diff * 0.382)  # 38.2%
        level_500 = low + (diff * 0.500)  # 50%
        level_618 = low + (diff * 0.618)  # 61.8%
        level_100 = high  # 100%
        
        return {
            'fib_0': level_0,
            'fib_236': level_236,
            'fib_382': level_382,
            'fib_500': level_500,
            'fib_618': level_618,
            'fib_100': level_100
        }
    
    @staticmethod
    def calculate_recent_levels(df, lookback=20):
        """
        Calculate support/resistance from recent highs/lows
        
        Args:
            df (pd.DataFrame): DataFrame with price data
            lookback (int): Number of periods to look back
        
        Returns:
            dict: Recent levels
        """
        recent_data = df.tail(lookback)
        
        recent_high = recent_data['High'].max()
        recent_low = recent_data['Low'].min()
        current_price = recent_data['Close'].iloc[-1]
        
        # Distance to levels
        distance_to_high = recent_high - current_price
        distance_to_low = current_price - recent_low
        
        return {
            'recent_resistance': recent_high,
            'recent_support': recent_low,
            'distance_to_resistance': distance_to_high,
            'distance_to_support': distance_to_low,
            'current_price': current_price
        }
    
    @staticmethod
    def calculate_moving_average_support(df):
        """
        Use moving averages as dynamic support/resistance
        
        Args:
            df (pd.DataFrame): DataFrame with indicators
        
        Returns:
            dict: MA-based levels
        """
        last = df.iloc[-1]
        
        return {
            'sma_20': last.get('SMA_20', float('nan')),
            'ema_12': last.get('EMA_12', float('nan')),
            'bb_upper': last.get('BB_Upper', float('nan')),
            'bb_lower': last.get('BB_Lower', float('nan')),
            'bb_middle': last.get('BB_Middle', float('nan'))
        }
    
    @staticmethod
    def get_all_levels(df):
        """
        Get all support and resistance levels
        
        Args:
            df (pd.DataFrame): DataFrame with OHLC and indicators
        
        Returns:
            dict: All levels
        """
        # Ensure indicators are calculated
        if 'SMA_20' not in df.columns:
            df = TechnicalAnalysis.add_indicators(df)
        
        levels = {
            'pivot_points': SupportResistance.calculate_pivot_points(df),
            'fibonacci': SupportResistance.calculate_fibonacci_levels(df),
            'recent_levels': SupportResistance.calculate_recent_levels(df),
            'moving_averages': SupportResistance.calculate_moving_average_support(df)
        }
        
        return levels


class DataAnalyzer:
    """
    General data analysis functions
    """
    
    @staticmethod
    def calculate_statistics(df):
        """
        Calculate basic statistics for stock data
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
        
        Returns:
            dict: Statistics
        """
        return {
            'mean': df['Close'].mean(),
            'median': df['Close'].median(),
            'std_dev': df['Close'].std(),
            'min': df['Close'].min(),
            'max': df['Close'].max(),
            'range': df['Close'].max() - df['Close'].min()
        }
    
    @staticmethod
    def calculate_returns(df, period=1):
        """
        Calculate periodic returns
        
        Args:
            df (pd.DataFrame): DataFrame with 'Close' column
            period (int): Period for returns calculation
        
        Returns:
            pd.Series: Returns
        """
        return df['Close'].pct_change(periods=period)
    
    @staticmethod
    def export_to_csv(df, filename):
        """
        Export DataFrame to CSV
        
        Args:
            df (pd.DataFrame): DataFrame to export
            filename (str): Output filename
        """
        try:
            df.to_csv(filename)
            logger.info(f"Data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")

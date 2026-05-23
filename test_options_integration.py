#!/usr/bin/env python
"""Integration test for options analysis pipeline"""

import sys
sys.path.insert(0, 'src')

from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, SupportResistance, OptionsAnalysis
import numpy as np

# Quick test with AAPL
print("Testing Options Analysis Pipeline...")
print("-" * 50)

try:
    connector = YahooFinanceConnector()
    df = connector.fetch_historical_data('AAPL', '2024-11-01', '2024-12-15')
    info = connector.fetch_stock_info('AAPL')
    current_price = df['Close'].iloc[-1]
    print(f"[OK] Data fetched: {len(df)} bars, Current Price: ${current_price:.2f}")
except Exception as e:
    print(f"[ERROR] Failed to fetch data: {e}")
    sys.exit(1)

try:
    # Test technical analysis
    ta = TechnicalAnalysis()
    df_analysis = ta.add_indicators(df)
    rsi = df_analysis['RSI_14'].iloc[-1]
    macd = df_analysis['MACD'].iloc[-1]
    print(f"[OK] Technical Indicators: RSI={rsi:.2f}, MACD={macd:.4f}")
except Exception as e:
    print(f"[ERROR] Failed to calculate indicators: {e}")
    sys.exit(1)

try:
    # Test support resistance
    sr = SupportResistance()
    levels = sr.get_all_levels(df)
    pivot = levels["pivot_points"]["Pivot"]
    print(f"[OK] S/R Levels: Pivot=${pivot:.2f}")
except Exception as e:
    print(f"[ERROR] Failed to calculate S/R levels: {e}")
    sys.exit(1)

try:
    # Test options analysis
    oa = OptionsAnalysis()
    strategy = oa.get_strategy_recommendation(df_analysis, info, rsi, macd, current_price)
    print(f"[OK] Strategy: {strategy['strategy']} ({strategy['direction']}), Confidence: {strategy['confidence']}")
except Exception as e:
    print(f"[ERROR] Failed to get strategy recommendation: {e}")
    sys.exit(1)

try:
    # Test Greeks
    greeks = oa.calculate_greeks(current_price, current_price, 30/365, 0.05, 0.25)
    print(f"[OK] Greeks (ATM): Delta={greeks['delta']:.3f}, Theta={greeks['theta']:.4f}, Vega={greeks['vega']:.3f}")
except Exception as e:
    print(f"[ERROR] Failed to calculate Greeks: {e}")
    sys.exit(1)

try:
    # Test POP
    pop = oa.calculate_probability_of_profit(current_price, current_price, 30/365, 0.05, 0.25, 'call')
    print(f"[OK] Probability of Profit: {pop:.1f}%")
except Exception as e:
    print(f"[ERROR] Failed to calculate POP: {e}")
    sys.exit(1)

print("-" * 50)
print("✓✓✓ ALL TESTS PASSED - Options Analysis Ready ✓✓✓")

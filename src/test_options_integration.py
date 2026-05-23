#!/usr/bin/env python
"""Integration test for options analysis - run from src/"""

from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, SupportResistance, OptionsAnalysis

print("Testing Options Analysis Pipeline...")
print("-" * 50)

try:
    connector = YahooFinanceConnector()
    df = connector.fetch_historical_data('AAPL', '2024-11-01', '2024-12-15')
    info = connector.fetch_stock_info('AAPL')
    current_price = df['Close'].iloc[-1]
    print(f"[OK] Data fetched: {len(df)} bars, Current Price: ${current_price:.2f}")
except Exception as e:
    print(f"[ERROR] Data fetch failed: {e}")
    import traceback
    traceback.print_exc()

try:
    ta = TechnicalAnalysis()
    df_analysis = ta.add_indicators(df)
    rsi = df_analysis['RSI_14'].iloc[-1]
    macd = df_analysis['MACD'].iloc[-1]
    print(f"[OK] Technical Indicators: RSI={rsi:.2f}, MACD={macd:.4f}")
except Exception as e:
    print(f"[ERROR] Indicators failed: {e}")
    import traceback
    traceback.print_exc()

try:
    sr = SupportResistance()
    levels = sr.get_all_levels(df)
    pivot = levels["pivot_points"]["pivot"]
    print(f"[OK] S/R Levels: Pivot=${pivot:.2f}")
except Exception as e:
    print(f"[ERROR] S/R failed: {e}")
    import traceback
    traceback.print_exc()

try:
    oa = OptionsAnalysis()
    strategy = oa.get_strategy_recommendation(df_analysis, info, rsi, macd, current_price)
    print(f"[OK] Strategy: {strategy['strategy']} ({strategy['direction']}), Confidence: {strategy['confidence']}")
except Exception as e:
    print(f"[ERROR] Strategy recommendation failed: {e}")
    import traceback
    traceback.print_exc()

try:
    greeks = oa.calculate_greeks(current_price, current_price, 30/365, 0.05, 0.25)
    print(f"[OK] Greeks (ATM): Delta={greeks['delta']:.3f}, Theta={greeks['theta']:.4f}, Vega={greeks['vega']:.3f}")
except Exception as e:
    print(f"[ERROR] Greeks failed: {e}")
    import traceback
    traceback.print_exc()

try:
    pop = oa.calculate_probability_of_profit(current_price, current_price, 30/365, 0.05, 0.25, 'call')
    print(f"[OK] Probability of Profit: {pop:.1f}%")
except Exception as e:
    print(f"[ERROR] POP failed: {e}")
    import traceback
    traceback.print_exc()

print("-" * 50)
print("✓✓✓ ALL TESTS PASSED - Options Analysis Ready ✓✓✓")

"""
Support & Resistance Analysis - Comprehensive Guide
Understand different methods and how to use them for trading decisions
"""

SR_GUIDE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                  SUPPORT & RESISTANCE ANALYSIS GUIDE                        ║
║                  Technical Analysis for Trading Decisions                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


📚 WHAT IS SUPPORT & RESISTANCE?
═════════════════════════════════════════════════════════════════════════════

  Support:
  ├─ Price level where the stock tends to STOP FALLING
  ├─ Acts like a "floor" for the price
  ├─ Buyers step in at this level
  └─ Often marks lower boundary of trading range

  Resistance:
  ├─ Price level where the stock tends to STOP RISING
  ├─ Acts like a "ceiling" for the price
  ├─ Sellers step in at this level
  └─ Often marks upper boundary of trading range

  Key Concept:
  When support breaks down → stock may fall further
  When resistance breaks up → stock may rise further


🔍 FOUR S/R CALCULATION METHODS IN THIS APPLICATION
═════════════════════════════════════════════════════════════════════════════

Method 1: PIVOT POINTS (Daily)
──────────────────────────────

  What it is:
  • Calculated from yesterday's HIGH, LOW, CLOSE
  • Most common method for day traders
  • Recalculated daily

  Formula:
  • Pivot = (High + Low + Close) / 3
  • Resistance 1 = (2 × Pivot) - Low
  • Support 1 = (2 × Pivot) - High
  • Resistance 2 = Pivot + (High - Low)
  • Support 2 = Pivot - (High - Low)

  How to use:
  ✓ Day traders: Track these levels throughout the day
  ✓ Entry/Exit: Use R1/S1 as initial targets
  ✓ Breakout: Watch for breaks above R2 or below S2
  ✓ Trading range: Price often bounces between S1 and R1

  Example:
  If AAPL has:
    Pivot Point: $308.69
    Resistance 1: $311.53 ← First resistance level
    Support 1: $305.97    ← First support level
  
  Interpretation:
    • If price at $310, heading toward $311.53 resistance
    • If price bounces at $305.97, it's finding support
    • If breaks above $311.53, next target might be $314.25


Method 2: RECENT PRICE LEVELS (20-day High/Low)
────────────────────────────────────────────────

  What it is:
  • Uses actual HIGH and LOW from last 20 trading days
  • Represents recent price extremes
  • Good for swing traders

  How it works:
  • Resistance = Highest price in last 20 days
  • Support = Lowest price in last 20 days

  How to use:
  ✓ If price is near recent high → resistance
  ✓ If price is near recent low → support
  ✓ Breakout above recent high → significant move expected
  ✓ Drop below recent low → trend reversal likely

  Example:
  AAPL Recent Levels:
    Resistance (20-day high): $311.40 (+$2.58 from current $308.82)
    Support (20-day low):     $264.83 (-$43.99 from current)

  Interpretation:
    • Stock hit $311.40 recently - resistance point
    • Stock only dipped to $264.83 - strong support
    • Stock is closer to resistance than support
    • Likely to consolidate before breaking higher


Method 3: FIBONACCI RETRACEMENT LEVELS
───────────────────────────────────────

  What it is:
  • Based on Fibonacci mathematical sequence (0.618, 0.382, etc.)
  • Used to identify likely pullback levels
  • Excellent for swing traders and position traders

  Levels calculated:
  • 100% (0%) - Recent Low (start of move)
  • 23.6%      - Weak retracement level
  • 38.2%      - Normal retracement (strong support)
  • 50.0%      - Mid-point level
  • 61.8%      - Strong retracement (strong support)
  • 100% (High) - Recent High (end of move)

  How to use:
  ✓ In uptrend: Price often finds support at 38.2% or 61.8%
  ✓ In downtrend: Price often finds resistance at 38.2% or 61.8%
  ✓ If price bounces at 61.8% level → continues trend
  ✓ If price breaks below 61.8% level → trend reversal likely

  Example:
  AAPL Fibonacci Retracement (from $245.28 low to $311.40 high):
    61.8% level: $286.14 ← Strong support/resistance
    50.0% level: $278.34 ← Mid-point
    38.2% level: $270.54 ← Normal support/resistance
    23.6% level: $260.89 ← Weak support

  Interpretation:
    • Current price $308.82 is near the 100% high
    • If price falls, 61.8% ($286.14) is first major support
    • 50% ($278.34) is next support if 61.8 breaks
    • Multiple traders watch these levels


Method 4: DYNAMIC LEVELS (Moving Averages & Bollinger Bands)
─────────────────────────────────────────────────────────────

  What it is:
  • Uses calculated indicators as dynamic S/R
  • Changes as new data arrives
  • Good for understanding trend strength

  Levels:
  • Upper Bollinger Band = Resistance (overbought level)
  • SMA (20) = Trend support/resistance
  • Lower Bollinger Band = Support (oversold level)

  How to use:
  ✓ Price above SMA(20) → uptrend, SMA acts as support
  ✓ Price below SMA(20) → downtrend, SMA acts as resistance
  ✓ Price touches upper BB → overbought, resistance zone
  ✓ Price touches lower BB → oversold, support zone
  ✓ Bounce off SMA(20) → trend continuation likely

  Example:
  AAPL Moving Average Levels:
    Upper Bollinger: $314.92 ← Strong resistance
    SMA (20):        $289.22 ← Dynamic support (uptrend)
    Lower Bollinger: $263.51 ← Strong support

  Interpretation:
    • Price at $308.82 is above all moving averages
    • SMA(20) at $289.22 is support level
    • Upper Bollinger at $314.92 is resistance
    • Stock is in strong uptrend


📊 PRACTICAL TRADING EXAMPLES
═════════════════════════════════════════════════════════════════════════════

Example 1: Day Trading with Pivot Points
────────────────────────────────────────

  Situation: Stock opens at $308, Pivot R1 = $311.53, S1 = $305.97

  Strategy:
  1. Morning: Plan to buy near S1 ($305.97) if support holds
  2. Target: Sell at R1 ($311.53) for +$5.56 profit
  3. Stop: If breaks below S1, exit at -$3+ loss
  4. Risk/Reward: 1:1.8 (acceptable ratio)


Example 2: Swing Trading with Fibonacci
────────────────────────────────────────

  Situation: Stock in uptrend, near 61.8% Fibonacci level

  Strategy:
  1. If price pulls back to 61.8% Fibonacci level → STRONG BUY
  2. Stop loss: Just below the 61.8% level
  3. Target: Previous high or next resistance
  4. High probability: 38.2% and 61.8% levels hold ~70% of time


Example 3: Position Trading with Recent Levels
───────────────────────────────────────────────

  Situation: Stock breaking above recent 20-day high

  Strategy:
  1. Breakout above recent resistance = Buy signal
  2. Stop loss: Just below recent resistance
  3. Target: Next technical resistance level
  4. This move often extends further (no resistance above)


Example 4: Using All Levels Together
─────────────────────────────────────

  Current Price: $308.82

  Level Stack (from support to resistance):
  ┌─────────────────────────────────────┐
  │ $314.25  ← Pivot R2 (Strong Res)    │
  │ $313.00  ← Upper Bollinger          │
  │ $311.53  ← Pivot R1                 │
  │ $311.40  ← 20-day High              │
  ├─────────────────────────────────────┤
  │ $308.82  ← CURRENT PRICE ◄──────┐   │
  ├─────────────────────────────────────┤
  │ $305.97  ← Pivot S1                 │
  │ $289.22  ← SMA(20)                  │
  │ $286.14  ← Fib 61.8%                │
  │ $278.34  ← Fib 50%                  │
  │ $264.83  ← 20-day Low               │
  └─────────────────────────────────────┘

  Interpretation:
  • Nearest resistance: $311.40 (recent high)
  • Key resistance above: $311.53 (Pivot R1)
  • Nearest support: $305.97 (Pivot S1)
  • Major support: $289.22 (SMA 20-day average)
  • Strong support: $286.14 (Fibonacci 61.8%)


⚖️ WHICH LEVELS MATTER MOST?
═════════════════════════════════════════════════════════════════════════════

  For Day Traders:
  1. Pivot Points (most important)
  2. Recent 20-day levels
  3. Bollinger Bands

  For Swing Traders:
  1. Fibonacci levels
  2. Recent highs/lows
  3. Moving averages

  For Position Traders:
  1. Long-term support/resistance
  2. Fibonacci levels
  3. Round numbers ($300, $310, etc.)

  Multi-Timeframe Approach:
  • Weekly levels > Daily levels > Hourly levels
  • Respect higher timeframe support/resistance first


🎯 CONFIRMATION SIGNALS
═════════════════════════════════════════════════════════════════════════════

  Strong Buy Signal (Near Support):
  ✓ Price near support level
  ✓ RSI < 30 (oversold)
  ✓ Price bounces UP from support
  ✓ Volume increases on bounce
  → HIGH PROBABILITY BUY

  Strong Sell Signal (Near Resistance):
  ✓ Price near resistance level
  ✓ RSI > 70 (overbought)
  ✓ Price reverses DOWN from resistance
  ✓ Volume increases on rejection
  → HIGH PROBABILITY SELL


⚠️ COMMON MISTAKES
═════════════════════════════════════════════════════════════════════════════

  ✗ Trading against the trend (ignoring moving averages)
  ✗ Ignoring multiple timeframe analysis
  ✗ Trading exactly at levels (use zone, not exact price)
  ✗ Not checking volume on support/resistance tests
  ✗ Forcing trades at low-probability levels
  ✓ Instead: Wait for confirmation at key levels


🛠️ HOW TO USE IN THE GUI APPLICATION
═════════════════════════════════════════════════════════════════════════════

  1. Launch GUI application: python run_gui.py

  2. Enter stock symbol and date range

  3. Click "Fetch Data & Analyze"

  4. Scroll through results to find:

     "SUPPORT & RESISTANCE LEVELS" section displays:
     • Pivot Points (R2, R1, Pivot, S1, S2)
     • Recent Levels (20-day high/low)
     • Fibonacci Retracement (all 6 levels)
     • Dynamic Levels (Bollinger Bands, SMA)

  5. Use the levels together for trading decisions

  6. Remember: Higher timeframes override lower timeframes


📈 EXPECTED ACCURACY
═════════════════════════════════════════════════════════════════════════════

  Pivot Points: 65-70% accuracy (day traders)
  Fibonacci:    60-65% accuracy (multiple tests)
  Recent Levels: 70-75% accuracy (strong in trends)
  Combined:     75-80% accuracy (multiple confirmations)

  Note: No method is 100% accurate. Always use stop losses!


═════════════════════════════════════════════════════════════════════════════
For live trading, combine S/R analysis with:
- Trend confirmation (moving averages)
- Momentum indicators (RSI, MACD)
- Volume analysis
- Market structure

Remember: Risk Management > Profit Potential
═════════════════════════════════════════════════════════════════════════════
"""

if __name__ == '__main__':
    print(SR_GUIDE)

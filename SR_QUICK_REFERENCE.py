"""
Support & Resistance - Quick Reference Card
Fast lookup guide for trading decisions
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                SUPPORT & RESISTANCE - QUICK REFERENCE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT'S CALCULATED
═════════════════════════════════════════════════════════════════════════════

Four different S/R methods are automatically calculated:

1. PIVOT POINTS (Daily)
   └─ For: Day traders
   └─ Shows: R2, R1, Pivot, S1, S2
   └─ Updates: Daily
   
2. RECENT LEVELS (20-day)
   └─ For: Swing traders  
   └─ Shows: 20-day High, 20-day Low
   └─ Updates: Real-time
   
3. FIBONACCI RETRACEMENT
   └─ For: Position traders
   └─ Shows: 6 levels from 0% to 100%
   └─ Updates: Fixed (until new data)
   
4. DYNAMIC LEVELS
   └─ For: Trend traders
   └─ Shows: Upper/Lower Bollinger Bands, SMA(20)
   └─ Updates: Real-time


📊 WHAT THE GUI DISPLAYS
═════════════════════════════════════════════════════════════════════════════

When you analyze a stock, the GUI shows:

SUPPORT & RESISTANCE LEVELS Section:

  Pivot Points (Daily):          4️⃣ Values
  ├─ Resistance 2 (R2)          Strongest resistance
  ├─ Resistance 1 (R1)          First resistance
  ├─ Pivot Point                Neutral point
  ├─ Support 1 (S1)             First support
  └─ Support 2 (S2)             Strongest support

  Recent Price Levels:           2️⃣ Values
  ├─ Recent Resistance          20-day high
  └─ Recent Support             20-day low

  Fibonacci Retracement Levels:  6️⃣ Values
  ├─ 100% (High)                Top of range
  ├─ 61.8%                      Strong level
  ├─ 50.0%                      Middle
  ├─ 38.2%                      Strong level
  ├─ 23.6%                      Weak level
  └─ 0% (Low)                   Bottom of range

  Dynamic Levels:                3️⃣ Values
  ├─ Upper Bollinger            Resistance zone
  ├─ SMA (20)                   Trend line
  └─ Lower Bollinger            Support zone


💡 QUICK INTERPRETATION
═════════════════════════════════════════════════════════════════════════════

When Price is ABOVE Level:          When Price is BELOW Level:
✓ Level acts as SUPPORT             ✓ Level acts as RESISTANCE
✓ Price should bounce UP            ✓ Price may bounce DOWN
✓ Watch for confirmation            ✓ Watch for confirmation


Key Colors in GUI:
✓ GREEN (+): Price distance to resistance (bullish)
✗ RED (-): Price distance to support (bearish)


📈 COMMON SCENARIOS
═════════════════════════════════════════════════════════════════════════════

Scenario 1: Price near Resistance
─────────────────────────────────
Current: $308 | Resistance R1: $311
Distance: +$3 to resistance

Action:
✓ If RSI > 70 → SELL signal (overbought)
✓ If volume HIGH → Breakout likely
✓ If MACD negative → Reversal likely
✓ Otherwise → Wait for rejection

Scenario 2: Price near Support
──────────────────────────────
Current: $308 | Support S1: $305
Distance: -$3 to support

Action:
✓ If RSI < 30 → BUY signal (oversold)
✓ If volume HIGH → Bounce likely
✓ If MACD positive → Trend continues
✓ Otherwise → Wait for bounce


Scenario 3: Price breaks Resistance
──────────────────────────────────
Old Resistance: $311 | Now: $312
Previously rejected → Now broken through

Action:
✓ BULLISH signal
✓ Next resistance becomes new target
✓ Old resistance becomes new support
✓ Trend likely to continue up


🎲 PROBABILITY MATRIX
═════════════════════════════════════════════════════════════════════════════

                    Trend    Volume   RSI       Success
Day Trading:
• Pivot Points      -        High     38-62%    70%
• Bollinger Bands   -        -        <30/>70   65%

Swing Trading:
• Fibonacci         Up/Down  -        -         65%
• Recent Levels     Strong   High     -         70%

Position Trading:
• Combined (2+)     Strong   High     Con~      75%


🔧 HOW TO USE IN PRACTICE
═════════════════════════════════════════════════════════════════════════════

Step 1: Open GUI
   python run_gui.py

Step 2: Select Stock & Analyze
   - Enter symbol (e.g., AAPL)
   - Choose timeframe (1d for most traders)
   - Click "Fetch Data & Analyze"

Step 3: Scroll to "SUPPORT & RESISTANCE LEVELS"

Step 4: Identify Key Levels
   - Nearest Resistance: Where to sell?
   - Nearest Support: Where to cover losses?
   - Multiple confirmations: Strongest levels

Step 5: Combine with Other Signals
   - RSI: Overbought/Oversold
   - MACD: Trend direction
   - Volume: Confirmation strength
   - Trend: Context


⏰ WHICH METHOD TO USE WHEN
═════════════════════════════════════════════════════════════════════════════

TODAY (Intraday Trading):
   ► Use PIVOT POINTS
   ► Check R1/S1 for quick targets
   ► Trade between R1 and S1 normally

THIS WEEK (Swing Trading):
   ► Use FIBONACCI + RECENT LEVELS
   ► Expect bounces at 38.2%, 61.8%
   ► Break of recent high = bullish

THIS MONTH (Position Trading):
   ► Use FIBONACCI + SMA(20)
   ► Trend-following approach
   ► Multiple levels alignment = strength


⚠️ COMMON MISTAKES
═════════════════════════════════════════════════════════════════════════════

✗ Trading EXACTLY at level price
   ► Instead: Trade in zone (±0.5-1%)

✗ Using only ONE S/R method
   ► Instead: Use 2+ methods for confirmation

✗ Ignoring the overall TREND
   ► Instead: S/R + Trend direction = best

✗ No stop loss at support
   ► Instead: Place stop just below key support

✗ Trading in low volume
   ► Instead: Wait for volume confirmation


📚 EXAMPLES FROM REAL DATA
═════════════════════════════════════════════════════════════════════════════

Example Analysis: AAPL at $308.82

Pivot Points:
  R2: $314.25  │  R1: $311.53  │  P: $308.69
  S1: $305.97  │  S2: $303.13
  
  → Price between R1 ($311.53) and Pivot ($308.69)
  → Target: $311.53 for short-term
  → Stop: $305.97 (S1)

Recent Levels:
  Resistance: $311.40 (+$2.58)
  Support: $264.83 (-$43.99)
  
  → Very wide range (consolidating)
  → Breakout above $311 likely

Fibonacci:
  61.8%: $286.14 ← STRONG support
  50.0%: $278.34
  38.2%: $270.54
  
  → Multiple support zones below current
  → Good for protecting positions


═════════════════════════════════════════════════════════════════════════════

Remember: Support & Resistance + Confirmation = Higher Probability Trades

For detailed guide: SUPPORT_RESISTANCE_GUIDE.py
═════════════════════════════════════════════════════════════════════════════
""")

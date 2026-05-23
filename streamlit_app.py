"""
Yahoo Finance Trading Analysis - Web App
Streamlit-based interface for stock analysis with technical indicators, 
support/resistance levels, and options strategy recommendations.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, SupportResistance, DataAnalyzer, OptionsAnalysis

# Configure Streamlit
st.set_page_config(
    page_title="Stock Trading Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Stock Trading Analysis Dashboard")
st.markdown("Analyze stocks with technical indicators, support/resistance levels, and options strategies")

# Sidebar - Input Controls
st.sidebar.header("📊 Analysis Settings")

symbol = st.sidebar.text_input("Stock Symbol", value="AAPL", max_chars=5).upper()
col1, col2 = st.sidebar.columns(2)

with col1:
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=90)
    )

with col2:
    end_date = st.sidebar.date_input(
        "End Date",
        value=datetime.now()
    )

interval = st.sidebar.selectbox(
    "Time Interval",
    ["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"],
    index=5  # Default to 1d
)

analyze_button = st.sidebar.button("🔍 Fetch & Analyze", use_container_width=True)

# Main Analysis
if analyze_button or symbol:
    try:
        with st.spinner(f"Fetching data for {symbol}..."):
            # Initialize connectors
            connector = YahooFinanceConnector()
            ta = TechnicalAnalysis()
            sr = SupportResistance()
            da = DataAnalyzer()
            oa = OptionsAnalysis()
            
            # Fetch data
            df = connector.fetch_historical_data(symbol, str(start_date), str(end_date), interval)
            info = connector.fetch_stock_info(symbol)
            
            if df is None or len(df) == 0:
                st.error(f"No data found for {symbol}. Please check the symbol and date range.")
            else:
                # Add technical indicators
                df_analysis = ta.add_indicators(df)
                stats = da.calculate_statistics(df)
                
                # Get latest values
                current_price = df['Close'].iloc[-1]
                rsi = df_analysis['RSI_14'].iloc[-1]
                macd = df_analysis['MACD'].iloc[-1]
                sma20 = df_analysis['SMA_20'].iloc[-1]
                
                # Create tabs
                tab1, tab2, tab3 = st.tabs(["📊 Technical Analysis", "🎯 Options Strategies", "📈 Charts"])
                
                # ==================== TAB 1: TECHNICAL ANALYSIS ====================
                with tab1:
                    # Company Info
                    st.subheader(f"{info.get('name', symbol)} ({symbol})")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Current Price", f"${current_price:.2f}")
                    with col2:
                        change = ((current_price - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
                        st.metric("Period Change", f"{change:+.2f}%", f"${current_price - df['Close'].iloc[0]:+.2f}")
                    with col3:
                        st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
                    with col4:
                        st.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
                    
                    # Price Statistics
                    st.markdown("### 📊 Price Statistics")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("Mean", f"${stats['mean']:.2f}")
                    with col2:
                        st.metric("Median", f"${stats['median']:.2f}")
                    with col3:
                        st.metric("Std Dev", f"${stats['std_dev']:.2f}")
                    with col4:
                        st.metric("High", f"${stats['max']:.2f}")
                    with col5:
                        st.metric("Low", f"${stats['min']:.2f}")
                    
                    # Technical Indicators
                    st.markdown("### 📈 Technical Indicators")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        rsi_color = "🔴" if rsi > 70 else "🟢" if rsi < 30 else "🟡"
                        st.metric(f"{rsi_color} RSI (14)", f"{rsi:.2f}", help="Overbought > 70, Oversold < 30")
                    
                    with col2:
                        macd_color = "🟢" if macd > 0 else "🔴"
                        st.metric(f"{macd_color} MACD", f"{macd:.4f}", help="Positive = Bullish, Negative = Bearish")
                    
                    with col3:
                        ema12 = df_analysis['EMA_12'].iloc[-1]
                        st.metric("EMA (12)", f"${ema12:.2f}")
                    
                    with col4:
                        bb_upper = df_analysis['BB_Upper'].iloc[-1]
                        bb_lower = df_analysis['BB_Lower'].iloc[-1]
                        bb_mid = df_analysis['BB_Middle'].iloc[-1]
                        bb_width = ((bb_upper - bb_lower) / bb_mid) * 100
                        st.metric("BB Width %", f"{bb_width:.2f}%", help="Bollinger Bands volatility")
                    
                    # Support & Resistance Levels
                    st.markdown("### 🎯 Support & Resistance Levels")
                    
                    levels = sr.get_all_levels(df)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Pivot Points**")
                        pp = levels['pivot_points']
                        st.text(
                            f"R2: ${pp['resistance2']:.2f}\n"
                            f"R1: ${pp['resistance1']:.2f}\n"
                            f"Pivot: ${pp['pivot']:.2f}\n"
                            f"S1: ${pp['support1']:.2f}\n"
                            f"S2: ${pp['support2']:.2f}"
                        )
                    
                    with col2:
                        st.markdown("**Dynamic Levels**")
                        recent = levels.get('recent_levels', {})
                        if recent:
                            st.text(
                                f"Resistance: ${recent.get('resistance', 'N/A')}\n"
                                f"Support: ${recent.get('support', 'N/A')}\n"
                                f"Current: ${current_price:.2f}"
                            )
                
                # ==================== TAB 2: OPTIONS STRATEGIES ====================
                with tab2:
                    # Get strategy recommendation
                    strategy = oa.get_strategy_recommendation(df_analysis, info, rsi, macd, current_price)
                    
                    st.markdown("### 🎯 Strategy Recommendation")
                    
                    # Strategy Card
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        direction_color = "🟢" if strategy['direction'] == "BULLISH" else "🔴" if strategy['direction'] == "BEARISH" else "🟡"
                        st.metric(f"{direction_color} Market Direction", strategy['direction'])
                    
                    with col2:
                        confidence_color = "🟢" if strategy['confidence'] == "HIGH" else "🟡" if strategy['confidence'] == "MEDIUM" else "🔴"
                        st.metric(f"{confidence_color} Confidence", strategy['confidence'])
                    
                    with col3:
                        st.metric("Strategy Type", strategy['strategy'])
                    
                    st.info(f"📌 **Rationale:** {strategy['rationale']}")
                    
                    # Greeks Analysis for ATM Strike
                    st.markdown("### 📊 Greeks Analysis (ATM Strike)")
                    
                    # Calculate Greeks for ATM strike
                    days_to_expiry = 30  # Default 30 DTE
                    volatility = 0.25    # Default 25% IV
                    risk_free_rate = 0.05  # Default 5%
                    
                    greeks = oa.calculate_greeks(
                        current_price, 
                        current_price,  # ATM strike
                        days_to_expiry / 365,
                        risk_free_rate,
                        volatility,
                        strategy['type'].split('_')[1] if '_' in strategy['type'] else 'call'
                    )
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("Delta (Δ)", f"{greeks['delta']:.3f}", 
                                help="Price sensitivity. 0.5 = moves $0.50 for $1 move in stock")
                    
                    with col2:
                        st.metric("Gamma (Γ)", f"{greeks['gamma']:.3f}",
                                help="Delta acceleration")
                    
                    with col3:
                        st.metric("Theta (Θ)", f"{greeks['theta']:.4f}",
                                help="Daily time decay")
                    
                    with col4:
                        st.metric("Vega (ν)", f"{greeks['vega']:.3f}",
                                help="Volatility sensitivity")
                    
                    with col5:
                        st.metric("Rho (ρ)", f"{greeks['rho']:.3f}",
                                help="Interest rate sensitivity")
                    
                    # Probability of Profit
                    st.markdown("### 📈 Probability of Profit")
                    
                    pop = oa.calculate_probability_of_profit(
                        current_price,
                        current_price,  # ATM
                        days_to_expiry / 365,
                        risk_free_rate,
                        volatility,
                        strategy['type'].split('_')[1] if '_' in strategy['type'] else 'call'
                    )
                    
                    pop_color = "🟢" if pop > 65 else "🟡" if pop > 50 else "🔴"
                    st.metric(f"{pop_color} Probability of Profit (30 DTE)", f"{pop:.1f}%")
                    
                    if pop > 65:
                        st.success("High probability setup - Favorable risk/reward")
                    elif pop > 50:
                        st.info("Moderate probability setup - Fair risk/reward")
                    else:
                        st.warning("Lower probability setup - Consider risk management")
                    
                    # Strike Recommendations
                    st.markdown("### 🎯 Recommended Strikes")
                    
                    atr = df_analysis['ATR_14'].iloc[-1]
                    atm_strike = round(current_price, 0)
                    otm_strikes = [
                        round(current_price + atr, 0),
                        round(current_price - atr, 0)
                    ]
                    
                    st.write(f"**ATM (At-The-Money):** ${atm_strike:.0f}")
                    st.write(f"**OTM Strikes:** ${otm_strikes[0]:.0f} / ${otm_strikes[1]:.0f}")
                    
                    # Risk Management
                    st.markdown("### ⚠️ Risk Management Rules")
                    st.write("""
                    - **Entry:** Use technical confirmation (support/resistance levels)
                    - **Stop Loss:** Place below S1 (support) or above R1 (resistance)
                    - **Take Profit:** Target R1 for profit-taking
                    - **Position Size:** Risk max 2% of account per trade
                    - **Expiration:** Avoid last 7 days of expiration (Theta decay accelerates)
                    """)
                
                # ==================== TAB 3: CHARTS ====================
                with tab3:
                    st.markdown("### 📈 Price Chart with Indicators")
                    
                    import plotly.graph_objects as go
                    
                    fig = go.Figure()
                    
                    # Candlestick
                    fig.add_trace(go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name='Price'
                    ))
                    
                    # SMA 20
                    fig.add_trace(go.Scatter(
                        x=df_analysis.index,
                        y=df_analysis['SMA_20'],
                        name='SMA 20',
                        line=dict(color='orange', width=1)
                    ))
                    
                    # EMA 12
                    fig.add_trace(go.Scatter(
                        x=df_analysis.index,
                        y=df_analysis['EMA_12'],
                        name='EMA 12',
                        line=dict(color='blue', width=1)
                    ))
                    
                    fig.update_layout(
                        title=f"{symbol} - Price with Moving Averages",
                        yaxis_title="Price ($)",
                        xaxis_title="Date",
                        template="plotly_white",
                        height=400,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # RSI Chart
                    fig_rsi = go.Figure()
                    fig_rsi.add_trace(go.Scatter(
                        x=df_analysis.index,
                        y=df_analysis['RSI_14'],
                        name='RSI (14)',
                        line=dict(color='purple')
                    ))
                    
                    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                    
                    fig_rsi.update_layout(
                        title=f"{symbol} - RSI (14)",
                        yaxis_title="RSI",
                        xaxis_title="Date",
                        template="plotly_white",
                        height=300,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig_rsi, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        st.info("Please check your inputs and try again.")

# Footer
st.markdown("---")
st.markdown(
    """
    **Yahoo Finance Trading Analysis** | 
    [GitHub](https://github.com) | 
    Data from Yahoo Finance API
    """
)

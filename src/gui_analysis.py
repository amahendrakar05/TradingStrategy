"""
GUI Application for Yahoo Finance Technical Analysis
Interactive interface to select stocks and date ranges, display technical statistics
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from yahoo_finance import YahooFinanceConnector
from analysis import TechnicalAnalysis, DataAnalyzer, SupportResistance, OptionsAnalysis
import threading
import yfinance as yf

class YahooFinanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahoo Finance Technical Analysis")
        self.root.geometry("900x750")
        self.root.configure(bg='#f0f0f0')
        
        self.connector = YahooFinanceConnector()
        self.df_data = None
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Yahoo Finance Technical Analysis", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # --- Input Section ---
        input_frame = ttk.LabelFrame(main_frame, text="Stock Selection", padding="10")
        input_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Stock Symbol
        ttk.Label(input_frame, text="Stock Symbol:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.symbol_entry = ttk.Entry(input_frame, width=15)
        self.symbol_entry.insert(0, "AAPL")
        self.symbol_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Start Date
        ttk.Label(input_frame, text="Start Date:").grid(row=0, column=2, sticky=tk.W, padx=5)
        start_default = (datetime.now() - timedelta(days=365)).date()
        self.start_date_entry = DateEntry(input_frame, width=15, background='darkblue',
                                         foreground='white', borderwidth=2,
                                         year=start_default.year,
                                         month=start_default.month,
                                         day=start_default.day)
        self.start_date_entry.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # End Date
        ttk.Label(input_frame, text="End Date:").grid(row=1, column=0, sticky=tk.W, padx=5)
        end_default = datetime.now().date()
        self.end_date_entry = DateEntry(input_frame, width=15, background='darkblue',
                                       foreground='white', borderwidth=2,
                                       year=end_default.year,
                                       month=end_default.month,
                                       day=end_default.day)
        self.end_date_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Interval
        ttk.Label(input_frame, text="Interval:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.interval_var = tk.StringVar(value="1d")
        interval_combo = ttk.Combobox(input_frame, textvariable=self.interval_var,
                                     values=["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"],
                                     width=10, state="readonly")
        interval_combo.grid(row=1, column=3, sticky=tk.W, padx=5)
        
        # Button Frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        self.fetch_button = ttk.Button(button_frame, text="Fetch Data & Analyze",
                                      command=self.fetch_and_analyze)
        self.fetch_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = ttk.Label(input_frame, text="Ready", foreground="green")
        self.status_label.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=5)
        
        # --- Results Section with Tabs ---
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Technical Analysis
        self.tech_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tech_frame, text="Technical Analysis")
        
        self.results_text = scrolledtext.ScrolledText(self.tech_frame, height=25, width=95,
                                                      font=("Courier", 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags
        self.results_text.tag_config("header", font=("Courier", 11, "bold"), foreground="blue")
        self.results_text.tag_config("subheader", font=("Courier", 10, "bold"), foreground="darkblue")
        self.results_text.tag_config("positive", foreground="green")
        self.results_text.tag_config("negative", foreground="red")
        self.results_text.tag_config("neutral", foreground="black")
        
        # Tab 2: Options Strategy
        self.options_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.options_frame, text="Options Strategies")
        
        self.options_text = scrolledtext.ScrolledText(self.options_frame, height=25, width=95,
                                                      font=("Courier", 9))
        self.options_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for options
        self.options_text.tag_config("header", font=("Courier", 11, "bold"), foreground="blue")
        self.options_text.tag_config("subheader", font=("Courier", 10, "bold"), foreground="darkblue")
        self.options_text.tag_config("bullish", foreground="green", font=("Courier", 9, "bold"))
        self.options_text.tag_config("bearish", foreground="red", font=("Courier", 9, "bold"))
        self.options_text.tag_config("neutral", foreground="orange", font=("Courier", 9, "bold"))
        self.options_text.tag_config("positive", foreground="green")
        self.options_text.tag_config("negative", foreground="red")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
    
    def fetch_and_analyze(self):
        """Fetch data and perform analysis"""
        symbol = self.symbol_entry.get().upper().strip()
        
        if not symbol:
            messagebox.showerror("Error", "Please enter a stock symbol")
            return
        
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date_entry.get_date().strftime('%Y-%m-%d')
        interval = self.interval_var.get()
        
        # Disable button during fetch
        self.fetch_button.config(state="disabled")
        self.status_label.config(text="Fetching data...", foreground="orange")
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Run in thread to prevent UI freezing
        thread = threading.Thread(target=self._fetch_thread, args=(symbol, start_date, end_date, interval))
        thread.start()
    
    def _fetch_thread(self, symbol, start_date, end_date, interval):
        """Fetch data in background thread"""
        try:
            # Fetch data
            self.df_data = self.connector.fetch_historical_data(symbol, start_date, end_date, interval)
            
            if self.df_data is None or self.df_data.empty:
                self.root.after(0, lambda: self._show_error(f"No data found for {symbol}"))
                return
            
            # Get stock info
            info = self.connector.fetch_stock_info(symbol)
            
            # Add technical indicators
            df_analysis = TechnicalAnalysis.add_indicators(self.df_data)
            
            # Calculate statistics
            stats = DataAnalyzer.calculate_statistics(self.df_data)
            
            # Display results
            self.root.after(0, lambda: self._display_results(symbol, info, df_analysis, stats, start_date, end_date))
            
            # Get options analysis
            self.root.after(0, lambda: self._display_options_analysis(symbol, df_analysis, info))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error: {str(e)}"))
    
    def _display_results(self, symbol, info, df_analysis, stats, start_date, end_date):
        """Display analysis results in text area"""
        try:
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            # Header
            header_text = f"{'='*95}\n"
            header_text += f"TECHNICAL ANALYSIS: {symbol} ({start_date} to {end_date})\n"
            header_text += f"{'='*95}\n\n"
            self.results_text.insert(tk.END, header_text, "header")
            
            # Stock Information
            if info:
                self.results_text.insert(tk.END, "COMPANY INFORMATION\n", "subheader")
                self.results_text.insert(tk.END, f"{'-'*95}\n")
                self.results_text.insert(tk.END, f"Company Name:        {info.get('company_name', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Sector:              {info.get('sector', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Industry:            {info.get('industry', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Current Price:       ${info.get('current_price', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Market Cap:          ${info.get('market_cap', 'N/A'):,}\n")
                self.results_text.insert(tk.END, f"P/E Ratio:           {info.get('pe_ratio', 'N/A')}\n")
                self.results_text.insert(tk.END, f"52-Week High:        ${info.get('52_week_high', 'N/A')}\n")
                self.results_text.insert(tk.END, f"52-Week Low:         ${info.get('52_week_low', 'N/A')}\n\n")
            
            # Price Statistics
            self.results_text.insert(tk.END, "PRICE STATISTICS\n", "subheader")
            self.results_text.insert(tk.END, f"{'-'*95}\n")
            self.results_text.insert(tk.END, f"Mean:                ${stats['mean']:.2f}\n")
            self.results_text.insert(tk.END, f"Median:              ${stats['median']:.2f}\n")
            self.results_text.insert(tk.END, f"Std Dev:             ${stats['std_dev']:.2f}\n")
            self.results_text.insert(tk.END, f"Min Price:           ${stats['min']:.2f}\n")
            self.results_text.insert(tk.END, f"Max Price:           ${stats['max']:.2f}\n")
            self.results_text.insert(tk.END, f"Price Range:         ${stats['range']:.2f}\n\n")
            
            # Support and Resistance Levels
            levels = SupportResistance.get_all_levels(df_analysis)
            self.results_text.insert(tk.END, "SUPPORT & RESISTANCE LEVELS\n", "subheader")
            self.results_text.insert(tk.END, f"{'-'*95}\n")
            
            current = df_analysis.iloc[-1]['Close']
            
            # Pivot Points
            self.results_text.insert(tk.END, "Pivot Points (Daily):\n")
            pp = levels['pivot_points']
            self.results_text.insert(tk.END, f"  Resistance 2:       ${pp['resistance2']:.2f}")
            
            if pp['resistance2'] > current:
                distance = pp['resistance2'] - current
                self.results_text.insert(tk.END, f"  (+${distance:.2f})\n", "positive")
            else:
                distance = current - pp['resistance2']
                self.results_text.insert(tk.END, f"  (-${distance:.2f})\n", "negative")
            
            self.results_text.insert(tk.END, f"  Resistance 1:       ${pp['resistance1']:.2f}")
            if pp['resistance1'] > current:
                distance = pp['resistance1'] - current
                self.results_text.insert(tk.END, f"  (+${distance:.2f})\n", "positive")
            else:
                distance = current - pp['resistance1']
                self.results_text.insert(tk.END, f"  (-${distance:.2f})\n", "negative")
            
            self.results_text.insert(tk.END, f"  Pivot Point:        ${pp['pivot']:.2f}\n")
            
            self.results_text.insert(tk.END, f"  Support 1:          ${pp['support1']:.2f}")
            if pp['support1'] < current:
                distance = current - pp['support1']
                self.results_text.insert(tk.END, f"  (-${distance:.2f})\n", "negative")
            else:
                distance = pp['support1'] - current
                self.results_text.insert(tk.END, f"  (+${distance:.2f})\n", "positive")
            
            self.results_text.insert(tk.END, f"  Support 2:          ${pp['support2']:.2f}")
            if pp['support2'] < current:
                distance = current - pp['support2']
                self.results_text.insert(tk.END, f"  (-${distance:.2f})\n\n", "negative")
            else:
                distance = pp['support2'] - current
                self.results_text.insert(tk.END, f"  (+${distance:.2f})\n\n", "positive")
            
            # Recent Levels
            recent = levels['recent_levels']
            self.results_text.insert(tk.END, "Recent Price Levels (20 days):\n")
            self.results_text.insert(tk.END, f"  Recent Resistance:  ${recent['recent_resistance']:.2f}")
            distance = recent['recent_resistance'] - current
            self.results_text.insert(tk.END, f"  (+${distance:.2f})\n", "positive")
            
            self.results_text.insert(tk.END, f"  Recent Support:     ${recent['recent_support']:.2f}")
            distance = current - recent['recent_support']
            self.results_text.insert(tk.END, f"  (-${distance:.2f})\n\n", "negative")
            
            # Moving Average Levels
            ma_levels = levels['moving_averages']
            self.results_text.insert(tk.END, "Dynamic Levels (Moving Averages):\n")
            self.results_text.insert(tk.END, f"  Upper Bollinger:    ${ma_levels['bb_upper']:.2f}")
            if ma_levels['bb_upper'] > current:
                distance = ma_levels['bb_upper'] - current
                self.results_text.insert(tk.END, f"  (Resistance)\n", "positive")
            else:
                self.results_text.insert(tk.END, f"  (Above current)\n", "neutral")
            
            self.results_text.insert(tk.END, f"  SMA (20):           ${ma_levels['sma_20']:.2f}")
            if ma_levels['sma_20'] > current:
                self.results_text.insert(tk.END, f"  (Resistance)\n", "negative")
            else:
                self.results_text.insert(tk.END, f"  (Support)\n", "positive")
            
            self.results_text.insert(tk.END, f"  Lower Bollinger:    ${ma_levels['bb_lower']:.2f}")
            if ma_levels['bb_lower'] < current:
                distance = current - ma_levels['bb_lower']
                self.results_text.insert(tk.END, f"  (Support)\n\n", "negative")
            else:
                self.results_text.insert(tk.END, f"  (Below current)\n\n", "neutral")
            
            # Fibonacci Levels
            fib = levels['fibonacci']
            self.results_text.insert(tk.END, "Fibonacci Retracement Levels:\n")
            self.results_text.insert(tk.END, f"  100.0% (High):      ${fib['fib_100']:.2f}\n")
            self.results_text.insert(tk.END, f"  61.8%:              ${fib['fib_618']:.2f}")
            if fib['fib_618'] > current:
                self.results_text.insert(tk.END, f"  (Resistance)\n", "positive")
            else:
                self.results_text.insert(tk.END, f"  (Support)\n", "negative")
            
            self.results_text.insert(tk.END, f"  50.0%:              ${fib['fib_500']:.2f}\n")
            self.results_text.insert(tk.END, f"  38.2%:              ${fib['fib_382']:.2f}")
            if fib['fib_382'] < current:
                self.results_text.insert(tk.END, f"  (Support)\n", "negative")
            else:
                self.results_text.insert(tk.END, f"  (Resistance)\n", "positive")
            
            self.results_text.insert(tk.END, f"  23.6%:              ${fib['fib_236']:.2f}\n")
            self.results_text.insert(tk.END, f"  0.0% (Low):         ${fib['fib_0']:.2f}\n\n")
            
            # Latest Indicators
            self.results_text.insert(tk.END, "LATEST TECHNICAL INDICATORS (Most Recent)\n", "subheader")
            self.results_text.insert(tk.END, f"{'-'*95}\n")
            
            latest = df_analysis.iloc[-1]
            
            # Price
            current_price = latest['Close']
            prev_price = df_analysis.iloc[-2]['Close'] if len(df_analysis) > 1 else current_price
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price * 100) if prev_price != 0 else 0
            
            tag = "positive" if price_change >= 0 else "negative"
            self.results_text.insert(tk.END, f"Current Close Price: ${current_price:.2f} ", tag)
            self.results_text.insert(tk.END, f"({price_change:+.2f} / {price_change_pct:+.2f}%)\n", tag)
            self.results_text.insert(tk.END, f"Volume:              {int(latest.get('Volume', 0)):,}\n")
            self.results_text.insert(tk.END, f"\n")
            
            # Moving Averages
            self.results_text.insert(tk.END, "Moving Averages:\n")
            self.results_text.insert(tk.END, f"  SMA (20):          ${latest.get('SMA_20', float('nan')):.2f}\n")
            self.results_text.insert(tk.END, f"  EMA (12):          ${latest.get('EMA_12', float('nan')):.2f}\n")
            
            # Momentum Indicators
            self.results_text.insert(tk.END, f"\nMomentum Indicators:\n")
            rsi = latest.get('RSI_14', float('nan'))
            rsi_status = ""
            if rsi < 30:
                rsi_status = "(Oversold)"
            elif rsi > 70:
                rsi_status = "(Overbought)"
            self.results_text.insert(tk.END, f"  RSI (14):          {rsi:.2f} {rsi_status}\n")
            
            macd = latest.get('MACD', float('nan'))
            macd_signal = latest.get('MACD_Signal', float('nan'))
            self.results_text.insert(tk.END, f"  MACD:              {macd:.4f}\n")
            self.results_text.insert(tk.END, f"  MACD Signal:       {macd_signal:.4f}\n")
            self.results_text.insert(tk.END, f"  MACD Histogram:    {latest.get('MACD_Hist', float('nan')):.4f}\n")
            
            # Bollinger Bands
            self.results_text.insert(tk.END, f"\nBollinger Bands:\n")
            self.results_text.insert(tk.END, f"  Upper Band:        ${latest.get('BB_Upper', float('nan')):.2f}\n")
            self.results_text.insert(tk.END, f"  Middle Band (SMA): ${latest.get('BB_Middle', float('nan')):.2f}\n")
            self.results_text.insert(tk.END, f"  Lower Band:        ${latest.get('BB_Lower', float('nan')):.2f}\n")
            
            # ATR
            self.results_text.insert(tk.END, f"\nVolatility Indicators:\n")
            self.results_text.insert(tk.END, f"  ATR (14):          ${latest.get('ATR', float('nan')):.2f}\n")
            
            # Recent Data Table
            self.results_text.insert(tk.END, f"\n\nRECENT DATA (Last 10 Days)\n", "subheader")
            self.results_text.insert(tk.END, f"{'-'*95}\n")
            
            # Table header
            header = f"{'Date':<20} {'Open':>12} {'High':>12} {'Low':>12} {'Close':>12} {'Volume':>15}\n"
            self.results_text.insert(tk.END, header)
            self.results_text.insert(tk.END, f"{'-'*95}\n")
            
            # Display last 10 rows
            for idx, row in df_analysis.tail(10).iterrows():
                date_str = str(idx.date()) if hasattr(idx, 'date') else str(idx)[:10]
                self.results_text.insert(tk.END, 
                    f"{date_str:<20} ${row['Open']:>11.2f} ${row['High']:>11.2f} ${row['Low']:>11.2f} ${row['Close']:>11.2f} {int(row.get('Volume', 0)):>14,}\n")
            
            self.results_text.insert(tk.END, f"\n{'='*95}\n")
            self.results_text.insert(tk.END, "Analysis completed successfully!\n")
            
            self.results_text.config(state=tk.DISABLED)
            self.status_label.config(text=f"✓ Analysis complete for {len(df_analysis)} records", foreground="green")
            
        finally:
            self.fetch_button.config(state="normal")
    
    def _show_error(self, message):
        """Show error message and reset UI"""
        messagebox.showerror("Error", message)
        self.status_label.config(text="Error occurred", foreground="red")
        self.fetch_button.config(state="normal")
    
    def _display_options_analysis(self, symbol, df_analysis, info):
        """Display options strategy analysis"""
        try:
            self.options_text.config(state=tk.NORMAL)
            self.options_text.delete(1.0, tk.END)
            
            current_price = df_analysis.iloc[-1]['Close']
            latest = df_analysis.iloc[-1]
            
            # Get technical indicators for recommendation
            rsi_14 = latest.get('RSI_14', 50)
            macd = latest.get('MACD', 0)
            
            # Get strategy recommendation
            recommendation = OptionsAnalysis.get_strategy_recommendation(
                df_analysis, info, rsi_14, macd, current_price
            )
            
            # Header
            header_text = f"{'='*95}\n"
            header_text += f"OPTIONS STRATEGY ANALYSIS: {symbol} | Current Price: ${current_price:.2f}\n"
            header_text += f"{'='*95}\n\n"
            self.options_text.insert(tk.END, header_text, "header")
            
            # Recommended Strategy Section
            self.options_text.insert(tk.END, "RECOMMENDED STRATEGY\n", "subheader")
            self.options_text.insert(tk.END, f"{'-'*95}\n")
            
            strategy_tag = "bullish" if recommendation['direction'] == 'BULLISH' else \
                          "bearish" if recommendation['direction'] == 'BEARISH' else "neutral"
            
            self.options_text.insert(tk.END, f"Strategy:      ", "neutral")
            self.options_text.insert(tk.END, f"{recommendation['strategy']}\n", strategy_tag)
            
            self.options_text.insert(tk.END, f"Direction:     ", "neutral")
            self.options_text.insert(tk.END, f"{recommendation['direction']}\n", strategy_tag)
            
            self.options_text.insert(tk.END, f"Confidence:    {recommendation['confidence']}\n")
            self.options_text.insert(tk.END, f"Rationale:     {recommendation['rationale']}\n\n")
            
            # Strike Price Recommendations Section
            self.options_text.insert(tk.END, "STRIKE PRICE RECOMMENDATIONS\n", "subheader")
            self.options_text.insert(tk.END, f"{'-'*95}\n")
            
            # ATM and OTM strikes
            atm_strike = round(current_price)
            otm_long = round(current_price * 1.02) if recommendation['direction'] == 'BULLISH' else round(current_price * 0.98)
            otm_short = round(current_price * 1.05) if recommendation['direction'] == 'BULLISH' else round(current_price * 0.95)
            
            if recommendation['direction'] == 'BULLISH':
                self.options_text.insert(tk.END, f"\nBUY CALL Strategy:\n")
                self.options_text.insert(tk.END, f"  Long Call Strike:    ${atm_strike:.2f}  (ATM or slightly OTM)\n", "positive")
                self.options_text.insert(tk.END, f"  Short Call Strike:   ${otm_short:.2f}  (Further OTM for spread)\n", "positive")
                self.options_text.insert(tk.END, f"\n  Strategy Benefits:\n")
                self.options_text.insert(tk.END, f"  • Lower cost with call spread vs single call\n")
                self.options_text.insert(tk.END, f"  • Max profit capped but defined risk\n")
                self.options_text.insert(tk.END, f"  • Theta decay works in seller's favor\n")
                
            elif recommendation['direction'] == 'BEARISH':
                self.options_text.insert(tk.END, f"\nBUY PUT Strategy:\n")
                self.options_text.insert(tk.END, f"  Long Put Strike:     ${atm_strike:.2f}  (ATM or slightly OTM)\n", "negative")
                self.options_text.insert(tk.END, f"  Short Put Strike:    ${otm_short:.2f}  (Further OTM for spread)\n", "negative")
                self.options_text.insert(tk.END, f"\n  Strategy Benefits:\n")
                self.options_text.insert(tk.END, f"  • Lower cost with put spread vs single put\n")
                self.options_text.insert(tk.END, f"  • Max profit capped but defined risk\n")
                self.options_text.insert(tk.END, f"  • Theta decay works in seller's favor\n")
                
            else:  # NEUTRAL
                self.options_text.insert(tk.END, f"\nIRON CONDOR Strategy (Neutral):\n")
                self.options_text.insert(tk.END, f"  Call Strike (Long):  ${round(current_price * 1.05):.2f}   Sell: ${round(current_price * 1.02):.2f}\n", "neutral")
                self.options_text.insert(tk.END, f"  Put Strike (Long):   ${round(current_price * 0.95):.2f}   Sell: ${round(current_price * 0.98):.2f}\n", "neutral")
                self.options_text.insert(tk.END, f"\n  Strategy Benefits:\n")
                self.options_text.insert(tk.END, f"  • Profit from theta decay on both sides\n")
                self.options_text.insert(tk.END, f"  • Profits if stock stays in range\n")
                self.options_text.insert(tk.END, f"  • Limited max profit and max loss\n")
            
            # Greeks Analysis
            self.options_text.insert(tk.END, f"\n\nGREEKS ANALYSIS (For ATM ${atm_strike:.0f} Strike)\n", "subheader")
            self.options_text.insert(tk.END, f"{'-'*95}\n")
            
            volatility = df_analysis['Close'].std() / df_analysis['Close'].mean()
            T = 30 / 365  # Assume 30 DTE
            r = 0.05
            
            if recommendation['direction'] == 'BULLISH':
                greeks = OptionsAnalysis.calculate_greeks(current_price, atm_strike, T, r, volatility, 'call')
                pop = OptionsAnalysis.calculate_probability_of_profit(current_price, atm_strike, T, r, volatility, 'call')
                option_type = "CALL"
            elif recommendation['direction'] == 'BEARISH':
                greeks = OptionsAnalysis.calculate_greeks(current_price, atm_strike, T, r, volatility, 'put')
                pop = OptionsAnalysis.calculate_probability_of_profit(current_price, atm_strike, T, r, volatility, 'put')
                option_type = "PUT"
            else:
                greeks = {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
                pop = 50
                option_type = "STRADDLE"
            
            self.options_text.insert(tk.END, f"Option Type:         {option_type}\n")
            self.options_text.insert(tk.END, f"Strike Price:        ${atm_strike:.2f}\n")
            self.options_text.insert(tk.END, f"Days to Expiration:  30 (Estimated)\n\n")
            
            self.options_text.insert(tk.END, f"Greeks:\n")
            self.options_text.insert(tk.END, f"  Delta (Δ):         {greeks['delta']:.4f}  (Price sensitivity)\n")
            self.options_text.insert(tk.END, f"  Gamma (Γ):         {greeks['gamma']:.6f}  (Delta acceleration)\n")
            self.options_text.insert(tk.END, f"  Theta (Θ):         {greeks['theta']:.4f}  (Daily decay)\n")
            self.options_text.insert(tk.END, f"  Vega (ν):          {greeks['vega']:.4f}  (Volatility exposure)\n")
            self.options_text.insert(tk.END, f"  Rho (ρ):           {greeks['rho']:.4f}  (Rate sensitivity)\n\n")
            
            # Probability of Profit
            self.options_text.insert(tk.END, f"Probability Analysis:\n")
            if pop > 65:
                pop_tag = "positive"
            elif pop > 50:
                pop_tag = "neutral"
            else:
                pop_tag = "negative"
            
            self.options_text.insert(tk.END, f"  Probability of Profit (POP): ", "neutral")
            self.options_text.insert(tk.END, f"{pop:.1f}%\n", pop_tag)
            
            if pop > 65:
                self.options_text.insert(tk.END, f"  Interpretation: High probability trade\n")
            elif pop > 50:
                self.options_text.insert(tk.END, f"  Interpretation: Reasonable probability trade\n")
            else:
                self.options_text.insert(tk.END, f"  Interpretation: Low probability, use caution\n")
            
            # Risk Management
            self.options_text.insert(tk.END, f"\n\nRISK MANAGEMENT\n", "subheader")
            self.options_text.insert(tk.END, f"{'-'*95}\n")
            
            self.options_text.insert(tk.END, f"Entry Rules:\n")
            self.options_text.insert(tk.END, f"  • Execute when technical setup is confirmed\n")
            self.options_text.insert(tk.END, f"  • Use limit orders (don't market order)\n")
            self.options_text.insert(tk.END, f"  • Risk no more than 2% per trade\n\n")
            
            self.options_text.insert(tk.END, f"Exit Rules:\n")
            self.options_text.insert(tk.END, f"  • Take profit at 50-75% of max profit\n")
            self.options_text.insert(tk.END, f"  • Cut loss if 20-30 DTE and not working\n")
            self.options_text.insert(tk.END, f"  • Close at 21 DTE to avoid pin risk\n")
            self.options_text.insert(tk.END, f"  • Trail stops if trade goes your way\n\n")
            
            self.options_text.insert(tk.END, f"Position Sizing:\n")
            self.options_text.insert(tk.END, f"  • Size = Account Risk / Max Loss Per Contract\n")
            self.options_text.insert(tk.END, f"  • Example: $10,000 account, 2% risk = $200\n")
            self.options_text.insert(tk.END, f"  • If max loss is $200, buy 1 contract\n\n")
            
            # Technical Signals Confirmation
            self.options_text.insert(tk.END, f"TECHNICAL SIGNALS CONFIRMATION\n", "subheader")
            self.options_text.insert(tk.END, f"{'-'*95}\n")
            
            self.options_text.insert(tk.END, f"Current Technical Setup:\n")
            self.options_text.insert(tk.END, f"  RSI (14):          {rsi_14:.2f}")
            if rsi_14 > 70:
                self.options_text.insert(tk.END, f"  (Overbought)\n", "negative")
            elif rsi_14 < 30:
                self.options_text.insert(tk.END, f"  (Oversold)\n", "positive")
            else:
                self.options_text.insert(tk.END, f"  (Neutral)\n", "neutral")
            
            self.options_text.insert(tk.END, f"  MACD:              {macd:+.4f}")
            if macd > 0:
                self.options_text.insert(tk.END, f"  (Bullish)\n", "positive")
            else:
                self.options_text.insert(tk.END, f"  (Bearish)\n", "negative")
            
            self.options_text.insert(tk.END, f"  Price vs SMA(20):  ", "neutral")
            sma_20 = latest.get('SMA_20', current_price)
            if current_price > sma_20:
                self.options_text.insert(tk.END, f"Above  (Uptrend)\n", "positive")
            else:
                self.options_text.insert(tk.END, f"Below  (Downtrend)\n", "negative")
            
            self.options_text.insert(tk.END, f"\n{'='*95}\n")
            self.options_text.insert(tk.END, "Analysis completed successfully!\n")
            self.options_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.options_text.config(state=tk.NORMAL)
            self.options_text.delete(1.0, tk.END)
            self.options_text.insert(tk.END, f"Error generating options analysis: {str(e)}")
            self.options_text.config(state=tk.DISABLED)
    
    def clear_results(self):
        """Clear results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        self.options_text.config(state=tk.NORMAL)
        self.options_text.delete(1.0, tk.END)
        self.options_text.config(state=tk.DISABLED)
        
        self.status_label.config(text="Ready", foreground="green")
        self.symbol_entry.delete(0, tk.END)
        self.symbol_entry.insert(0, "AAPL")


def main():
    root = tk.Tk()
    app = YahooFinanceGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

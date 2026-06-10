import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

tickers = ['1155.KL', '5347.KL', '5183.KL', '1295.KL', '1023.KL']

end_date   = datetime.today()
start_date = end_date - timedelta(days=40)

analysis_list = []
capital = 1000.0

def get_stock_data(ticker):
    """Download 1 month of stock price data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    data  = stock.history(start=start_date, end=end_date)
    return data
 
 
def get_metrics(ticker, name=None):
    """Calculate yesterday price, today price, return, and investment figures."""
    data = get_stock_data(ticker)
    if data is None or len(data) < 2:
        return

    yesterday_price = round(float(data['Close'].iloc[-2]), 2)
    today_price     = round(float(data['Close'].iloc[-1]), 2)
    daily_return    = round(today_price - yesterday_price, 2)
 
    shares       = int(capital / yesterday_price) if yesterday_price > 0 else 0
    total_return = round(shares * daily_return, 2)
    return_pct   = round((total_return / capital) * 100, 2)

    analysis_list.append({
        'Ticker': ticker,
        'Yesterday Closing Price': yesterday_price,
        'Today Closing Price': today_price,
        'Daily Return': daily_return,
        'Number of Shares Purchasable': shares,
        'Estimated Total Return': total_return,
        'Return Percentage': return_pct
    })

for t in tickers:
    get_metrics(t)

# Create the Question 1 DataFrame
df_q1 = pd.DataFrame(analysis_list)
print("--- Question 1: Stock Analysis DataFrame ---")
print(df_q1.to_string())
print("\n")

# Question 2: Data Manipulation

portfolio_summary = df_q1[['Ticker', 'Yesterday Closing Price', 'Today Closing Price', 'Estimated Total Return', 'Return Percentage']]
print("--- Question 2a: Portfolio Summary Table ---")
print(portfolio_summary.to_string())
print("\n")

# (b) GroupBy Analysis
def categorize_performance(return_pct):
    if return_pct < 0:
        return 'Negative Return'
    elif 0 <= return_pct <= 2:
        return 'Moderate Return'
    else:
        return 'High Return'

# Apply the function to create the new column
df_q1['Performance Category'] = df_q1['Return Percentage'].apply(categorize_performance)

# Use groupby() to calculate the average Estimated Total Return
grouped_performance = df_q1.groupby('Performance Category')['Estimated Total Return'].mean().reset_index()
print("--- Question 2b: GroupBy Analysis ---")
print(grouped_performance.to_string())
print("\n")

# Create df_close for charting
df_close = pd.DataFrame()
for ticker in tickers:
    data = get_stock_data(ticker)
    df_close[ticker] = data['Close']

# Chart 1: Closing Price Trend (Line Chart)
plt.figure(figsize=(10, 5))
for ticker in tickers:
    plt.plot(df_close.index, df_close[ticker], label=ticker)

plt.title('1-Month Closing Price Trend (May 2026)')
plt.xlabel('Date')
plt.ylabel('Closing Price (RM)')
plt.legend(title="Stock Tickers")
plt.grid(True)
# Save or display the plot
# plt.savefig("chart1_trend.png") 
plt.show()

# Chart 2: Portfolio Performance Comparison (Bar Chart)
plt.figure(figsize=(8, 5))
plt.bar(df_q1['Ticker'], df_q1['Estimated Total Return'], color='skyblue')

plt.title('Estimated Total Return Comparison by Stock')
plt.xlabel('Stock Ticker')
plt.ylabel('Estimated Total Return (RM)')
plt.axhline(0, color='black', linewidth=0.8) # Adds a line at 0 for easier loss/gain viewing
plt.grid(axis='y', linestyle='--', alpha=0.7)
# Save or display the plot
# plt.savefig("chart2_comparison.png")
plt.show()
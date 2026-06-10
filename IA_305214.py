import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ['1155.KL', '5347.KL', '5183.KL', '1295.KL', '1023.KL']
capital = 1000.0

# Fetch the last 1 month of closing prices dynamically to ensure valid data
print("Downloading stock data...")
df_close = yf.download(tickers, period='1mo')['Close']

data_rows = []

for stock in tickers:
   
    stock_data = df_close[stock].dropna()
    
   
    if len(stock_data) < 2:
        print(f"Warning: Not enough data for {stock}. Skipping.")
        continue
        
    ytd_price = stock_data.iloc[-2]
    today_price = stock_data.iloc[-1]
    
    daily_change = today_price - ytd_price
    shares_bought = capital // ytd_price
    est_return = shares_bought * daily_change
    return_pct = (est_return / capital) * 100
    
    data_rows.append({
        'Ticker': stock,
        'Yesterday Closing Price': round(ytd_price, 2),
        'Today Closing Price': round(today_price, 2),
        'Daily Return': round(daily_change, 2),
        'Number of Shares Purchasable': int(shares_bought),
        'Estimated Total Return': round(est_return, 2),
        'Return Percentage': round(return_pct, 2)
    })

df_q1 = pd.DataFrame(data_rows)
print("\n--- QUESTION 1: MAIN TABLE ---")
print(df_q1.to_string())



# 2(a): Slice the table
summary_table = df_q1[['Ticker', 'Yesterday Closing Price', 'Today Closing Price', 'Estimated Total Return', 'Return Percentage']]
print("\n--- QUESTION 2(a): PORTFOLIO SUMMARY TABLE ---")
print(summary_table.to_string())

# 2(b): GroupBy Performance Category
categories = []
for pct in df_q1['Return Percentage']:
    if pct < 0:
        categories.append('Negative Return')
    elif pct <= 2:
        categories.append('Moderate Return')
    else:
        categories.append('High Return')

df_q1['Performance Category'] = categories

grouped_table = df_q1.groupby('Performance Category')['Estimated Total Return'].mean().reset_index()
print("\n--- QUESTION 2(b): GROUPBY TABLE ---")
print(grouped_table.to_string())


# Chart 1: Line Chart (Window 1)
plt.figure(1, figsize=(10, 5))
for stock in tickers:
    plt.plot(df_close.index, df_close[stock], label=stock)
plt.title('Recent 1-Month Closing Price Trend')
plt.xlabel('Date')
plt.ylabel('Closing Price (RM)')
plt.legend()
plt.grid(True)

# Chart 2: Bar Chart (Window 2)
plt.figure(2, figsize=(8, 5))
plt.bar(df_q1['Ticker'], df_q1['Estimated Total Return'], color='red')
plt.title('Estimated Total Return Comparison')
plt.xlabel('Stock Ticker')
plt.ylabel('Estimated Total Return (RM)')
plt.axhline(0, color='black', linewidth=1)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show both windows simultaneously
plt.show()
import pandas as pd
import plotly.express as px
import yfinance as yf

#Gets stock Information
def get_stock_data(Token):
    data = yf.download(Token, period="1y")
    return data

watchList = []
valid_tickers = []

#Asks user for what stocks
while True:
    x = input("Input a Token (type STOP to stop) ").upper()
    if x == "STOP":
        break
    else:
        watchList.append(x)

correlation = pd.DataFrame()
percentage_return_df = pd.DataFrame()

for Token in watchList:
    df = get_stock_data(Token)
    if df.empty: 
        print("Invalid Token, please try again")
    else:
        #Moving Averages
        df = df.reset_index()

        df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

        df = df.sort_values(by="Date")

        df['moving_average_short'] = df['Close'].rolling(window=50).mean()

        df['moving_average_long'] = df['Close'].rolling(window=200).mean()

        #Moving Averages Graph
        fig = px.line(df, x=('Date'), y=['Close', 'moving_average_short', 'moving_average_long'], title=f"{Token} Stock Price over the Year")

        fig.show()

        #Correlation
        correlation[Token] = df['Close']

        #Percent Returns
        valid_tickers.append(Token)
        percentage_return_df[Token] = (df['Close'] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100

#Correlation Heatmap
correlation = correlation.corr()
correlation_fig = px.imshow(correlation)
correlation_fig.show()

#Percent Returns Graph
new_df = percentage_return_df.reset_index()
fig2 = px.line(new_df, x="Date", y=valid_tickers, title="Percentage Returns over the Year")
fig2.show()

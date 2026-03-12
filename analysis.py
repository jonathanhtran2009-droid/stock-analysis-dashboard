import pandas as pd
import plotly.express as px
import yfinance as yf

def get_stock_data(Token):
    data = yf.download(Token, period="1y")
    return data

watchList = []
valid_tickers = []

while True:
    x = input("Input a Token (type STOP to stop) ").upper()
    if x == "STOP":
        break
    else:
        watchList.append(x)

new_df = pd.DataFrame()


for Token in watchList:
    df = get_stock_data(Token)
    if df.empty:
        print("Invalid Token, please try again")
    else:
        valid_tickers.append(Token)
        new_df[Token] = (df['Close'] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100

new_df = new_df.reset_index()
fig = px.line(new_df, x="Date", y=valid_tickers, title="Percentage Returns over the Year")
fig.show()

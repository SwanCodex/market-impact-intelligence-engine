import pandas as pd
import yfinance as yf

def fetch_market_data(symbol="^NSEI", start="2024-01-01"):
    data = yf.download(symbol, start=start)
    data.reset_index(inplace=True)
    data = data[["Date", "Close"]]
    data.rename(columns={"Close": "index_close"}, inplace=True)
    return data


if __name__ == "__main__":
    df = fetch_market_data()
    df.to_csv("data/raw/market_data.csv", index=False)
    print(f"Saved {len(df)} market records")

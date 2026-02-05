import pandas as pd

def compute_returns(df, days):
    return df["index_close"].shift(-days) / df["index_close"] - 1


def align_news_with_market(news_path, market_path, output_path):
    news = pd.read_csv(news_path)
    market = pd.read_csv(market_path)
    
    # Ensure numeric prices (CRITICAL FIX)
    market["index_close"] = pd.to_numeric(market["index_close"], errors="coerce")


    news["published_at"] = pd.to_datetime(news["published_at"]).dt.date
    market["Date"] = pd.to_datetime(market["Date"]).dt.date

    market.sort_values("Date", inplace=True)
    market["ret_1d"] = compute_returns(market, 1)
    market["ret_3d"] = compute_returns(market, 3)
    market["ret_7d"] = compute_returns(market, 7)

    aligned = pd.merge(
        news,
        market,
        left_on="published_at",
        right_on="Date",
        how="left"
    )

    aligned.to_csv(output_path, index=False)
    print(f"Aligned dataset saved to {output_path}")


if __name__ == "__main__":
    align_news_with_market(
        news_path="data/processed/news_with_events.csv",
        market_path="data/raw/market_data.csv",
        output_path="data/processed/news_market_aligned.csv"
    )

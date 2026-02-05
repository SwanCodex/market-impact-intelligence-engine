import pandas as pd
import numpy as np

def impact_analysis(input_path, output_path):
    df = pd.read_csv(input_path)

    # Keep only rows with valid returns
    df = df.dropna(subset=["ret_1d", "ret_3d", "ret_7d"], how="all")


    results = []

    for event in df["event_type"].unique():
        subset = df[df["event_type"] == event]

        results.append({
            "event_type": event,
            "count": len(subset),
            "avg_ret_1d": subset["ret_1d"].mean(),
            "avg_ret_3d": subset["ret_3d"].mean(),
            "avg_ret_7d": subset["ret_7d"].mean(),
            "volatility_1d": subset["ret_1d"].std(),
            "volatility_3d": subset["ret_3d"].std(),
            "volatility_7d": subset["ret_7d"].std(),
        })

    impact_df = pd.DataFrame(results)
    impact_df.to_csv(output_path, index=False)
    print(f"Impact analysis saved to {output_path}")


if __name__ == "__main__":
    impact_analysis(
        input_path="data/processed/news_market_aligned.csv",
        output_path="data/processed/event_impact_summary.csv"
    )

import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query="economy OR inflation OR market OR stocks", page_size=50):
    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
    }

    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    structured_news = []

    for article in articles:
        structured_news.append({
            "source": article["source"]["name"],
            "title": article["title"],
            "description": article["description"],
            "content": article["content"],
            "published_at": article["publishedAt"],
            "fetched_at": datetime.utcnow().isoformat()
        })

    return pd.DataFrame(structured_news)


if __name__ == "__main__":
    df = fetch_news()
    df.to_csv("data/raw/news_raw.csv", index=False)
    print(f"Saved {len(df)} news articles")

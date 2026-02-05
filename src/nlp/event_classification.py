import pandas as pd
from transformers import pipeline

CLASSIFIER_MODEL = "facebook/bart-large-mnli"

LABELS = [
    "Economics",
    "Politics",
    "Global Trade",
    "Monetary Policy",
    "Inflation",
    "Geopolitics",
    "Corporate"
]

def run_event_classification(input_path, output_path):
    df = pd.read_csv(input_path)

    classifier = pipeline(
        "zero-shot-classification",
        model=CLASSIFIER_MODEL
    )

    predicted_labels = []
    confidence_scores = []

    for text in df["title"].fillna(""):
        if text.strip() == "":
            predicted_labels.append("Unknown")
            confidence_scores.append(0.0)
        else:
            result = classifier(
                text[:512],
                candidate_labels=LABELS,
                multi_label=False
            )
            predicted_labels.append(result["labels"][0])
            confidence_scores.append(result["scores"][0])

    df["event_type"] = predicted_labels
    df["event_confidence"] = confidence_scores

    df.to_csv(output_path, index=False)
    print(f"Event classification complete. Saved to {output_path}")


if __name__ == "__main__":
    run_event_classification(
        input_path="data/processed/news_with_sentiment.csv",
        output_path="data/processed/news_with_events.csv"
    )

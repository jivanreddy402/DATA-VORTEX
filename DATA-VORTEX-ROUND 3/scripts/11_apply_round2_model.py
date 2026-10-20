import pandas as pd
import joblib
from pathlib import Path

# --------------------------------------------------
# PATHS
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/meta_one_round3_unified.csv"
)

VECTORIZER_FILE = Path(
    "models/tfidf_vectorizer.pkl"
)

MODEL_FILE = Path(
    "models/naive_bayes_sentiment_model.pkl"
)

OUTPUT_FILE = Path(
    "data/processed/meta_one_round3_sentiment.csv"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("ROUND 2 MODEL → ROUND 3 LIVE DATA")
print("=" * 60)

print(f"Input records: {len(df)}")


# --------------------------------------------------
# LOAD ROUND 2 ARTIFACTS
# --------------------------------------------------

vectorizer = joblib.load(VECTORIZER_FILE)
model = joblib.load(MODEL_FILE)

print(f"Vectorizer: {type(vectorizer).__name__}")
print(f"Model: {type(model).__name__}")


# --------------------------------------------------
# TRANSFORM TEXT
# --------------------------------------------------

X = vectorizer.transform(
    df["text"].fillna("").astype(str)
)


# --------------------------------------------------
# PREDICT SENTIMENT
# --------------------------------------------------

df["predicted_sentiment"] = model.predict(X)


# --------------------------------------------------
# PREDICT PROBABILITIES
# --------------------------------------------------

probabilities = model.predict_proba(X)

df["sentiment_confidence"] = probabilities.max(axis=1)


# --------------------------------------------------
# SAVE
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\nSentiment distribution:")
print(
    df["predicted_sentiment"]
    .value_counts()
)

print("\nAverage confidence:")
print(
    round(df["sentiment_confidence"].mean(), 4)
)

print("\nSample predictions:")
print(
    df[
        [
            "platform",
            "published_at",
            "predicted_sentiment",
            "sentiment_confidence",
            "text"
        ]
    ].head(10).to_string(index=False)
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("=" * 60)
print("ROUND 2 MODEL APPLIED SUCCESSFULLY")
print("=" * 60)
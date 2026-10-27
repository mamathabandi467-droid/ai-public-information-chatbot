
import pandas as pd
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "public_info.csv"
)


def load_data():
    if not DATA_FILE.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(DATA_FILE).fillna("")
    except (OSError, pd.errors.ParserError):
        return pd.DataFrame()


def search_information(query, limit=3):
    data = load_data()

    if data.empty:
        return []

    query_words = set(query.lower().split())
    scored_results = []

    for _, row in data.iterrows():
        searchable_text = " ".join(
            str(row[column])
            for column in [
                "organization_name",
                "category",
                "location",
                "services",
                "faq",
                "answer",
            ]
            if column in data.columns
        ).lower()

        text_words = set(searchable_text.split())
        score = len(query_words & text_words)

        if score > 0:
            scored_results.append((score, row.to_dict()))

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        item[1]
        for item in scored_results[:limit]
    ]

import pandas as pd
import numpy as np
import re

def load_and_preprocess(path):
    df = pd.read_csv(path)

    df = df.rename(columns={
        "Title": "course_name",
        "Skills": "skills",
        "Ratings": "rating",
        "Review counts": "reviews",
        "Metadata": "metadata"
    })

    df = df.dropna(subset=["course_name", "skills", "metadata"])

    df["skills_list"] = df["skills"].apply(
        lambda x: [s.strip().lower() for s in x.split(",")]
    )

    def extract_level(meta):
        if "Beginner" in meta: return 0
        if "Intermediate" in meta: return 1
        if "Advanced" in meta: return 2
        return None

    df["level"] = df["metadata"].apply(extract_level)
    df = df.dropna(subset=["level"])

    def extract_reviews(text):
        match = re.search(r'\((.*?) reviews\)', str(text))
        if match:
            val = match.group(1)
            if "K" in val:
                return float(val.replace("K", "")) * 1000
            return float(val)
        return 0

    df["num_reviews"] = df["reviews"].apply(extract_reviews)

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

    df["popularity"] = df["rating"] * np.log1p(df["num_reviews"])

    df["popularity"] = (df["popularity"] - df["popularity"].min()) / (
        df["popularity"].max() - df["popularity"].min()
    )

    df["combined_text"] = df.apply(
        lambda x: x["course_name"] + " " + " ".join(x["skills_list"]),
        axis=1
    )

    df = df.reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = load_and_preprocess("data/raw/coursera_course_dataset.csv")
    df.to_csv("data/processed/cleaned.csv", index=False)
    print("Preprocessing done!")
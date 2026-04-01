import mlflow
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

mlflow.set_experiment("course-recommender")

with mlflow.start_run():

    df = pd.read_csv("data/processed/cleaned.csv")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(df["combined_text"].tolist())

    np.save("models/embeddings.npy", embeddings)

    mlflow.log_param("model", "MiniLM")
    mlflow.log_param("num_samples", len(df))

    mlflow.log_artifact("models/embeddings.npy")

    print("Embeddings generated!")
import mlflow
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

mlflow.set_experiment("course-recommender")

with mlflow.start_run():

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    df = pd.read_csv("data/processed/cleaned.csv")

    # -----------------------------
    # LOAD MODEL
    # -----------------------------
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    # -----------------------------
    # CREATE EMBEDDINGS
    # -----------------------------
    embeddings = model.encode(df["combined_text"].tolist())

    np.save("models/embeddings.npy", embeddings)

    # -----------------------------
    # LOG PARAMETERS
    # -----------------------------
    mlflow.log_param("model", "MiniLM")
    mlflow.log_param("num_samples", len(df))

    # -----------------------------
    # METRIC 1: Avg Similarity
    # -----------------------------
    sample_size = min(100, len(embeddings))
    sim_matrix = cosine_similarity(embeddings[:sample_size])
    avg_similarity = np.mean(sim_matrix)

    mlflow.log_metric("avg_similarity", float(avg_similarity))

    # -----------------------------
    # METRIC 2: Avg Embedding Norm (optional)
    # -----------------------------
    avg_norm = np.mean(np.linalg.norm(embeddings, axis=1))
    mlflow.log_metric("avg_embedding_norm", float(avg_norm))

    # -----------------------------
    # SAVE ARTIFACT
    # -----------------------------
    mlflow.log_artifact("models/embeddings.npy")

    print("✅ Embeddings + basic monitoring metrics logged!")
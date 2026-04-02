import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/processed/cleaned.csv")
embeddings = np.load("models/embeddings.npy")
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

def generate_learning_path(user_input, min_similarity=0.4):

    user_input = [s.lower().strip() for s in user_input]
    user_embedding = model.encode([" ".join(user_input)])

    sims = cosine_similarity(user_embedding, embeddings)[0]

    df_temp = df.copy()
    df_temp["similarity"] = sims

    df_filtered = df_temp[df_temp["similarity"] >= min_similarity]\
        .sort_values("similarity", ascending=False).head(10)

    return df_filtered[["course_name", "similarity"]]
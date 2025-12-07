import os
from typing import List, Dict

import numpy as np
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
# from sklearn.metrics.pairwise import cosine_similarity 

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("No API key found. Set GEMINI_API_KEY or API_KEY in your .env file.")

genai.configure(api_key=API_KEY)

EMBEDDING_MODEL = "models/text-embedding-004"

def get_embedding(text: str,model: str = EMBEDDING_MODEL,task_type: str | None = None,output_dimensionality: int | None = None,) -> np.ndarray:
    result = genai.embed_content(
        model=model,
        content=text,
        task_type=task_type,
        output_dimensionality=output_dimensionality,
    )
    return np.array(result["embedding"], dtype=np.float32)


def cosine_similarity_scalar(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    dot = float(np.dot(vec_a, vec_b))
    norm_a = float(np.linalg.norm(vec_a))
    norm_b = float(np.linalg.norm(vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot / (norm_a * norm_b)

def embed_simple_phrases():
    phrases = [
        "The cat sits on the mat.",
        "A dog is playing in the park.",
        "Quantum physics explores the nature of reality.",
        "Machine learning models can learn from data.",
    ]

    embeddings = [
        get_embedding(p, task_type="SEMANTIC_SIMILARITY")
        for p in phrases
    ]

    n = len(phrases)
    sim_matrix = np.zeros((n, n), dtype=np.float32)

    for i in range(n):
        for j in range(n):
            sim_matrix[i, j] = cosine_similarity_scalar(embeddings[i], embeddings[j])

    for i in range(n):
        for j in range(n):
            print(f"Similarity between [{i}] and [{j}]: {sim_matrix[i, j]:.4f}")
        print()

    return phrases, embeddings, sim_matrix


def apply_chunking(article: pd.Series,chunk_size: int = 1000,overlap: int = 200,) -> pd.Series:
    text = article.html_content
    start = 0
    chunks: list[str] = []

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())

        start = end - overlap
        if start < 0:
            start = 0

    return pd.Series(
        [chunks, list(range(len(chunks)))],
        index=["chunk_text", "chunk_index"],
    )

def embed_article(article_chunk: pd.Series) -> pd.Series:

    exists_in_qdrant = bool(article_chunk.get("exists_in_qdrant", False))
    if exists_in_qdrant:
        return pd.Series([None], index=["embedding"])

    if article_chunk["chunk_index"] >= 2:
        return pd.Series([None], index=["embedding"])

    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=article_chunk["chunk_text"],
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768,
    )

    embedding = np.array(result["embedding"], dtype=np.float32)

    return pd.Series([embedding], index=["embedding"])


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    results = df.apply(embed_article, axis=1)
    df = pd.concat([df, results], axis=1)
    return df


def chunk_documents(df: pd.DataFrame) -> pd.DataFrame:
    chunks = df.apply(apply_chunking, axis=1)
    df_chunks = pd.concat([df, chunks], axis=1).explode(["chunk_index", "chunk_text"])
    df_chunks["chunk_index"] = df_chunks["chunk_index"].astype(int)
    df_chunks["chunk_text"] = df_chunks["chunk_text"].astype(str)
    return df_chunks

def save_embeddings(df: pd.DataFrame, output_path: str = "chunk_embeddings.csv") -> None:
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    embed_simple_phrases()

    # Example structure for documents DataFrame:
    # df_docs = pd.DataFrame(
    #     [
    #         {"id": 1, "html_content": "Some long scientific article text ..."},
    #         {"id": 2, "html_content": "Another article ..."},
    #     ]
    # )
    #
    # df_chunks = chunk_documents(df_docs)
    # df_with_embeddings = embed_documents(df_chunks)
    # print(df_with_embeddings.head())

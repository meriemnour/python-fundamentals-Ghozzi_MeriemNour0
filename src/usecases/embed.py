from google import genai
from google.genai import types
import pandas as pd
import numpy as np

client = genai.Client()


def apply_chunking(
    article: pd.Series, chunk_size: int = 1000, overlap: int = 200
) -> pd.Series:
    text = article.md_text
    start = 0
    chunks: list[str] = []
    while start < len(article.md_text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return pd.Series([chunks, range(len(chunks))], index=["chunk_text", "chunk_index"])


def embed_article(article_chunk: pd.Series) -> pd.Series:
    if article_chunk.exists_in_qdrant:
        return pd.Series([None], index=["embedding"])

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[article_chunk.chunk_text],
        config=types.EmbedContentConfig(
            output_dimensionality=768, task_type="RETRIEVAL_DOCUMENT"
        ),
    )

    if result.embeddings is None:
        return pd.Series([None], index=["embedding"])

    return pd.Series([np.array(result.embeddings[0].values)], index=["embedding"])


def embed_documents(df: pd.DataFrame) -> pd.DataFrame:
    results = df.progress_apply(embed_article, axis=1)  # type: ignore[operator]
    df = pd.concat([df, results], axis=1)
    return df


def chunk_documents(df: pd.DataFrame) -> pd.DataFrame:
    chunks = df.progress_apply(apply_chunking, axis=1)  # type: ignore[operator]
    return pd.concat([df, chunks], axis=1).explode(["chunk_index", "chunk_text"])
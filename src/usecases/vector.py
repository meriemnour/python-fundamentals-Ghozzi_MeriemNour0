import pandas as pd
from models.chunk import ScientificArticleChunk
from storage.vector import COLLECTION_NAME, client
from qdrant_client.models import PointStruct
import uuid


def get_point_id(article_chunk: pd.Series) -> uuid.UUID:
    point_id = uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"{article_chunk.arxiv_id}_chunk_{article_chunk.chunk_index}",
    )
    return point_id


def check_if_chunk_exists(article_chunk: pd.Series) -> pd.Series:
    point_id = get_point_id(article_chunk)
    records = client.retrieve(COLLECTION_NAME, ids=[point_id])
    return pd.Series([len(records) > 0], index=["exists_in_qdrant"], dtype=bool)


def insert_embeddings(article_chunk: pd.Series) -> pd.Series:
    _id = get_point_id(article_chunk)
    if article_chunk.embedding is None:
        return pd.Series([_id], index=["point_id"])

    point = PointStruct(
        id=_id,
        vector=article_chunk.embedding,
        payload=ScientificArticleChunk(
            title=article_chunk.title,
            summary=article_chunk.summary,
            arxiv_id=article_chunk.arxiv_id,
            author_full_name=article_chunk.author_full_name,
            chunk_text=article_chunk.chunk_text,
            chunk_index=article_chunk.chunk_index,
        ).model_dump(),
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

    return pd.Series([_id], index=["point_id"])


def save_to_qdrant(df: pd.DataFrame) -> pd.DataFrame:
    df.apply(insert_embeddings, axis=1)
    return df


def check_chunks_in_qdrant(df: pd.DataFrame) -> pd.DataFrame:
    exists = df.apply(check_if_chunk_exists, axis=1)
    df = pd.concat([df, exists], axis=1)
    return df
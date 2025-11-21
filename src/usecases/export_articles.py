from pathlib import Path
from typing import Any

import pandas as pd
import pymupdf4llm
import storage.mongo  # noqa: F401
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from mongoengine import DoesNotExist


def save_article(article: pd.Series[Any]) -> pd.Series[Any]:
    try:
        m_author = MongoAuthor(
            db_id=article.author_db_id,
            full_name=article.author_full_name,
            author_title=article.author_title,
        )

        file_path = Path(article.file_path)
        if not file_path.exists():
            print(f"File not found, skipping: {article.file_path}")
            md_text = ""
        else:
            md_text = pymupdf4llm.to_markdown(article.file_path)

        kwargs = {
            "db_id": article.db_id,
            "title": article.title,
            "summary": article.summary,
            "file_path": article.file_path,
            "arxiv_id": article.arxiv_id,
            "author": m_author,
            "text": md_text,
        }

        m_article: MongoArticle
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
            m_article.reload()
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()

        print(f"success :{article.arxiv_id}")
        mongo_db_id: str = str(m_article.id)
        return pd.Series([mongo_db_id], index=["mongo_db_id"])
    except Exception as e:
        print(f"Failure :{e}")
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_article, axis=1)
    ids.name = "mongo_id"
    df = pd.concat([df, ids], axis=1)
    return df

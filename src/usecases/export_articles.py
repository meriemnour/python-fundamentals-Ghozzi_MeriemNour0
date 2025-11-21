from typing import cast

import pandas as pd
import pymupdf4llm
import storage.mongo  # noqa: F401
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from models.pandas import ScientificArticle
from mongoengine import DoesNotExist


def save_article(article: ScientificArticle) -> MongoArticle | None:
    try:
        m_author = MongoAuthor(
            db_id=article.author_db_id,
            full_name=article.author_full_name,
            author_title=article.author_title,
        )
        md_text = pymupdf4llm.to_markdown(article.file_path)

        kwargs = dict(
            db_id=article.db_id,
            title=article.title,
            summary=article.summary,
            file_path=article.file_path,
            arxiv_id=article.arxiv_id,
            author=m_author,
            text=md_text,
        )
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
            m_article.reload()
            return cast(MongoArticle, m_article)
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()
            return m_article
    except Exception as e:
        print(f"Failure :{e}")
        return None


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    new_articles = []
    for article in df.to_records():
        m_article = save_article(article)
        if m_article:
            new_articles.append(m_article)

    df["mongo_id"] = [a.id for a in new_articles]
    df["mongo_id"] = df["mongo_id"].astype(str)
    return df

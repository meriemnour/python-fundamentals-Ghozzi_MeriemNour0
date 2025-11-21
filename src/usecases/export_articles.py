import pandas as pd
import pymupdf4llm
import storage.mongo  # noqa: F401
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from models.pandas import ScientificArticle
from mongoengine import DoesNotExist
from typing import Optional
from pathlib import Path  # Add this import


def save_article(article: ScientificArticle) -> Optional[MongoArticle]:
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
            'db_id': article.db_id,
            'title': article.title,
            'summary': article.summary,
            'file_path': article.file_path,
            'arxiv_id': article.arxiv_id,
            'author': m_author,
            'text': md_text,
        }
        
        m_article: Optional[MongoArticle] = None
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
            m_article.reload()
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()
        
        print(f"success :{article.arxiv_id}")
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

    
    if new_articles:
        df["mongo_id"] = [str(a.id) for a in new_articles]
    else:
        df["mongo_id"] = ""  
    
    return df
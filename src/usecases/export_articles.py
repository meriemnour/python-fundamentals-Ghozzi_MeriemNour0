from pathlib import Path
import pymupdf4llm

from typing import Any
from urllib.parse import urlparse

import pandas as pd
import requests
import storage.mongo  # noqa: F401
from bs4 import BeautifulSoup
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from mongoengine import DoesNotExist


def extract_clean_text(html_content: str) -> str:
    if not html_content:
        return ""   
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup(['script', 'style']):
            element.decompose()
        text = soup.get_text()
        lines = [line.strip() for line in text.splitlines()]
        text = ' '.join(line for line in lines if line)
        return text
    except Exception as e:
        print(f"Error extracting text from HTML: {e}")
        return ""


def download_file(article: pd.Series[Any]) -> pd.Series[Any]:
    parsed_url = urlparse(article.file_path)
    if parsed_url.scheme:
        filename = Path(parsed_url.path).name
        new_path = f"data/papers/{filename}.pdf"
        if not Path(new_path).exists():
            response = requests.get(article.file_path)
            with open(new_path, "wb") as f:
                f.write(response.content)
    else:
        new_path = article.file_path

    return pd.Series([new_path], index=["local_file_path"])
def convert_article_to_markdown(article: pd.Series) -> pd.Series:
    md_text = pymupdf4llm.to_markdown(article.local_file_path)
    with open(f"{article.local_file_path}.md", "w") as f:
        f.write(md_text)
    return pd.Series([md_text], index=["md_text"], dtype="string")

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

        text_content_from_html = extract_clean_text(article.html_content)

        kwargs = {
            "db_id": article.db_id,
            "title": article.title,
            "summary": article.summary,
            "file_path": str(article.file_path),
            "arxiv_id": article.arxiv_id,
            "author": m_author,
            "text": text_content_from_html,
        }

        m_article: MongoArticle
        try:
            m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
            m_article.update(**kwargs)
            m_article.reload()
        except DoesNotExist:
            m_article = MongoArticle(**kwargs)
            m_article.save()

        print(f"success: {article.arxiv_id}")
        mongo_db_id: str = str(m_article.id)
        return pd.Series([mongo_db_id], index=["mongo_db_id"])
    except Exception as e:
        print(f"Failure processing {article.arxiv_id}: {e}")
        return pd.Series([""], index=["mongo_db_id"])


def create_in_mongo(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Processing {len(df)} articles into MongoDB...")
    ids = df.apply(save_article, axis=1)
    ids.name = "mongo_id"
    df = pd.concat([df, ids], axis=1)
    return df


def download_files(df: pd.DataFrame) -> pd.DataFrame:
    filenames = df.apply(download_file, axis=1)
    df = pd.concat([df, filenames], axis=1)
    return df


def download_html_article(row: pd.Series[Any]) -> str | None:
    try:
        response = requests.get(row["arxiv_id"])
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"No existing arxiv_id: {row['arxiv_id']}: {e}")
        return None


def add_html_content(df: pd.DataFrame) -> pd.DataFrame:
    df["html_content"] = df.apply(download_html_article, axis=1)
    return df


def convert_to_markdown(df: pd.DataFrame) -> pd.DataFrame:
    texts = df.progress_apply(convert_article_to_markdown, axis=1)  # type: ignore[operator]
    df = pd.concat([df, texts], axis=1)
    return df
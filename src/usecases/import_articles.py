from pathlib import Path

import pandas as pd
from models.relational import Author, ScientificArticle
from sqlalchemy.exc import IntegrityError
from storage.relational_db import Session

pd.set_option("display.max_columns", None)


def save_articles(line: pd.Series) -> pd.Series:
    with Session() as session:
        try:
            existing_article = (
                session.query(ScientificArticle)
                .filter_by(arxiv_id=line["arxiv_id"])
                .first()
            )
            if existing_article:
                print(f"Article already exists: {line['arxiv_id']}")
                return pd.Series(
                    [existing_article.id, existing_article.author.id],
                    index=["db_id", "author_db_id"],
                )

            author = Author(
                full_name=line["author_full_name"], title=line["author_title"]
            )

            article = ScientificArticle(
                title=line["title"],
                summary=line["summary"],
                file_path=line["file_path"],
                arxiv_id=line["arxiv_id"],
                author=author,
            )
            session.add(article)
            session.commit()
            session.refresh(article)
            print(f"Success: {article.arxiv_id}")
            return pd.Series([article.id, author.id], index=["db_id", "author_db_id"])

        except IntegrityError as e:
            print(f"Failure: {e}")
            session.rollback()
            return pd.Series([0, 0], index=["db_id", "author_db_id"])


def load_data_from_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(Path(path), delimiter=";", dtype="string")


def load_from_xml(path: str) -> pd.DataFrame:
    df = pd.read_xml(
        Path(path),
        xpath="/atom:feed/atom:entry",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )[["id", "title", "summary"]]

    df["author_title"] = "PhD"

    links_df = pd.read_xml(
        Path(path),
        xpath="/atom:feed/atom:entry/atom:link[@type='application/pdf']",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )["href"]

    authors_df = pd.read_xml(
        Path(path),
        xpath="/atom:feed/atom:entry/atom:author[1]",
        namespaces={"atom": "http://www.w3.org/2005/Atom"},
    )["name"]

    return pd.concat(
        [
            df.rename(columns={"id": "arxiv_id"}),
            links_df.rename("file_path"),
            authors_df.rename("author_full_name"),
        ],
        axis=1,
    )


def create_in_relational_db(df: pd.DataFrame) -> pd.DataFrame:
    ids = df.apply(save_articles, axis=1)
    df = pd.concat([df, ids], axis=1)
    return df

from pathlib import Path

import numpy as np
import pandas as pd
from models.relational import Author, ScientificArticle
from sqlalchemy.exc import IntegrityError
from storage.relational_db import Session


def save_articles(line: dict[str, str]) -> None:
    with Session() as session:
        try:
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
            return article
        #           return pd.Series(
        #               [article.id, author.id], index=["db_id", "author_db_id"]
        #            )

        except IntegrityError as e:
            print(f"Failure: {e}")
            return None


# def load_data_from_csv(path: Path) -> list[ScientificArticle]:

#    df = pd.read_csv(path, delimiter=";", dtype='string')
#    print(df.dtypes)
#    print(df)


#    articles: list[ScientificArticle] = []
#    for index, row in df.iterrows():
#        line_dict = {
#            "title": row["title"],
#            "summary": row["summary"],
#            "file_path": row["file_path"],
#            "arxiv_id": row["arxiv_id"],
#            "author_full_name": row["author_full_name"],
#            "author_title": row["author_title"]
#        }
#        article = save_articles(line_dict)
#        if article:
#            articles.append(article)
#
#    articles: list[ScientificArticle]=[]
#    with open(path, "r") as f:
#        reader = csv.DictReader(f, delimiter=";")
#        for line in reader:
#           article=save_articles(line)
#            if article:
#                articles.append(article)
#
#    return articles


def load_data_from_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, delimiter=";", dtype="string")


def create_in_relational_db(df: pd.DataFrame) -> pd.DataFrame:
    articles_ids: list[int] = []
    author_ids: list[int] = []

    # Method 1:   I can use to_records() - returns
    for line in df.to_records():
        print("line", line)
        article = save_articles(line)
        articles_ids.append(article.id if article else 0)
        author_ids.append(article.author_id if article else 0)

    df["db_id"] = articles_ids
    df["db_id"] = df["db_id"].astype(np.int32)
    df["author_db_id"] = author_ids
    df["author_db_id"] = df["author_db_id"].astype(np.int32)

    # Method 2: I can use iterrows() - returns (index, row) tuples
    # for index, row in df.iterrows():
    #    # Convert the row to a dictionary
    #    line_dict = row.to_dict()
    #    article = save_articles(line_dict)
    #    if article:
    #        articles.append(article)

    return df
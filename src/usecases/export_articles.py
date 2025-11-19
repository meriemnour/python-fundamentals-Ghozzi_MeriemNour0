import os

import pymupdf4llm
import storage.mongo  # noqa: F401
from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from models.relational import ScientificArticle
from mongoengine import DoesNotExist
from sqlalchemy import select
from storage.relational_db import Session







def export_from_db() -> None:
    with Session() as session:
        query = select(ScientificArticle)
        result = session.execute(query)

        for article in result.scalars().all():
            print(f"Processing: {article.title}")

            # Check if author exists
            if article.author is None:
                print(f"Article has no author, skipping: {article.title}")
                continue  # Skip articles without authors

            m_author = MongoAuthor(
                db_id=article.author.id,
                full_name=article.author.full_name,
                author_title=article.author.title,
            )

            # Convert PDF to markdown if file exists
            md_text = ""
            if os.path.exists(article.file_path):
                try:
                    md_text = pymupdf4llm.to_markdown(article.file_path)
                    kwargs= dict(
                        db_id=article.id,
                        title=article.title,
                        summary=article.summary,
                        file_path=article.file_path,
                        created_at=article.created_at,
                        arxiv_id=article.arxiv_id,
                        author=m_author,
                        text=md_text,
                    )
                    print(f"  Converted PDF to markdown: {len(md_text)} characters")
                except Exception as e:
                    print(f"  Warning: Could not convert PDF: {e}")
                    md_text = article.summary
            else:
                print(f"  Warning: File not found: {article.file_path}")
                md_text = article.summary

            try:
                # Try to find existing article by arxiv_id
                m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
                # Update existing article
                m_article.update(
kwarg
                )
                print("Updated existing article")

            except DoesNotExist:
                # Create new article
                m_article = MongoArticle(

                )
                m_article.save()
                print("Created new article")

    print("Export completed successfully!")






def export_from_db1() -> None:



if __name__ == "__main__":
    export_from_db()

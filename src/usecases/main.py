import logging

from usecases.arxiv import fetch_arxiv_articles
from usecases.export_articles import add_html_content, create_in_mongo, download_files
from usecases.import_articles import (
    create_in_relational_db,
)
from usecases.search_text import search_text_index

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

if __name__ == "__main__":
    try:
        df = (
            fetch_arxiv_articles("quantum")
            .pipe(create_in_relational_db)
            .pipe(download_files)
            .pipe(add_html_content)
            .pipe(create_in_mongo)
        )
        print("DataFrame after (relational DB insertion and export to mongodb):")
        print(df)

        results = search_text_index("quantum entanglement")
        print("len results:", len(results))
        for article in results:
            print(f"{article['arxiv_id']}: {article['title']}")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Error occurred: {e}")

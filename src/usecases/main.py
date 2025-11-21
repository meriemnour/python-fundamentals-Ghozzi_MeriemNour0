import logging
from pathlib import Path

from usecases.export_articles import create_in_mongo
from usecases.import_articles import create_in_relational_db, load_data_from_csv
from usecases.search_text import search_text_index

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

if __name__ == "__main__":
    try:
        df = (
            load_data_from_csv(Path("data/articles.csv"))
            .pipe(create_in_relational_db)
            .pipe(create_in_mongo)
        )
        print("Dataframe after relational DB insertion:")
        print(df.head())

        results = search_text_index("Resonant Conversions in Hal")
        for article in results:
            print(f"{article.arxiv_id} : {article.title}")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Error occurred: {e}")

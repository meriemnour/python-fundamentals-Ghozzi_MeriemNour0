import logging

from usecases.arxiv import fetch_arxiv_articles,load_from_xml
from usecases.export_articles import  (
    convert_to_markdown,
    add_html_content, 
    create_in_mongo, 
    download_files
    )
from usecases.import_articles import (
    create_in_relational_db,
    )
from usecases.embed import chunk_documents, embed_documents
from usecases.search_text import search_text_index
from usecases.vector import check_chunks_in_qdrant, save_to_qdrant
import pandas as pd

from tqdm.auto import tqdm 

tqdm.pandas(desc="loading articles")

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

if __name__ == "__main__":
    try:
        df = (
            fetch_arxiv_articles("proton")
            .pipe(create_in_relational_db)
            .pipe(download_files)
            .pipe(convert_to_markdown)
            .pipe(chunk_documents)
            .pipe(check_chunks_in_qdrant)
            .pipe(embed_documents)
            .pipe(save_to_qdrant)
            #.pipe(create_in_mongo)
        )
        print("DataFrame after (relational DB insertion and export to mongodb):")
        print(df)

        results = search_text_index("angular")
        print("len results:", len(results))
        for article in results:
            print(f"{article['arxiv_id']}: {article['title']}")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Error occurred: {e}")

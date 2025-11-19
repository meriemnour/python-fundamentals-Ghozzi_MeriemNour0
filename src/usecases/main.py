from usecases.export_articles import export_from_db
from usecases.import_articles import load_data_from_csv
from usecases.search_text import search_text_index

if __name__ == "__main__":
    new_articles_sqla = load_data_from_csv("data/articles.csv")

    mongo_articles_mongo = export_from_db(new_articles_sqla)

    results = search_text_index(mongo_articles_mongo, " Resonant Conversions in Hal")
    for article in results:
        print(f"{article.arxiv_id} : {article.title}")

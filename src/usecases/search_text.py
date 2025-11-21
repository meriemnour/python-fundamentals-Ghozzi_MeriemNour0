import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle
from utils.timeit import timeit


@timeit("search icontains")
def search_text(keyword: str) -> list[ScientificArticle]:
    query = ScientificArticle.objects(text__icontains=keyword)
    return list(query)


@timeit("search text index")
def search_text_index(keyword: str) -> list[ScientificArticle]:
    query = ScientificArticle.objects.search_text(keyword)
    return list(query)  # Convert to list to match return type


if __name__ == "__main__":
    results = search_text("Mixing between dark photons and visible photons")
    for article in results:
        print(f"{article.arxiv_id} : {article.title}")

    results2 = search_text_index("low-frequency correlators")
    for article in results2:  # Fixed variable name from 'ar' to 'article'
        print(f"{article.arxiv_id} : {article.title}")

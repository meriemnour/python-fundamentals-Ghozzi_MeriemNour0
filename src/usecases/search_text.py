import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle
from utils.timeit import timeit


@timeit("search icontains")
def search_text(keyword: str) -> list[ScientificArticle]:
    query = ScientificArticle.objects(text__icontains=keyword)
    return list(query)


if __name__ == "__main__":
    results = search_text("Mixing between dark photons and visible photons")
    for article in results:
        print(f"{article.arxiv_id} : {article.title}")

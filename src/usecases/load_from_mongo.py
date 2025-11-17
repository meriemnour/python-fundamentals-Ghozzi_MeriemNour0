import storage.mongo  # noqa: F401
from models.mongo import ScientificArticle


def list_articles() -> list[ScientificArticle]:
    return ScientificArticle.objects.all()  # type: ignore[no-any-return]


if __name__ == "__main__":
    for a in list_articles():
        print(a.text[:200])

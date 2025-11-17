from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    StringField,
)


class Author(EmbeddedDocument):  # type: ignore[misc]
    db_id = IntField(required=True)
    full_name = StringField()
    author_title = StringField()


class ScientificArticle(Document):  # type: ignore[misc]
    db_id = IntField(required=True)
    title = StringField()
    summary = StringField()
    file_path = StringField()
    created_at = DateTimeField()

    arxiv_id = StringField()

    author = EmbeddedDocumentField(Author)

    text = StringField()

    meta = {
        "collection": "scientific_articles",
        "indexes": [
            "db_id",
            "arxiv_id",
            {"fields": [("text", "text")], "default_language": "english"},
        ],
    }

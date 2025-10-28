from datetime import datetime

from mongodb_class import MongoUser, MongoUserList
from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    IntField,
    ListField,
    StringField,
    connect,
)

MONGO_URL = "mongodb://meriemnourG:secret2@localhost:27017/mongode?authSource=admin"
connect("mongode", host=MONGO_URL)


class Order(EmbeddedDocument):  # type: ignore[misc]
    order_id = IntField(required=True)
    product = StringField(required=True)
    amount = IntField(min_value=0)


class Profile(EmbeddedDocument):  # type: ignore[misc]
    age = IntField(min_value=0, max_value=120)
    city = StringField(max_length=100)
    interests = ListField(StringField())


class User(Document):  # type: ignore[misc]
    meta = {"collection": "users", "indexes": ["username", "email"]}

    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)
    created_at = DateTimeField(default=datetime.utcnow)

    orders = EmbeddedDocumentListField(Order)


def list_users() -> list[MongoUser]:
    return MongoUserList.validate_python(User.objects.all())


if __name__ == "__main__":
    print("All users in MongoDB:")
    for user in list_users():
        print(
            [user.id],
            f"Username: {user.username}, Email: {user.email}, Created At: {user.created_at}",
        )

    users = list_users()

    with open("data/mongoengine_users.json", "wb") as f:
        f.write(MongoUserList.dump_json(users, indent=2))

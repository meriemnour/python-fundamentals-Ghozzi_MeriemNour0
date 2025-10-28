from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, TypeAdapter, field_validator
from pymongo import MongoClient

MONGO_URL = "mongodb://root:secret@localhost:27017/"
client: MongoClient[dict[str, Any]] = MongoClient(MONGO_URL)
users_col = client.pythonde.users


class Profile(BaseModel):
    class Config:
        from_attributes = True

    age: int | None = None
    city: str | None = None
    interests: list[str] | None = None


class MongoUser(BaseModel):
    class Config:
        from_attributes = True

    id: str = Field(alias="id")
    username: str
    email: str
    profile: Profile
    created_at: datetime | None = None

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        return str(v)


MongoUserList = TypeAdapter(list[MongoUser])


def list_users() -> list[MongoUser]:
    users = users_col.find()
    cleaned_users = MongoUserList.validate_python(list(users))
    return cleaned_users


def get_user_by_username(username: str) -> MongoUser | None:
    user_data = users_col.find_one({"username": username})
    if user_data:
        return MongoUser.model_validate(user_data)
    return None


if __name__ == "__main__":
    users = list_users()
    with open("data/mongo_users.json", "wb") as f:
        f.write(MongoUserList.dump_json(users, indent=2))

    print("Mongo user with username 'alice':", get_user_by_username("alice"))

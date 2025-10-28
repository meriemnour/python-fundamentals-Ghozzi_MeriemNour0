from datetime import datetime
from typing import List, Optional

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    StringField,
    connect,
)

MONGO_URL = "mongodb://meriemnourG:secret2@localhost:27017/mongode?authSource=admin"
connect("mongode", host=MONGO_URL)


class Profile(EmbeddedDocument):
    age = IntField(min_value=0, max_value=120)
    city = StringField(max_length=100)
    interests = ListField(StringField(max_length=70))


class User(Document):
    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "users"}


def create_user(
    username: str,
    email: str,
    age: Optional[int] = None,
    city: Optional[str] = None,
    interests: Optional[List[str]] = None,
) -> User:
    profile = Profile(age=age, city=city, interests=interests or [])
    user = User(username=username, email=email, profile=profile)
    user.save()
    return user


def get_user_by_username(username: str) -> Optional[User]:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def get_all_users() -> List[User]:
    return list(User.objects.all())


def update_user(
    username: str,
    email: Optional[str] = None,
    age: Optional[int] = None,
    city: Optional[str] = None,
    interests: Optional[List[str]] = None,
) -> bool:
    try:
        user = User.objects.get(username=username)

        if email is not None:
            user.email = email

        if any([age is not None, city is not None, interests is not None]):
            if not user.profile:
                user.profile = Profile()
            if age is not None:
                user.profile.age = age
            if city is not None:
                user.profile.city = city
            if interests is not None:
                user.profile.interests = interests

        user.save()
        return True
    except User.DoesNotExist:
        return False


def delete_user_by_username(username: str) -> bool:
    try:
        user = User.objects.get(username=username)
        user.delete()
        return True
    except User.DoesNotExist:
        return False


def update_interests(username: str, new_interest: str) -> bool:
    try:
        user = User.objects.get(username=username)
        if not user.profile:
            user.profile = Profile(interests=[])
        if new_interest not in user.profile.interests:
            user.profile.interests.append(new_interest)
            user.save()
            return True
        return False
    except User.DoesNotExist:
        return False


if __name__ == "__main__":
    user_obj = create_user(
        username="mimo6",
        email="mimo6@gmail.com",
        age=25,
        city="germany",
        interests=["music", "swimming"],
    )
    print(f"Created user: {user_obj.username}")

    user = get_user_by_username("mimou")
    if user:
        print(f"User: {user.username}, Email: {user.email}")

    all_users = get_all_users()
    for user in all_users:
        print(f"User: {user.username}, Email: {user.email}")

    update_success = update_user("mimou", age=26, city="Berlin")
    print(f"Update successful: {update_success}")

    update_interests("mimou", "reading")

    username_to_delete = input("\nEnter username to delete: ")
    delete_success = delete_user_by_username(username_to_delete)
    print(f"Delete successful: {delete_success}")

    remaining_users = get_all_users()
    print("Rest of the users:")
    for user in remaining_users:
        print(f"- {user.username} ({user.email})")

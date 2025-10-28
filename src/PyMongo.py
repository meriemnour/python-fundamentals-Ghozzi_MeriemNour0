from datetime import datetime
from typing import Any, List, Optional

from bson import ObjectId
from pymongo import MongoClient

MONGO_URL = "mongodb://meriemnourG:secret2@localhost:27017/mongode?authSource=admin"
client: MongoClient[Any] = MongoClient(MONGO_URL)
users_col = client.mongode.users


def create_user(
    username: str,
    email: str,
    age: Optional[int] = None,
    city: Optional[str] = None,
    interests: Optional[List[str]] = None,
) -> Any:
    user_data = {
        "username": username,
        "email": email,
        "profile": {"age": age, "city": city, "interests": interests or []},
        "created_at": datetime.utcnow(),
    }
    result = users_col.insert_one(user_data)
    return result.inserted_id


def get_user(user_id: str) -> Optional[dict[str, Any]]:
    return users_col.find_one({"_id": ObjectId(user_id)})


def get_all_users() -> List[dict[str, Any]]:
    return list(users_col.find())


def update_user(
    username: str,
    email: Optional[str] = None,
    age: Optional[int] = None,
    city: Optional[str] = None,
    interests: Optional[List[str]] = None,
) -> bool:
    update_data: dict[str, Any] = {}

    if email is not None:
        update_data["email"] = email

    # Build profile updates
    profile_updates: dict[str, Any] = {}
    if age is not None:
        profile_updates["age"] = age
    if city is not None:
        profile_updates["city"] = city
    if interests is not None:
        profile_updates["interests"] = interests

    # If any profile fields are updated, add them to update_data
    if profile_updates:
        update_data["profile"] = profile_updates

    result = users_col.update_one(
        {"username": username},  # Find by username
        {"$set": update_data},
    )
    return result.modified_count > 0


def delete_user_by_username(username: str) -> bool:
    result = users_col.delete_one({"username": username})
    return result.deleted_count > 0


def get_user_by_username(username: str) -> Optional[dict[str, Any]]:
    return users_col.find_one({"username": username})


# Add a new interest to user's interests array => pull operator
def update_interests(user_id: str, new_interest: str) -> bool:
    result = users_col.update_one(
        {"_id": ObjectId(user_id)}, {"$push": {"profile.interests": new_interest}}
    )
    return result.modified_count > 0


if __name__ == "__main__":
    #    user_id = create_user(
    #        username="lolo",
    #        email="lolo@gmail.com",
    #        age=25,
    #        city="germany",
    #        interests=["music", "swimming"]
    #    )
    #    print(f"Created user with ID: {user_id}")

    #    user = get_user(user_id)
    #    print(f"User: {user}")

    all_users = get_all_users()
    for user in all_users:
        print(f"User: {user['username']}, Email: {user['email']}")

    update_success = update_user("mimou", age=26, city="Berlin")
    print(f"Update successful: {update_success}")

    # update_interests(user_id, "reading")

    username_to_delete = input("\nEnter username to delete: ")
    delete_success = delete_user_by_username(username_to_delete)
    all_users = get_all_users()
    for user in all_users:
        print(f"User: {user['username']}, Email: {user['email']}")

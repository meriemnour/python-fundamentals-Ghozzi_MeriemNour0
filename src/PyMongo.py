from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

MONGO_URL = "mongodb://meriemnourG:secret2@localhost:27017/mongode?authSource=admin"


def main() -> None:
    client: MongoClient[Dict[str, Any]] = MongoClient(MONGO_URL)
    db: Database[Dict[str, Any]] = client.mongode  # Add type parameter here
    users_collection: Collection[Dict[str, Any]] = db.users

    # Example CRUD operations
    # Create
    new_user: Dict[str, Any] = {
        "username": "nour",
        "email": "nour@example.com",
        "age": 25,
    }

    # Insert user
    result = users_collection.insert_one(new_user)
    print(f"Inserted user with ID: {result.inserted_id}")

    # Read
    user: Optional[Dict[str, Any]] = users_collection.find_one({"username": "nour"})
    if user:
        print(f"Found user: {user}")

    # Update
    update_result = users_collection.update_one(
        {"username": "nour"}, {"$set": {"age": 26}}
    )
    print(f"Updated {update_result.modified_count} documents")

    # Delete
    delete_result = users_collection.delete_one({"username": "nour"})
    print(f"Deleted {delete_result.deleted_count} documents")

    client.close()


if __name__ == "__main__":
    main()

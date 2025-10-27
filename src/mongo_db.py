from pymongo import MongoClient

MONGO_URL = "mongodb://meriemnourG:secret2@localhost:27017/mongode?authSource=admin"

client = MongoClient(MONGO_URL)
db = client.mongode

# users = list(db.users.find())
# print("Users found:", users)

new_user = {
    "username": "nour",
    "email": "nour@example.com",
    "profile": {
        "age": 20,
        "city": "germany",
        "interest": ["StreetDance", "Art", "violon", "swimming"],
    },
    "orders": [{"order_id": 1, "product": "camera", "amount": 1200}],
}
# insert_result = db.users.insert_one(new_user)
# print("inserted user ", insert_result.inserted_id)

user_nour = db.users.find_one({"username": "nour"})
print(user_nour["username"], user_nour["email"])
print(f"nour's orders: {user_nour['orders'][0]['product']}")


update_nour = db.users.update_one({"username": "nour"}, {"$set": {"profile.age": 18}})
updated_user = db.users.find_one({"username": "nour"})
print(updated_user["profile"]["age"])


r = db.users.find()
print("users in MonDB")
for user in r:
    print(type(user), user)

from mongoengine import connect

MONGO_URL = "mongodb://meriemnourG:secret2@localhost:27017/mongode?authSource=admin"
connect("mongode", host=MONGO_URL)

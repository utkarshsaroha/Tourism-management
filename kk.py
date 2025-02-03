from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["tourism_system"]
users_collection = db["users"]

test_user = {
    "username": "test_user",
    "email": "test@example.com",
    "password": "hashed_password"
}
users_collection.insert_one(test_user)
print("User inserted successfully!")

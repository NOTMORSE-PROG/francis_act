import os
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    client = MongoClient(os.environ.get("MONGO_URI"))
    return client["flaskapp"]

def get_items(db):
    return [{"id": str(d["_id"]), "name": d["name"], "desc": d.get("desc", "")} for d in db["items"].find()]

def add_item(db, data):
    result = db["items"].insert_one({"name": data["name"], "desc": data.get("desc", "")})
    return {"inserted_id": str(result.inserted_id)}

def delete_item(db, item_id):
    db["items"].delete_one({"_id": ObjectId(item_id)})
    return {"status": "deleted"}

def register_user(db, name, password):
    if db["users"].find_one({"name": name}):
        return {"error": "User already exists"}
    db["users"].insert_one({"name": name, "password": generate_password_hash(password)})
    return {"message": "User registered successfully"}

def login_user(db, name, password):
    user = db["users"].find_one({"name": name})
    if not user or not check_password_hash(user["password"], password):
        return None
    return {"message": "Login successful"}

from bson.binary import Binary
from bson.objectid import ObjectId

from config import URL

from pymongo import MongoClient

from werkzeug.security import check_password_hash, generate_password_hash


USER_COLLECTION = MongoClient(URL)["loveat2"]["user"]


def add(data):
    if USER_COLLECTION.find_one({"userName": data["userName"]}) is None:
        USER_COLLECTION.insert_one({
            "userName": data["userName"],
            "password": generate_password_hash(data['password']),
            "gender": data["gender"],
            "phone": data["phone"],
            "email": data["email"],
            "birth": data["birth"],
            "role": data["role"],
            "avatar": Binary(b'')
        })
        return True
    else:
        return False


def find(id, profile=False):
    if profile:
        projection = {
            "password": 0,
            "role": 0,
            "token": 0
        }
    else:
        projection = {
            "role": 1,
            "userName": 1
        }
    return USER_COLLECTION.find_one({
        "_id": ObjectId(id)
    }, projection)


def validate_user(data, email=False, password=False):
    if email:
        user = USER_COLLECTION.find_one({
            "userName": data["userName"],
            "email": data["email"]
        }, {
            "_id": 1
        })
        if user:
            return user["_id"]
    elif password:
        user = USER_COLLECTION.find_one({
            "userName": data["userName"]
        }, {
            "_id": 1,
            "password": 1
        })
        if user and check_password_hash(user["password"], data["password"]):
            return user["_id"]
    return None


def update_password(id, password):
    USER_COLLECTION.update_one({
        "_id": ObjectId(id)
    }, {
        "$set": {
            "password": generate_password_hash(password)
        }
    })

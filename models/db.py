from config import URL

from pymongo import MongoClient

DB = MongoClient(URL)["loveat2"]

BUSINESS_COLLECTION = DB["businessTime"]
IMAGE_COLLECTION = DB["image"]
TYPE_COLLECTION = DB["type"]
ITEM_COLLECTION = DB["item"]
COMBO_COLLECTION = DB["combo"]
ORDER_COLLECTION = DB["order"]
USER_COLLECTION = DB["user"]

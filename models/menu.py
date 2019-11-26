from config import URL

from pymongo import MongoClient

DB = MongoClient(URL)['loveat2']
TYPE_COLLECTION = DB["type"]
ITEM_COLLECTION = DB["item"]
COMBO_COLLECTION = DB["combo"]


def get_all():
    item_result = list(TYPE_COLLECTION.aggregate([
        {
            '$match': {
                'category': 'item'
            }
        }, {
            '$lookup': {
                'from': 'item',
                'localField': '_id',
                'foreignField': 'type',
                'as': 'content'
            }
        }, {
            '$project': {
                '_id': 0,
                'content.type': 0
            }
        }
    ]))
    combo_result = list(TYPE_COLLECTION.aggregate([
        {
            '$match': {
                'category': 'combo'
            }
        }, {
            '$lookup': {
                'from': 'combo',
                'localField': '_id',
                'foreignField': 'type',
                'as': 'content'
            }
        }, {
            '$project': {
                '_id': 0,
                'content.type': 0,
                'content.content.id': 0
            }
        }
    ]))
    for item in item_result:
        for content in item["content"]:
            content["_id"] = str(content["_id"])
        item['type'] = item.pop('name')

    for combo in combo_result:
        for content in combo["content"]:
            content["_id"] = str(content["_id"])
        combo['type'] = combo.pop('name')
    return item_result + combo_result

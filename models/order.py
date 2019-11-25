from config import URL

from pymongo import MongoClient

DB = MongoClient(URL)['loveat2']
ORDER_COLLECTION = DB['order']
ITEM_COLLECTION = DB['item']
COMBO_COLLECTION = DB['combo']


def get(start, end):
    cursor = ORDER_COLLECTION.find(
        {
            'takenAt': {
                '$gte': start,
                '$lte': end
            },
            'state': 'end'
        }, {
            'content._id': 0,
            '_id': 0,
            'takenAt': 0,
            'state': 0,
            'total': 0,
            'userName': 0
        }
    )
    return list(cursor)

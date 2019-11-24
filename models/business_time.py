from config import URL

from pymongo import MongoClient

COLLECTION = MongoClient(URL)['loveat2']['businessTime']


def get():
    data = COLLECTION.find_one()
    return data


def update(data):
    # establish update data
    update_data = {}
    week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    for day in week:
        update_data[day] = {
            "start": data[day]["start"],
            "end": data[day]["end"],
        }
    # start update
    COLLECTION.update_one({}, {
        "$set": update_data
    })

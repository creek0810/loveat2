from config import URL

from pymongo import MongoClient

DB = MongoClient(URL)["loveat2"]
ORDER_COLLECTION = DB["order"]
ITEM_COLLECTION = DB["item"]
COMBO_COLLECTION = DB["combo"]


def find_by_time(start, end):
    return {"takenAt": {"$gte": start, "$lte": end}, "state": "end"}


def get_raw_history(start, end):
    return ORDER_COLLECTION.find(
        find_by_time(start, end),
        {
            "content._id": 0,
            "content.type": 0,
            "_id": 0,
            "takenAt": 0,
            "state": 0,
            "total": 0,
            "userName": 0,
        },
    )


def build_analysis_struct(interval, slot):
    result = {
        "interval": [],
        "itemAnalysis": {},
        "genderAnalysis": [
            {"female": 0, "male": 0, "total": 0} for i in range(slot)
        ],
    }
    for i in range(slot):
        if i == slot - 1:
            result["interval"].append("{}+".format(i * interval))
        else:
            result["interval"].append(
                "{}-{}".format(i * interval, interval * (i + 1) - 1)
            )
    return result


def get_analysis_data(start, end):
    interval = 10
    slot = 7
    result = build_analysis_struct(interval, slot)
    # query
    raw_data = ORDER_COLLECTION.aggregate(
        [
            {"$match": find_by_time(start, end)},
            {
                "$lookup": {
                    "from": "user",
                    "localField": "userName",
                    "foreignField": "userName",
                    "as": "user",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "content.name": 1,
                    "content.quantity": 1,
                    "user.birth": 1,
                    "user.gender": 1,
                    "user.userName": 1,
                    "takenAt": 1,
                }
            },
            {
                "$unwind": {
                    "path": "$user",
                    "preserveNullAndEmptyArrays": False,
                }
            },
        ]
    )
    # first calc
    for data in raw_data:
        age = (data["takenAt"] - data["user"]["birth"]).days // 365
        index = min(age // interval, slot - 1)
        # build gender analysis
        result["genderAnalysis"][index][data["user"]["gender"]] += 1
        # build item analysis
        for content in data["content"]:
            if content["name"] not in result["itemAnalysis"]:
                result["itemAnalysis"][content["name"]] = {
                    "female": [0] * slot,
                    "male": [0] * slot,
                    "sum": [0] * slot,
                    "femaleTotal": 0,
                    "maleTotal": 0,
                    "total": 0,
                }
            result["itemAnalysis"][content["name"]][data["user"]["gender"]][
                index
            ] += 1
    # sum
    for genderAnalysis in result["genderAnalysis"]:
        genderAnalysis["total"] = (
            genderAnalysis["female"] + genderAnalysis["male"]
        )
    for itemAnalysis in result["itemAnalysis"].values():
        itemAnalysis["femaleTotal"] = sum(itemAnalysis["female"])
        itemAnalysis["maleTotal"] = sum(itemAnalysis["male"])
        itemAnalysis["sum"] = [
            itemAnalysis["male"][i] + itemAnalysis["female"][i]
            for i in range(slot)
        ]
        itemAnalysis["total"] = (
            itemAnalysis["femaleTotal"] + itemAnalysis["maleTotal"]
        )
    return result

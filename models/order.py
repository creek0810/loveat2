from datetime import datetime, timedelta

from bson.objectid import ObjectId

from models import db


MAX_ORDERID = -1

# projection for unknown page
UNKNOWN_PROJECT = [
    {"$project": {"content.id": 0, "content.category": 0}},
    {
        "$project": {
            "_id": {"$toString": "$_id"},
            "takenAt": {
                "$dateToString": {
                    "format": "%Y/%m/%d %H:%M",
                    "date": "$takenAt",
                }
            },
            "content": 1,
            "notes": 1,
        }
    },
]


def find_by_time(start, end):
    return {"takenAt": {"$gte": start, "$lte": end}, "state": "end"}


def get_raw_history(start, end):
    return db.ORDER_COLLECTION.find(
        find_by_time(start, end),
        {
            "content.id": 0,
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
    raw_data = db.ORDER_COLLECTION.aggregate(
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
            ] += content["quantity"]
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


def get_max_orderid():
    result = list(
        db.ORDER_COLLECTION.aggregate(
            [
                {"$addFields": {"orderID": {"$toInt": "$orderID"}}},
                {"$group": {"_id": None, "max": {"$max": "$orderID"}}},
            ]
        )
    )
    if len(result) == 0:
        return 0
    else:
        return result[0]["max"]


def get_not_end_by_username(user_name):
    return db.ORDER_COLLECTION.aggregate(
        [
            {
                "$match": {
                    "userName": user_name,
                    "state": {"$nin": ["end"]},
                    "takenAt": {"$gte": datetime.now() - timedelta(days=1)},
                }
            },
            {
                "$addFields": {
                    "takenAt": {
                        "$dateToString": {
                            "format": "%Y/%m/%d %H:%M",
                            "date": "$takenAt",
                        }
                    },
                    "_id": {"$toString": "$_id"},
                }
            },
            {
                "$project": {
                    "createdAt": 0,
                    "userName": 0,
                    "total": 0,
                    "content.id": 0,
                    "content.type": 0,
                }
            },
        ]
    )


def add_order(data):
    def build_business_time(time_str):
        result = data["takenAt"][:-6] + "-" + time_str
        return datetime.strptime(result, "%Y-%m-%d-%H:%M")

    # init max orderid
    global MAX_ORDERID
    if MAX_ORDERID == -1:
        MAX_ORDERID = get_max_orderid()

    # convert data to correct type
    taken_at = datetime.strptime(data["takenAt"], "%Y-%m-%dT%H:%M")
    business_time = list(
        db.BUSINESS_COLLECTION.find_one({}, {"_id": 0}).values()
    )
    business_time = business_time[taken_at.isoweekday() - 1]
    start = build_business_time(business_time["start"])
    end = build_business_time(business_time["end"])

    # check if content is empty, takenAt is > now and in business interval
    if (
        start <= taken_at <= end
        and len(data["content"]) > 0
        and taken_at > datetime.now()
    ):
        MAX_ORDERID += 1
        for meal in data["content"]:
            meal["id"] = ObjectId(meal["id"])
            tar_col = {
                "item": db.ITEM_COLLECTION,
                "combo": db.COMBO_COLLECTION,
            }
            tar = tar_col[meal["category"]].find_one(
                {"_id": meal["id"]}, {"name": 1}
            )
            meal["name"] = tar["name"]

        result = db.ORDER_COLLECTION.insert_one(
            {
                "userName": data["userName"],
                "notes": data["notes"],
                "total": data["total"],
                "content": data["content"],
                "state": "unknown",
                "createdAt": datetime.now(),
                "takenAt": taken_at,
                "orderID": str(MAX_ORDERID),
            }
        )

        pipeline = [{"$match": {"_id": result.inserted_id}}] + UNKNOWN_PROJECT
        return list(db.ORDER_COLLECTION.aggregate(pipeline))[0]
    else:
        return None


def update_state(data):
    state = ["doing", "cancel", "finish", "end"]
    if data["state"] in state:
        db.ORDER_COLLECTION.update_one(
            {"_id": ObjectId(data["id"])}, {"$set": {"state": data["state"]}}
        )
        result = db.ORDER_COLLECTION.find_one(
            {"_id": ObjectId(data["id"])},
            {"userName": 1, "_id": 1, "orderID": 1, "state": 1},
        )
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            return None
    else:
        return None


def get_todo_order(id=None):
    if id:
        match = {
            "$match": {
                "state": {"$in": ["doing", "finish"]},
                "_id": ObjectId(id),
            }
        }
    else:
        match = {"$match": {"state": {"$in": ["doing", "finish"]}}}

    result = db.ORDER_COLLECTION.aggregate(
        [
            match,
            {
                "$lookup": {
                    "from": "user",
                    "localField": "userName",
                    "foreignField": "userName",
                    "as": "user",
                }
            },
            {"$unwind": {"path": "$user"}},
            {"$project": {"content.id": 0, "content.category": 0}},
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "orderID": {"$toInt": "$orderID"},
                    "takenAt": {
                        "$dateToString": {
                            "format": "%Y/%m/%d %H:%M",
                            "date": "$takenAt",
                        }
                    },
                    "state": 1,
                    "content": 1,
                    "notes": 1,
                    "user_id": {"$toString": "$user._id"},
                    "phone": "$user.phone",
                }
            },
            {"$sort": {"orderID": 1}},
        ]
    )
    return result


def get_unknown_order():
    pipeline = (
        [{"$match": {"state": "unknown"}}]
        + UNKNOWN_PROJECT
        + [{"$sort": {"orderID": 1}}]
    )
    result = db.ORDER_COLLECTION.aggregate(pipeline)
    return result


def update_food_amount(data):
    result = db.ORDER_COLLECTION.find_one(
        {"_id": ObjectId(data["id"])}, {"content": 1, "_id": 0}
    )
    for meal in result["content"]:
        if meal["type"] == "item":
            db.ITEM_COLLECTION.update(
                {"name": meal["name"]}, {"$setOnInsert": {"sell": 0}}
            )
        db.ITEM_COLLECTION.update(
            {"name": meal["name"]}, {"$inc": {"sell": meal["quantity"]}}
        )
        if meal["type"] == "combo":
            db.COMBO_COLLECTION.update(
                {"name": meal["name"]}, {"$setOnInsert": {"sell": 0}}
            )
        db.COMBO_COLLECTION.update(
            {"name": meal["name"]}, {"$inc": {"sell": meal["quantity"]}}
        )

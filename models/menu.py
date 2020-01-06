import json
import uuid

from bson.objectid import ObjectId

from lib.custom_except import duplicateError

from models import db


def get_all():
    item_result = list(
        db.TYPE_COLLECTION.aggregate(
            [
                {"$match": {"category": "item"}},
                {
                    "$lookup": {
                        "from": "item",
                        "localField": "_id",
                        "foreignField": "type",
                        "as": "content",
                    }
                },
                {"$project": {"_id": 0, "content.type": 0}},
            ]
        )
    )
    combo_result = list(
        db.TYPE_COLLECTION.aggregate(
            [
                {"$match": {"category": "combo"}},
                {
                    "$lookup": {
                        "from": "combo",
                        "localField": "_id",
                        "foreignField": "type",
                        "as": "content",
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "content.type": 0,
                        "content.content.id": 0,
                    }
                },
            ]
        )
    )

    TOP_RANK = 3
    top_item_result = list(
        db.ITEM_COLLECTION.find().sort([("sell", -1)]).limit(TOP_RANK)
    )
    top_item_list = []
    for item in top_item_result:
        top_item_list.append(str(item["_id"]))

    for item in item_result:
        for content in list(item["content"]):
            content["_id"] = str(content["_id"])
            if content["_id"] in top_item_list:
                content["top"] = True
            else:
                content["top"] = False
        item["type"] = item.pop("name")

    top_combo_result = list(
        db.COMBO_COLLECTION.find().sort([("sell", -1)]).limit(TOP_RANK)
    )
    top_combo_list = []
    for combo in top_combo_result:
        top_combo_list.append(str(combo["_id"]))

    for combo in combo_result:
        for content in combo["content"]:
            content["_id"] = str(content["_id"])
            if content["_id"] in top_combo_list:
                content["top"] = True
            else:
                content["top"] = False
        combo["type"] = combo.pop("name")

    return item_result + combo_result


def get_item_by_id(data, detail=False):
    id = [ObjectId(i) for i in data]
    pipeline = [
        {"$match": {"_id": {"$in": id}}},
        {
            "$addFields": {
                "_id": {"$toString": "$_id"},
                "type": {"$toString": "$type"},
            }
        },
    ]
    if detail is False:
        pipeline.append({"$project": {"name": 1, "price": 1}})
    result = list(db.ITEM_COLLECTION.aggregate(pipeline))
    return result


def get_combo_by_id(data, detail=False):
    id = [ObjectId(i) for i in data]
    pipeline = [
        {"$match": {"_id": {"$in": id}}},
        {
            "$addFields": {
                "_id": {"$toString": "$_id"},
                "type": {"$toString": "$type"},
                "content": {
                    "$map": {
                        "input": "$content",
                        "as": "t",
                        "in": {
                            "id": {"$toString": "$$t.id"},
                            "quantity": "$$t.quantity",
                            "name": "$$t.name",
                        },
                    }
                },
            }
        },
    ]
    if detail is False:
        pipeline.append({"$project": {"name": 1, "price": 1}})

    result = db.COMBO_COLLECTION.aggregate(pipeline)
    return list(result)


def get_type(item=False, combo=False):
    # build match
    match = []
    if item:
        match.append("item")
    if combo:
        match.append("combo")
    # start query
    return list(
        db.TYPE_COLLECTION.aggregate(
            [
                {"$match": {"category": {"$in": match}}},
                {"$project": {"_id": {"$toString": "$_id"}, "name": 1}},
            ]
        )
    )


def add_item(data, pic):
    cur_item = db.ITEM_COLLECTION.find_one({"name": data.get("name")})
    if cur_item:
        raise duplicateError
    else:
        pic_id = str(uuid.uuid4())
        db.ITEM_COLLECTION.insert_one(
            {
                "type": ObjectId(data.get("type")),
                "name": data.get("name"),
                "picture": pic_id,
                "price": int(data.get("price")),
                "description": data.get("description"),
            }
        )
        db.IMAGE_COLLECTION.insert_one({"uuid": pic_id, "picture": pic})


def add_combo(data, pic):
    cur_combo = db.COMBO_COLLECTION.find_one({"name": data.get("name")})
    if cur_combo:
        raise duplicateError
    else:
        pic_id = str(uuid.uuid4())
        # pre processing content field
        content = json.loads(data.get("content"))
        for item in content:
            item["id"] = ObjectId(item["id"])
            item["name"] = db.ITEM_COLLECTION.find_one(
                {"_id": item["id"]}, {"name": 1}
            )["name"]
        # start insert
        db.COMBO_COLLECTION.insert_one(
            {
                "type": ObjectId(data.get("type")),
                "name": data.get("name"),
                "picture": pic_id,
                "price": int(data.get("price")),
                "description": data.get("description"),
                "content": content,
            }
        )
        db.IMAGE_COLLECTION.insert_one({"uuid": pic_id, "picture": pic})


def add_type(data):
    cur_type = db.TYPE_COLLECTION.find_one(
        {"category": data["category"], "name": data["type"]}
    )
    if cur_type:
        raise duplicateError
    else:
        db.TYPE_COLLECTION.insert_one(
            {"category": data["category"], "name": data["type"]}
        )


def delete_item(id):
    object_id = ObjectId(id)
    item = db.ITEM_COLLECTION.find_one({"_id": object_id}, {"picture": 1})
    db.ITEM_COLLECTION.delete_one({"_id": object_id})
    db.IMAGE_COLLECTION.delete_one({"uuid": item["picture"]})
    # delete cur item in combo
    db.COMBO_COLLECTION.update_many(
        {"content.id": object_id}, {"$pull": {"content": {"id": object_id}}}
    )


def delete_combo(id):
    object_id = ObjectId(id)
    combo = db.COMBO_COLLECTION.find_one({"_id": object_id}, {"picture": 1})
    db.COMBO_COLLECTION.delete_one({"_id": ObjectId(id)})
    db.IMAGE_COLLECTION.delete_one({"uuid": combo["picture"]})


def delete_type(id):
    # update item or combo type to undefined
    object_id = ObjectId(id)
    cur_type = db.TYPE_COLLECTION.find_one({"_id": object_id})
    if cur_type["category"] == "item":
        new_id = db.TYPE_COLLECTION.find_one({"name": "未分類(單品)"})["_id"]
        db.ITEM_COLLECTION.update_many(
            {"type": object_id}, {"$set": {"type": new_id}}
        )
    elif cur_type["category"] == "combo":
        new_id = db.TYPE_COLLECTION.find_one({"name": "未分類(套餐)"})["_id"]
        db.COMBO_COLLECTION.update_many(
            {"type": object_id}, {"$set": {"type": new_id}}
        )

    # start delete
    db.TYPE_COLLECTION.delete_one({"_id": object_id})


def update_item(data, pic):
    if db.ITEM_COLLECTION.find_one(
        {"_id": {"$ne": ObjectId(data["id"])}, "name": data["name"]}
    ):
        raise duplicateError
    else:
        pic_id = db.ITEM_COLLECTION.find_one(
            {"_id": ObjectId(data.get("id"))}, {"picture": 1}
        )["picture"]
        # update item
        db.ITEM_COLLECTION.update_one(
            {"_id": ObjectId(data.get("id"))},
            {
                "$set": {
                    "type": ObjectId(data.get("type")),
                    "name": data.get("name"),
                    "price": int(data.get("price")),
                    "description": data.get("description"),
                }
            },
        )
        # update item name in combo
        db.COMBO_COLLECTION.update_many(
            {"content.id": ObjectId(data.get("id"))},
            {"$set": {"content.$.name": data.get("name")}},
        )
        # update pic
        if pic != b"":
            db.IMAGE_COLLECTION.update_one(
                {"uuid": pic_id}, {"$set": {"picture": pic}}
            )


def update_combo(data, pic):
    if db.COMBO_COLLECTION.find_one(
        {"_id": {"$ne": ObjectId(data["id"])}, "name": data["name"]}
    ):
        raise duplicateError
    else:
        pic_id = db.COMBO_COLLECTION.find_one(
            {"_id": ObjectId(data.get("id"))}, {"picture": 1}
        )["picture"]
        # pre processing content field
        content = json.loads(data.get("content"))
        for item in content:
            item["id"] = ObjectId(item["id"])
            item["name"] = db.ITEM_COLLECTION.find_one(
                {"_id": item["id"]}, {"name": 1}
            )["name"]
        # start update
        db.COMBO_COLLECTION.update_one(
            {"_id": ObjectId(data.get("id"))},
            {
                "$set": {
                    "type": ObjectId(data.get("type")),
                    "name": data.get("name"),
                    "price": int(data.get("price")),
                    "description": data.get("description"),
                    "content": content,
                }
            },
        )
        if pic != b"":
            db.IMAGE_COLLECTION.update_one(
                {"uuid": pic_id}, {"$set": {"picture": pic}}
            )


def update_type(data):
    if db.TYPE_COLLECTION.find_one({"name": data["type"]}):
        raise duplicateError
    else:
        db.TYPE_COLLECTION.update_one(
            {"_id": ObjectId(data["id"])}, {"$set": {"name": data["type"]}}
        )

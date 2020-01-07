import io

from bson.binary import Binary
from bson.objectid import ObjectId

from models import db

URL_PREFIX = "/api/menu/item"


class TestItem(object):
    update_item = {
        "id": "5dd67f098f0f6afb3ebc1b69",
        "type": "5dd678b95f19051c7c4f0bb3",
        "name": "new name",
        "price": 6742,
        "description": "new description",
    }
    update_item_duplicate_name = {
        "id": "5dd67f098f0f6afb3ebc1b69",
        "type": "5dd678b95f19051c7c4f0bb3",
        "name": "紅茶",
        "price": 6742,
        "description": "new description",
    }
    """ can't run, because mongomock doesn't support addfields
    def test_get_item_success(self, client):
        # check get item api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(
                ["5dd67f098f0f6afb3ebc1b69", "5dd67f098f0f6afb3ebc1b6a"]
            ),
            content_type="application/json",
        )
        assert json.loads(rv.data) == [
            {"_id": "5dd67f098f0f6afb3ebc1b69", "price": 20, "name": "奶茶"},
            {"_id": "5dd67f098f0f6afb3ebc1b6a", "price": 20, "name": "茉莉綠茶"},
        ]
    """

    """ can't run, because mongomock doesn't support addfields
    def test_get_item_empty(self, client):
        # check get item api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(["6dd67f098f0f6afb3ebc1b69"]),
            content_type="application/json",
        )
        assert json.loads(rv.data) == []
        assert rv.status_code == 200
    """
    # update item
    def test_update_item_unauthorized(self, client):
        url = URL_PREFIX + "/update"
        data = self.update_item.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 403

    def test_update_item_by_customer(self, client, customer):
        url = URL_PREFIX + "/update"
        data = self.update_item.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 403

    def test_update_item_duplicate_name(self, client, admin):
        url = URL_PREFIX + "/update"
        data = self.update_item_duplicate_name.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 409

    def test_update_item_with_pic(self, client, admin):
        url = URL_PREFIX + "/update"
        data = self.update_item.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 200
        cur_item = db.ITEM_COLLECTION.find_one(
            {"_id": ObjectId(self.update_item["id"])}
        )
        cur_img = db.IMAGE_COLLECTION.find_one({"uuid": cur_item["picture"]})
        assert cur_item["type"] == ObjectId(self.update_item["type"])
        assert cur_item["name"] == self.update_item["name"]
        assert cur_item["price"] == self.update_item["price"]
        assert cur_item["description"] == self.update_item["description"]
        print(cur_img["picture"])
        assert cur_img["picture"] == b"6742"

    def test_update_item_no_pic(self, client, admin):
        url = URL_PREFIX + "/update"
        # update pic to 6742
        cur_item = db.ITEM_COLLECTION.find_one(
            {"_id": ObjectId(self.update_item["id"])}
        )
        db.IMAGE_COLLECTION.update_one(
            {"uuid": cur_item["picture"]},
            {"$set": {"picture": Binary(b"6742")}},
        )

        # try update item has no pic
        data = self.update_item.copy()
        data["picture"] = (io.BytesIO(b""), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 200
        cur_item = db.ITEM_COLLECTION.find_one(
            {"_id": ObjectId(self.update_item["id"])}
        )
        cur_img = db.IMAGE_COLLECTION.find_one({"uuid": cur_item["picture"]})
        assert cur_item["type"] == ObjectId(self.update_item["type"])
        assert cur_item["name"] == self.update_item["name"]
        assert cur_item["price"] == self.update_item["price"]
        assert cur_item["description"] == self.update_item["description"]
        print(cur_img["picture"])
        assert cur_img["picture"] == Binary(b"6742")

    def test_delete_anonymous(self, client):
        # test there is an item named 奶茶 in collection
        exist_item = db.ITEM_COLLECTION.find_one({"name": "奶茶"})
        assert exist_item is not None
        # test delete the exist item anonymons
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps({
                "id": str(exist_item["_id"])
            }),
            content_type="application/json",
        )
        assert rv.status_code == 403

    def test_delete_by_customer(self, client, customer):
        # test there is an item named 奶茶 in collection
        exist_item = db.ITEM_COLLECTION.find_one({"name": "奶茶"})
        assert exist_item is not None
        # test delete the exist item by customer
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps({
                "id": str(exist_item["_id"])
            }),
            content_type="application/json",
        )
        assert rv.status_code == 403

    def test_delete_by_admin(self, client, admin):
        # test there is an item named 奶茶 in collection
        exist_item = db.ITEM_COLLECTION.find_one({"name": "奶茶"})
        assert exist_item is not None
        # test delete the exist item by boss
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps({
                "id": str(exist_item["_id"])
            }),
            content_type="application/json",
        )
        assert rv.status_code == 200

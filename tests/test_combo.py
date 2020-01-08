import io
import json

from bson.binary import Binary
from bson.objectid import ObjectId

from models import db

URL_PREFIX = "/api/menu/combo"


class TestCombo(object):
    update_combo = {
        "id": "5dda567d09d84aa89699121c",
        "type": "5dd681c44a608a104f89914e",
        "name": "new combo name",
        "price": 6742,
        "description": "new description",
        "content": json.dumps(
            [
                {"id": "5de35fc5fdb6b28d6100d776", "quantity": 10},
                {"id": "5de22841f6bf2b651e091f6e", "quantity": 20},
            ]
        ),
    }
    update_combo_duplicate_name = {
        "id": "5dda567d09d84aa89699121c",
        "type": "5dd681c44a608a104f89914e",
        "name": "鐵板麵套餐(無熱狗)",
        "price": 6742,
        "description": "new description",
        "content": json.dumps(
            [
                {"id": "5de35fc5fdb6b28d6100d776", "quantity": 10},
                {"id": "5de22841f6bf2b651e091f6e", "quantity": 20},
            ]
        ),
    }
    new_combo = {
        "type": "5dd681c44a608a104f899151",
        "name": "好哦謝謝",
        "price": 70,
        "description": "",
        "content": json.dumps(
            [
                {"id": "5de35fc5fdb6b28d6100d776", "quantity": 10},
                {"id": "5de22841f6bf2b651e091f6e", "quantity": 20},
            ]
        ),
    }
    exist_combo = {
        "type": "5dd681c44a608a104f89914e",
        "name": "鐵板麵套餐",
        "price": 6742,
        "description": "yoyoyo",
        "content": json.dumps(
            [
                {"id": "5de35fc5fdb6b28d6100d776", "quantity": 10},
                {"id": "5de22841f6bf2b651e091f6e", "quantity": 20},
            ]
        ),
    }
    """ can't run, because mongomock doesn't support addfields
    def test_get_combo_success(self, client):
        # check get combo api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(
                ["5dda567d09d84aa89699121c"]
            ),
            content_type="application/json",
        )
        assert json.loads(rv.data) == [
            {
                "_id": "5dda567d09d84aa89699121c",
                "name": "鐵板麵套餐",
                "price": 70
            }
        ]
    """

    """ can't run, because mongomock doesn't support addfields
    def test_get_combo_empty(self, client):
        # check get combo api
        url = URL_PREFIX
        rv = client.post(
            url,
            data=json.dumps(["6dd67f098f0f6afb3ebc1b60"]),
            content_type="application/json",
        )
        assert json.loads(rv.data) == []
        assert rv.status_code == 200
    """
    # update combo
    def test_update_combo_unauthorized(self, client):
        url = URL_PREFIX + "/update"
        data = self.update_combo.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 403

    def test_update_combo_by_customer(self, client, customer):
        url = URL_PREFIX + "/update"
        data = self.update_combo.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 403

    def test_update_combo_duplicate_name(self, client, admin):
        url = URL_PREFIX + "/update"
        data = self.update_combo_duplicate_name.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 409

    def test_update_combo_with_picture(self, client, admin):
        url = URL_PREFIX + "/update"
        data = self.update_combo.copy()
        data["picture"] = (io.BytesIO(b"6742"), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 200
        cur_combo = db.COMBO_COLLECTION.find_one(
            {"_id": ObjectId(self.update_combo["id"])}
        )
        cur_image = db.IMAGE_COLLECTION.find_one(
            {"uuid": cur_combo["picture"]}
        )["picture"]
        assert cur_combo == {
            "_id": ObjectId("5dda567d09d84aa89699121c"),
            "content": [
                {
                    "id": ObjectId("5de35fc5fdb6b28d6100d776"),
                    "name": "鮮奶茶2",
                    "quantity": 10,
                },
                {
                    "id": ObjectId("5de22841f6bf2b651e091f6e"),
                    "name": "紅茶",
                    "quantity": 20,
                },
            ],
            "description": "new description",
            "name": "new combo name",
            "picture": "06dcc1d4-90aa-4ba9-8758-6de813bc5fa4",
            "price": 6742,
            "type": ObjectId("5dd681c44a608a104f89914e"),
        }
        assert cur_image == b"6742"

    def test_update_combo_no_picture(self, client, admin):
        url = URL_PREFIX + "/update"
        # update pic to 6742
        cur_combo = db.COMBO_COLLECTION.find_one(
            {"_id": ObjectId(self.update_combo["id"])}
        )
        db.IMAGE_COLLECTION.update_one(
            {"uuid": cur_combo["picture"]},
            {"$set": {"picture": Binary(b"6742")}},
        )
        # start update
        data = self.update_combo.copy()
        data["picture"] = (io.BytesIO(b""), "test.jpg")
        rv = client.post(url, content_type="multipart/form-data", data=data)
        assert rv.status_code == 200
        cur_combo = db.COMBO_COLLECTION.find_one(
            {"_id": ObjectId(self.update_combo["id"])}
        )
        cur_image = db.IMAGE_COLLECTION.find_one(
            {"uuid": cur_combo["picture"]}
        )["picture"]
        assert cur_combo == {
            "_id": ObjectId("5dda567d09d84aa89699121c"),
            "content": [
                {
                    "id": ObjectId("5de35fc5fdb6b28d6100d776"),
                    "name": "鮮奶茶2",
                    "quantity": 10,
                },
                {
                    "id": ObjectId("5de22841f6bf2b651e091f6e"),
                    "name": "紅茶",
                    "quantity": 20,
                },
            ],
            "description": "new description",
            "name": "new combo name",
            "picture": "06dcc1d4-90aa-4ba9-8758-6de813bc5fa4",
            "price": 6742,
            "type": ObjectId("5dd681c44a608a104f89914e"),
        }
        assert cur_image == Binary(b"6742")

    # add combo
    def test_add_unauthorized(self, client):
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.new_combo["name"]}
        )
        assert tmp_combo is None
        url = URL_PREFIX + "/new"
        data = self.new_combo.copy()
        data["picture"] = (io.BytesIO(b"6724"), "test.jpg")
        rv = client.post(url, data=data, content_type="multipart/form-data")
        assert rv.status_code == 403
        # check : doesn't add in DB
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.new_combo["name"]}, {"_id": 0}
        )
        assert tmp_combo is None

    def test_add_by_customer(self, client, customer):
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.new_combo["name"]}
        )
        assert tmp_combo is None
        url = URL_PREFIX + "/new"
        data = self.new_combo.copy()
        data["picture"] = (io.BytesIO(b"6724"), "test.jpg")
        rv = client.post(url, data=data, content_type="multipart/form-data")
        assert rv.status_code == 403
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.new_combo["name"]}
        )
        assert tmp_combo is None

    def test_add_success(self, client, admin):
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.new_combo["name"]}
        )
        assert tmp_combo is None
        url = URL_PREFIX + "/new"
        data = self.new_combo.copy()
        data["picture"] = (io.BytesIO(b"6724"), "test.jpg")
        rv = client.post(url, data=data, content_type="multipart/form-data")
        assert rv.status_code == 200
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.new_combo["name"]}, {"_id": 0}
        )
        tmp_image = db.IMAGE_COLLECTION.find_one(
            {"uuid": tmp_combo["picture"]}
        )["picture"]
        assert tmp_combo is not None
        assert tmp_image is not None
        assert tmp_combo == {
            "type": ObjectId("5dd681c44a608a104f899151"),
            "name": "好哦謝謝",
            "price": 70,
            "description": "",
            "content": [
                {
                    "id": ObjectId("5de35fc5fdb6b28d6100d776"),
                    "name": "鮮奶茶2",
                    "quantity": 10,
                },
                {
                    "id": ObjectId("5de22841f6bf2b651e091f6e"),
                    "name": "紅茶",
                    "quantity": 20,
                },
            ],
            "picture": tmp_combo["picture"],
            "sell":0,
        }

    def test_add_duplicate(self, client, admin):
        tmp_combo = list(
            db.COMBO_COLLECTION.find({"name": self.exist_combo["name"]})
        )
        assert len(tmp_combo) == 1
        url = URL_PREFIX + "/new"
        data = self.exist_combo.copy()
        data["picture"] = (io.BytesIO(b"6724"), "test.jpg")
        rv = client.post(url, data=data, content_type="multipart/form-data")
        # duplicate code : 409
        assert rv.status_code == 409
        tmp_combo = list(
            db.COMBO_COLLECTION.find({"name": self.exist_combo["name"]})
        )
        assert len(tmp_combo) == 1

    # delete combo
    def test_delete_unauthorized(self, client):
        # test there is a combo in collection
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.exist_combo["name"]}
        )
        assert tmp_combo is not None
        # test delete the exist combo anonymons
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps({"id": str(tmp_combo["_id"])}),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test there is a combo in collection
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.exist_combo["name"]}
        )
        assert tmp_combo is not None

    def test_delete_by_customer(self, client, customer):
        # test there is a combo in collection
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.exist_combo["name"]}
        )
        assert tmp_combo is not None
        # test delete the exist combo by customer
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps({"id": str(tmp_combo["_id"])}),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test there is a combo in collection
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.exist_combo["name"]}
        )
        assert tmp_combo is not None

    def test_delete_by_admin(self, client, admin):
        # test there is a combo in collection
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.exist_combo["name"]}
        )
        assert tmp_combo is not None
        # test delete the exist combo by boss
        url = URL_PREFIX + "/delete"
        rv = client.post(
            url,
            data=json.dumps({"id": str(tmp_combo["_id"])}),
            content_type="application/json",
        )
        assert rv.status_code == 200
        # test there is no combo which has been deleted in collection
        tmp_combo = db.COMBO_COLLECTION.find_one(
            {"name": self.exist_combo["name"]}
        )
        assert tmp_combo is None

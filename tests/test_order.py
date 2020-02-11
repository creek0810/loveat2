import json

from bson.objectid import ObjectId

from freezegun import freeze_time

from models import db


URL_PREFIX = "/api/order"


class TestOrder(object):
    new_order = {
        "takenAt": "2020-02-11T11:00",
        "notes": "不要番茄醬",
        "total": 600,
        "content": [
            {
                "id": "5dd67f098f0f6afb3ebc1b69",
                "category": "item",
                "quantity": 3,
            }
        ],
    }
    wrong_order = {
        "wrong_format": "2019-10-31T12:00",
        "notes": "不要番茄醬",
        "total": 600,
        "content": [
            {
                "id": "5dd67f098f0f6afb3ebc1b68",
                "category": "item",
                "quantity": 3,
            }
        ],
    }
    update_order_id = "5dd8f94ff5a90a5568400a57"
    update_nonexist_order_id = "6dd8f94ff5a90a5568400a57"

    @freeze_time("2020-02-10 10:00:00")
    def test_add_success(self, client, customer):
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps(self.new_order),
            content_type="application/json",
        )
        assert rv.status_code == 200

    @freeze_time("2020-02-10 10:00:00")
    def test_add_by_frozen(self, client, frozen):
        # test add api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps(self.new_order),
            content_type="application/json",
        )
        assert rv.status_code == 403

    @freeze_time("2020-02-10 10:00:00")
    def test_add_taken_past(self, client, customer):
        # test add api
        url = URL_PREFIX + "/new"
        cur_order = self.new_order.copy()
        cur_order["takenAt"] = "2020-02-08T11:00"
        rv = client.post(
            url, data=json.dumps(cur_order), content_type="application/json"
        )
        assert rv.status_code == 422

    @freeze_time("2020-02-10 10:00:00")
    def test_add_taken_not_in_business_interval(self, client, customer):
        # test add api
        url = URL_PREFIX + "/new"
        # change "takenAt" to the time that not in business interval
        cur_order = self.new_order.copy()
        cur_order["takenAt"] = "2020-02-11T23:00"
        rv = client.post(
            url, data=json.dumps(cur_order), content_type="application/json"
        )
        assert rv.status_code == 422

    @freeze_time("2020-02-10 10:00:00")
    def test_add_unauthorized(self, client):
        # test add api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps(self.new_order),
            content_type="application/json",
        )
        assert rv.status_code == 401

    @freeze_time("2020-02-10 10:00:00")
    def test_add_wrong_format(self, client, customer):
        # test add api
        url = URL_PREFIX + "/new"
        rv = client.post(
            url,
            data=json.dumps(self.wrong_order),
            content_type="application/json",
        )
        assert rv.status_code == 422

    # update order state
    def test_update_success(self, client, admin):
        # TODO: check when order is updated to "finish",
        #  then update the "sell" field of item and combo
        url = URL_PREFIX + "/update"
        state_enum = ["doing", "cancel", "finish", "end"]
        for state in state_enum:
            rv = client.post(
                url,
                data=json.dumps({"id": self.update_order_id, "state": state}),
                content_type="application/json",
            )
            assert rv.status_code == 200
            cur_state = db.ORDER_COLLECTION.find_one(
                {"_id": ObjectId(self.update_order_id)}, {"state": 1}
            )["state"]
            assert cur_state == state

    def test_update_unauthorized(self, client):
        # test update api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"id": self.update_order_id, "state": "cancel", "content": ""}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test if order update state
        cur_state = db.ORDER_COLLECTION.find_one(
            {"_id": ObjectId(self.update_order_id)}, {"state": 1}
        )["state"]
        assert cur_state == "unknown"

    def test_update_by_customer(self, client, customer):
        # test update api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"id": self.update_order_id, "state": "cancel", "content": ""}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 403
        # test if order update state
        cur_state = db.ORDER_COLLECTION.find_one(
            {"_id": ObjectId(self.update_order_id)}, {"state": 1}
        )["state"]
        assert cur_state == "unknown"

    def test_update_nonexist_order(self, client, admin):
        # test update api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {
                    "id": self.update_nonexist_order_id,
                    "state": "cancel",
                    "content": "",
                }
            ),
            content_type="application/json",
        )
        assert rv.status_code == 404

    def test_update_nonexist_state(self, client, admin):
        # test update api
        url = URL_PREFIX + "/update"
        rv = client.post(
            url,
            data=json.dumps(
                {"id": self.update_nonexist_order_id, "state": "i don't know"}
            ),
            content_type="application/json",
        )
        assert rv.status_code == 404

    # get todo order
    def test_get_todo_unauthorized(self, client):
        url = URL_PREFIX + "/todo"
        rv = client.get(url)
        assert rv.status_code == 403

    def test_get_todo_by_customer(self, client, customer):
        url = URL_PREFIX + "/todo"
        rv = client.get(url)
        assert rv.status_code == 403

    def test_get_todo_success(self, client, admin):
        url = URL_PREFIX + "/todo"
        rv = client.get(url)
        assert rv.status_code == 200
        assert json.loads(rv.data) == [
            {
                "_id": "5dd8f94ff5a90a5568400a58",
                "content": [
                    {"name": "起司豬排蛋吐司", "quantity": 2},
                    {"name": "原味蛋餅", "quantity": 2},
                    {"name": "火腿蛋吐司", "quantity": 3},
                    {"name": "培根蛋吐司", "quantity": 1},
                ],
                "notes": "吐司不加美乃滋",
                "orderID": 3,
                "phone": "0945678912",
                "state": "doing",
                "takenAt": "2019/11/23 17:18",
                "user_id": "5dde223874fbccb7319f4cb8",
            },
            {
                "_id": "5dd8f94ff5a90a5568400a59",
                "content": [{"name": "小熱狗(3根)", "quantity": 2}],
                "notes": "蛋半熟",
                "orderID": 4,
                "phone": "0920198409",
                "state": "finish",
                "takenAt": "2019/11/23 21:16",
                "user_id": "5dd8a604371301b428df5602",
            },
        ]

    # order history
    def test_search_raw_history_unauthorized(self, client):
        # test history api by anonymous
        url = URL_PREFIX + "/history"
        rv = client.get(url)
        assert rv.status_code == 403

    def test_search_raw_history_by_customer(self, client, customer):
        # test history api by customer
        url = URL_PREFIX + "/history"
        rv = client.get(url)
        assert rv.status_code == 403

    def test_search_raw_history(self, client, admin):
        # test history api by boss
        url = (
            URL_PREFIX + "/history?start=2019-12-09T01:01&end=2019-12-09T23:01"
        )  # noqa
        rv = client.get(url)
        assert rv.status_code == 200
        assert json.loads(rv.data) == [
            {
                "content": [{"name": "火腿蛋吐司", "quantity": 2}],
                "createdAt": "Sun, 08 Dec 2019 17:18:07 GMT",
                "notes": "吐司不加美乃滋",
                "orderID": "7",
            }
        ]

    def test_search_analysis_unauthorized(self, client):
        # test analysis history api by anonymous
        url = URL_PREFIX + "/analysis-data"
        rv = client.get(url)
        assert rv.status_code == 403

    def test_search_analysis_by_customer(self, client, customer):
        # test analysis history api by customer
        url = URL_PREFIX + "/analysis-data"
        rv = client.get(url)
        assert rv.status_code == 403

    def test_search_analysis_history(self, client, admin):
        # test analysis history api by boss
        url = (
            URL_PREFIX
            + "/analysis-data?start=2019-12-09T01:01&end=2019-12-09T23:01"
        )  # noqa
        rv = client.get(url)
        assert rv.status_code == 200
        print(json.loads(rv.data))
        assert json.loads(rv.data) == {
            "genderAnalysis": [
                {"female": 0, "male": 0, "total": 0},
                {"female": 1, "male": 0, "total": 1},
                {"female": 0, "male": 0, "total": 0},
                {"female": 0, "male": 0, "total": 0},
                {"female": 0, "male": 0, "total": 0},
                {"female": 0, "male": 0, "total": 0},
                {"female": 0, "male": 0, "total": 0},
            ],
            "interval": [
                "0-9",
                "10-19",
                "20-29",
                "30-39",
                "40-49",
                "50-59",
                "60+",
            ],
            "itemAnalysis": {
                "火腿蛋吐司": {
                    "female": [0, 2, 0, 0, 0, 0, 0],
                    "femaleTotal": 2,
                    "male": [0, 0, 0, 0, 0, 0, 0],
                    "maleTotal": 0,
                    "sum": [0, 2, 0, 0, 0, 0, 0],
                    "total": 2,
                }
            },
        }

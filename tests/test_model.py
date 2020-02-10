import datetime

from bson import ObjectId

from freezegun import freeze_time

from models import business_time, menu, order, user


class TestUserModel(object):
    def test_get_user_info(self, mockdb):
        tmp = list(user.get_user_info("5dd8a604371301b428df5602"))
        assert tmp == [
            {
                "_id": ObjectId("5dd8a604371301b428df5602"),
                "userName": "admin_name",
                "gender": "female",
                "phone": "0920198409",
                "email": "admin@gmail.com",
                "birth": datetime.datetime(1999, 11, 21, 23, 10, 42, 908000),
                "avatar": "64c4638b-b6ae-4335-80ec-1441e346b4e9",
                "state": "activate",
            }
        ]


class TestBusinessTimeModel(object):
    def test_get(self, mockdb):
        result = business_time.get()
        assert result == {
            "mon": {"start": "06:00", "end": "13:00"},
            "tue": {"start": "06:00", "end": "13:00"},
            "wed": {"start": "06:00", "end": "13:00"},
            "thu": {"start": "06:00", "end": "13:00"},
            "fri": {"start": "06:00", "end": "13:00"},
            "sat": {"start": "06:00", "end": "13:00"},
            "sun": {"start": "06:00", "end": "13:00"},
        }


class TestOrderModel(object):
    def test_get_unknown_order(self, mockdb):
        result = list(order.get_unknown_order())
        assert result == [
            {
                "_id": "5dd8f94ff5a90a5568400a57",
                "takenAt": datetime.datetime(2019, 11, 23, 18, 8, 7, 908000),
                "content": [
                    {"quantity": 1, "name": "鐵板麵套餐"},
                    {"quantity": 2, "name": "起司豬排蛋堡"},
                ],
                "notes": "漢堡加蛋",
            },
            {
                "_id": "5dd8f94ff5a90a5568400a5a",
                "takenAt": datetime.datetime(2019, 11, 23, 21, 30, 7, 954000),
                "content": [{"quantity": 2, "name": "火腿蛋吐司"}],
                "notes": "吐司不加美乃滋",
            },
        ]

    @freeze_time("2008-02-10 10:00:00")
    def test_get_not_end_by_username(self, mockdb):
        result = list(order.get_not_end_by_username("customer_name"))
        assert result == [
            {
                "_id": "5dd8f94ff5a90a5568400a57",
                "content": [
                    {"category": "combo", "name": "鐵板麵套餐", "quantity": 1},
                    {"category": "item", "name": "起司豬排蛋堡", "quantity": 2},
                ],
                "notes": "漢堡加蛋",
                "orderID": "2",
                "state": "unknown",
                "takenAt": "2019/11/23 18:08",
            },
            {
                "_id": "5dd8f94ff5a90a5568400a58",
                "content": [
                    {"category": "item", "name": "起司豬排蛋吐司", "quantity": 2},
                    {"category": "item", "name": "原味蛋餅", "quantity": 2},
                    {"category": "item", "name": "火腿蛋吐司", "quantity": 3},
                    {"category": "item", "name": "培根蛋吐司", "quantity": 1},
                ],
                "notes": "吐司不加美乃滋",
                "orderID": "3",
                "state": "doing",
                "takenAt": "2019/11/23 17:18",
            },
        ]


class TestTypeModel(object):
    def test_get_type(self, mockdb):
        result = menu.get_type(item=True, combo=True)
        assert result == [
            {"_id": "5dd678905f19051c7c4f0bb2", "name": "漢堡"},
            {"_id": "5dd678b95f19051c7c4f0bb3", "name": "吐司"},
            {"_id": "5dd678d05f19051c7c4f0bb4", "name": "蛋餅"},
            {"_id": "5dd67bf6e256197fec55f213", "name": "總匯"},
            {"_id": "5dd67d66f9725c676db6585c", "name": "輕食"},
            {"_id": "5dd67d66f9725c676db6585d", "name": "麵食"},
            {"_id": "5dd681c44a608a104f89914b", "name": "A餐"},
            {"_id": "5dd681c44a608a104f89914c", "name": "B餐"},
            {"_id": "5dd681c44a608a104f89914d", "name": "C餐"},
            {"_id": "5dd681c44a608a104f89914e", "name": "D餐"},
            {"_id": "5dd681c44a608a104f89914f", "name": "經典套餐"},
            {"_id": "5dd681c44a608a104f899150", "name": "活力套餐"},
            {"_id": "5dd681c44a608a104f899151", "name": "鐵板麵套餐"},
            {"_id": "5dd681c44a608a104f899152", "name": "招牌套餐"},
            {"_id": "5dd681c44a608a104f899153", "name": "兒童套餐"},
            {"_id": "5dd93c9a84e3f22bcb206f06", "name": "吐司套餐"},
            {"_id": "5dd93c9a84e3f22bcb206f07", "name": "輕食套餐"},
            {"_id": "5dd93c9a84e3f22bcb206f08", "name": "漢堡套餐"},
            {"_id": "5dd93c9a84e3f22bcb206f09", "name": "歡樂套餐"},
            {"_id": "5dd93c9a84e3f22bcb206f0a", "name": "養生套餐"},
            {"_id": "5dd9429ae10e8d1d0b6b2aea", "name": "果醬吐司"},
            {"_id": "5de22978558c6ebb84d05c14", "name": "未分類(套餐)"},
            {"_id": "5de2298f558c6ebb84d05c17", "name": "未分類(單品)"},
            {"_id": "5de236555ac223853943397b", "name": "滿福堡"},
            {"_id": "5de35bb170a5892250dfdc6c", "name": "飲料"},
            {"_id": "5de35d6370a5892250dfdc6f", "name": "超值套餐"},
            {"_id": "5de3cf61eea6ba4eee57c137", "name": "testType"},
        ]

import json

URL_PREFIX = "/api/menu/"


class TestMenu(object):
    menu_test = [
        {"category": "combo", "content": [], "type": "經典套餐"},
        {"category": "combo", "content": [], "type": "活力套餐"},
        {
            "category": "combo",
            "content": [
                {
                    "_id": "5dda567d09d84aa89699121c",
                    "content": [
                        {"name": "黑胡椒鐵板麵", "quantity": 1},
                        {"name": "小熱狗(3根)", "quantity": 1},
                        {"name": "紅茶", "quantity": 1},
                    ],
                    "description": "",
                    "name": "鐵板麵套餐",
                    "picture": "06dcc1d4-90aa-4ba9-8758-6de813bc5fa4",
                    "price": 70,
                    'top': True,
                },
                {
                    "_id": "5dda567d09d84aa89699121a",
                    "content": [
                        {"name": "黑胡椒鐵板麵", "quantity": 1},
                        {"name": "紅茶", "quantity": 1},
                    ],
                    "description": "",
                    "name": "鐵板麵套餐(無熱狗)",
                    "picture": "a9e7793c-02c4-4697-a14f-0f4c8a6d175a",
                    "price": 70,
                    'top': True,
                },
            ],
            "type": "鐵板麵套餐",
        },
        {"category": "combo", "content": [], "type": "招牌套餐"},
    ]

    # get menu
    def test_list_menu_unauthorized(self, client):
        # test history api by anonymous
        rv = client.get(URL_PREFIX)
        assert rv.status_code == 200
        assert json.loads(rv.data)[15:19] == self.menu_test

    def test_list_menu_by_customer(self, client, customer):
        # test history api by anonymous
        rv = client.get(URL_PREFIX)
        assert rv.status_code == 200
        assert json.loads(rv.data)[15:19] == self.menu_test

    def test_list_menu_by_admin(self, client, admin):
        # test history api by anonymous
        rv = client.get(URL_PREFIX)
        assert rv.status_code == 200
        assert json.loads(rv.data)[15:19] == self.menu_test

    # get item detail
    def test_get_item_success(self, client):
        url = URL_PREFIX + "item"
        rv = client.post(
            url,
            data=json.dumps(["5dd67f098f0f6afb3ebc1b69"]),
            content_type = "application/json",
        )
        assert rv.status_code == 200
        assert json.loads(rv.data) == [
            {"_id": "5dd67f098f0f6afb3ebc1b69", "name": "奶茶", "price": 20}
        ]

    # get combo detail
    """ can't execute, because mongomock doesn't support $map
    def test_get_combo_success(self, client):
        url = URL_PREFIX + "combo"
        rv = client.post(
            url,
            data=json.dumps(["5dda567d09d84aa89699121c"]),
            content_type="application/json",
        )
        assert rv.status_code == 200
        assert json.loads(rv.data) == [
            {"_id": "5dd67f098f0f6afb3ebc1b69", "name": "奶茶", "price": 20}
        ]
    """

import json
import os

from bson.json_util import loads

import main

import mongomock

import pytest


FILE_DIR = os.path.dirname(__file__)


def establish_order(cur_client):
    dir = os.path.join(FILE_DIR, "data/order.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.order
        colletion.insert_many(data)
        return colletion
    return None


def establish_item(cur_client):
    dir = os.path.join(FILE_DIR, "data/item.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.item
        colletion.insert_many(data)
        return colletion
    return None


def establish_business_time(cur_client):
    dir = os.path.join(FILE_DIR, "data/businessTime.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.businessTime
        colletion.insert_many(data)
        return colletion
    return None


def establish_user(cur_client):
    dir = os.path.join(FILE_DIR, "data/user.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.user
        colletion.insert_many(data)
        return colletion
    return None


def establish_type(cur_client):
    dir = os.path.join(FILE_DIR, "data/type.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.type
        colletion.insert_many(data)
        return colletion
    return None


def establish_image(cur_client):
    dir = os.path.join(FILE_DIR, "data/image.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.image
        colletion.insert_many(data)
        return colletion
    return None


def establish_combo(cur_client):
    dir = os.path.join(FILE_DIR, "data/combo.json")
    with open(dir, "r", encoding="utf-8") as file:
        data = loads(file.read())
        colletion = cur_client.combo
        colletion.insert_many(data)
        return colletion
    return None


@pytest.fixture(scope="function")
def client(monkeypatch):
    cur_client = mongomock.MongoClient().db
    monkeypatch.setattr(
        "models.db.USER_COLLECTION", establish_user(cur_client)
    )
    monkeypatch.setattr(
        "models.db.ORDER_COLLECTION", establish_order(cur_client)
    )
    monkeypatch.setattr(
        "models.db.ITEM_COLLECTION", establish_item(cur_client)
    )
    monkeypatch.setattr(
        "models.db.TYPE_COLLECTION", establish_type(cur_client)
    )
    monkeypatch.setattr(
        "models.db.IMAGE_COLLECTION", establish_image(cur_client)
    )
    monkeypatch.setattr(
        "models.db.COMBO_COLLECTION", establish_combo(cur_client)
    )
    monkeypatch.setattr(
        "models.db.BUSINESS_COLLECTION", establish_business_time(cur_client)
    )

    return main.app.test_client()


@pytest.fixture(scope="function")
def mockdb(monkeypatch):
    cur_client = mongomock.MongoClient().db
    monkeypatch.setattr(
        "models.db.USER_COLLECTION", establish_user(cur_client)
    )
    monkeypatch.setattr(
        "models.db.ORDER_COLLECTION", establish_order(cur_client)
    )
    monkeypatch.setattr(
        "models.db.ITEM_COLLECTION", establish_item(cur_client)
    )
    monkeypatch.setattr(
        "models.db.TYPE_COLLECTION", establish_type(cur_client)
    )
    monkeypatch.setattr(
        "models.db.IMAGE_COLLECTION", establish_image(cur_client)
    )
    monkeypatch.setattr(
        "models.db.COMBO_COLLECTION", establish_combo(cur_client)
    )
    monkeypatch.setattr(
        "models.db.BUSINESS_COLLECTION", establish_business_time(cur_client)
    )


@pytest.fixture(scope="function")
def customer(client):
    info = {"userName": "customer_name", "password": "123456789"}
    yield client.post(
        "/api/user/login",
        data=json.dumps(info),
        content_type="application/json",
    )
    client.get("/user/logout")


@pytest.fixture(scope="function")
def admin(client):
    info = {"userName": "admin_name", "password": "123456789"}
    yield client.post(
        "/api/user/login",
        data=json.dumps(info),
        content_type="application/json",
    )
    client.get("/user/logout")


@pytest.fixture(scope="function")
def frozen(client):
    info = {"userName": "frozen_account", "password": "123456789"}
    yield client.post(
        "/api/user/login",
        data=json.dumps(info),
        content_type="application/json",
    )
    client.get("/user/logout")

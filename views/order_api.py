from datetime import datetime

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from lib import push
from lib.auth import admin_required

from models import order, user

order_api = Blueprint("order_api", __name__)
push.init()


@order_api.route("/history", methods=["GET"])
@admin_required
def history():
    args = request.args
    start = datetime.strptime(args.get("start"), "%Y-%m-%dT%H:%M")
    end = datetime.strptime(args.get("end"), "%Y-%m-%dT%H:%M")
    print("=============================")
    return jsonify(list(order.get_raw_history(start, end)))


@order_api.route("/analysis-data", methods=["GET"])
@admin_required
def analysis_data():
    args = request.args
    start = datetime.strptime(args.get("start"), "%Y-%m-%dT%H:%M")
    end = datetime.strptime(args.get("end"), "%Y-%m-%dT%H:%M")
    return jsonify(order.get_analysis_data(start, end))


@order_api.route("/new", methods=["POST"])
@login_required
def add_order():
    data = request.get_json()
    data["userName"] = current_user.name
    try:
        if order.add_order(data):
            return "", 200
        else:
            return "", 422
    except KeyError:
        return "", 422


@order_api.route("/update", methods=["POST"])
@admin_required
def update_order_state():
    data = request.get_json()
    user_name = order.update_state(data)
    message = {
        "doing": {"title": "訂單已接受", "content": "老闆已接受您的訂單"},
        "cancel": {"title": "訂單被拒絕", "content": "抱歉，老闆拒絕了您的訂單"},
        "finish": {"title": "訂單已完成", "content": "餐點已製作完成，請儘速來取餐"},
    }
    if user_name:
        token = user.get_token_by_username(user_name)["token"]
        if data["state"] in message:
            push.send_to_customer(token, message[data["state"]])
        return "", 200
    else:
        return "", 404

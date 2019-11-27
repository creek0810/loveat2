from datetime import datetime

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from lib.auth import admin_required

from models import order

order_api = Blueprint('order_api', __name__)


@order_api.route('/history', methods=["GET"])
@admin_required
def history():
    args = request.args
    start = datetime.strptime(args.get('start'), '%Y-%m-%dT%H:%M')
    end = datetime.strptime(args.get('end'), '%Y-%m-%dT%H:%M')
    return jsonify(list(order.get_raw_history(start, end)))


@order_api.route('/analysis-data', methods=["GET"])
@admin_required
def analysis_data():
    args = request.args
    start = datetime.strptime(args.get('start'), '%Y-%m-%dT%H:%M')
    end = datetime.strptime(args.get('end'), '%Y-%m-%dT%H:%M')
    return jsonify(order.get_analysis_data(start, end))


@order_api.route('/new', methods=["POST"])
@login_required
def add_order():
    data = request.get_json()
    data['userName'] = current_user.name
    try:
        if order.add_order(data):
            return "", 200
        else:
            return "", 422
    except KeyError:
        return "", 422

from datetime import datetime

from flask import Blueprint, jsonify, request

from models import order

order_api = Blueprint('order_api', __name__)


@order_api.route('/history', methods=["GET"])
def history():
    args = request.args
    start = request.args.get('start')
    start = datetime.strptime(args.get('start'), '%Y-%m-%dT%H:%M')
    end = datetime.strptime(args.get('end'), '%Y-%m-%dT%H:%M')
    return jsonify(order.get(start, end))

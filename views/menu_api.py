from flask import Blueprint, jsonify

from models import menu

menu_api = Blueprint('menu_api', __name__)


@menu_api.route('/', methods=["GET"])
def get_menu():
    return jsonify(menu.get_all())

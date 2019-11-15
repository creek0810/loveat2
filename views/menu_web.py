from flask import Blueprint

menu_web = Blueprint('menu_web', __name__)


@menu_web.route('/', methods=["GET"])
def menu():
    return "menu"


@menu_web.route('/edit', methods=["GET"])
def edit_menu():
    return "edit menu"


@menu_web.route('/item/new', methods=["GET"])
def new_item():
    return "new item"


@menu_web.route('/item/<id>/edit', methods=["GET"])
def edit_item(id):
    return "edit item"


@menu_web.route('/combo/new', methods=["GET"])
def new_combo():
    return "new combo"


@menu_web.route('/combo/<id>/edit', methods=["GET"])
def edit_combo(id):
    return "edit combo"

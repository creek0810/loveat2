from flask import Blueprint, render_template
from flask_login import login_required, current_user
from lib.auth import admin_required
from datetime import datetime,timedelta



order_web = Blueprint("order_web", __name__)

time_format = '%Y-%m-%dT%H:%M'

@order_web.route("/new", methods=["GET"])
def cart():
    return "cart"


@order_web.route("/history", methods=["GET"])
def history():
    return render_template('history.html', auth=current_user.role, name=current_user.name, begin = (datetime.now() - timedelta(days = 7)).strftime(time_format), end = datetime.now().strftime(time_format))


@order_web.route("/pending", methods=["GET"])
def pending():
    return "pending"


@order_web.route("/todo", methods=["GET"])
def todo():
    return "todo"


@order_web.route("/state", methods=["GET"])
def state():
    return "state"

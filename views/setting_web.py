from flask import Blueprint

setting_web = Blueprint('setting_web', __name__)


@setting_web.route('/business-time', methods=["GET"])
def business_time():
    return "business time"

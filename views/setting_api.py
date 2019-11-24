from flask import Blueprint, request

from lib.auth import admin_required

from models import business_time

setting_api = Blueprint('setting_api', __name__)


@setting_api.route('/business-time', methods=["POST"])
@admin_required
def update_business_time():
    data = request.get_json()
    try:
        business_time.update(data)
        return "", 200
    except KeyError:
        return "", 400

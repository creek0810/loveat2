from datetime import datetime

from config import SECRET_KEY

from dateutil.relativedelta import relativedelta

from flask import Blueprint, request

from flask_login import login_user

from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer

from lib import send_email
from lib.auth import User

from models import user


user_api = Blueprint("user_api", __name__)


@user_api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    id = user.validate_user(data, password=True)
    if id:
        login_user(User(id))
        return "", 200
    else:
        return "", 401


@user_api.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        data["birth"] = datetime.now() - relativedelta(years=data["age"])
        data["role"] = "customer"
        if user.add(data):
            return "", 200
        else:
            return "", 409
    except KeyError:
        return "", 400


@user_api.route("/password/forget", methods=["POST"])
def forget_password():
    data = request.get_json()
    id = user.validate_user(data, email=True)
    if id:
        s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
        token = s.dumps({"reset_id": str(id)})
        send_email.send_forget_password_email(
            data["email"],
            "https://loveat2.appspot.com/user/password/reset/{token}".format(
                token=token.decode()
            ),
        )
        return "", 200
    else:
        return "", 401


@user_api.route("/password/reset/<token>", methods=["POST"])
def reset_password(token):
    try:
        s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=3600)
        id = s.loads(token)["reset_id"]
        password = request.get_json()["password"]
        user.update_password(id, password)
        return "", 200
    except SignatureExpired:
        return "", 401

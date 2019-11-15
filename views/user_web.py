from flask import Blueprint

user_web = Blueprint('user_web', __name__)


@user_web.route('/logout', methods=["GET"])
def logout():
    return "logout"


@user_web.route('/password/reset', methods=["GET"])
def reset_password():
    return "reset password"


@user_web.route('/password/forget', methods=["GET"])
def forget_password():
    return "forget password"


@user_web.route('/profile/<id>', methods=["GET"])
def profile(id):
    return "profile"

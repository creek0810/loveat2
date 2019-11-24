from functools import wraps

from flask import abort

from flask_login import (
    AnonymousUserMixin,
    LoginManager,
    UserMixin,
    current_user,
)

from models import user


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.role = "anonymous"
        self.name = "anonymous"
        self.id = "anonymous"

    def get_role(self):
        return self.role


class User(UserMixin):
    def __init__(self, id):
        result = user.find(id)
        self.id = id
        self.name = result["userName"]
        self.role = result["role"]

    def get_role(self):
        return self.role


login_manager = LoginManager()
login_manager.anonymous_user = Anonymous


@login_manager.user_loader
def user_loader(id):
    return User(id)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrap

import config

from flask import Flask

from lib.auth import login_manager

from views import (
    menu_api,
    menu_web,
    order_api,
    order_web,
    setting_api,
    setting_web,
    user_api,
    user_web,
)


def register_web(app):
    app.register_blueprint(menu_web.menu_web, url_prefix='/menu')
    app.register_blueprint(order_web.order_web, url_prefix='/order')
    app.register_blueprint(user_web.user_web, url_prefix='/user')
    app.register_blueprint(setting_web.setting_web, url_prefix='/setting')


def register_api(app):
    app.register_blueprint(menu_api.menu_api, url_prefix='/api/menu')
    app.register_blueprint(order_api.order_api, url_prefix='/api/order')
    app.register_blueprint(setting_api.setting_api, url_prefix='/api/setting')
    app.register_blueprint(user_api.user_api, url_prefix='/api/user')


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    login_manager.init_app(app)
    register_api(app)
    register_web(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run("127.0.0.1", port=8080)

# project/__init__.py

import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_principal import Principal

#config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

#initializing extensions
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app)
mail = Mail(app)
db = SQLAlchemy(app)
Bootstrap(app)
Principal(app)

#blueprints
from project.main.views import main_blueprint
from project.user.views import user_blueprint
from project.coin.views import coin_blueprint
from project.wallet.views import wallet_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(coin_blueprint)
app.register_blueprint(wallet_blueprint)

# flask-login

from project.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# error handlers
@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500


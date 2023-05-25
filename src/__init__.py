from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
login_manager = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)


app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.app_context().push()
bcrypt = Bcrypt(app)
# login_manager.login_view = "login_page"
# login_manager.login_message_category = "info"
# from market import routes

from src import routers
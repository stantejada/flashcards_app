from flask import Flask
from config import Development
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
migrate = Migrate(app, db=db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models



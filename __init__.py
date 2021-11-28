from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

from config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['DEBUG'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,'profile_pics')
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
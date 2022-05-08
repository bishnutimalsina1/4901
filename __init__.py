from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail
from config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'timely4901@gmail.com'
app.config['MAIL_PASSWORD'] = 'Timely4901!$'
mail = Mail(app)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['DEBUG'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,'profile_pics')
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
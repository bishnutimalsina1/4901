import flask_bcrypt
from flask import render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import pymysql
from __init__ import create_app
from models import *

app = create_app('dev')

debug = True


class create_user_form(FlaskForm):
    first_name = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'First Name'})
    last_name = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg','placeholder': 'Last Name'})
    email = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg','placeholder': 'Email'})
    business_name = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg','placeholder': 'Business Name'})
    password = PasswordField(
        validators=[InputRequired(), Length(min=6)],
        render_kw={'class': 'form-control form-control-lg','placeholder': 'Password'})
    submit = SubmitField(
        "Sign Up",
        render_kw={'class': 'register_input'})

    def validate_username(self, email):
        user = UserInfo.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Username already exists, please choose a different one or login if you already have an account")


@app.route('/')
def home():  # put application's code here
    user_data = UserInfo.query.all()
    for user in user_data:
        print(user.first_name)
    debug = True
    return render_template('index.html', user_data=user_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    from flask import request
    form = create_user_form()
    debug = True
    if form.validate_on_submit():
        passwd = flask_bcrypt.generate_password_hash(form.password.data)
        user = UserInfo(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        username=form.username.data,
                        password=passwd)
        db.session.add(user)
        db.session.commit()
        debug = True
        return redirect('/')
    else:
        flash(form.errors)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()

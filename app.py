import bcrypt
import flask_bcrypt
from flask import render_template, url_for, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import pymysql
from __init__ import create_app
from models import *

app = create_app('dev')
login_manager = LoginManager()
login_manager.init_app(app)

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
    business_type= SelectField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form control-lg'}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=6)],
        render_kw={'class': 'form-control form-control-lg','placeholder': 'Password'})
    submit = SubmitField(
        "Sign Up",
        render_kw={'class': 'register_input'})

    def validate_email(self, email):
        user = Business.query.filter_by(email=email.data).first()
        debug=True
        if user:
            raise ValidationError(
                "Username already exists, please choose a different one or login if you already have an account")

class loginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'Email'})
    password = PasswordField(
        validators=[InputRequired(), Length(min=6)],
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'Password'})
    submit = SubmitField(
        "Login",
        render_kw={'class': 'register_input'})
    def validate_password(self,password,):
        user = UserInfo.query.filter_by(email=self.email.data).first()
        if user:
            if not bcrypt.checkpw(password.data.encode('utf-8'),user.password.encode('utf-8')):
                raise ValidationError('Incorrect Username or Password')
        else:
            raise ValidationError('Incorrect Username or Password')

@app.route('/')
def home():  # put application's code here
    user_data = UserInfo.query.all()
    for user in user_data:
        print(user.first_name)
    debug = True
    return render_template('index.html', user_data=user_data)


@app.route('/dashboard')
def dashboard():  # put application's code here
    user_data = UserInfo.query.all()
    for user in user_data:
        print(user.first_name)
    debug = True
    return render_template('about.html', user_data=user_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    from flask import request
    business_type_opts = BusinessType.query.all()
    choices = [

    ]
    form = create_user_form()

    for opt in business_type_opts:
        choices.append((opt.id,opt.description))
    form.business_type.choices = choices
    if form.validate_on_submit():
        business_type = form.business_type.data
        business_name = form.business_name.data
        passwd = flask_bcrypt.generate_password_hash(form.password.data)
        business = Business(name=form.business_name.data,
                            type=form.business_type.data,
                            phone=None,
                            email=form.email.data,
                            description=None)
        db.session.add(business)
        db.session.commit()
        business_id = db.engine.execute(f'select id from business where name in ("{form.business_name.data}"); ').fetchone()
        print(business_id['id'])
        user = UserInfo(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=passwd,
                        business=business_id['id'])
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        flash(form.errors)

    return render_template('register.html', form=form)

@login_manager.user_loader
def load_user(id):
    return UserInfo.query.filter_by(id=id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user = UserInfo.query.filter_by(email=email).first()
        debug=True
        login_user(user)
        return render_template('index.html')
    return render_template('login.html',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()

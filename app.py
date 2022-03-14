import bcrypt
import flask_bcrypt
import flask_login
from flask import render_template, url_for, redirect, flash, session, request, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, DecimalField, \
    FileField
from wtforms.validators import InputRequired, Length, ValidationError, Optional
import time
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import pymysql
from werkzeug.utils import secure_filename
from __init__ import create_app
import os
from uuid import uuid4
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
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'Last Name'})
    email = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'Email'})
    business_name = StringField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'Business Name'})
    business_type = SelectField(
        validators=[InputRequired()],
        render_kw={'class': 'form-control form control-lg'}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=6)],
        render_kw={'class': 'form-control form-control-lg', 'placeholder': 'Password'})
    submit = SubmitField(
        "Sign Up",
        render_kw={'class': 'register_input'})

    def validate_email(self, email):
        user = UserInfo.query.filter_by(email=email.data).first()
        debug = True
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

    def validate_password(self, password, ):
        user = UserInfo.query.filter_by(email=self.email.data).first()
        if user:
            if not bcrypt.checkpw(password.data.encode('utf-8'), user.password.encode('utf-8')):
                raise ValidationError('Incorrect Username or Password')
        else:
            raise ValidationError('Incorrect Username or Password')


class contractorProfileForm(FlaskForm):
    first_name = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    last_name = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    user_description = TextAreaField(
        render_kw={'class': 'form-control form-control-lg'})
    salary = IntegerField(
        validators=[Optional()],
        render_kw={'class': 'form-control form-control-lg'})
    employment_type = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    experience = IntegerField(
        validators=[Optional()],
        render_kw={'class': 'form-control form-control-lg'})
    email = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    phone = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    city = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    state = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    skills = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    twitter_link = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    facebook_link = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    website_link = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    profile_picture = FileField(
        render_kw={'class': 'form-control form-control-lg'})
    submit = SubmitField(
        "Update"
    )


class businessProfileForm(FlaskForm):
    business_name = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    business_description = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    business_needs = StringField(
        render_kw={'class': 'form-control form-control-lg'})
    contractor_type = SelectField(
        render_kw={'class': 'form-control form-control-lg'})
    submit = SubmitField(
        "Update"
    )


@app.route('/')
def home():  # put application's code here
    user_data = UserInfo.query.all()
    # for user in user_data:
    #     print(user.first_name)
    # jobs = db.engine.execute(f'''select * from jobs where user_id = 57''').fetchall()
    debug = True
    return render_template('index.html', user_data=user_data)


@app.route('/dashboard')
@login_required
def dashboard():  # put application's code here

    user_data = db.engine.execute(f'''select * from user_profile where user_id = {current_user.id}''')

    # job_data = db.engine.execute(f'''select * from jobs
    #                                  join business b on b.id = jobs.business_id
    #                                  where is_active = 'T' and user_id = {current_user.id}''').fetchall()
    job_data = db.engine.execute(f'''select * from jobs ''').fetchall()
    job_data = [dict(u) for u in job_data]
    debug = True
    events = [
        {
            'todo': 'Plumbing',
            'date': '2022-02-01'
        },
        {
            'todo': 'Tap',
            'date': '2022-02-03',
            'end': '2022-02-04'
        },
        {
            'todo': 'Finishing',
            'date': '2022-02-06T12:30:00',
        }
    ]
    return render_template('dashboard.html', events=events, user_data=user_data, job_data=job_data)


@app.route('/dashboard/projects')
@login_required
def projects():  # put application's code here

    user_data = db.engine.execute(f'''select * from user_profile where user_id = {current_user.id}''')

    project_data = db.engine.execute(f'''select * from projects
                                     join business b on b.id = projects.business_id
                                     where is_approved = 0 and user_id = {current_user.id}''').fetchall()
    job_data = db.engine.execute(f'''select * from projects ''').fetchall()
    job_data = [dict(u) for u in job_data]

    return render_template('projects.html', user_data=user_data, job_data=job_data, project_data=project_data)


@app.route('/addTask', methods=['POST'])
@login_required
def addTask():
    task_name = request.form.get('task_name')
    start_time = request.form.get('eventstarttime')
    start_date = request.form.get('eventstartdate')
    end_time = request.form.get('eventendtime')
    end_date = request.form.get('eventenddate')
    progress = request.form.get('progress')
    color = request.form.get('exampleColorInput')
    start = start_date + ' ' + start_time + ":00"
    end = end_date + ' ' + end_time + ":00"
    user_id = request.form.get('user_id')


    db.engine.execute(text('''insert into jobs
         (job_title, job_description, job_hourly_pay, business_id, user_id, job_required_skills, is_active, is_complete, job_started_on, job_complete_on, progress, color)
         values (:job_title, :job_description, :job_hourly_pay, :business_id, :user_id, :job_required_skills, :is_active, :is_complete, :job_started_on, :job_complete_on,:progress, :color)
         '''), job_title=task_name, job_description="", job_hourly_pay=10, business_id=user_id, user_id=user_id, job_required_skills="", is_active='T', is_complete='F', job_started_on=start, job_complete_on=end, progress=progress, color=color)
    return redirect(url_for('dashboard'))

@app.route('/editTask', methods=['POST'])
@login_required
def addTask():

    task_name = request.form.get('task_name')
    start_time = request.form.get('eventstarttime')
    start_date = request.form.get('eventstartdate')
    end_time = request.form.get('eventendtime')
    end_date = request.form.get('eventenddate')
    progress = request.form.get('progress')
    color = request.form.get('exampleColorInput')
    start = start_date + ' ' + start_time + ":00"
    end = end_date + ' ' + end_time + ":00"
    user_id = request.form.get('user_id')


    db.engine.execute(text('''insert into jobs
         (job_title, job_description, job_hourly_pay, business_id, user_id, job_required_skills, is_active, is_complete, job_started_on, job_complete_on, progress, color)
         values (:job_title, :job_description, :job_hourly_pay, :business_id, :user_id, :job_required_skills, :is_active, :is_complete, :job_started_on, :job_complete_on,:progress, :color)
         '''), job_title=task_name, job_description="", job_hourly_pay=10, business_id=user_id, user_id=user_id, job_required_skills="", is_active='T', is_complete='F', job_started_on=start, job_complete_on=end, progress=progress, color=color)
    return redirect(url_for('dashboard'))


@app.route('/customer_dashboard')
@login_required
def customer_dashboard():  # put application's code here
    user_data = db.engine.execute(f'''select * from user_profile up
                                       join user_info ui on ui.id = up.user_id
                                       join business b on b.id = up.business
                                       where b.business_type = 1;''').fetchall()
    user_data = [dict(u) for u in user_data]

    for user in user_data:
        if user['profile_picture_path']:
            user['profile_pic'] = os.path.join(app.config['UPLOAD_FOLDER'], user['profile_picture_path'])
    debug = True
    return render_template('customer_dashboard.html', user_data=user_data)


@app.route('/profile_pics/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/hire', methods=['POST'])
@login_required
def hire_contractor():
    contractor_id = int(request.form.get('contractor_id'))
    # username = request.form.get('username')
    c_user_id = request.form.get('user_id')
    # print("contId: " + str(contractor_id))
    # print("c_Id: " + str(c_user_id))
    # print("username: " + str(username))
    db.engine.execute(text('''insert into projects 
         (business_id, user_id) 
         values (:business_id, :user_id)
         '''), business_id=contractor_id, user_id=c_user_id)
    return redirect(url_for('customer_dashboard'))


@app.route('/approve', methods=['GET', 'POST'])
@login_required
def approve_request():
    project_id = request.form.get('project_id')
    user_id = request.form.get('user_id')
    business_id = request.form.get('business_id')
    project = Projects.query.filter_by(project_id=project_id).first()

    if request.method == 'POST':
        if project:
            db.session.delete(project)
            db.session.commit()

            db.engine.execute(text('''insert into projects 
                     (project_id, user_id, business_id, is_approved) 
                     values (:project_id, :user_id, :business_id, :is_approved)
                     '''), project_id=project_id, user_id=user_id, business_id=business_id, is_approved=1)

    return redirect(url_for('projects'))


@app.route('/user_profile/<id>', methods=['GET', 'POST'])
@login_required
def user_profile(id):
    debug = True
    # if id != session['_user_id']:
    #     return redirect(url_for('home'))
    user_data = dict(db.engine.execute(f'''select * from user_profile up
                                    join user_info ui on ui.id = up.user_id
                                    join business b on b.id = up.business   
                                    where up.user_id in("{id}"); ''').fetchone())

    if user_data['business_type'] == '1':
        contractor_form = contractorProfileForm()
        if contractor_form.validate_on_submit():
            ## Assign form data to variables
            email = contractor_form.email.data
            city = contractor_form.city.data
            employment_type = contractor_form.employment_type.data
            facebook_link = contractor_form.facebook_link.data
            phone = contractor_form.phone.data
            salary = contractor_form.salary.data
            skills_description = contractor_form.skills.data
            state = contractor_form.state.data
            twitter_link = contractor_form.twitter_link.data
            first_name = contractor_form.first_name.data
            last_name = contractor_form.last_name.data
            website_link = contractor_form.website_link.data
            user_description = contractor_form.user_description.data
            experience = contractor_form.experience.data
            profile_picture = contractor_form.profile_picture.data
            file_ext = uuid4().__str__()
            file = profile_picture
            if file.filename == '':
                profile_update = UserProfile.query.filter_by(user_id=id).update(
                    dict(user_description=user_description,
                         salary=salary,
                         experience_years=experience,
                         employment_type=employment_type,
                         phone=phone,
                         city=city,
                         state=state,
                         twitter_link=twitter_link,
                         facebook_link=facebook_link,
                         website_link=website_link,
                         skills_description=skills_description))
            else:
                filename = secure_filename(file.filename)
                unique_filename = f'{file_ext}_{filename}'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                profile_update = UserProfile.query.filter_by(user_id=id).update(
                    dict(user_description=user_description,
                         salary=salary,
                         experience_years=experience,
                         employment_type=employment_type,
                         phone=phone,
                         city=city,
                         state=state,
                         twitter_link=twitter_link,
                         facebook_link=facebook_link,
                         website_link=website_link,
                         skills_description=skills_description,
                         profile_picture_path=unique_filename if 'profile_picture' in request.files else None,
                         profile_picture_filename=filename if 'profile_picture' in request.files else None))

            user_update = UserInfo.query.filter_by(id=id).update(dict(first_name=first_name,
                                                                      last_name=last_name,
                                                                      email=email))
            db.session.commit()
        user_data = dict(db.engine.execute(f'''select * from user_profile up
                                           join user_info ui on ui.id = up.user_id
                                           join business b on b.id = up.business   
                                           where up.user_id in("{id}"); ''').fetchone())
        # print(contractor_form.errors)
        ## set form data to pre-existing data if exists
        contractor_form.email.data = user_data['email'] if user_data['email'] else None
        contractor_form.city.data = user_data['city'] if user_data['city'] else None
        contractor_form.employment_type.data = user_data['employment_type'] if user_data['employment_type'] else None
        contractor_form.experience.data = user_data['experience_years'] if user_data['experience_years'] else None
        contractor_form.facebook_link.data = user_data['facebook_link'] if user_data['facebook_link'] else None
        contractor_form.phone.data = user_data['phone'] if user_data['phone'] else None
        contractor_form.salary.data = user_data['salary'] if user_data['salary'] else None
        contractor_form.skills.data = user_data['skills_description'] if user_data['skills_description'] else None
        contractor_form.state.data = user_data['state'] if user_data['state'] else None
        contractor_form.twitter_link.data = user_data['twitter_link'] if user_data['twitter_link'] else None
        contractor_form.first_name.data = user_data['first_name'] if user_data['first_name'] else None
        contractor_form.last_name.data = user_data['last_name'] if user_data['last_name'] else None
        contractor_form.website_link.data = user_data['website_link'] if user_data['website_link'] else None
        contractor_form.user_description.data = user_data['user_description'] if user_data['user_description'] else None
        contractor_form.profile_picture.data = user_data['profile_picture_path'] if user_data[
            'profile_picture_path'] else None

    else:
        contractor_form = None
    # if not user_data:
    #     return redirect(url_for('home'))
    # current_id= user_data.id
    debug = True
    return render_template('profile.html', user_data=user_data, contractor_form=contractor_form)


@app.route('/business_profile/<id>', methods=['GET', 'POST'])
@login_required
def business_profile(id):
    if id != session['_user_id']:
        return redirect(url_for('home'))
    contractor_type_opts = db.engine.execute(f'''select * from business_categories''').fetchall()
    contractor_type_opts = [dict(c) for c in contractor_type_opts]
    business_data = db.engine.execute(f'''select * from business_profile bp
                                        join user_info ui on ui.business = bp.business_id
                                        join business b on b.id = bp.business_id
                                        where ui.id in ("{id}")''').fetchone()
    if business_data:
        business_data = dict(business_data)
    choices = []
    for opt in contractor_type_opts:
        choices.append((opt['id'], opt['description']))
    if business_data['business_type'] == '2':
        business_form = businessProfileForm()
        business_form.contractor_type.choices = choices
        if business_form.validate_on_submit():
            business_name = business_form.business_name.data
            business_description = business_form.business_description.data
            business_needs = business_form.business_needs.data
            contractor_type = business_form.contractor_type.data

            profile_update = BusinessProfile.query.filter_by(business_id=business_data['business_id']).update(
                dict(business_description=business_description,
                     business_needs=business_needs,
                     contractor_type=contractor_type)
            )
            business_update = Business.query.filter_by(id=business_data['business_id']).update(
                dict(business_name=business_name)
            )
            db.session.commit()

            business_data = dict(db.engine.execute(f'''select * from business_profile bp
                                                    join user_info ui on ui.business = bp.business_id
                                                    join business b on b.id = bp.business_id
                                                    where ui.id in ("{id}")''').fetchone())
        contractor_select = dict(db.engine.execute(
            f'''select description, id from business_categories where id ={business_data['business_type']}''').fetchone())
        business_form.business_name.data = business_data['business_name']
        business_form.business_description.data = business_data['business_description']
        business_form.business_needs.data = business_data['business_needs']
        business_form.contractor_type.data = contractor_select['id']

    else:
        business_form = None

    return render_template('business_profile.html', business_form=business_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    from flask import request
    business_type_opts = BusinessType.query.all()
    choices = [

    ]
    form = create_user_form()

    for opt in business_type_opts:
        choices.append((opt.id, opt.description))
    form.business_type.choices = choices
    if form.validate_on_submit():
        business_type = form.business_type.data
        business_name = form.business_name.data
        passwd = flask_bcrypt.generate_password_hash(form.password.data)
        business = Business(business_name=form.business_name.data,
                            business_type=form.business_type.data,
                            phone=None,
                            email=form.email.data,
                            description=None)
        db.session.add(business)
        db.session.commit()
        business_id = db.engine.execute(
            f'select id,business_type from business where business_name in ("{form.business_name.data}") and business_type in ("{form.business_type.data}"); ').fetchone()
        # print(business_id['id'])
        user = UserInfo(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=passwd,
                        business=business_id['id'],
                        business_type=business_id['business_type'])

        db.session.add(user)
        db.session.commit()
        user_id = db.engine.execute(
            f'select id, business_type from user_info where email in ("{form.email.data}");').fetchone()
        if user_id['business_type'] == 1:
            user_profile = UserProfile(user_id=user_id['id'],
                                       business=business_id['id'])
            db.session.add(user_profile)
            db.session.commit()

        elif user_id['business_type'] == 2:
            business_profile = BusinessProfile(user_id=user_id['id'],
                                               business_id=business_id['id'])
            db.session.add(business_profile)
            db.session.commit()
        login_user(user)
        return redirect('/')
    else:
        flash(form.errors)

    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(id):
    return UserInfo.query.filter_by(id=id).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserInfo.query.filter_by(email=email).first()
        debug = True
        login_user(user)
        return render_template('index.html')
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()

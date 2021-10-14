from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import pymysql
from Timely.__init__ import create_app, db

app = create_app('dev')

debug=True
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(45))
    last_name = db.Column(db.VARCHAR(45))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

@app.route('/')
def hello_world():  # put application's code here
    user_data = UserInfo.query.all()
    for user in user_data:
        print(user.first_name)
    debug=True
    return render_template('index.html', user_data=user_data)


if __name__ == '__main__':
    app.run()

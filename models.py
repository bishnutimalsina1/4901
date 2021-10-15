from __init__ import db

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(45))
    last_name = db.Column(db.VARCHAR(45))
    username = db.Column(db.VARCHAR(45), nullable=False)
    password = db.Column(db.VARCHAR(300), nullable=False)

    def __init__(self, first_name, last_name,username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

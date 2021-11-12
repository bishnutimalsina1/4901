from __init__ import db


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(45))
    last_name = db.Column(db.VARCHAR(45))
    email = db.Column(db.VARCHAR(45), nullable=False)
    password = db.Column(db.VARCHAR(300), nullable=False)
    business = db.Column(db.Integer)
    business_type = db.Column(db.Integer)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, first_name, last_name, email, password, business, business_type):
        self.first_name = first_name or None
        self.last_name = last_name or None
        self.email = email or None
        self.password = password or None
        self.business = business or None
        self.business_type = business_type or None


class BusinessType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR)
    description = db.Column(db.VARCHAR)

    def __init__(self, title, description):
        self.title = title or None
        self.description = description or None


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    phone = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    description = db.Column(db.VARCHAR)
    type = db.Column(db.VARCHAR)

    def __init__(self, name, phone, email, description, type):
        self.name = name or None
        self.phone = phone or None
        self.email = email or None
        self.description = description or None
        self.type = type or None

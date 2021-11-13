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


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    business = db.Column(db.Integer)
    user_description = db.Column(db.VARCHAR)
    salary = db.Column(db.Integer)
    pay_frequency = db.Column(db.VARCHAR)
    experience_years = db.Column(db.Integer)
    employment_type = db.Column(db.VARCHAR)
    phone = db.Column(db.VARCHAR)
    city = db.Column(db.VARCHAR)
    state = db.Column(db.VARCHAR)
    twitter_link = db.Column(db.VARCHAR)
    facebook_link = db.Column(db.VARCHAR)
    website_link = db.Column(db.VARCHAR)
    skills_description = db.Column(db.VARCHAR)
    profile_picture_path = db.Column(db.VARCHAR)

    def __init__(self, id, user_id, business, user_description, salary, pay_frequency, experience_years,
                 employment_type,
                 phone, city, state, twitter_link, facebook_link, website_link, skills_description,
                 profile_picture_path):
        self.id = id or None
        self.user_id = user_id or None
        self.business = business or None
        self.user_description = user_description or None
        self.salary = salary or None
        self.pay_frequency = pay_frequency or None
        self.experience_years = experience_years or None
        self.employment_type = employment_type or None
        self.phone = phone or None
        self.city = city or None
        self.state = state or None
        self.twitter_link = twitter_link or None
        self.facebook_link = facebook_link or None
        self.website_link = website_link or None
        self.skills_description = skills_description or None
        self.profile_picture_path = profile_picture_path or None
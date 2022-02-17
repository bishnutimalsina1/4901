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
    business_name = db.Column(db.VARCHAR)
    business_phone = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    description = db.Column(db.VARCHAR)
    type = db.Column(db.VARCHAR)

    def __init__(self, business_name, phone, email, description, type):
        self.business_name = business_name or None
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
    profile_picture_filename = db.Column(db.VARCHAR)

    def __init__(self, user_id=None, business=None, user_description=None, salary=None, pay_frequency=None,
                 experience_years=None,
                 employment_type=None,
                 phone=None, city=None, state=None, twitter_link=None, facebook_link=None, website_link=None,
                 skills_description=None,
                 profile_picture_path=None, profile_picture_filename=None):
        self.user_id = user_id
        self.business = business
        self.user_description = user_description
        self.salary = salary
        self.pay_frequency = pay_frequency
        self.experience_years = experience_years
        self.employment_type = employment_type
        self.phone = phone
        self.city = city
        self.state = state
        self.twitter_link = twitter_link
        self.facebook_link = facebook_link
        self.website_link = website_link
        self.skills_description = skills_description
        self.profile_picture_path = profile_picture_path
        self.profile_picture_filename = profile_picture_filename

class BusinessProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    business_description = db.Column(db.VARCHAR)
    business_needs = db.Column(db.VARCHAR)
    contractor_type = db.Column(db.Integer)
    profile_picture_filename = db.Column(db.VARCHAR)

    def __init__(self, business_id=None, user_id=None, business_description=None, business_needs=None, contractor_type=None, profile_picture_filename=None):
        self.business_id = business_id
        self.user_id = user_id
        self.business_description = business_description
        self.business_needs = business_needs
        self.contractor_type = contractor_type
        self.profile_picture_filename = profile_picture_filename

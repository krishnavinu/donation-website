from datetime import datetime
from decimal import Decimal
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('donor', 'volunteer', 'admin', 'ngo'), default='donor')
    reward_points = db.Column(db.Integer, default=0)
    
    # Relationships
    donations = db.relationship('Donation', backref='user', lazy=True)
    pickup_requests = db.relationship('PickupRequest', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)

class NGO(db.Model):
    __tablename__ = 'ngos'
    ngo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    location = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    donations = db.relationship('Donation', backref='ngo', lazy=True)
    requests = db.relationship('Request', backref='ngo', lazy=True)

class Donation(db.Model):
    __tablename__ = 'donations'
    donation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.ngo_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2))
    type = db.Column(db.String(50))  # monetary or goods
    status = db.Column(db.String(50))
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)

class PickupRequest(db.Model):
    __tablename__ = 'pickup_requests'
    pickup_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.ngo_id'), nullable=False)
    address = db.Column(db.Text)
    pickup_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    items = db.Column(db.Text)  # JSON string containing item details

    ngo = db.relationship('NGO', backref='pickup_requests')

class Request(db.Model):
    __tablename__ = 'requests'
    request_id = db.Column(db.Integer, primary_key=True)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.ngo_id'), nullable=False)
    type = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    needed_by = db.Column(db.DateTime) 

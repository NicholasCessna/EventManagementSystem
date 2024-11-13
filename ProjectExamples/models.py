#!!!! When done coding, run in terminal: git status, git add ., git commit -m "message", git push origin master to commit to the repo
# Next time start a new codespace to get everyones commited changes. Youre active codespace wont update with the other members changes without starting a new codespace
# Dont forget to set up a new codespace adding python extension and "pip install"ing missing packages

# Model Logic for creating Database
# Install packages "pip install Flask" && "pip install flask-sqlalchemy"
# models.py
# models.py
# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    signups = db.relationship('SignUp', back_populates='event', cascade="all, delete-orphan")
    organizer = db.relationship('User', back_populates='organized_events')

    @classmethod
    def get_all_upcoming(cls):
        today = datetime.today().date()
        return cls.query.filter(cls.date >= today).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Event {self.name} on {self.date} at {self.time} in {self.location}>"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    organized_events = db.relationship('Event', back_populates='organizer', cascade="all, delete-orphan")
    signups = db.relationship('SignUp', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"

class SignUp(db.Model):
    __tablename__ = 'signups'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    event = db.relationship('Event', back_populates='signups')
    user = db.relationship('User', back_populates='signups')

    @classmethod
    def is_signed_up(cls, event_id, user_id):
        return cls.query.filter_by(event_id=event_id, user_id=user_id).first() is not None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<SignUp Event ID: {self.event_id}, User ID: {self.user_id}>"

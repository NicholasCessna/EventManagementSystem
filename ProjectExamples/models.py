#!!!! When done coding, run in terminal: git status, git add ., git commit -m "message", git push origin master to commit to the repo
# Next time start a new codespace to get everyones commited changes. Youre active codespace wont update with the other members changes without starting a new codespace
# Dont forget to set up a new codespace adding python extension and "pip install"ing missing packages

# Model Logic for creating Database
# Install packages "pip install Flask" && "pip install flask-sqlalchemy"
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()

# Setup configuration for SQLite
DATABASE_URI = 'sqlite:///event_app.db'  # Connects to our SQLite database

# Define Classes for database models

# Class for an event
class Event(db.Model):
    # Naming the table
    __tablename__ = 'events'
    # Defining columns for the Event table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Allowable string length specified as String(100)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)
    location = db.Column(db.String(100), nullable = False)
    # One-to-many relationship with SignUp
    signups = db.relationship('SignUp', back_populates='event', cascade="all, delete-orphan")
    
    # This method helps during debugging by returning info about an Event instance
    def __repr__(self):
        return f"<Event {self.name} on {self.date} at {self.time} in {self.location}>"
    
    
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    signups = db.relationship('SignUp', back_populates='user', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# Class to represent the sign-up, linking an user to an event
class SignUp(db.Model):
    __tablename__ = 'signups'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to link to the Event table
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    # Foreign key to link to the user table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Relationships to access Event and user objects
    event = db.relationship('Event', back_populates='signups')
    user = db.relationship('User', back_populates='signups')
    
    def __repr__(self):
        return f"<SignUp Event ID: {self.event_id}, User ID: {self.user_id}>"
    
    
    
    
    
    

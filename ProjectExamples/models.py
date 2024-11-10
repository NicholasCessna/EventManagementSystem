# Model Logic for creating Database
# Install packages "pip install Flask" && "pip install flask-sqlalchemy"
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy 

# Initialize SQLAlchemy
db = SQLAlchemy()

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
    description = db.Column(db.String(200), nullable=True)
    # One-to-many relationship with SignUp
    signups = db.relationship('SignUp', back_populates='event', cascade="all, delete-orphan")
    
    # This method helps during debugging by returning info about an Event instance
    def __repr__(self):
        return f"<Event {self.name}>"

# Class for an attendee of an event
class Attendee(db.Model):
    __tablename__ = 'attendees'
    # Columns for the Attendee table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Nullable=False specifies that this field is required
    email = db.Column(db.String(100), nullable=False, unique=True)  # Unique=True enforces unique email addresses
    # One-to-many relationship with SignUp
    signups = db.relationship('SignUp', back_populates='attendee', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Attendee {self.name}>"

# Class to represent the sign-up, linking an attendee to an event
class SignUp(db.Model):
    __tablename__ = 'signups'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to link to the Event table
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    # Foreign key to link to the Attendee table
    attendee_id = db.Column(db.Integer, db.ForeignKey('attendees.id'), nullable=False)
    # Relationships to access Event and Attendee objects
    event = db.relationship('Event', back_populates='signups')
    attendee = db.relationship('Attendee', back_populates='signups')
    
    def __repr__(self):
        return f"<SignUp Event ID: {self.event_id}, Attendee ID: {self.attendee_id}>"
    
    
    
    
    
    

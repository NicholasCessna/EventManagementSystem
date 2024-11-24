# controllers.py
from flask_login import login_user, logout_user
from models import db, Event, User, SignUp
from datetime import datetime

class UserController:
    @staticmethod
    def login_user_controller(username, password):
        user = User.find_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return True
        return False
    
    @staticmethod
    def logout_user_controller():
        logout_user()
    
    @staticmethod
    def register_user(username, password, email, name, role):
        user = User(username=username, email=email, name=name, role=role)
        user.set_password(password)
        user.save()
        return user
    
    @staticmethod
    def get_user_info(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def update_user_profile(user_id, name, email):
        user = User.query.get(user_id)
        user.name = name
        user.email = email
        user.save()
    
    @staticmethod
    def check_password(user_id, password):
        user = User.query.get(user_id)
        return user.check_password(password)
    
    @staticmethod
    def change_password(user_id, password):
        user = User.query.get(user_id)
        user.set_password(password)
        user.save()
        
        
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user.role == 'event_creator':
            events = Event.query.filter_by(organizer_id=user_id).all()
            for event in events:
                event.delete()
        user.delete()
        
    @staticmethod
    def get_user_type(user_id):
        user = User.query.get(user_id)
        return user.role
    

class EventController:
    @staticmethod
    def add_event(name, description, date, time, location, organizer_id):
        new_event = Event(name=name, description=description, date=date, time=time, location=location, organizer_id=organizer_id)
        new_event.save()
    
class EventController:
    @staticmethod
    def get_all_events():
        return Event.get_all_upcoming()

    @staticmethod
    def get_event(event_id):
        return Event.query.get(event_id)
    
    @staticmethod
    def search_events(query):
        return Event.query.filter(
            Event.name.contains(query) | Event.description.contains(query)
        ).order_by(Event.date, Event.time)
    
    @staticmethod
    def get_user_events(user_id):
        return Event.query.filter_by(organizer_id=user_id).all()
    
    @staticmethod
    def delete_event(event_id):
        event = Event.query.get(event_id)
        event.delete()
        
    @staticmethod
    def edit_event(event_id, name, description, date_str, time_str, location):
        event = Event.query.get(event_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        # Strip seconds if present
        if len(time_str) > 5:
            time_str = time_str[:5]
        time = datetime.strptime(time_str, '%H:%M').time()
        event.edit(name, description, date, time, location)
        

class SignUpController:
    @staticmethod
    def add_sign_up(event_id, user_id):
        if not SignUp.is_signed_up(event_id, user_id):
            sign_up = SignUp(event_id=event_id, user_id=user_id)
            sign_up.save()
            return "Signed up successfully"
        return "Already signed up"

    @staticmethod
    def check_for_signup(event_id, user_id):
        return SignUp.is_signed_up(event_id, user_id)

    @staticmethod
    def get_signups_for_event(event_id):
        event = Event.query.get(event_id)
        return event.signups if event else None
    
    @staticmethod
    def get_events_for_user(user_id):
        signups = SignUp.query.filter_by(user_id=user_id).all()
        events = [Event.query.get(signup.event_id) for signup in signups]
        return events
    
    @staticmethod
    def remove_sign_up(event_id, user_id):
        signup = SignUp.query.filter_by(event_id=event_id, user_id=user_id).first()
        if signup:
            signup.delete()
            return "Unsign successful"
        return "Not signed up"

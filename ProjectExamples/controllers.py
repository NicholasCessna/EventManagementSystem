# controllers.py
from flask_login import login_user, logout_user
from models import db, Event, User, SignUp

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

class EventController:
    @staticmethod
    def add_event(name, description, date, time, location, organizer_id):
        new_event = Event(name=name, description=description, date=date, time=time, location=location, organizer_id=organizer_id)
        new_event.save()
    
    @staticmethod
    def get_all_events():
        return Event.get_all_upcoming()

    @staticmethod
    def get_event(event_id):
        return Event.query.get(event_id)

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

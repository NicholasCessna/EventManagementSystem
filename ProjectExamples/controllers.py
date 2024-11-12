from flask_login import login_user, logout_user
from models import db, Event, User, SignUp



class UserController:
    
    def login_user_controller(username, password):
        user=User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return True
        return False    
    
    def logout_user_controller():
        logout_user()
    
    def register_user(username,password,email,name,account_type):
        user = User(username=username, email=email, name=name, account_type=account_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_user_info(user_id):
        user = User.query.get(user_id)
        return user


class EventController:

    def add_event(name, description, date, time, location):
        new_event = Event(name=name, description = description, date=date, time=time, location=location)
        db.session.add(new_event)
        db.session.commit()
    
    def get_all_events():
        return Event.query.all()

    def get_event(event_id):
        return Event.query.get(event_id)



class SignUpController:
    
    def add_sign_up(event_id, user_id):
        check = SignUp.query.filter_by(event_id=event_id, user_id=user_id).first() is not None
        if  not check:
            sign_up = SignUp(event_id=event_id, user_id=user_id)
            db.session.add(sign_up)
            db.session.commit()
        else:    
            return "You are already signed up for this event"
        

    def check_for_signup(event_id,user_id) -> bool:
        return SignUp.query.filter_by(event_id=event_id, user_id=user_id).first() is not None

    def get_signups_for_event(event_id):
        event = Event.query.get(event_id)
        return event.signups if event else None
    


from flask_login import login_user, logout_user
from models import db, Event, User, SignUp

def add_event(name, description, date, time, location):
    new_event = Event(name=name, description = description, date=date, time=time, location=location)
    db.session.add(new_event)
    db.session.commit()
    
def register_user(username,password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def login_user_controller(username, password):
    user=User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return True
    return False

def logout_user_controller():
    logout_user()
    
def add_sign_up(event_id, user_id):
    #add logic to prevent multiple signups
    #is_signed_up = check_for_signup(event_id, user_id)
    #if (!is_signed_up):
    sign_up = SignUp(event_id=event_id, user_id=user_id)
    db.session.add(sign_up)
    db.session.commit()
    
def get_all_events():
    return Event.query.all()

def get_event(event_id):
    return Event.query.get(event_id)

# def check_for_signup(event_id,user_id):
#     return SignUp.query.filter_by(event_id=event_id, user_id=user_id).first()

def get_signups_for_event(event_id):
    event = Event.query.get(event_id)
    return event.signups if event else None


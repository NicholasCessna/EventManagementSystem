from models import db, Event, Attendee, SignUp

# Get all events from the database
def get_all_events():
    return Event.query.all()

# Retrieve a specific event byID
def get_event(event_id):
    return Event.query.get(event_id)

# Add an event to a database
def add_event(name, description=""):
    # Create a new event instance
    new_event = Event(name = name, description = description)
    # Command to add new event instance to database
    db.session.add(new_event)
    db.session.commit()
    
# Same as add event    
def add_attendee(name, email):
    attendee = Attendee(name=name, email=email)
    db.session.add(attendee)
    db.session.commit()
    return attendee

# same as others creating an instance, adding it to the database, and committing it
def add_sign_up(event_id, attendee_id):
    sign_up = SignUp(event_id = event_id, attendee_id = attendee_id)
    db.session.add(sign_up)
    db.session.commit()
    
# Returning a list of event signups for an event    
def get_signups_for_event(event_id):
    # Query an event by the event_id
    event = Event.query.get(event_id)
    # return all signups for that id
    return event.signups if event else None
    
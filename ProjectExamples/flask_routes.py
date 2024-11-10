# flask_routes.py
from flask import render_template, request, redirect, url_for
from controllers import get_all_events, get_event, add_attendee, add_sign_up, get_signups_for_event, add_event

def register_routes(app):
    # Route to display all events
    @app.route('/')
    def events():
        events = get_all_events()
        return render_template('events.html', events=events)
    
    
    @app.route('/event/<int:event_id>/add_attendee', methods=['GET', 'POST'])
    def add_attendee_route(event_id):
        event = get_event(event_id)
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            attendee = add_attendee(name, email)
            add_sign_up(event_id, attendee.id)  # Link attendee to event
            return redirect(url_for('view_signups', event_id=event_id))
        return render_template('add_attendee.html', event=event)

    # Route to display form for adding a new event
    @app.route('/add_event', methods=['GET', 'POST'])
    def add_event_route():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form.get('description', '')
            add_event(name, description)
            return redirect(url_for('events'))
        return render_template('add_event.html')  # GET request shows form

    # Route to display a sign-up page for a specific event
    @app.route('/event/<int:event_id>/signup')
    def signup_page(event_id):
        event = get_event(event_id)
        if event:
            return render_template('signup.html', event=event)
        return "Event not found", 404

    # Route to handle form submission for signing up to an event
    @app.route('/event/<int:event_id>/signup', methods=['POST'])
    def signup(event_id):
        name = request.form['name']
        email = request.form['email']
        attendee = add_attendee(name, email)
        add_sign_up(event_id, attendee.id)
        return redirect(url_for('view_signups', event_id=event_id))

    # Route to view all sign-ups for a specific event
    @app.route('/event/<int:event_id>/signups')
    def view_signups(event_id):
        event = get_event(event_id)
        signups = get_signups_for_event(event_id)
        return render_template('view_signups.html', event=event, signups=signups)

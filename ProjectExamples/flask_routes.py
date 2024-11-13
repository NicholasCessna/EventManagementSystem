# flask_routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers import UserController, EventController, SignUpController
from datetime import datetime

def register_routes(app):
    
    @app.route('/')
    def events():
        events = EventController.get_all_events()
        event_signup_status = {}
        if current_user.is_authenticated:
            for event in events:
                event_signup_status[event.id] = SignUpController.check_for_signup(event.id, current_user.id)
        return render_template('events.html', events=events, event_signup_status=event_signup_status)

    @app.route('/event/<int:event_id>')
    def event_detail(event_id):
        event = EventController.get_event(event_id)
        signup_status = False
        if current_user.is_authenticated:
            signup_status = SignUpController.check_for_signup(event_id, current_user.id)
        return render_template('event_detail.html', event=event, signup_status=signup_status)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            name = request.form['name']
            role = request.form['role']
            if UserController.get_user_info(username):
                flash('Username already exists')
                return redirect(url_for('register'))
            UserController.register_user(username, password, email, name, role)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if UserController.login_user_controller(username, password):
                flash('Logged in successfully!')
                return redirect(url_for('events'))
            flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        UserController.logout_user_controller()
        flash('Logged out successfully')
        return redirect(url_for('events'))

    @app.route('/add_event', methods=['GET', 'POST'])
    @login_required
    def add_event_route():
        if current_user.role != 'event_creator':  # Ensure only event creators can access
            flash("You don't have permission to add events.")
            return redirect(url_for('events'))

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            date_str = request.form['date']
            time_str = request.form['time']
            location = request.form['location']
            
            # Parse date and time inputs
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
            
            # Call EventController to add event with the organizer ID
            EventController.add_event(name, description, date, time, location, current_user.id)
            flash('Event added successfully!')
            return redirect(url_for('events'))
        return render_template('add_event.html')

    @app.route('/event/<int:event_id>/signup', methods=['GET', 'POST'])
    @login_required
    def signup(event_id):
        if request.method == 'POST':
            message = SignUpController.add_sign_up(event_id, current_user.id)
            flash(message)
            return redirect(url_for('event_detail', event_id=event_id))
        event = EventController.get_event(event_id)
        return render_template('signup.html', event=event)

# flask_routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from controllers import get_all_events, get_event, add_sign_up, add_event, register_user, login_user_controller, logout_user_controller 
from models import User
from datetime import datetime

def register_routes(app):
    # Route to display all events public (Landing Page)
    @app.route('/')
    def events():
        events = get_all_events()
        return render_template('events.html', events=events)
    
    
    @app.route('/register', methods = ['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username = username).first():
                flash('Username Already Exists')
                return redirect(url_for('register'))
            register_user(username, password)
            flash('Registration Successful! Please log in.')
            return redirect(url_for('login'))
        return render_template('register.html')
    
    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if login_user_controller(username, password):
                flash('Logged in successfully!')
                return redirect(url_for('events'))
            flash('Invalid Username or Password')
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        logout_user_controller()
        flash('Logged out successfully')
        return redirect(url_for('events'))
    

    @app.route('/add_event', methods=['GET', 'POST'])
    def add_event_route():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            # Convert date and time strings to Python date and time objects
            date_str = request.form['date']
            time_str = request.form['time']
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert to date object
            time = datetime.strptime(time_str, '%H:%M').time()      # Convert to time object
            location = request.form['location']
            # Add the event to the database
            add_event(name, description, date, time, location)
            return redirect(url_for('events'))
        return render_template('add_event.html')

    # Route to display a sign-up page for a specific event
    @app.route('/event/<int:event_id>/signup', methods = ['GET', 'POST'])
    @login_required
    def signup(event_id):
        event = get_event(event_id)
        if request.method == 'POST':
            add_sign_up(event_id, current_user.id)
            flash('You successfully Signed Up for the event')
            return redirect(url_for('events'))
        return render_template('signup.html',event=event)
            



    
    

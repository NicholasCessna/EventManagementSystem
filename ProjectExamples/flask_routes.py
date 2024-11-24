# flask_routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers import UserController, EventController, SignUpController
from datetime import datetime

def register_routes(app):
    
    @app.route('/', methods=['GET', 'POST'])
    def events():
        page = request.args.get('page', 1, type=int)
        per_page = 20

        search_query = request.form.get('search') if request.method == 'POST' else None
        events_query = EventController.search_events(search_query) if search_query else EventController.get_all_events()

        # Paginate the events query
        pagination = events_query.paginate(page=page, per_page=per_page)

        event_signup_status = {}
        if current_user.is_authenticated:
            for event in pagination.items:
                event_signup_status[event.id] = SignUpController.check_for_signup(event.id, current_user.id)

        return render_template(
            'events.html',
            events=pagination.items,
            event_signup_status=event_signup_status,
            prev_page=pagination.prev_num if pagination.has_prev else None,
            next_page=pagination.next_num if pagination.has_next else None
        )



    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        if request.method == 'POST':
            if 'update_profile' in request.form:
                name = request.form.get('name')
                email = request.form.get('email')
                UserController.update_user_profile(current_user.id, name, email)
                flash('Your profile has been updated')
            elif 'change_password' in request.form:
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')
                if not UserController.check_password(current_user.id, old_password):
                    flash('Incorrect password')
                elif new_password != confirm_password:
                    flash('Passwords do not match')
                else:
                    UserController.change_password(current_user.id, new_password)
                    flash('Password changed successfully')
            elif 'delete_account' in request.form:
                UserController.delete_user(current_user.id)
                logout()
                flash('Your account has been deleted')
                return redirect(url_for('events'))
            return redirect(url_for('profile')) 
           
        if UserController.get_user_type(current_user.id) == 'attendee':
            events_for_user = SignUpController.get_events_for_user(current_user.id)
            return render_template('profile.html', user=current_user, events_for_user=events_for_user)
        
        elif UserController.get_user_type(current_user.id) == 'event_creator':
            events_for_user = SignUpController.get_events_for_user(current_user.id)
            created_events = EventController.get_user_events(current_user.id)
            return render_template('profile.html', user=current_user, events_for_user=events_for_user, created_events=created_events)
                        
                        
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

    @app.route('/event/<int:event_id>/delete', methods=['POST'])
    @login_required
    def delete_event(event_id):
        EventController.delete_event(event_id)
        flash('Event deleted successfully')
        return redirect(url_for('profile'))
    
    @app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_event(event_id):
        if request.method == 'POST':
            EventController.edit_event(event_id, request.form['name'], request.form['description'], request.form['date'], request.form['time'], request.form['location'])
            flash('Event edited successfully')
            return redirect(url_for('profile'))
        else:
            event = EventController.get_event(event_id)
            return render_template('edit_event.html', event=event)
    
    

    @app.route('/event/<int:event_id>/unsign', methods=['POST'])
    @login_required
    def unsign_event(event_id):
        message = SignUpController.remove_sign_up(event_id, current_user.id)
        flash(message)
        return redirect(url_for('profile'))
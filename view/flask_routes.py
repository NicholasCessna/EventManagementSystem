# flask_routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.controllers import UserController, EventController, SignUpController
from utils.email_verifier import EmailVerifier
from datetime import datetime

def register_routes(app):
    
    @app.route('/', methods=['GET', 'POST'])
    def events():
        page = request.args.get('page', 1, type=int)
        per_page = 20

        search_query = request.form.get('search') if request.method == 'POST' else None
        events_query = EventController.search_events(search_query) if search_query else EventController.get_all_events()

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
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                email = request.form.get('email')

                UserController.update_user_profile(current_user.id, first_name, last_name, email)
                flash('Your profile has been updated.', 'success')
            elif 'change_password' in request.form:
                old_password = request.form.get('old_password')
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                if not UserController.check_password(current_user.id, old_password):
                    flash('Incorrect password.', 'error')
                elif new_password != confirm_password:
                    flash('Passwords do not match.', 'error')
                else:
                    UserController.change_password(current_user.id, new_password)
                    flash('Password changed successfully.', 'success')
            elif 'delete_account' in request.form:
                UserController.delete_user(current_user.id)
                logout()
                flash('Your account has been deleted.', 'success')
                return redirect(url_for('events'))
            return redirect(url_for('profile'))

        events_for_user = SignUpController.get_events_for_user(current_user.id)
        created_events = []
        if UserController.get_user_type(current_user.id) == 'event_creator':
            created_events = EventController.get_user_events(current_user.id)

        return render_template(
            'profile.html',
            user=current_user,
            events_for_user=events_for_user,
            created_events=created_events,
        )

                        
                        
                        
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
            try:
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                username = request.form['username']
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                email = request.form['email']
                role = request.form['role']
                registration_code = request.form.get('registration_code')

                if password != confirm_password:
                    flash('Passwords do not match', 'error')
                    return redirect(url_for('register'))

                if UserController.get_user_info(username):
                    flash('Username already exists', 'error')
                    return redirect(url_for('register'))

                if UserController.get_user_by_email(email):
                    flash('Email is already registered', 'error')
                    return redirect(url_for('register'))

                if not EmailVerifier.verify(email):
                    flash('Email verification failed.', 'error')
                    return redirect(url_for('register'))

                UserController.register_user(username, password, email, first_name, last_name, role, registration_code)
                flash('Registration successful! Please log in.')
                return redirect(url_for('login'))
            except Exception as e:
                flash('An error occurred during registration.', 'error')
                print(f"Error: {e}")
                return redirect(url_for('register'))
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
        if current_user.role != 'event_creator':
            flash("You don't have permission to add events.")
            return redirect(url_for('events'))

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            date_str = request.form['date']
            time_str = request.form['time']
            location = request.form['location']
            image = request.files.get('image')
            
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()

            EventController.add_event(name, description, date, time, location, current_user.id, image)

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
        event = EventController.get_event(event_id)

        if request.method == 'POST':
            # Collect form data
            name = request.form['name']
            description = request.form['description']
            date_str = request.form['date']
            time_str = request.form['time']
            location = request.form['location']
            remove_image = request.form.get('remove_image', None) == "yes"
            image = request.files.get('image')

            EventController.edit_event(event_id, name, description, date_str, time_str, location, image, remove_image)
            flash('Event updated successfully!')
            return redirect(url_for('profile'))

        return render_template('edit_event.html', event=event)
    
    

    @app.route('/event/<int:event_id>/unsign', methods=['POST'])
    @login_required
    def unsign_event(event_id):
        message = SignUpController.remove_sign_up(event_id, current_user.id)
        flash(message)
        return redirect(url_for('profile'))

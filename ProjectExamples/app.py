from flask import Flask
from models import db, DATABASE_URI, User
from flask_routes import register_routes
from flask_login import LoginManager

# Creates base to run flask app
app = Flask(__name__)
app.secret_key = '12345'


#Configure the SQLite database URI 
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Tie database and app together
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create db tables before first db instance is made
with app.app_context():
    db.create_all()

    
# register routes from flask routes  
register_routes(app)


if __name__ == '__main__':
    app.run(debug = True)
    
    
    



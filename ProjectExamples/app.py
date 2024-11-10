from flask import Flask
from models import db, DATABASE_URI
from flask_routes import register_routes

# Creates base to run flask app
app = Flask(__name__)


#Configure the SQLite database URI 
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Tie database and app together
db.init_app(app)

# Create db tables before first db instance is made
with app.app_context():
    db.create_all()

    
# register routes from flask routes  
register_routes(app)


if __name__ == '__main__':
    app.run(debug = True)
    
    
    



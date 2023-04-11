from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Dorm, User, Rating, Vote

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zjzeoxah:LV11ax-kxElV7gDmQ7SnoywqoL5kH5dO@lallah.db.elephantsql.com/zjzeoxah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Add your Flask app routes and other code below

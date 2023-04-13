from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Dorm, User, Rating, Vote
from models.user import User
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zjzeoxah:LV11ax-kxElV7gDmQ7SnoywqoL5kH5dO@lallah.db.elephantsql.com/zjzeoxah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Add your Flask app routes and other code below






#db (connect to db here)

@app.route("/register-user", methods=["POST"])
def register_client():
    user = User(
        request.form["logeuser"], request.form["logemail"], request.form["logpass"])
    )
   # db.insert(user.__dict__) sudo code changes depending on the database we use
    return 

@app.route("/login", methods=["POST"])
def login():
    logemail = request.form["logemail"]
    logpass = request.form["logpass"]
    user = info.find_one({"email": logemail, "password": logpass})
    if user:
        return "logged in"
    else:
        return "try again"

if __name__ == "__main__":
    app.run(debug=True)

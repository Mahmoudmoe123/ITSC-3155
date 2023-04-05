from datetime import datetime
from flask_login import UserMixin
from app import db, login_manger

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Dorm model
class Dorm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    ratings = db.relationship('Rating', backref='dorm', lazy='dynamic')

    def __repr__(self):
        return '<Dorm {}>'.format(self.name)

# Rating model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dorm_id = db.Column(db.Integer, db.ForeignKey('dorm.id'))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Rating {}>'.format(self.id)

    def upvote(self):
        self.upvotes += 1

    def downvote(self):
        self.downvotes += 1

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
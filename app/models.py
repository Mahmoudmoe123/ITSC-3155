from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dorm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String)
    maps_url = db.Column(db.String)

    ratings = db.relationship('Rating', backref='dorm', lazy=True)

    def __repr__(self):
        return f'<Dorm {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    ratings = db.relationship('Rating', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dorm_id = db.Column(db.Integer, db.ForeignKey('dorm.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)

    votes = db.relationship('Vote', backref='rating', lazy=True)

    def __repr__(self):
        return f'<Rating {self.id} by User {self.user_id} for Dorm {self.dorm_id}>'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vote_type = db.Column(db.Enum('upvote', 'downvote', name='vote_types'), nullable=False)

    def __repr__(self):
        return f'<Vote {self.vote_type} by User {self.user_id} for Rating {self.rating_id}>'

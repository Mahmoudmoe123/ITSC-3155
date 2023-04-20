from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, User, Dorm, Rating, Vote
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dorm_rating.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('ratings'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('signin.html')

@app.route('/dorms')
def dorms():
    all_dorms = Dorm.query.all()
    return render_template('dorms.html', dorms=all_dorms)

@app.route('/dorms/<int:dorm_id>')
def dorm_page(dorm_id):
    dorm = Dorm.query.get_or_404(dorm_id)
    ratings = Rating.query.filter_by(dorm_id=dorm_id).all()
    return render_template('dorm_page.html', dorm=dorm, ratings=ratings)

@app.route('/add_dorm', methods=['GET', 'POST'])
def add_dorm():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']
        maps_url = request.form['maps_url']

        new_dorm = Dorm(name=name, description=description, image_url=image_url, maps_url=maps_url)
        db.session.add(new_dorm)
        db.session.commit()

        flash('Dorm added successfully', 'success')
        return redirect(url_for('dorms'))

    return render_template('add_dorm.html')


@app.route('/')
def dashboard():
    dorms = [
        {
            'name': 'Martin Hall',
            'image': 'https://www.ratemydorm.com/media/images/large/1623139572.069_500_348.jpg',
            'rating': '4.2'
        },
        {
            'name': 'Holshouser Hall',
            'image': 'https://www.ratemydorm.com/media/images/large/1623097272.604_500_348.jpg',
            'rating': '4.0'
        },
        {
            'name': 'Scott Hall',
            'image': 'https://www.ratemydorm.com/media/images/large/1623243475.225_500_348.jpg',
            'rating': '3.9'
        }
    ]
    return render_template('dashboard.html', dorms=dorms)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ratings')
@login_required
def ratings():
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    return render_template('ratings.html', ratings=user_ratings)



if __name__ == '__main__':
    create_tables() 
    app.run(debug=True)
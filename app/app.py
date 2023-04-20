from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_oauthlib.client import OAuth
from models import db, User, Dorm, Rating, Vote, School
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import abort

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dorm_rating.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)    

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def create_tables():
    with app.app_context():
        db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/schools')
@admin_required
def admin_schools():
    all_schools = School.query.all()
    return render_template('admin_schools.html', schools=all_schools)

@app.route('/admin/dorms')
@admin_required
def admin_dorms():
    dorms = Dorm.query.options(db.joinedload(Dorm.school)).all()
    return render_template('admin_dorms.html', dorms=dorms)

@app.route('/admin/ratings')
@admin_required
def admin_ratings():
    all_ratings = Rating.query.all()
    return render_template('admin_ratings.html', ratings=all_ratings)

@app.route('/admin/users')
@admin_required
def admin_users():
    all_users = User.query.all()
    return render_template('admin_users.html', users=all_users)

@app.route('/admin/add_school', methods=['GET', 'POST'])
@admin_required
def add_school():
    if request.method == 'POST':
        name = request.form['name']
        new_school = School(name=name)
        db.session.add(new_school)
        db.session.commit()
        flash('School added successfully', 'success')
        return redirect(url_for('admin_schools'))
    return render_template('add_school.html')

@app.route('/admin/edit_school/<int:school_id>', methods=['GET', 'POST'])
@admin_required
def edit_school(school_id):
    school = School.query.get_or_404(school_id)
    if request.method == 'POST':
        school.name = request.form['name']
        db.session.commit()
        flash('School updated successfully', 'success')
        return redirect(url_for('admin_schools'))
    return render_template('edit_school.html', school=school)

@app.route('/admin/delete_school/<int:school_id>', methods=['POST'])
@admin_required
def delete_school(school_id):
    school = School.query.get_or_404(school_id)
    db.session.delete(school)
    db.session.commit()
    flash('School deleted successfully', 'success')
    return redirect(url_for('admin_schools'))


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
    dorms = Dorm.query.options(db.joinedload(Dorm.school)).all()
    for dorm in dorms:
        ratings = Rating.query.filter_by(dorm_id=dorm.id).all()
        if ratings:
            dorm.average_rating = sum([rating.rating for rating in ratings]) / len(ratings)
        else:
            dorm.average_rating = None
    return render_template('dorms.html', dorms=dorms)


@app.route('/dorms/<int:dorm_id>')
def dorm_page(dorm_id):
    dorm = Dorm.query.get_or_404(dorm_id)
    ratings = Rating.query.filter_by(dorm_id=dorm_id).all()
    return render_template('dorm_page.html', dorm=dorm, ratings=ratings)

from flask import Flask, render_template, request, redirect, url_for, flash
from models import Dorm, School

@app.route('/add_dorm', methods=['GET', 'POST'])
@app.route('/add_dorm/<int:dorm_id>', methods=['GET', 'POST'])
def add_dorm(dorm_id=None):
    dorm = None
    if dorm_id:
        dorm = Dorm.query.get_or_404(dorm_id)
    schools = School.query.all()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']
        maps_url = request.form['maps_url']
        school_id = request.form['school_id']

        if school_id == 'misc':
            # Create a miscellaneous school if it doesn't exist
            misc_school = School.query.filter_by(name='Miscellaneous').first()
            if not misc_school:
                misc_school = School(name='Miscellaneous')
                db.session.add(misc_school)
                db.session.commit()
            school_id = misc_school.id

        if dorm:
            # Update existing dorm
            dorm.name = name
            dorm.description = description
            dorm.image_url = image_url
            dorm.maps_url = maps_url
            dorm.school_id = school_id
            flash('Dorm updated successfully', 'success')
        else:
            # Add new dorm
            new_dorm = Dorm(name=name, description=description, image_url=image_url, maps_url=maps_url, school_id=school_id)
            db.session.add(new_dorm)
            flash('Dorm added successfully', 'success')

        db.session.commit()
        return redirect(url_for('dorms'))

    return render_template('add_dorm.html', dorm=dorm, schools=schools)

@app.route('/schools')
def schools():
    all_schools = School.query.all()
    for school in all_schools:
        dorms = Dorm.query.filter_by(school_id=school.id).all()
        school.dorm_count = len(dorms)
        ratings = Rating.query.join(Dorm, Dorm.id == Rating.dorm_id).filter(Dorm.school_id == school.id).all()
        school.total_ratings = len(ratings)
    return render_template('schools.html', schools=all_schools)


@app.route('/schools/<int:school_id>')
def school_page(school_id):
    school = School.query.get_or_404(school_id)
    dorms = Dorm.query.filter_by(school_id=school_id).all()
    for dorm in dorms:
        ratings = Rating.query.filter_by(dorm_id=dorm.id).all()
        if ratings:
            dorm.average_rating = sum([rating.rating for rating in ratings]) / len(ratings)
        else:
            dorm.average_rating = None
    return render_template('school_page.html', school=school, dorms=dorms)



@app.route('/dash')
def dashboard():
    # Query all dorms and their ratings
    dorms = Dorm.query.all()
    
    # Calculate the average rating for each dorm
    for dorm in dorms:
        ratings = Rating.query.filter_by(dorm_id=dorm.id).all()
        total_ratings = sum(rating.rating for rating in ratings)
        if ratings:
            dorm.average_rating = total_ratings / len(ratings)
        else:
            dorm.average_rating = None

    # Sort the dorms by their average rating, descending
    dorms.sort(key=lambda dorm: dorm.average_rating or 0, reverse=True)


    # Separate the dorms into featured and normal dorms
    featured_dorms = dorms[:2]
    normal_dorms = dorms[2:]

    # Query the latest ratings
    latest_ratings = Rating.query.order_by(Rating.id.desc()).limit(5).all()

    return render_template('dashboard.html', featured_dorms=featured_dorms, normal_dorms=normal_dorms, latest_ratings=latest_ratings)

@app.route('/')
def landing():
    # Query all dorms and their ratings
    dorms = Dorm.query.all()
    
    # Calculate the average rating for each dorm
    for dorm in dorms:
        ratings = Rating.query.filter_by(dorm_id=dorm.id).all()
        total_ratings = sum(rating.rating for rating in ratings)
        if ratings:
            dorm.average_rating = total_ratings / len(ratings)
        else:
            dorm.average_rating = None

    # Sort the dorms by their average rating, descending
    dorms.sort(key=lambda dorm: dorm.average_rating or 0, reverse=True)


    # Separate the dorms into featured and normal dorms
    featured_dorms = dorms[:2]
    normal_dorms = dorms[2:]

    # Query the latest ratings
    latest_ratings = Rating.query.order_by(Rating.id.desc()).limit(5).all()

    return render_template('landing_page.html', featured_dorms=featured_dorms, normal_dorms=normal_dorms, latest_ratings=latest_ratings)



@app.route('/rate_dorm/<int:dorm_id>', methods=['GET', 'POST'])
@login_required
def rate_dorm(dorm_id):
    dorm = Dorm.query.get_or_404(dorm_id)

    # Check if the user has already rated this dorm
    existing_rating = Rating.query.filter_by(user_id=current_user.id, dorm_id=dorm_id).first()

    if request.method == 'POST':
        rating_value = float(request.form['rating'])
        comment = request.form['comment']

        if existing_rating:
            # Update the existing rating
            existing_rating.rating = rating_value
            existing_rating.comment = comment
        else:
            # Create a new rating
            rating = Rating(user_id=current_user.id, dorm_id=dorm_id, rating=rating_value, comment=comment)
            db.session.add(rating)

        db.session.commit()

        flash('Your rating has been submitted.', 'success')
        return redirect(url_for('dorm_page', dorm_id=dorm_id))

    return render_template('rate_dorm.html', dorm=dorm)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/ratings')
@login_required
def ratings():
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    return render_template('ratings.html', ratings=user_ratings)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user:
            flash('A user with this username or email already exists.', 'danger')
        else:
            new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('signin'))

    return render_template('sign_up.html')

@app.route('/admin/users/<int:user_id>/toggle_admin')
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()

    if user.is_admin:
        flash(f"{user.username} is now an admin.", "success")
    else:
        flash(f"{user.username} is no longer an admin.", "success")

    return redirect(url_for('admin_users'))

@app.route('/signout')
@login_required
def signout():
    logout_user()
    flash('You have been signed out.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    create_tables() 
    app.run(debug=True)
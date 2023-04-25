from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models import School, Dorm, Rating, User, db
from functools import wraps
from flask_login import current_user

admin_routes = Blueprint('admin_routes', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_routes.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@admin_routes.route('/admin/schools')
@admin_required
def admin_schools():
    all_schools = School.query.all()
    return render_template('admin_schools.html', schools=all_schools)

@admin_routes.route('/admin/dorms')
@admin_required
def admin_dorms():
    dorms = Dorm.query.options(db.joinedload(Dorm.school)).all()
    return render_template('admin_dorms.html', dorms=dorms)

@admin_routes.route('/admin/ratings')
@admin_required
def admin_ratings():
    all_ratings = Rating.query.all()
    return render_template('admin_ratings.html', ratings=all_ratings)

@admin_routes.route('/admin/users')
@admin_required
def admin_users():
    all_users = User.query.all()
    return render_template('admin_users.html', users=all_users)

@admin_routes.route('/admin/users/<int:user_id>/toggle_admin')
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

@admin_routes.route('/admin/add_school', methods=['GET', 'POST'])
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

@admin_routes.route('/admin/edit_school/<int:school_id>', methods=['GET', 'POST'])
@admin_required
def edit_school(school_id):
    school = School.query.get_or_404(school_id)
    if request.method == 'POST':
        school.name = request.form['name']
        db.session.commit()
        flash('School updated successfully', 'success')
        return redirect(url_for('admin_schools'))
    return render_template('edit_school.html', school=school)

@admin_routes.route('/admin/delete_school/<int:school_id>', methods=['POST'])
@admin_required
def delete_school(school_id):
    school = School.query.get_or_404(school_id)
    db.session.delete(school)
    db.session.commit()
    flash('School deleted successfully', 'success')
    return redirect(url_for('admin_schools'))

@admin_routes.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = request.form.get('is_admin', False)

        new_user = User(username=username, email=email, is_admin=is_admin)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect(url_for('admin_routes.admin_users'))
    return render_template('add_user.html')

@admin_routes.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = request.form.get('is_admin', False)

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin_routes.admin_users'))
    return render_template('edit_user.html', user=user)

@admin_routes.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_routes.admin_users'))

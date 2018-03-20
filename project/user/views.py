# project/user/views.py

from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from project.token import generate_confirmation_token, confirm_token
from project.models import User, Role, UserRoles, Coin
from project.email import send_email
from project.decorators import check_confirmed, roles_accepted, roles_required
from datetime import datetime
from project import db, bcrypt
from .forms import LoginForm, RegisterForm, ChangePasswordForm

user_blueprint = Blueprint('user', __name__,)


# Routes

"""
Creates the form object for user registration. On submit, creates the user record and sends
verification email to the registering user
"""
@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, username=form.username.data, active=False)

        db.session.add(user)
        db.session.commit()

        role = Role.query.filter_by(name="member").first()

        user_role = UserRoles(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')

        return redirect(url_for('user.unconfirmed'))                                 

    return render_template('user/signup.html', form=form)


# Route for the login process. Verifies the user password.
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Welcome.', 'success')

                return redirect(url_for('user.dashboard'))                               

        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)

    return render_template('user/login.html', form=form)

# Logout route
@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('main.home'))                                       

# Route for the profile page. Can change a user password.
@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)

# Route which checks if the user has confirmed or not
@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.active:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('main.home'))

    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()

    if user.email == email:
        user.active = True
        user.confirmed_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account!', 'success')
        flash('Please login using your credentials.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')

    return redirect(url_for('main.home'))

# Route for unconfirmed users
@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.active:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')

# Route for resending email verification
@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))


# Route for the dashboard. Displays options for the iframe on the html
@user_blueprint.route('/dashboard')
@login_required
@check_confirmed
def dashboard():
    timers = ["10 min", "20 min", "30 min", "40 min", "50 min", "60 min", "70 min", "90 min"]
    coins = Coin.query.all()
    return render_template('user/dashboard.html', username=current_user.username, timers=timers, coins=coins)

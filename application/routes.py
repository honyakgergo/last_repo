from flask import redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, current_user, login_required, logout_user

from application import app, db, bcrypt
from application.models import User
from application.data import test_users
from application.forms import NewUserForm, LoginForm

from flask import request, jsonify
from application.predict import predict


with app.app_context():
    db.create_all()
    for test_user in test_users:
        hashed_pswd = bcrypt.generate_password_hash('alma24').decode('utf-8')
        user_obj = User(username=test_user['username'], email=test_user['email'], password=hashed_pswd)
        db.session.add(user_obj)
    db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='WasteWarrior')


@app.route('/predict', methods=['POST'])
def predict_route():
    return predict()


@app.route('/message_board')
def message_board():
    return redirect(url_for('home'))


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewUserForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Please log in!', 'success')
        print(User.query.all())
        return redirect(url_for('home'))
    return render_template('register.html', title='Create User Account', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Check the email and password you entered!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='User Account')
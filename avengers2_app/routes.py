from avengers2_app import app, db

from flask import render_template, request, redirect, url_for

from avengers2_app.forms import UserInfoForm, LoginForm, NewPhoneForm

from avengers2_app.models import User, check_password_hash

#Import for Flask Login functions - login_required
# login_user, current_user, logout_user
from flask_login import login_required, login_user, current_user, logout_user

@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users = users)

@app.route('/register', methods = ['GET', 'POST'])
def register():

    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        print(f"New user {name} added with email: {email} and phone: "\
                + f"{phone}.")
        # Init of our User class(aka model)
        user = User(name, phone, email, password)
        # Open a connection to the database
        db.session.add(user)
        # Commit all data to the database
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('register.html', user_form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        logged_user = User.query.filter(User.email == email).first()

        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', login_form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/details/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user = user)

@app.route('/phoneupdate/<int:user_id>', methods = ['GET','POST'])
def phone_update(user_id):
    form = NewPhoneForm()
    user = User.query.get_or_404(user_id)
    if request.method == 'POST' and form.validate():
        phone = form.phone.data

        user.phone = phone

        db.session.commit()
        return redirect(url_for('home'))
        
    return render_template('phone_update.html', phone_form = form)

@app.route('/delete/<int:user_id>', methods=['GET', 'DELETE'])
@login_required
def account_del(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))
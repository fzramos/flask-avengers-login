from avengers2_app import app, db

from flask import render_template, request

from avengers2_app.forms import UserInfoForm#, LoginForm

from avengers2_app.models import User, check_password_hash

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():

    form = UserInfoForm()
    print('did this run?')
    if request.method == 'POST' and form.validate():
        print('did this run??')
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

    return render_template('register.html', user_form = form)

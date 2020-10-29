from avengers2_app import app, db

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    phone = db.Column(db.String(15), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    
    def __init__(self, name, phone, email, password):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        """
            Grab the password that is passed into the method
            return the hashed verson of the password 
            which will be stored inside the database
        """
        return generate_password_hash(password)

    def __repr__(self):
        return f'{self.name} has been created with the following phone'\
            + f': {self.phone} and the email: {self.email}'
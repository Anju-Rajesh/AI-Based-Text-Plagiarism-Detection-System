from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import models after db initialization to avoid circular imports
# from models import User 
# For now, we'll define a simple user model here or wait for models.py to be created and imported properly
# To keep it simple for the first run, let's assume models.py will handle the DB classes
# import models 

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/ai_detection')
# @login_required
def ai_detection():
    return render_template('ai_detection.html')

@app.route('/plagiarism')
# @login_required
def plagiarism():
    return render_template('plagiarism.html')

@app.route('/similarity')
# @login_required
def similarity():
    return render_template('similarity.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

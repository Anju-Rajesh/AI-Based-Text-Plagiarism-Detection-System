import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, AIAnalysis, SimilarityAnalysis
from utils.ai_detector import analyze_text_ai
from utils.similarity_checker import calculate_similarity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('ai_detection'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ai_detection'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ai_detection'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('ai_detection'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/ai-detection', methods=['GET', 'POST'])
@login_required
def ai_detection():
    result = None
    if request.method == 'POST':
        text = ""
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if file.filename.endswith('.txt'):
                text = file.read().decode('utf-8')
            else:
                flash('Only .txt files are allowed.', 'warning')
        else:
            text = request.form.get('text', '')

        if text.strip():
            probability, conclusion = analyze_text_ai(text)
            
            # Save to database
            analysis = AIAnalysis(user_id=current_user.id, input_text=text[:500] + '...', ai_probability=probability, conclusion=conclusion)
            db.session.add(analysis)
            db.session.commit()
            
            result = {'probability': probability, 'conclusion': conclusion}
        else:
            flash('Please provide some text or upload a file.', 'info')
            
    return render_template('ai_detection.html', result=result)

@app.route('/similarity', methods=['GET', 'POST'])
@login_required
def similarity():
    result = None
    if request.method == 'POST':
        source_text = request.form.get('source_text', '')
        comparison_text = request.form.get('comparison_text', '')
        
        if source_text.strip() and comparison_text.strip():
            sim_percentage = calculate_similarity(source_text, comparison_text)
            
            # Save to database
            analysis = SimilarityAnalysis(
                user_id=current_user.id, 
                source_text=source_text[:500] + '...', 
                comparison_text=comparison_text[:500] + '...', 
                similarity_percentage=sim_percentage
            )
            db.session.add(analysis)
            db.session.commit()
            
            result = {'percentage': sim_percentage}
        else:
            flash('Please provide both source and comparison text.', 'info')
            
    return render_template('similarity.html', result=result)

@app.route('/plagiarism')
@login_required
def plagiarism():
    return render_template('plagiarism.html')


if __name__ == '__main__':
    app.run(debug=True)

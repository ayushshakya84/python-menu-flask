from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import subprocess
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    about = db.Column(db.String(500), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.email = request.form.get('email')
        current_user.about = request.form.get('about')
        db.session.commit()
        flash('Profile updated successfully!')
    return render_template('profile.html')

@app.route('/local_menu')
@login_required
def local_menu():
    return render_template('local_menu.html')

@app.route('/remote_menu')
@login_required
def remote_menu():
    return render_template('remote_menu.html')

@app.route('/networking_menu')
@login_required
def networking_menu():
    return render_template('networking_menu.html')

@app.route('/local/<action>', methods=['POST'])
@login_required
def local_action(action):
    if action == 'create_file':
        file_name = request.form.get('file_name')
        if file_name:
            subprocess.run(["touch", file_name])
            return jsonify({"status": "success", "message": f"File '{file_name}' created successfully."})
        else:
            return jsonify({"status": "error", "message": "File name cannot be empty."})
    elif action == 'create_folder':
        folder_name = request.form.get('folder_name')
        if folder_name:
            subprocess.run(["mkdir", folder_name])
            return jsonify({"status": "success", "message": f"Folder '{folder_name}' created successfully."})
        else:
            return jsonify({"status": "error", "message": "Folder name cannot be empty."})
    elif action == 'show_date':
        result = subprocess.run(["date"], capture_output=True, text=True)
        return jsonify({"status": "success", "message": result.stdout})
    elif action == 'show_calendar':
        result = subprocess.run(["cal"], capture_output=True, text=True)
        return jsonify({"status": "success", "message": result.stdout})
    elif action == 'install_software':
        software_name = request.form.get('software_name')
        if software_name:
            subprocess.run(["sudo", "apt", "install", "-y", software_name])
            return jsonify({"status": "success", "message": f"Software '{software_name}' installed successfully."})
        else:
            return jsonify({"status": "error", "message": "Software name cannot be empty."})
    else:
        return jsonify({"status": "error", "message": "Invalid action."})

@app.route('/remote/<action>', methods=['POST'])
@login_required
def remote_action(action):
    ip = request.form.get('ip')
    if not ip:
        return jsonify({"status": "error", "message": "Remote IP cannot be empty."})
    if action == 'create_file':
        file_name = request.form.get('file_name')
        if file_name:
            subprocess.run(["ssh", ip, "touch", file_name])
            return jsonify({"status": "success", "message": f"File '{file_name}' created on remote server."})
        else:
            return jsonify({"status": "error", "message": "File name cannot be empty."})
    elif action == 'create_folder':
        folder_name = request.form.get('folder_name')
        if folder_name:
            subprocess.run(["ssh", ip, "mkdir", folder_name])
            return jsonify({"status": "success", "message": f"Folder '{folder_name}' created on remote server."})
        else:
            return jsonify({"status": "error", "message": "Folder name cannot be empty."})
    elif action == 'show_date':
        result = subprocess.run(["ssh", ip, "date"], capture_output=True, text=True)
        return jsonify({"status": "success", "message": result.stdout})
    elif action == 'show_calendar':
        result = subprocess.run(["ssh", ip, "cal"], capture_output=True, text=True)
        return jsonify({"status": "success", "message": result.stdout})
    elif action == 'install_software':
        software_name = request.form.get('software_name')
        if software_name:
            subprocess.run(["ssh", ip, "sudo", "apt", "install", "-y", software_name])
            return jsonify({"status": "success", "message": f"Software '{software_name}' installed on remote server."})
        else:
            return jsonify({"status": "error", "message": "Software name cannot be empty."})
    else:
        return jsonify({"status": "error", "message": "Invalid action."})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

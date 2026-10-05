import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

# File path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Exact path for Frontend/templates and Frontend/static based on VS Code layout
TEMPLATE_DIR = os.path.join(BASE_DIR, 'Frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'Frontend', 'static')

# Fallback in case backend/app.py structure is used in GitHub
if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'Frontend', 'templates')
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(BASE_DIR, '..', 'Frontend', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'ngo_donation_secret_key_2026'

# Dynamic Data Storage (Fallback / In-Memory Data)
USERS = {
    "donor@example.com": {"password": "123", "name": "John Donor", "role": "donor"},
    "ngo@example.com": {"password": "123", "name": "Helping NGO", "role": "ngo"},
    "volunteer@example.com": {"password": "123", "name": "David Volunteer", "role": "volunteer"}
}

NGO_LIST = [
    {"name": "Helping Hands Foundation", "desc": "Supporting children and education.", "cat": "Education", "location": "Chennai"},
    {"name": "Hope Medical Foundation", "desc": "Providing healthcare support.", "cat": "Healthcare", "location": "Coimbatore"},
    {"name": "Future Education Trust", "desc": "Helping students achieve their dreams.", "cat": "Education", "location": "Madurai"}
]

# Optional DB Bypass
db = None
cursor = None
try:
    import mysql.connector
    db = mysql.connector.connect(host="localhost", user="root", password="your_password", database="ngo_db")
    cursor = db.cursor()
except Exception as e:
    print("Database bypassed:", e)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ngos')
def ngos():
    return render_template('ngos.html', ngos=NGO_LIST)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in USERS and USERS[email]['password'] == password:
            session['user'] = USERS[email]
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid Email or Password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

app = app

if __name__ == '__main__':
    app.run(debug=True)

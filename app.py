import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute Path Resolution for Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(BASE_DIR, 'Frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'Frontend', 'static')

# If templates are directly under root/templates, fallback handles it smoothly
if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'ngo_donation_secret_key_2026'

# Dynamic Data Storage (Fallback Data)
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

TRACKING_DATA = {
    "TRK1001": {"status": "In Transit", "donor": "John Donor", "type": "Money (₹1000)", "ngo": "Helping Hands Foundation", "step": 3},
    "TRK1002": {"status": "Delivered", "donor": "Priya", "type": "Books & Clothes", "ngo": "Future Education Trust", "step": 4}
}

# Safe Database Connection for Cloud/Vercel Serverless
db = None
cursor = None

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ngo_db"
    )
    cursor = db.cursor()
except Exception as e:
    print("Database Connection Error (Bypassed for Serverless):", e)

# Routes
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error rendering index.html: {str(e)}"

@app.route('/ngos')
def ngos():
    try:
        return render_template('ngos.html', ngos=NGO_LIST)
    except Exception as e:
        return f"Error loading ngos.html: {str(e)}"

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
            
    try:
        return render_template('login.html')
    except Exception as e:
        return f"Error loading login.html: {str(e)}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        return render_template('register.html')
    except Exception as e:
        return f"Error loading register.html: {str(e)}"

# Export for Vercel Serverless
app = app

if __name__ == '__main__':
    app.run(debug=True)

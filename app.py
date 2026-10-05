import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Find the exact directory of this app.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Map to Frontend/templates and Frontend/static directory
TEMPLATE_DIR = os.path.join(BASE_DIR, 'Frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'Frontend', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'ngo_donation_secret_key_2026'

# Dummy data so application runs seamlessly without DB dependency
USERS = {
    "donor@example.com": {"password": "123", "name": "John Donor", "role": "donor"},
    "ngo@example.com": {"password": "123", "name": "Helping NGO", "role": "ngo"}
}

NGO_LIST = [
    {"name": "Helping Hands Foundation", "desc": "Supporting children and education.", "cat": "Education", "location": "Chennai"},
    {"name": "Hope Medical Foundation", "desc": "Providing healthcare support.", "cat": "Healthcare", "location": "Coimbatore"}
]

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
            flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# Essential for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)

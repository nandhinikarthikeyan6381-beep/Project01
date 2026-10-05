import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'Frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'Frontend', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'ngo_donation_secret_key_2026'

# Dynamic Data Storage
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

@app.route('/')
def index():
    return render_template('index.html', ngos=NGO_LIST)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/ngos')
def ngos():
    return render_template('ngos.html', ngos=NGO_LIST)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in USERS and USERS[email]['password'] == password:
            session['user'] = email
            session['name'] = USERS[email]['name']
            session['role'] = USERS[email]['role']
            
            role = USERS[email]['role']
            if role == 'donor':
                return redirect(url_for('donor_dashboard'))
            elif role == 'volunteer':
                return redirect(url_for('volunteer_dashboard'))
            elif role == 'ngo':
                return redirect(url_for('ngo_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid Email or Password! Try: donor@example.com / 123', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'donor')
        
        USERS[email] = {"password": password, "name": name, "role": role}
        flash('Account registered successfully! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    qr_url = None
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        if amount:
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa=ngodonation@upi%26pn=NGO%20Donation%26am={amount}"
            flash(f'Scan QR Code below to pay ₹{amount}', 'success')
        else:
            flash(f'Resource donation request for {category} submitted!', 'success')
            return redirect(url_for('tracking'))
            
    return render_template('donate.html', ngos=NGO_LIST, qr_url=qr_url)

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# FIX: Function name tracking-nu vachittom, donation_detail endpoint support-kaga rendu aliases include panni irukom
@app.route('/tracking', methods=['GET', 'POST'], endpoint='tracking')
@app.route('/donation_detail', methods=['GET', 'POST'], endpoint='donation_detail')
def tracking():
    tracking_id = request.args.get('trk') or request.form.get('tracking_id') or 'TRK1001'
    data = TRACKING_DATA.get(tracking_id.upper(), TRACKING_DATA['TRK1001'])
    return render_template('donation_detail.html', data=data, tracking_id=tracking_id.upper())

@app.route('/donor_dashboard')
def donor_dashboard():
    return render_template('donor_dashboard.html', name=session.get('name', 'Donor'))

@app.route('/ngo_dashboard')
def ngo_dashboard():
    return render_template('ngo_dashboard.html', name=session.get('name', 'NGO Admin'))

@app.route('/volunteer_dashboard')
def volunteer_dashboard():
    return render_template('volunteer_dashboard.html', name=session.get('name', 'Volunteer'))

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from signals.indicators import calculate_signal
from config.secrets import ADMIN_PASSWORD_HASH
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'backend/users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quotex_id TEXT UNIQUE,
                        telegram TEXT,
                        whatsapp TEXT,
                        referral TEXT,
                        approved INTEGER DEFAULT 0,
                        device TEXT
                      )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        quotex_id = request.form['quotex_id']
        telegram = request.form.get('telegram')
        whatsapp = request.form['whatsapp']
        referral = request.form['referral']

        # Referral check
        if referral != 'YOUR_REFERRAL_LINK':
            return "Invalid referral link!"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (quotex_id, telegram, whatsapp, referral) VALUES (?, ?, ?, ?)',
                           (quotex_id, telegram, whatsapp, referral))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Quotex ID already exists!"
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        quotex_id = request.form['quotex_id']
        device = request.remote_addr
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT approved, device FROM users WHERE quotex_id=?', (quotex_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return "User not found!"
        approved, saved_device = user
        if approved == 0:
            conn.close()
            return "Your account is not approved yet!"
        if saved_device and saved_device != device:
            conn.close()
            return "Device mismatch! Only 1 device allowed."
        # Update device
        cursor.execute('UPDATE users SET device=? WHERE quotex_id=?', (device, quotex_id))
        conn.commit()
        conn.close()
        session['quotex_id'] = quotex_id
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'quotex_id' not in session:
        return redirect(url_for('login'))
    quotex_id = session['quotex_id']
    # Calculate signal (placeholder)
    signal = calculate_signal()
    return render_template('dashboard.html', signal=signal, quotex_id=quotex_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

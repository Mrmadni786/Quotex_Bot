from flask import Flask, request, jsonify
import sqlite3
from config.secrets import ADMIN_PASSWORD_HASH
import hashlib

app = Flask(__name__)
DATABASE = '../backend/users.db'

def verify_password(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash == ADMIN_PASSWORD_HASH

@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    if verify_password(data['password']):
        return jsonify({"status":"success"})
    return jsonify({"status":"fail"}), 401

@app.route('/approve_user', methods=['POST'])
def approve_user():
    quotex_id = request.json['quotex_id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET approved=1 WHERE quotex_id=?', (quotex_id,))
    conn.commit()
    conn.close()
    return jsonify({"status":"approved"})

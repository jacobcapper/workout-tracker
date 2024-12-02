from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Serve static files (QR Codes)
@app.route('/qr/<filename>')
def serve_qr(filename):
    return send_from_directory('static/qr', filename)

# Endpoint for scanning QR codes
@app.route('/scan', methods=['POST'])
def scan_qr():
    data = request.json
    qr_code = data.get('qr_code')

    if not qr_code:
        return jsonify({'error': 'QR code is required'}), 400

    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    # Find user by QR code
    user = cursor.execute('SELECT id, name FROM users WHERE qr_code = ?', (qr_code,)).fetchone()
    if not user:
        return jsonify({'error': 'Invalid QR code'}), 404

    user_id = user[0]
    user_name = user[1]
    timestamp = datetime.now()

    # Log scan
    cursor.execute('INSERT INTO scans (user_id) VALUES (?)', (user_id,))
    
    # Increment monthly count
    month, year = timestamp.month, timestamp.year
    cursor.execute('''
        INSERT INTO monthly_counts (user_id, month, year, count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(user_id, month, year)
        DO UPDATE SET count = count + 1
    ''', (user_id, month, year))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Scan recorded', 'user': user_name, 'time': str(timestamp)})

# View scan history
@app.route('/history/<int:user_id>')
def view_history(user_id):
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    scans = cursor.execute('SELECT timestamp FROM scans WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    return jsonify({"history": [scan[0] for scan in scans]})

# QR Codes page for Dakboard
@app.route('/qr_page')
def qr_page():
    qr_codes = [
        {"name": "John Doe", "url": "/qr/john_doe_qr.png"},
        {"name": "Jane Doe", "url": "/qr/jane_doe_qr.png"}
    ]
    return render_template('qr_page.html', qr_codes=qr_codes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


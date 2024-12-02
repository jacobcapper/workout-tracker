from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Serve static files (QR Codes)
@app.route('/qr/<filename>')
def serve_qr(filename):
    return send_from_directory('static/qr', filename)

# Add a route for adding new users
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        qr_code = f"{name.lower()}_qr_code"  # Generate a simple QR code name
        
        if not name:
            return "Name is required", 400

        conn = sqlite3.connect('workout_tracker.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (name, qr_code) VALUES (?, ?)', (name, qr_code))
            conn.commit()
        except sqlite3.IntegrityError:
            return "User already exists or QR code conflict", 400
        finally:
            conn.close()

        # Generate QR code for the user
        import qrcode
        img = qrcode.make(qr_code)
        img.save(f"static/qr/{name}_qr.png")

        return redirect(url_for('home'))
    return render_template('add_user.html')

# Other routes...

from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Serve static files (QR Codes)
@app.route('/qr/<filename>')
def serve_qr(filename):
    return send_from_directory('static/qr', filename)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            return "Name is required", 400

        conn = sqlite3.connect('workout_tracker.db')
        cursor = conn.cursor()

        try:
            # Insert the user and get their assigned ID
            cursor.execute('INSERT INTO users (name, qr_code) VALUES (?, ?)', (name, ''))
            user_id = cursor.lastrowid
            
            # Generate the URL for the user's QR code
            qr_code_url = f"http://192.168.1.23:5000/scan/{user_id}"

            # Update the user's QR code field in the database
            cursor.execute('UPDATE users SET qr_code = ? WHERE id = ?', (qr_code_url, user_id))
            conn.commit()

            # Generate and save the QR code
            import qrcode
            img = qrcode.make(qr_code_url)
            img.save(f"static/qr/{name}_qr.png")

        except sqlite3.IntegrityError:
            return "User already exists or QR code conflict", 400
        finally:
            conn.close()

        return redirect(url_for('home'))
    return render_template('add_user.html')


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

# Home page with users and their information
@app.route('/')
def home():
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    # Fetch users and their workout counts for the current month
    month = datetime.now().month
    year = datetime.now().year
    users = cursor.execute('''
        SELECT u.id, u.name, COUNT(s.id) as workout_count
        FROM users u
        LEFT JOIN scans s ON u.id = s.user_id
        WHERE strftime('%m', s.timestamp) = ? AND strftime('%Y', s.timestamp) = ?
        GROUP BY u.id
    ''', (f'{month:02}', f'{year}')).fetchall()

    conn.close()

 # Print the users list to the terminal
    print(users)
    
    return render_template('index.html', users=users)

# Separate page to show the QR codes
@app.route('/qr_page')
def qr_page():
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    # Fetch all users
    users = cursor.execute('SELECT id, name FROM users').fetchall()

    conn.close()

    return render_template('qr_page.html', users=users)

# Separate page to show the chart
@app.route('/chart_page')
def chart_page():
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    # Fetch users and their workout counts for the current month
    month = datetime.now().month
    year = datetime.now().year
    users = cursor.execute('''
        SELECT u.id, u.name, COUNT(s.id) as workout_count
        FROM users u
        LEFT JOIN scans s ON u.id = s.user_id
        WHERE strftime('%m', s.timestamp) = ? AND strftime('%Y', s.timestamp) = ?
        GROUP BY u.id
    ''', (f'{month:02}', f'{year}')).fetchall()

    conn.close()

    return render_template('chart_page.html', users=users, month=month, year=year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

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
@app.route('/scan/<int:user_id>', methods=['GET'])
def scan(user_id):
    try:
        conn = sqlite3.connect('workout_tracker.db')
        cursor = conn.cursor()

        # Check if the user exists
        user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            conn.close()
            return "User not found", 404

        # Log the scan (record a timestamp for the workout)
        cursor.execute('INSERT INTO scans (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()

        # Respond to the scan (can be a simple message or redirect)
        return f"Workout logged for {user[1]}!", 200

    except Exception as e:
        print(f"Error: {e}")  # Log the error message to the console
        return "Internal Server Error", 500
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

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = sqlite3.connect('workout_tracker.db')
    cursor = conn.cursor()

    try:
        # Delete the user from the users table
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        # Optionally, delete the user’s QR code image file from the server
        import os
        user_name = cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,)).fetchone()[0]
        qr_code_path = f"static/qr/{user_name}_qr.png"
        if os.path.exists(qr_code_path):
            os.remove(qr_code_path)

        conn.commit()
    except Exception as e:
        print(f"Error deleting user: {e}")
        return "Error deleting user", 500
    finally:
        conn.close()

    # Redirect back to the home page after deletion
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

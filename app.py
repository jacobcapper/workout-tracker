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

    # Debug prints
    print(f"Current Month: {month}, Current Year: {year}")
    print(f"Users fetched: {users}")

    return render_template('index.html', users=users)

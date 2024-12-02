# Workout Tracker

A simple workout tracker using QR codes.

---

## 🚀 Features
- 📸 Generate QR codes for users.
- 🌐 Access user-specific workout QR codes via a web interface.
- 🔄 Scan QR codes via an API to log workouts.

---
## ⚙️ Prerequisites

Before you start, make sure you have the following:

- A **Debian-based server** (such as Ubuntu or Debian itself).
- **Python 3** and **pip** installed.
- **Git** to clone the repository.
- The required Python libraries:  
  Install the dependencies using `pip`:
  
  ```bash
  pip install qrcode[pil] flask
  ```
## 💻 Installation

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/jacobcapper/workout-tracker.git
```
Navigate into the project directory:
```bash
cd workout-tracker
```

## ⚙️ Setup Instructions

### 🛠️ Database Initialization
Initialize the SQLite database by running:

```bash
python3 init_db.py
```

🖼️ Generate QR Codes

Create the static/qr/ Directory:
```bash
mkdir -p static/qr
```

Generate user-specific QR codes with:
```bash
python3 qr_generator.py
```
▶️ Run the Application

Start the Flask server by executing:

```bash
python3 app.py
```
---
🧑‍💻 Usage
📄 Access QR Codes

View user-specific QR codes by visiting or embedding:
```bash
http://<your-server-ip>:5000/qr/<qr_code_name>.png
```
For example:
```bash
http://<your-server-ip>:5000/qr/john_doe_qr.png
```
🌍 QR Code Web Page

Access or embed a web page displaying all QR codes:
```bash
http://<your-server-ip>:5000/qr_page
```
🛠️ API for Scanning

Log a workout by scanning a QR code and posting data to the API.

Endpoint:
```bash
POST http://<your-server-ip>:5000/scan
```
JSON Payload:
```bash
{
  "qr_code": "user_1"
}
```

How to Move to a Production-Ready Server:

If you're just testing or using this app on your local network (as a personal project or for internal use), you can continue using the development server.

If you plan to deploy this on a public-facing server or expect higher traffic, here's what you can do:

    Install Gunicorn (a popular WSGI server for Flask):

pip3 install gunicorn

Run your Flask app with Gunicorn: Instead of using python3 app.py, run the following:

    gunicorn -b 0.0.0.0:5000 app:app

    This tells Gunicorn to bind to all IP addresses (0.0.0.0) and run on port 5000. This will give you better performance, handle multiple requests concurrently, and avoid the development server warning.

    Set up Reverse Proxy (Optional): If you want to deploy the app behind a web server (like Nginx or Apache) for better security, load balancing, and more, you can configure that as well.

In Summary:

    For local testing or personal use, you don't need to worry about the warning.
    For production, switch to a WSGI server like Gunicorn to ensure better performance and scalability.









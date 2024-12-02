# Workout Tracker

A simple workout tracker using QR codes.

---

## 🚀 Features
- 📸 Generate QR codes for users.
- 🌐 Access user-specific workout QR codes via a web interface.
- 🔄 Scan QR codes via an API to log workouts.

---

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










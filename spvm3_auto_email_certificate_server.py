"""
SPVM3 TECH SOLUTION — AUTOMATIC EMAIL CERTIFICATE & WELCOME SERVER
-------------------------------------------------------------------
A lightweight Flask + SQLite service that automatically captures student/visitor emails,
stores completed course certificate records, and sends rich HTML welcome/certificate emails
via SMTP (Gmail App Password, Brevo, Resend, or Mailjet) using non-blocking background threads.

How to Run:
    python spvm3_auto_email_certificate_server.py

Dependencies (install if needed):
    pip install flask flask-cors
"""

import os
import time
import sqlite3
import smtplib
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
DB_FILE = "spvm3_certificates.db"

# SMTP Settings (Set your Gmail App Password or Brevo/Resend SMTP keys here or in Env Vars)
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com") # or 'smtp-relay.brevo.com' / 'smtp.resend.com'
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "spvm3techsolution@gmail.com")
SMTP_PASS = os.environ.get("SMTP_PASS", "") # Put Gmail App Password or Brevo Key here
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "spvm3techsolution@gmail.com")
SENDER_NAME = "Sanjay GL — SPVM3 Tech Solution"

# -----------------------------------------------------------------------------
# DATABASE INITIALIZATION
# -----------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Certificate delivery table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            subject_id TEXT,
            course_title TEXT NOT NULL,
            cert_id TEXT UNIQUE NOT NULL,
            course_hours TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            email_sent INTEGER DEFAULT 0
        )
    """)
    
    # General signup / visitor leads table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            welcome_email_sent INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

# -----------------------------------------------------------------------------
# FLASK APPLICATION
# -----------------------------------------------------------------------------
app = Flask(__name__)

# Manual CORS handler for cross-origin fetch requests from local file:// or dev servers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# -----------------------------------------------------------------------------
# EMAIL SENDING LOGIC (ASYNC BACKGROUND THREADS)
# -----------------------------------------------------------------------------
def send_welcome_email_async(name, email, delay_seconds=120):
    """Sends a personalized welcome email after a short delay (default 2 mins after login)."""
    if delay_seconds > 0:
        time.sleep(delay_seconds)
        
    subject = "🚀 Welcome to SPVM3 Tech Solution Learning Space!"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #f1f5f9; padding: 20px; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #121a2b; border: 2px solid #6366f1; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .header {{ text-align: center; border-bottom: 1px dashed rgba(99,102,241,0.3); padding-bottom: 20px; margin-bottom: 24px; }}
        .title {{ color: #fbbf24; font-size: 22px; font-weight: 800; margin-top: 10px; }}
        .btn {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #06b6d4); color: #ffffff !important; padding: 12px 24px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 15px; }}
        .footer {{ font-size: 12px; color: #94a3b8; margin-top: 30px; border-top: 1px solid #1e293b; padding-top: 15px; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h2 style="color: #6366f1; margin: 0;">⚡ SPVM3 TECH SOLUTION</h2>
          <div style="color: #38bdf8; font-size: 13px; font-weight: bold;">SPVM3 EDUCATION PLATFORM</div>
        </div>
        
        <p>Dear <strong>{name}</strong>,</p>
        <p>Welcome to <strong>SPVM3 Tech Solution Learning Space</strong>! We are thrilled to have you join our ISO-Certified Computer Science & Software Engineering Hub.</p>
        
        <div style="background: rgba(99,102,241,0.15); border: 1px solid #6366f1; padding: 16px; border-radius: 12px; margin: 20px 0;">
          <h3 style="color: #fbbf24; margin-top: 0;">🎓 Certificate Unlocking Rule:</h3>
          <p style="margin-bottom: 0;">Study any of our 21 full computer notes. Once you reach <strong>80% course completion</strong>, your official ISO-Certified Certificate will automatically unlock and be emailed directly to your Gmail!</p>
        </div>
        
        <p style="text-align: center;">
          <a href="http://localhost:8000/index.html" class="btn" target="_blank">💻 Access All 21 Computer Notes</a>
        </p>
        
        <div class="footer">
          <p><strong>SPVM3 Tech Solution</strong> • Shivamogga, Karnataka, India</p>
          <p>📞 Phone/WhatsApp: +91 8123981877 | 📧 Email: spvm3techsolution@gmail.com</p>
          <p>Founder & Director: Sanjay GL</p>
        </div>
      </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = email
    msg.attach(MIMEText(html_body, "html"))
    
    try:
        if SMTP_PASS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE visitors SET welcome_email_sent = 1 WHERE email = ?", (email,))
            conn.commit()
            conn.close()
            print(f"[SUCCESS] Welcome email delivered to {email}")
        else:
            print(f"[SIMULATION] Welcome email queued for {email}")
    except Exception as e:
        print(f"[ERROR] Failed to send welcome email to {email}: {e}")

def send_certificate_email_async(student_name, student_email, course_title, cert_id, course_hours, record_id, delay_seconds=60):
    """Sends the official completion email in a background thread."""
    if delay_seconds > 0:
        time.sleep(delay_seconds)
        
    verify_url = f"http://localhost:8000/verify-certificate.html?certId={cert_id}"
    
    subject = f"🎓 Official Certificate of Completion — {course_title}"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #f1f5f9; padding: 20px; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #121a2b; border: 2px solid #6366f1; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        .header {{ text-align: center; border-bottom: 1px dashed rgba(99,102,241,0.3); padding-bottom: 20px; margin-bottom: 24px; }}
        .title {{ color: #fbbf24; font-size: 22px; font-weight: 800; margin-top: 10px; }}
        .name {{ font-size: 26px; font-weight: 800; color: #38bdf8; margin: 16px 0; text-align: center; }}
        .details {{ background: rgba(0,0,0,0.3); padding: 16px; border-radius: 10px; margin: 20px 0; }}
        .btn {{ display: inline-block; background: linear-gradient(135deg, #06b6d4, #0284c7); color: #ffffff !important; padding: 12px 24px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 15px; }}
        .footer {{ font-size: 12px; color: #94a3b8; margin-top: 30px; border-top: 1px solid #1e293b; padding-top: 15px; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h2 style="color: #6366f1; margin: 0;">⚡ SPVM3 TECH SOLUTION</h2>
          <div style="color: #38bdf8; font-size: 13px; font-weight: bold;">SPVM3 EDUCATION PLATFORM</div>
        </div>
        
        <p>Dear <strong>{student_name}</strong>,</p>
        <p>Congratulations! You have reached over 80% course completion and earned your official Certificate:</p>
        
        <div class="title" style="text-align: center;">{course_title}</div>
        
        <div class="details">
          <p style="margin: 6px 0;"><strong>📜 Certificate Unique ID:</strong> <span style="color: #fbbf24; font-family: monospace;">{cert_id}</span></p>
          <p style="margin: 6px 0;"><strong>⏱️ Certified Duration:</strong> {course_hours}</p>
          <p style="margin: 6px 0;"><strong>🗓️ Issued Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
          <p style="margin: 6px 0;"><strong>🟢 Status:</strong> 100% Verified & ISO Registered</p>
        </div>
        
        <p style="text-align: center;">
          <a href="{verify_url}" class="btn" target="_blank">🔍 Verify & Download Certificate</a>
        </p>
        
        <p style="margin-top: 25px; line-height: 1.6;">
          You can also download your certificate directly in <strong>3 Formats (Image, PDF, or Word Document)</strong> anytime on the SPVM3 Education Platform.
        </p>
        
        <div class="footer">
          <p><strong>SPVM3 Tech Solution</strong> • ISO Certified Computer Science Academy</p>
          <p>📞 Phone/WhatsApp: +91 8123981877 | 📧 Email: spvm3techsolution@gmail.com</p>
          <p>Verified & Approved by Sanjay GL (Founder & Lead Director)</p>
        </div>
      </div>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = student_email
    msg.attach(MIMEText(html_body, "html"))
    
    try:
        if SMTP_PASS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE certificates SET email_sent = 1 WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            print(f"[SUCCESS] Certificate email delivered to {student_email} (Cert ID: {cert_id})")
        else:
            print(f"[SIMULATION] SMTP_PASS not set. Certificate email prepared for {student_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send certificate email to {student_email}: {e}")

# -----------------------------------------------------------------------------
# API ROUTES
# -----------------------------------------------------------------------------
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "service": "SPVM3 Automatic Email Certificate Server",
        "endpoints": {
            "login": "POST /api/login",
            "send_certificate": "POST /api/send-certificate",
            "list_records": "GET /api/records"
        }
    })

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    data = request.get_json(force=True) or {}
    name = data.get("name", "Student").strip()
    email = data.get("email", "").strip()
    
    if not email or "@" not in email:
        return jsonify({"error": "Valid Gmail address required"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO visitors (name, email)
        VALUES (?, ?)
        ON CONFLICT(email) DO UPDATE SET name=excluded.name
    """, (name, email))
    
    conn.commit()
    conn.close()

    # Queue welcome email to be delivered automatically in 2 minutes (120 sec)
    thread = threading.Thread(
        target=send_welcome_email_async,
        args=(name, email, 120)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "success": True,
        "message": f"Welcome {name}! Login session stored.",
        "auto_welcome_email": "scheduled_2_mins"
    }), 200

@app.route('/api/send-certificate', methods=['POST', 'OPTIONS'])
def send_certificate():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    data = request.get_json(force=True) or {}
    
    name = data.get("name", "Student").strip()
    email = data.get("email", "").strip()
    subject_id = data.get("subject_id", "course")
    course_title = data.get("course_title", "Computer Notes")
    cert_id = data.get("cert_id", f"SPVM3-CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    course_hours = data.get("course_hours", "1.5 Hours")
    delay = data.get("delay_seconds", 60) # Default 1-2 min delay
    
    if not email or "@" not in email:
        return jsonify({"error": "Valid email address required"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO certificates (student_name, student_email, subject_id, course_title, cert_id, course_hours)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(cert_id) DO UPDATE SET student_name=excluded.student_name, student_email=excluded.student_email
    """, (name, email, subject_id, course_title, cert_id, course_hours))
    
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()

    # Queue certificate email delivery in background thread
    thread = threading.Thread(
        target=send_certificate_email_async,
        args=(name, email, course_title, cert_id, course_hours, record_id, delay)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "success": True,
        "message": f"Certificate delivery queued for {name} ({email})",
        "cert_id": cert_id,
        "email_delivery": "queued_async"
    }), 200

@app.route('/api/records', methods=['GET'])
def get_records():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificates ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows]), 200

# -----------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print("=====================================================================")
    print("🚀 SPVM3 AUTOMATIC EMAIL CERTIFICATE SERVER IS RUNNING!")
    print("📍 Listening on: http://localhost:5000")
    print("📧 SMTP User:", SMTP_USER)
    print("=====================================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)

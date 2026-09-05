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
import sys
import time
import json
import sqlite3
import smtplib
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

# Ensure Windows terminal doesn't crash on emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# -----------------------------------------------------------------------------
# CONFIGURATION & DYNAMIC SMTP LOADER
# -----------------------------------------------------------------------------
DB_FILE = "spvm3_certificates.db"

def get_smtp_config():
    """Dynamically loads SMTP settings from spvm3_smtp_config.json, .env, or env vars."""
    cfg = {
        "smtp_host": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
        "smtp_user": os.environ.get("SMTP_USER", "spvm3techsolution@gmail.com"),
        "smtp_pass": os.environ.get("SMTP_PASS", "").strip(),
        "sender_email": os.environ.get("SENDER_EMAIL", "spvm3techsolution@gmail.com"),
        "sender_name": "Sanjay GL — SPVM3 Tech Solution"
    }

    # Check local spvm3_smtp_config.json
    config_file = os.path.join(os.path.dirname(__file__), "spvm3_smtp_config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if saved.get("smtp_host"): cfg["smtp_host"] = saved["smtp_host"]
                if saved.get("smtp_port"): cfg["smtp_port"] = int(saved["smtp_port"])
                if saved.get("smtp_user"): cfg["smtp_user"] = saved["smtp_user"].strip()
                if saved.get("smtp_pass"): cfg["smtp_pass"] = saved["smtp_pass"].strip()
                if saved.get("sender_email"): cfg["sender_email"] = saved["sender_email"].strip()
                if saved.get("sender_name"): cfg["sender_name"] = saved["sender_name"].strip()
        except Exception as err:
            print(f"[CONFIG WARNING] Failed to parse spvm3_smtp_config.json: {err}")

    return cfg


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
    
    cfg = get_smtp_config()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{cfg['sender_name']} <{cfg['sender_email']}>"
    msg["To"] = email
    msg.attach(MIMEText(html_body, "html"))
    
    try:
        if cfg["smtp_pass"]:
            with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
                server.starttls()
                server.login(cfg["smtp_user"], cfg["smtp_pass"])
                server.send_message(msg)
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE visitors SET welcome_email_sent = 1 WHERE email = ?", (email,))
            conn.commit()
            conn.close()
            print(f"[SUCCESS] Welcome email delivered to {email}")
        else:
            print(f"[AUTHENTICATION REQUIRED] Cannot deliver live email to {email} because SMTP_PASS is empty.")
            print(f"👉 Please enter your 16-character Gmail App Password into 'spvm3_smtp_config.json' or .env")
            print(f"👉 Generate at: https://myaccount.google.com/apppasswords")
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
    
    cfg = get_smtp_config()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{cfg['sender_name']} <{cfg['sender_email']}>"
    msg["To"] = student_email
    msg.attach(MIMEText(html_body, "html"))
    
    try:
        if cfg["smtp_pass"]:
            with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
                server.starttls()
                server.login(cfg["smtp_user"], cfg["smtp_pass"])
                server.send_message(msg)
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE certificates SET email_sent = 1 WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            print(f"[SUCCESS] Certificate email delivered to {student_email} (Cert ID: {cert_id})")
        else:
            print(f"[AUTHENTICATION REQUIRED] Cannot deliver live email to {student_email} because SMTP_PASS is empty.")
            print(f"👉 Please enter your 16-character Gmail App Password into 'spvm3_smtp_config.json' or .env")
            print(f"👉 Generate at: https://myaccount.google.com/apppasswords")
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

    cfg = get_smtp_config()
    has_pass = bool(cfg["smtp_pass"])
    return jsonify({
        "success": True,
        "message": f"Certificate delivery registered for {name} ({email})",
        "cert_id": cert_id,
        "has_smtp_password": has_pass,
        "email_delivery": "live_dispatch" if has_pass else "simulation_needs_app_password"
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

@app.route('/api/smtp-status', methods=['GET'])
def smtp_status():
    cfg = get_smtp_config()
    has_pass = bool(cfg["smtp_pass"])
    masked_pass = (cfg["smtp_pass"][:2] + "****" + cfg["smtp_pass"][-2:]) if len(cfg["smtp_pass"]) >= 4 else ("****" if has_pass else "")
    return jsonify({
        "status": "ready" if has_pass else "authentication_required",
        "smtp_host": cfg["smtp_host"],
        "smtp_port": cfg["smtp_port"],
        "smtp_user": cfg["smtp_user"],
        "has_password": has_pass,
        "masked_pass": masked_pass,
        "instructions": "Set your 16-character Gmail App Password in spvm3_smtp_config.json or POST /api/smtp-config. Generate at: https://myaccount.google.com/apppasswords" if not has_pass else "Ready to deliver live emails to recipient inboxes"
    }), 200

@app.route('/api/smtp-config', methods=['POST', 'OPTIONS'])
def update_smtp_config():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    data = request.get_json(force=True) or {}
    config_file = os.path.join(os.path.dirname(__file__), "spvm3_smtp_config.json")
    
    current = get_smtp_config()
    for key in ["smtp_host", "smtp_port", "smtp_user", "smtp_pass", "sender_email", "sender_name"]:
        if key in data and str(data[key]).strip():
            current[key] = int(data[key]) if key == "smtp_port" else str(data[key]).strip()
            
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2)
        
    return jsonify({
        "success": True,
        "message": "SMTP configuration updated successfully.",
        "has_password": bool(current.get("smtp_pass"))
    }), 200

@app.route('/api/send-test-email', methods=['POST', 'OPTIONS'])
def send_test_email():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    data = request.get_json(force=True) or {}
    recipient = data.get("email", "sanjaygl3006@gmail.com").strip()
    name = data.get("name", "Sanjay GL").strip()
    
    cfg = get_smtp_config()
    if not cfg["smtp_pass"]:
        return jsonify({
            "success": False,
            "error": "SMTP_PASS is empty. Google requires a 16-character App Password to authenticate and send live emails.",
            "guide": "Go to https://myaccount.google.com/apppasswords -> Create password for 'SPVM3' -> Paste the 16 characters into spvm3_smtp_config.json"
        }), 400

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🧪 SPVM3 Tech Solution — Live SMTP Email Verification Test"
        msg["From"] = f"{cfg['sender_name']} <{cfg['sender_email']}>"
        msg["To"] = recipient
        
        body = f"""
        <html>
        <body style="font-family: sans-serif; background: #0b0f19; color: #f1f5f9; padding: 24px;">
          <div style="max-width: 540px; margin: 0 auto; background: #121a2b; border: 2px solid #10b981; border-radius: 16px; padding: 24px;">
            <h2 style="color: #10b981; margin: 0 0 10px;">✅ SMTP Email Connection Successful!</h2>
            <p>Hello <strong>{name}</strong>,</p>
            <p>This email confirms that your SPVM3 automatic email certificate engine is successfully connected and delivering live emails to <strong>{recipient}</strong>.</p>
            <p style="color: #38bdf8;">Your students will now automatically receive their official completion certificates and welcome emails directly in their Gmail inbox!</p>
            <hr style="border: none; border-top: 1px solid #1e293b; margin: 20px 0;">
            <p style="font-size: 12px; color: #94a3b8;">SPVM3 Tech Solution • ISO Certified IT Academy • Verified by Sanjay GL</p>
          </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))
        
        with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["smtp_user"], cfg["smtp_pass"])
            server.send_message(msg)
            
        return jsonify({
            "success": True,
            "message": f"Test email successfully delivered to {recipient}!"
        }), 200
    except Exception as err:
        return jsonify({
            "success": False,
            "error": f"SMTP Dispatch Error: {str(err)}",
            "tip": "Check your Gmail App Password or verify 2-Step Verification is enabled on your Google account."
        }), 500

# -----------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    print("=====================================================================")
    print("🚀 SPVM3 AUTOMATIC EMAIL CERTIFICATE SERVER IS RUNNING!")
    print("📍 Listening on: http://localhost:5000")
    print("📧 Config file: spvm3_smtp_config.json")
    print("=====================================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)


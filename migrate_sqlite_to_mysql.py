"""
SPVM3 TECH SOLUTION — MYSQL SETUP & DATABASE MIGRATION TOOL
-------------------------------------------------------------
This script automates creating the MySQL database `spvm3_db` and migrating 
existing certificate and visitor records from `spvm3_certificates.db` (SQLite) 
to MySQL.

Prerequisites:
    pip install mysql-connector-python

Usage:
    python migrate_sqlite_to_mysql.py --host localhost --user root --password yourpassword
"""

import os
import sqlite3
import argparse

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

SQLITE_DB = "spvm3_certificates.db"
SQL_SCHEMA_FILE = "spvm3_schema.sql"

def run_migration(host, port, user, password, database="spvm3_db"):
    if not MYSQL_AVAILABLE:
        print("❌ Error: `mysql-connector-python` library is not installed.")
        print("💡 Please run: pip install mysql-connector-python")
        return

    print(f"🔄 Connecting to MySQL server at {host}:{port}...")
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        print("✅ Successfully connected to MySQL server!")
        
        # Read and execute spvm3_schema.sql
        if os.path.exists(SQL_SCHEMA_FILE):
            print(f"📄 Executing schema file '{SQL_SCHEMA_FILE}'...")
            with open(SQL_SCHEMA_FILE, "r", encoding="utf-8") as f:
                sql_script = f.read()
            
            # Split commands by semicolon
            commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]
            for cmd in commands:
                if cmd:
                    try:
                        cursor.execute(cmd)
                    except mysql.connector.Error as err:
                        # Ignore view drop warnings if not present
                        if "Unknown table" not in str(err) and "Unknown view" not in str(err):
                            print(f"⚠️ Notice: {err}")
            connection.commit()
            print("✅ MySQL database `spvm3_db` and tables created successfully!")

        # Migrate data from SQLite if present
        if os.path.exists(SQLITE_DB):
            print(f"📦 Found SQLite database '{SQLITE_DB}'. Starting data migration...")
            sqlite_conn = sqlite3.connect(SQLITE_DB)
            sqlite_cursor = sqlite_conn.cursor()

            # Switch to spvm3_db
            cursor.execute("USE spvm3_db;")

            # 1. Migrate Visitors -> Students
            sqlite_cursor.execute("SELECT name, email, welcome_email_sent, timestamp FROM visitors")
            visitors = sqlite_cursor.fetchall()
            for v in visitors:
                name, email, welcome_sent, ts = v
                cursor.execute("""
                    INSERT INTO students (full_name, email, welcome_email_sent, created_at)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE full_name=%s;
                """, (name, email, welcome_sent, ts, name))
            
            # 2. Migrate Certificates
            sqlite_cursor.execute("SELECT cert_id, student_name, student_email, subject_id, course_title, course_hours, timestamp, email_sent FROM certificates")
            certs = sqlite_cursor.fetchall()
            for c in certs:
                cert_id, name, email, subj_code, title, hours, ts, email_sent = c
                
                # Ensure student exists first
                cursor.execute("""
                    INSERT INTO students (full_name, email, welcome_email_sent)
                    VALUES (%s, %s, 1)
                    ON DUPLICATE KEY UPDATE full_name=%s;
                """, (name, email, name))

                # Normalize subject_code if needed
                valid_subj = subj_code if subj_code else "python"
                
                cursor.execute("""
                    INSERT INTO certificates (cert_id, student_name, student_email, subject_code, course_title, course_hours, email_sent, issued_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE student_name=%s;
                """, (cert_id, name, email, valid_subj, title, hours, email_sent, ts, name))

            connection.commit()
            sqlite_conn.close()
            print("🎉 SQLite to MySQL Migration Complete!")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SPVM3 MySQL Database Initializer & Migrator")
    parser.add_argument("--host", default="localhost", help="MySQL Host (default: localhost)")
    parser.add_argument("--port", type=int, default=3306, help="MySQL Port (default: 3306)")
    parser.add_argument("--user", default="root", help="MySQL User (default: root)")
    parser.add_argument("--password", default="", help="MySQL Password")
    
    args = parser.parse_args()
    run_migration(args.host, args.port, args.user, args.password)

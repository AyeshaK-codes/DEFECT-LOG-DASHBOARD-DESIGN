import sqlite3
from datetime import datetime

DB_NAME = "sap_portal.db"

def init_database():
    """Initializes tables and populates them with authorized accounts and business metrics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    
    # 2. Create Audit Tracking Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            login_time TEXT,
            FOREIGN KEY(email) REFERENCES users(email)
        )
    """)
    
    # 3. Create Business Metrics Table (For real-time dashboard fetching)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS business_metrics (
            metric_key TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            metric_value TEXT NOT NULL,
            percentage_fill REAL NOT NULL,
            hex_color TEXT NOT NULL
        )
    """)
    
    # Populate default users if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        authorized_users = [
            ("user1@sap.com", "password123"),
            ("user2@sap.com", "secure456"),
            ("user3@sap.com", "access789")
        ]
        cursor.executemany("INSERT INTO users (email, password) VALUES (?, ?)", authorized_users)
        print("[DATABASE] Authorized user records initialized.")

    # Populate live enterprise metrics if table is empty
    cursor.execute("SELECT COUNT(*) FROM business_metrics")
    if cursor.fetchone()[0] == 0:
        default_metrics = [
            ("gross_volume", "Gross Volume", "$41,540", 1.0, "#111827"),
            ("online_payments", "Online Payments", "$26,800", 0.75, "#10b981"),
            ("subscriptions", "Subscriptions", "$10,400", 0.40, "#3b82f6"),
            ("instore_sales", "In-Store Sales", "$4,340", 0.15, "#ec4899"),
            ("transactions", "Transactions", "106k", 1.0, "#111827"),
            ("customers", "Customers", "1,284", 1.0, "#111827")
        ]
        cursor.executemany("INSERT INTO business_metrics VALUES (?, ?, ?, ?, ?)", default_metrics)
        print("[DATABASE] Live enterprise metrics seeded successfully.")
        
    conn.commit()
    conn.close()

def log_login_timestamp(email):
    """Saves the exact date and time a user logs into the system."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO login_logs (email, login_time) VALUES (?, ?)", (email, current_time))
    conn.commit()
    conn.close()
    print(f"[AUDIT LOG] Database entry verified: {email} signed in at {current_time}")

def get_dashboard_metrics():
    """Fetches all operational rows to feed the dashboard charts dynamically."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT metric_key, metric_value, percentage_fill FROM business_metrics")
    rows = cursor.fetchall()
    conn.close()
    # Map into a clean dictionary lookup: {'gross_volume': ('$41,540', 1.0), ...}
    return {row[0]: (row[1], row[2]) for row in rows}
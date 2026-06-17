import sqlite3

def inspect_audit_trail():
    print("=== EXAMINING SECURITY AUDIT TRAIL ===")
    conn = sqlite3.connect("sap_portal.db")
    cursor = conn.cursor()
    
    # Fetch all records from the login logs table
    cursor.execute("SELECT id, email, login_time FROM login_logs")
    logs = cursor.fetchall()
    
    if not logs:
        print("No login entries recorded yet.")
    else:
        print(f"{'ID':<5} | {'Authenticated User':<20} | {'Exact Login Time':<20}")
        print("-" * 52)
        for row in logs:
            print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<20}")
            
    conn.close()

if __name__ == "__main__":
    inspect_audit_trail()
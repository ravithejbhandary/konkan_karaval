import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all users and their passwords
cursor.execute("SELECT login_id, password FROM logins")
users = cursor.fetchall()

for login_id, password in users:
    # Check if the password is already hashed (to avoid double hashing)
    if not password.startswith("pbkdf2:sha256"):  
        hashed_password = generate_password_hash(password)
        cursor.execute("UPDATE logins SET password = ? WHERE login_id = ?", (hashed_password, login_id))
        print(f"Updated password for login_id {login_id}")

# Commit changes and close connection
conn.commit()
conn.close()

print("Passwords updated successfully!")

import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all users with plain text passwords
cursor.execute("SELECT user_id, password FROM users")
users = cursor.fetchall()

for user_id, password in users:
    if not password.startswith("scrypt:"):  # Avoid double hashing
        hashed_password = generate_password_hash(password)
        cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (hashed_password, user_id))
        print(f"Hashed password for user_id {user_id}")

conn.commit()
conn.close()

print("User passwords updated successfully!")

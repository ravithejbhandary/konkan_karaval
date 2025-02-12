import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# Database file stored in the same directory as app.py
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL, -- Store hashed password
        phone TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS family_details (
        family_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        nearest_city TEXT,
        details TEXT,
        num_children INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS interests (
        interest_id INTEGER PRIMARY KEY AUTOINCREMENT,
        family_id INTEGER NOT NULL,
        interest TEXT NOT NULL,
        FOREIGN KEY (family_id) REFERENCES family_details(family_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS logins ( 
        login_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER NOT NULL, 
        email TEXT UNIQUE NOT NULL, 
        password TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()

# Ensure database is initialized before running the app
init_db()

# Function to add a new user to the database
def add_user(name, email, password, phone, city, details, num_children, interests):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        flash("User already exists. Please log in.", "error")
        conn.close()
        return False  # Prevent duplicate registration
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    
    # Insert user details
    cursor.execute('''
        INSERT INTO users (name, email, password, phone) 
        VALUES (?, ?, ?, ?)
    ''', (name, email, hashed_password, phone))
    
    user_id = cursor.lastrowid  # Get the user ID of the newly inserted user

    # Insert family details
    cursor.execute('''
        INSERT INTO family_details (user_id, nearest_city, details, num_children) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, city, details, num_children))

    family_id = cursor.lastrowid  # Get family ID

    # Insert interests
    for interest in interests.split(","):  # Assuming interests are comma-separated
        cursor.execute('''
            INSERT INTO interests (family_id, interest) 
            VALUES (?, ?)
        ''', (family_id, interest.strip()))

    # Store login details
    cursor.execute('''
        INSERT INTO logins (user_id, email, password) 
        VALUES (?, ?, ?)
    ''', (user_id, email, hashed_password))

    conn.commit()
    conn.close()

    return True  # Registration successful


# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch user from users table
        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user:
            hashed_password = user[0]  # Extract hashed password
            
            # Check if the hashed password matches
            if check_password_hash(hashed_password, password):
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Incorrect password. Please try again.", "error")
        else:
            flash("User email does not exist. Please register first.", "error")

    return render_template('login.html')  # Stay on the same page if login fails




# Registration route
# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # Store hashed password in production
        phone = request.form['phone']
        city = request.form['city']
        details = request.form.get('family_details', '')
        num_children = request.form.get('children_count', 0)
        interests = request.form.get('interests', '')

        # Check if the user already exists before calling add_user
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        conn.close()

        if existing_user:
            flash("User already exists. Please log in.", "error")
            return redirect(url_for('login'))  # Redirect to login instead of showing duplicate messages

        # Add user to database
        success = add_user(name, email, password, phone, city, details, num_children, interests)

        if success:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))  # Redirect to login after successful registration

        flash("Registration failed. Try again.", "error")

    return render_template('JoinFamReg.html')



# Forgot Password Route
@app.route('/forgot-password')
def forgot_password():
    return "Forgot Password Page Coming Soon!"

if __name__ == '__main__':
    app.run(debug=True)

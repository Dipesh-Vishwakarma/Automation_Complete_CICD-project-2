import os
import time
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask application
# Templates are automatically served from the 'templates' directory
# Static files (CSS, JS) are automatically served from the 'static' directory
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure Flask secret key from environment variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')

# MySQL Configuration from docker-compose environment variables
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'db'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', 'root'),
    'database': os.environ.get('MYSQL_DATABASE', 'registration_db'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    """Get MySQL database connection"""
    if 'db' not in g:
        g.db = pymysql.connect(**MYSQL_CONFIG)
    return g.db

def get_db_without_database():
    """Get MySQL connection without specifying database (for creating databases)"""
    config = MYSQL_CONFIG.copy()
    config.pop('database', None)
    return pymysql.connect(**config)

@app.teardown_appcontext
def close_db(error):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_database():
    """Initialize main database and create users table if it doesn't exist"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Test database connection
            conn = pymysql.connect(**MYSQL_CONFIG)
            cur = conn.cursor()
            
            # Create users table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cur.close()
            conn.close()
            
            print("Main database initialized successfully!")
            print(f"Users table created/verified in database: {MYSQL_CONFIG['database']}")
            return True
            
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                print(f"Failed to initialize database after {max_retries} attempts: {str(e)}")
                raise
            print(f"Waiting for MySQL to be ready... (Attempt {retry_count}/{max_retries})")
            time.sleep(2)
    
    return False

def create_user_database(username):
    """Create a database for the specific username and initialize user_data table"""
    try:
        # Connect without specifying database
        conn = get_db_without_database()
        cur = conn.cursor()
        
        # Sanitize username for database name (only alphanumeric and underscore)
        db_name = f"user_{username.lower().replace(' ', '_').replace('-', '_')}"
        # Remove any special characters
        db_name = ''.join(c for c in db_name if c.isalnum() or c == '_')
        
        # Create database for the user
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        conn.commit()
        
        # Switch to the user's database
        cur.execute(f"USE `{db_name}`")
        
        # Create user_data table in the user's database
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_key VARCHAR(255) NOT NULL,
                data_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_data_key (data_key)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Created database '{db_name}' for user '{username}'")
        print(f"Created user_data table in database '{db_name}'")
        return db_name
        
    except Exception as e:
        print(f"Error creating user database: {str(e)}")
        raise

@app.route('/')
def home():
    """Home/Welcome page - shows username if logged in, otherwise redirects to login"""
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        
        try:
            db = get_db()
            cur = db.cursor()
            
            # Insert user into main users table
            cur.execute(
                "INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            db.commit()
            cur.close()
            
            # Create user-specific database and table
            try:
                user_db_name = create_user_database(username)
                print(f"User '{username}' registered successfully with database '{user_db_name}'")
            except Exception as e:
                print(f"Warning: User registered but database creation failed: {str(e)}")
            
            return redirect(url_for('login'))
        except Exception as e:
            error_msg = "Registration failed. Username or email may already exist."
            print(f"Registration error: {str(e)}")
            return render_template('registration.html', error=error_msg)
    
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cur.fetchone()
            cur.close()
            
            if user and check_password_hash(user['password'], password):
            #if user and user['password'] == password:
                session['username'] = username
                return redirect(url_for('home'))
            
            return render_template('login.html', error="Invalid username or password")
        except Exception as e:
            print(f"Login error: {str(e)}")
            return render_template('login.html', error="Login failed. Please try again.")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Initialize database before starting the app
    print("Starting Flask application...")
    print(f"Connecting to MySQL at {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}")
    print(f"Database: {MYSQL_CONFIG['database']}")
    
    init_database()
    
    print("Flask app is ready!")

    app.run(host="0.0.0.0", port=5000, debug=False)

import os
import time
import logging
import psycopg2

from psycopg2.extras import RealDictCursor
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    g
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ---------------------------------------------------
# Flask App Initialization
# ---------------------------------------------------

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# Secret Key Configuration
# ---------------------------------------------------

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY environment variable not set")

# ---------------------------------------------------
# Flask Session Security
# ---------------------------------------------------

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ---------------------------------------------------
# PostgreSQL Configuration
# ---------------------------------------------------

DB_CONFIG = {
    "host": os.environ.get("POSTGRES_HOST"),
    "database": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "port": os.environ.get("POSTGRES_PORT", 5432)
}

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------

def get_db():

    if 'db' not in g:

        g.db = psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port'],
            cursor_factory=RealDictCursor,
            connect_timeout=5
        )

    return g.db

# ---------------------------------------------------
# Close Database Connection
# ---------------------------------------------------

@app.teardown_appcontext
def close_db(error):

    db = g.pop('db', None)

    if db is not None:
        db.close()

# ---------------------------------------------------
# Database Initialization
# ---------------------------------------------------

def init_database():

    retries = 20

    while retries > 0:

        try:

            conn = psycopg2.connect(
                host=DB_CONFIG['host'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                port=DB_CONFIG['port'],
                cursor_factory=RealDictCursor,
                connect_timeout=5
            )

            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

            cur.close()
            conn.close()

            logger.info("DATABASE_INITIALIZED")

            return

        except Exception as e:

            logger.warning(
                f"POSTGRES_WAITING error={str(e)}"
            )

            retries -= 1

            time.sleep(5)

    raise Exception("Database initialization failed")

# ---------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------

@app.route("/health")
def health():

    return {
        "status": "healthy"
    }, 200

# ---------------------------------------------------
# Home Route
# ---------------------------------------------------

@app.route('/')
def home():

    if 'username' in session:

        return render_template(
            'index.html',
            username=session['username']
        )

    return redirect(url_for('login'))

# ---------------------------------------------------
# Registration Route
# ---------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:

            db = get_db()

            cur = db.cursor()

            cur.execute(
                """
                INSERT INTO users(username, email, password)
                VALUES (%s, %s, %s)
                """,
                (username, email, hashed_password)
            )

            db.commit()

            cur.close()

            logger.info(
                f"REGISTER_SUCCESS user={username}"
            )

            return redirect(url_for('login'))

        except Exception as e:

            try:
                db.rollback()
            except:
                pass

            logger.error(
                f"REGISTER_FAILED user={username} error={str(e)}"
            )

            return render_template(
                'registration.html',
                error="Registration failed. Username or email may already exist."
            )

    return render_template('registration.html')

# ---------------------------------------------------
# Login Route
# ---------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username'].strip()
        password = request.form['password']

        try:

            db = get_db()

            cur = db.cursor()

            cur.execute(
                """
                SELECT * FROM users
                WHERE username = %s
                """,
                (username,)
            )

            user = cur.fetchone()

            cur.close()

            if user and check_password_hash(
                user['password'],
                password
            ):

                session['username'] = username

                logger.info(
                    f"LOGIN_SUCCESS user={username}"
                )

                return redirect(url_for('home'))

            logger.warning(
                f"LOGIN_FAILED user={username}"
            )

            return render_template(
                'login.html',
                error="Invalid username or password"
            )

        except Exception as e:

            logger.error(
                f"LOGIN_ERROR user={username} error={str(e)}"
            )

            return render_template(
                'login.html',
                error="Login failed. Please try again."
            )

    return render_template('login.html')

# ---------------------------------------------------
# Logout Route
# ---------------------------------------------------

@app.route('/logout')
def logout():

    username = session.get('username', 'unknown')

    session.clear()

    logger.info(
        f"LOGOUT_SUCCESS user={username}"
    )

    return redirect(url_for('login'))

# ---------------------------------------------------
# Initialize Database on Startup
# ---------------------------------------------------

init_database()

logger.info("FLASK_APPLICATION_READY")

# ---------------------------------------------------
# Main Entry Point
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

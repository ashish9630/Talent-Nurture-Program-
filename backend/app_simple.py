from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import pymysql
from functools import wraps
import bcrypt
import pytz

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'rental_portal_secret_key_2024'

def get_indian_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

# Database Connection
def get_db_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Ashish@9630',
            database='rental',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def init_database():
    conn = get_db_connection()
    if not conn:
        print("Cannot connect to database. Please check MySQL is running.")
        return
        
    cursor = conn.cursor()
    
    # Create users table (compatible with both schemas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        )
    ''')
    
    # Create flats table (simple version)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            flat_no VARCHAR(50) UNIQUE NOT NULL,
            rent DECIMAL(10,2) NOT NULL,
            location VARCHAR(255) NOT NULL,
            available BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(255),
            flat_no VARCHAR(50),
            status VARCHAR(50) DEFAULT 'pending',
            created_at VARCHAR(100)
        )
    ''')
    
    # Insert sample data
    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", 
                      ('admin@rental.com', 'admin123', 'admin'))
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", 
                      ('user@rental.com', 'user123', 'user'))
        
        cursor.execute("INSERT INTO flats (flat_no, rent, location) VALUES (%s, %s, %s)", 
                      ('A101', 25000, 'Sector 32'))
        cursor.execute("INSERT INTO flats (flat_no, rent, location) VALUES (%s, %s, %s)", 
                      ('B202', 18000, 'Sector 60'))
    except pymysql.IntegrityError:
        pass
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# JWT Decorators
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token is missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"message": "Invalid token format"}), 401

        token = parts[1]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 401

        request.user = data
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Rental Portal Backend Running Successfully!"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    role = data.get('role', 'user')

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", 
                      (email, password, role))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"})
    except pymysql.IntegrityError:
        conn.close()
        return jsonify({"message": "Email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    cursor.execute("SELECT email, password, role FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and user['password'] == password:
        token = jwt.encode({
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/flats', methods=['GET'])
def get_flats():
    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flats ORDER BY id")
    flats = cursor.fetchall()
    conn.close()
    return jsonify(flats)

@app.route('/book-flat', methods=['POST'])
@token_required 
def book_flat():
    data = request.json
    email = request.user['email']
    flat_no = data['flat_no']

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500
        
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (user_email, flat_no, created_at) VALUES (%s, %s, %s)",
                  (email, flat_no, get_indian_time()))
    conn.commit()
    conn.close()
    return jsonify({"message": "Booking request sent"})

if __name__ == '__main__':
    print("Starting Rental Portal Backend...")
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
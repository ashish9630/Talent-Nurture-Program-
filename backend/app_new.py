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
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Ashish@9630',
        database='rental',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create register table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS register (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('USER', 'ADMIN') NOT NULL DEFAULT 'USER',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    # Create flats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            flat_no VARCHAR(50) UNIQUE NOT NULL,
            flat_type VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            status ENUM('Available', 'Booked') DEFAULT 'Available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    # Create booking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            flat_no VARCHAR(50) NOT NULL,
            status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES register(email) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (flat_no) REFERENCES flats(flat_no) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
    
    # Create admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_email VARCHAR(255) NOT NULL,
            admin_password VARCHAR(255) NOT NULL,
            approved_user_id INT,
            approval_status ENUM('Approved', 'Not Approved') DEFAULT 'Not Approved',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_email) REFERENCES register(email) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (approved_user_id) REFERENCES register(id) ON DELETE SET NULL ON UPDATE CASCADE
        )
    ''')
    
    # Insert sample admin user (password: admin123)
    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO register (email, password, role) VALUES (%s, %s, %s)",
            ('admin@rental.com', admin_password.decode('utf-8'), 'ADMIN')
        )
    except pymysql.IntegrityError:
        pass
    
    # Insert sample user (password: user123)
    user_password = bcrypt.hashpw('user123'.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO register (email, password, role) VALUES (%s, %s, %s)",
            ('user@rental.com', user_password.decode('utf-8'), 'USER')
        )
    except pymysql.IntegrityError:
        pass
    
    # Insert sample flats
    sample_flats = [
        ('A101', '1BHK', 15000.00, 'Available'),
        ('A102', '2BHK', 25000.00, 'Available'),
        ('A103', '3BHK', 35000.00, 'Available'),
        ('B201', '1BHK', 18000.00, 'Available'),
        ('B202', '2BHK', 28000.00, 'Available')
    ]
    
    for flat in sample_flats:
        try:
            cursor.execute(
                "INSERT INTO flats (flat_no, flat_type, price, status) VALUES (%s, %s, %s, %s)",
                flat
            )
        except pymysql.IntegrityError:
            pass
    
    conn.commit()
    conn.close()

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

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user.get('role') != 'ADMIN':
            return jsonify({"message": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Flat Booking System Backend Running Successfully!"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password'].encode('utf-8')
    role = data.get('role', 'USER').upper()
    
    # Validate role
    if role not in ['USER', 'ADMIN']:
        return jsonify({"message": "Invalid role. Must be USER or ADMIN"}), 400

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO register (email, password, role) VALUES (%s, %s, %s)",
            (email, hashed_password.decode('utf-8'), role)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": f"{role} registered successfully"})
    except pymysql.IntegrityError:
        conn.close()
        return jsonify({"message": "Email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password'].encode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, password, role FROM register WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            "token": token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "role": user['role']
            }
        })

    return jsonify({"message": "Email ID and Password is Invalid"}), 401

@app.route('/flats', methods=['GET'])
def get_flats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, flat_no, flat_type, price, status, created_at, updated_at
        FROM flats ORDER BY id
    ''')
    flats = cursor.fetchall()
    conn.close()
    
    result = []
    for flat in flats:
        result.append({
            "id": flat['id'],
            "flat_no": flat['flat_no'],
            "flat_type": flat['flat_type'],
            "price": float(flat['price']),
            "status": flat['status'],
            "created_at": str(flat['created_at']),
            "updated_at": str(flat['updated_at'])
        })
    return jsonify(result)

@app.route('/book-flat', methods=['POST'])
@token_required 
def book_flat():
    data = request.json
    user_email = request.user['email']
    flat_no = data['flat_no']

    # Check if flat is available
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM flats WHERE flat_no=%s", (flat_no,))
    flat = cursor.fetchone()
    
    if not flat:
        conn.close()
        return jsonify({"message": "Flat not found"}), 404
    
    if flat['status'] != 'Available':
        conn.close()
        return jsonify({"message": "Flat is not available"}), 400

    # Create booking
    cursor.execute(
        "INSERT INTO booking (user_email, flat_no) VALUES (%s, %s)",
        (user_email, flat_no)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking request sent successfully"})

@app.route('/my-bookings', methods=['GET'])
@token_required
def my_bookings():
    user_email = request.user['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.id as booking_id, b.flat_no, f.flat_type, f.price, b.status, b.created_at, b.updated_at
        FROM booking b
        JOIN flats f ON b.flat_no = f.flat_no
        WHERE b.user_email = %s
        ORDER BY b.created_at DESC
    ''', (user_email,))
    bookings = cursor.fetchall()
    conn.close()

    result = []
    for b in bookings:
        result.append({
            "booking_id": b['booking_id'],
            "flat_no": b['flat_no'],
            "flat_type": b['flat_type'],
            "price": float(b['price']),
            "status": b['status'],
            "created_at": str(b['created_at']),
            "updated_at": str(b['updated_at'])
        })

    return jsonify(result)

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=8081)
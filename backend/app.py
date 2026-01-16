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
app.config['SECRET_KEY'] = 'secret123'

def get_indian_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(ist).strftime('%m/%d/%y, %I:%M:%S %p')

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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            flat_no VARCHAR(50) UNIQUE NOT NULL,
            rent DECIMAL(10,2) NOT NULL,
            location VARCHAR(255) NOT NULL,
            available BOOLEAN DEFAULT TRUE,
            bedrooms INT NOT NULL,
            bathrooms INT NOT NULL,
            area_sqft INT NOT NULL,
            swimming_pool BOOLEAN DEFAULT FALSE,
            car_parking BOOLEAN DEFAULT FALSE,
            bike_parking BOOLEAN DEFAULT FALSE,
            gym BOOLEAN DEFAULT FALSE,
            garden BOOLEAN DEFAULT FALSE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_email VARCHAR(255),
            flat_no VARCHAR(50),
            status VARCHAR(50) DEFAULT 'pending',
            created_at VARCHAR(100),
            updated_at VARCHAR(100)
        )
    ''')
    
    # Sample admin user (password: admin123)
    try:
        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
            ('admin@rental.com', 'admin123', 'admin')
        )
    except pymysql.IntegrityError:
        pass
    
    # Sample user (password: user123)
    try:
        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
            ('user@rental.com', 'user123', 'user')
        )
    except pymysql.IntegrityError:
        pass
    
    # Add sample flats 
    sample_flats = [
        ('A101', 25000, 'Sector 32', 2, 2, 1200, True, True, True, False, False),
        ('B202', 18000, 'Sector 60', 1, 1, 800, False, True, True, True, False),
        ('C303', 35000, 'Sector 21', 3, 2, 1500, True, True, True, True, True),
        ('D404', 30000, 'Sector 30', 3, 2, 1000, True, True, True, True, True),
        ('E505', 31000, 'Sector 35', 3, 2, 1700, True, True, True, True, True),
        ('F606', 21000, 'Sector 50', 3, 2, 1500, True, True, True, True, True),
        ('G707', 35000, 'Sector 36', 3, 2, 1500, True, True, True, True, True),
        ('H808', 35000, 'Sector 31', 3, 2, 1500, True, True, True, True, True),
        ('A202', 35000, 'Sector 23', 3, 2, 1500, True, True, True, True, True)
        
    ]
    
    for flat in sample_flats:
        try:
            cursor.execute(
                "INSERT INTO flats (flat_no, rent, location, bedrooms, bathrooms, area_sqft, swimming_pool, car_parking, bike_parking, gym, garden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
        if request.user.get('role') != 'admin':
            return jsonify({"message": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Backend running successfully!!"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    role = data.get('role', 'user')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
            (email, password, role)
        )
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
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, password, role FROM users WHERE email=%s",
        (email,)
    )
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
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, flat_no, rent, location, available, bedrooms, bathrooms, area_sqft,
               swimming_pool, car_parking, bike_parking, gym, garden
        FROM flats ORDER BY id
    ''')
    flats = cursor.fetchall()
    conn.close()
    
    result = []
    for flat in flats:
        result.append({
            "id": flat['id'],
            "flat_no": flat['flat_no'],
            "rent": float(flat['rent']),
            "location": flat['location'],
            "available": bool(flat['available']),
            "amenities": {
                "swimming_pool": bool(flat['swimming_pool']),
                "car_parking": bool(flat['car_parking']),
                "bike_parking": bool(flat['bike_parking']),
                "gym": bool(flat['gym']),
                "garden": bool(flat['garden'])
            },
            "bedrooms": flat['bedrooms'],
            "bathrooms": flat['bathrooms'],
            "area_sqft": flat['area_sqft']
        })
    return jsonify(result)

@app.route('/book-flat', methods=['POST'])
@token_required 
def book_flat():
    data = request.json
    email = request.user['email']
    flat_no = data['flat_no']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (user_email, flat_no, created_at) VALUES (%s, %s, %s)",
        (email, flat_no, get_indian_time())
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking request sent"})

@app.route('/my-bookings', methods=['GET'])
@token_required
def my_bookings():
    user_email = request.user['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, flat_no, status, created_at, updated_at FROM bookings WHERE user_email=%s ORDER BY created_at DESC",
        (user_email,)
    )
    bookings = cursor.fetchall()
    conn.close()

    result = []
    for b in bookings:
        result.append({
            "booking_id": b['id'],
            "flat_no": b['flat_no'],
            "status": b['status'],
            "created_at": str(b['created_at']),
            "updated_at": str(b['updated_at']) if b['updated_at'] else None
        })

    return jsonify(result)

@app.route('/admin/bookings', methods=['GET'])
@token_required
@admin_required
def admin_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_email, flat_no, status, created_at, updated_at FROM bookings ORDER BY created_at DESC"
    )
    bookings = cursor.fetchall()
    conn.close()

    result = []
    for b in bookings:
        result.append({
            "booking_id": b['id'],
            "user_email": b['user_email'],
            "flat_no": b['flat_no'],
            "status": b['status'],
            "created_at": str(b['created_at']),
            "updated_at": str(b['updated_at']) if b['updated_at'] else None
        })
    return jsonify(result)

@app.route('/admin/update-status', methods=['POST'])
@token_required
@admin_required
def update_status():
    data = request.json
    booking_id = data['booking_id']
    new_status = data['status']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bookings SET status=%s, updated_at=%s WHERE id=%s",
        (new_status, get_indian_time(), booking_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"Status updated to {new_status}"})

@app.route('/admin/add-flat', methods=['POST'])
@token_required
@admin_required
def add_flat():
    data = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO flats (flat_no, rent, location, bedrooms, bathrooms, area_sqft, swimming_pool, car_parking, bike_parking, gym, garden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['flat_no'], data['rent'], data['location'], data['bedrooms'], data['bathrooms'], data['area_sqft'], 
             data.get('swimming_pool', False), data.get('car_parking', False), data.get('bike_parking', False), 
             data.get('gym', False), data.get('garden', False))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Flat added successfully"})
    except pymysql.IntegrityError:
        conn.close()
        return jsonify({"message": "Flat number already exists"}), 400

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5000)
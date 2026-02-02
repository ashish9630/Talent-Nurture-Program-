from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
import datetime
import pymysql
from functools import wraps
import pytz
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret123'

def get_indian_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.datetime.now(ist).strftime('%m/%d/%y, %I:%M:%S %p')

def get_db_connection():
    import os
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'Ashish@9630'),
        database=os.getenv('DB_NAME', 'rental'),
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
            garden BOOLEAN DEFAULT FALSE,
            image_url VARCHAR(255) DEFAULT NULL
        )
    ''')
    
    # Add image_url column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE flats ADD COLUMN image_url VARCHAR(255) DEFAULT NULL")
        conn.commit()
    except pymysql.err.OperationalError:
        pass  # Column already exists
    
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
    
    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", ('admin@rental.com', 'admin123', 'admin'))
    except pymysql.IntegrityError:
        pass
    
    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", ('user@rental.com', 'user123', 'user'))
    except pymysql.IntegrityError:
        pass
    
    # Update existing flats with image URLs
    cursor.execute("UPDATE flats SET image_url = '/images/flat1.jpg' WHERE flat_no = 'A101'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat2.jpg' WHERE flat_no = 'B202'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat3.jpg' WHERE flat_no = 'C303'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat4.jpg' WHERE flat_no = 'D404'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat5.jpg' WHERE flat_no = 'E505'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat6.jpg' WHERE flat_no = 'F606'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat7.jpg' WHERE flat_no = 'G707'")
    cursor.execute("UPDATE flats SET image_url = '/images/flat8.jpg' WHERE flat_no = 'H808'")
    
    sample_flats = [
        ('A101', 25000, 'Sector 32', 2, 2, 1200, True, True, True, False, False, '/images/flat1.jpg'),
        ('B202', 18000, 'Sector 60', 1, 1, 800, False, True, True, True, False, '/images/flat2.jpg'),
        ('C303', 35000, 'Sector 21', 3, 2, 1500, True, True, True, True, True, '/images/flat3.jpg'),
        ('D404', 30000, 'Sector 22', 3, 2, 1500, True, True, True, True, True, '/images/flat4.jpg'),
        ('E505', 25000, 'Sector 32', 2, 2, 1200, True, True, True, False, False, '/images/flat5.jpg'),
        ('F606', 18000, 'Sector 60', 1, 1, 800, False, True, True, True, False, '/images/flat6.jpg'),
        ('G707', 35000, 'Sector 21', 3, 2, 1500, True, True, True, True, True, '/images/flat7.jpg'),
        ('H808', 30000, 'Sector 22', 3, 2, 1500, True, True, True, True, True, '/images/flat8.jpg')
    ]
    
    for flat in sample_flats:
        try:
            cursor.execute("INSERT INTO flats (flat_no, rent, location, bedrooms, bathrooms, area_sqft, swimming_pool, car_parking, bike_parking, gym, garden, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", flat)
        except pymysql.IntegrityError:
            pass
    
    conn.commit()
    conn.close()

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
        cursor.execute("INSERT INTO users (email, password, role) VALUES (%s, %s, %s)", (email, password, role))
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
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flats ORDER BY id")
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
            "area_sqft": flat['area_sqft'],
            "image_url": flat.get('image_url', '/images/default-flat.jpg')
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
    cursor.execute("INSERT INTO bookings (user_email, flat_no, created_at) VALUES (%s, %s, %s)", (email, flat_no, get_indian_time()))
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking request sent"})

@app.route('/my-bookings', methods=['GET'])
@token_required
def my_bookings():
    user_email = request.user['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, flat_no, status, created_at, updated_at FROM bookings WHERE user_email=%s ORDER BY created_at DESC", (user_email,))
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
    cursor.execute("SELECT id, user_email, flat_no, status, created_at, updated_at FROM bookings ORDER BY created_at DESC")
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

@app.route('/admin/update-booking-status', methods=['POST'])
@token_required
@admin_required
def update_booking_status():
    print("=== UPDATE BOOKING STATUS CALLED ===")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request data: {request.json}")
    
    try:
        data = request.json
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({"success": False, "message": "No data provided"}), 400
            
        booking_id = data.get('booking_id')
        status = data.get('status')
        
        print(f"Booking ID: {booking_id}, Status: {status}")
        
        if not booking_id or not status:
            print("ERROR: Missing booking_id or status")
            return jsonify({"success": False, "message": "Missing data"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status=%s, updated_at=%s WHERE id=%s", (status, get_indian_time(), booking_id))
        conn.commit()
        conn.close()
        
        print("SUCCESS: Booking updated successfully")
        return jsonify({"success": True, "message": "Status updated successfully"})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/admin/update-status', methods=['POST'])
@token_required
@admin_required
def update_status():
    return update_booking_status()

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
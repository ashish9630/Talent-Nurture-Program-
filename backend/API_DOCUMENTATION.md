# 🏠 FLAT BOOKING SYSTEM - API DOCUMENTATION

## 📋 Database Structure

### 1. **register** table
```sql
- id (Primary Key, Auto Increment)
- email (Unique, Not Null)
- password (Hashed)
- role (ENUM: 'USER', 'ADMIN')
- created_at (Timestamp)
- updated_at (Timestamp)
```

### 2. **flats** table
```sql
- id (Primary Key, Auto Increment)
- flat_no (Unique, Not Null)
- flat_type (VARCHAR: '1BHK', '2BHK', '3BHK')
- price (Decimal)
- status (ENUM: 'Available', 'Booked')
- created_at (Timestamp)
- updated_at (Timestamp)
```

### 3. **booking** table
```sql
- id (Primary Key, Auto Increment)
- user_email (Foreign Key → register.email)
- flat_no (Foreign Key → flats.flat_no)
- status (ENUM: 'Pending', 'Approved', 'Rejected')
- created_at (Timestamp)
- updated_at (Timestamp)
```

### 4. **admin** table
```sql
- id (Primary Key, Auto Increment)
- admin_email (Foreign Key → register.email)
- admin_password (VARCHAR)
- approved_user_id (Foreign Key → register.id)
- approval_status (ENUM: 'Approved', 'Not Approved')
- created_at (Timestamp)
- updated_at (Timestamp)
```

---

## 🔗 API Endpoints

### **Authentication APIs**

#### 1. Register User
```http
POST /register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123",
    "role": "USER"  // or "ADMIN"
}
```

**Response:**
```json
{
    "message": "USER registered successfully"
}
```

#### 2. Login
```http
POST /login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

**Success Response:**
```json
{
    "token": "jwt_token_here",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "role": "USER"
    }
}
```

**Error Response:**
```json
{
    "message": "Email ID and Password is Invalid"
}
```

---

### **Flats APIs**

#### 3. Get All Flats
```http
GET /flats
```

**Response:**
```json
[
    {
        "id": 1,
        "flat_no": "A101",
        "flat_type": "1BHK",
        "price": 15000.00,
        "status": "Available",
        "created_at": "2024-01-11 12:00:00",
        "updated_at": "2024-01-11 12:00:00"
    }
]
```

---

### **Booking APIs**

#### 4. Book a Flat
```http
POST /book-flat
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "flat_no": "A101"
}
```

**Response:**
```json
{
    "message": "Booking request sent successfully"
}
```

#### 5. Get My Bookings
```http
GET /my-bookings
Authorization: Bearer <jwt_token>
```

**Response:**
```json
[
    {
        "booking_id": 1,
        "flat_no": "A101",
        "flat_type": "1BHK",
        "price": 15000.00,
        "status": "Pending",
        "created_at": "2024-01-11 12:00:00",
        "updated_at": "2024-01-11 12:00:00"
    }
]
```

---

### **Admin APIs**

#### 6. Get All Bookings (Admin Only)
```http
GET /admin/bookings
Authorization: Bearer <admin_jwt_token>
```

**Response:**
```json
[
    {
        "booking_id": 1,
        "user_email": "user@example.com",
        "user_role": "USER",
        "flat_no": "A101",
        "flat_type": "1BHK",
        "price": 15000.00,
        "status": "Pending",
        "created_at": "2024-01-11 12:00:00",
        "updated_at": "2024-01-11 12:00:00"
    }
]
```

#### 7. Update Booking Status (Admin Only)
```http
POST /admin/update-booking-status
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json

{
    "booking_id": 1,
    "status": "Approved"  // or "Rejected", "Pending"
}
```

**Response:**
```json
{
    "message": "Booking status updated to Approved"
}
```

#### 8. Add New Flat (Admin Only)
```http
POST /admin/add-flat
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json

{
    "flat_no": "C301",
    "flat_type": "2BHK",
    "price": 22000.00,
    "status": "Available"
}
```

**Response:**
```json
{
    "message": "Flat added successfully"
}
```

#### 9. Get All Users (Admin Only)
```http
GET /admin/users
Authorization: Bearer <admin_jwt_token>
```

**Response:**
```json
[
    {
        "id": 2,
        "email": "user@example.com",
        "role": "USER",
        "created_at": "2024-01-11 12:00:00",
        "updated_at": "2024-01-11 12:00:00"
    }
]
```

#### 10. Approve/Reject User (Admin Only)
```http
POST /admin/approve-user
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json

{
    "user_id": 2,
    "approval_status": "Approved"  // or "Not Approved"
}
```

**Response:**
```json
{
    "message": "User approved successfully"
}
```

---

## 🔐 Authentication Logic

### Login Validation:
1. User enters email and password
2. System checks if email exists in `register` table
3. System verifies password using bcrypt
4. If valid → Generate JWT token
5. If invalid → Show "Email ID and Password is Invalid"

### Role-Based Access:
- **USER**: Can view flats, book flats, view own bookings
- **ADMIN**: All USER permissions + manage bookings, add flats, approve users

---

## 🎯 Business Logic

### Booking Flow:
1. User selects available flat
2. System creates booking with status "Pending"
3. Admin reviews booking
4. Admin approves/rejects booking
5. If approved → Flat status changes to "Booked"
6. If rejected → Flat remains "Available"

### Admin Approval Flow:
1. Admin views all registered users
2. Admin can approve/reject users
3. Approval status stored in `admin` table
4. Users can be tracked for approval history

---

## 🚀 Sample Data

### Default Users:
- **Admin**: admin@rental.com / admin123
- **User**: user@rental.com / user123

### Sample Flats:
- A101 (1BHK) - ₹15,000
- A102 (2BHK) - ₹25,000
- A103 (3BHK) - ₹35,000
- B201 (1BHK) - ₹18,000
- B202 (2BHK) - ₹28,000

---

## 📊 Database Relationships

```
register (1) ←→ (M) booking
flats (1) ←→ (M) booking
register (1) ←→ (M) admin
register (1) ←→ (1) admin (approved_user_id)
```

---

## ⚡ Features Implemented

✅ User Registration with Role Selection (USER/ADMIN)  
✅ Secure Login with JWT Authentication  
✅ Password Hashing with bcrypt  
✅ Role-Based Access Control  
✅ Flat Management System  
✅ Booking Request System  
✅ Admin Approval/Rejection  
✅ User Approval System  
✅ Automatic Flat Status Updates  
✅ Foreign Key Constraints  
✅ Proper Error Handling  
✅ Indian Timezone Support  

---

## 🛠️ Setup Instructions

1. **Install Dependencies:**
```bash
pip install flask flask-cors pymysql bcrypt pyjwt pytz
```

2. **Setup MySQL Database:**
```sql
CREATE DATABASE rental_portal;
```

3. **Update Database Credentials in app_new.py:**
```python
host='localhost'
user='root'
password='Singh@123'
database='rental_portal'
```

4. **Run the Application:**
```bash
python app_new.py
```

5. **Server will start at:** http://localhost:8081

---

## 🔧 Testing the APIs

Use Postman or any API testing tool to test the endpoints. Make sure to:

1. Register users with different roles
2. Login to get JWT tokens
3. Use tokens in Authorization header: `Bearer <token>`
4. Test all CRUD operations
5. Verify role-based access control

---

**🎉 Your Complete Flat Booking System is Ready!**
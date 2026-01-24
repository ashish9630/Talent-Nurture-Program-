# Rental Portal Backend (Flask)

This project is a backend application built using **Python Flask** for managing a rental flat booking system.  
It provides secure authentication, role-based access control, and RESTful APIs for users and administrators.

---

## 🚀 Features

- User Registration and Login
- JWT-based Authentication
- Secure Password Hashing using bcrypt
- Role-Based Access Control (Admin / User)
- View Available Flats with Amenities
- Flat Booking Request System
- Admin Approval / Rejection of Bookings
- SQLite Database (Easily Migratable to PostgreSQL)
- REST API Architecture
- CORS Enabled (Frontend Ready)

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Authentication:** JWT (PyJWT)
- **Security:** bcrypt
- **Timezone Handling:** pytz
- **API Style:** RESTful APIs

---

## 🗂️ Database Design

- **Users Table**
  - Stores user credentials and roles
- **Flats Table**
  - Stores flat details, rent, amenities, and availability
- **Bookings Table**
  - Stores booking requests and status

---

## 🔐 Security

- Passwords are never stored in plain text
- JWT tokens are used for secure authentication
- Admin-only routes are protected using decorators

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/rental-portal-backend-flask.git
cd rental-portal-backend-flask

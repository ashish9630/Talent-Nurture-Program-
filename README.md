# 🏠 Rental Portal - Full Stack Web Application

A complete **Flat Booking System** built with **Flask (Backend)** and **Angular (Frontend)** with **MySQL** database. Features include user authentication, role-based access control, flat management, and booking system.

## 🚀 Live Demo

- **Frontend:** [Live Demo Link]
- **Backend API:** [API Documentation]



## ✨ Features

### 🔐 Authentication & Security
- User Registration & Login
- JWT Token-based Authentication
- Password Hashing with bcrypt
- Role-based Access Control (USER/ADMIN)

### 🏢 Flat Management
- View Available Flats
- Flat Details with Pricing
- Real-time Availability Status
- Admin Flat Management

### 📋 Booking System
- Flat Booking Requests
- Booking Status Tracking
- Admin Approval/Rejection
- Booking History

### 👨‍💼 Admin Panel
- Manage All Bookings
- User Management
- Flat Inventory Control
- Dashboard Analytics

## 🛠️ Tech Stack

### Backend
- **Framework:** Python Flask
- **Database:** MySQL
- **Authentication:** JWT (PyJWT)
- **Security:** bcrypt
- **API:** RESTful APIs
- **CORS:** Flask-CORS

### Frontend
- **Framework:** Angular 17
- **Language:** TypeScript
- **Styling:** CSS3, Bootstrap
- **HTTP Client:** Angular HttpClient
- **Routing:** Angular Router

### DevOps & Deployment
- **Containerization:** Docker & Docker Compose
- **Cloud:** Google Cloud Platform (Cloud Run, Cloud SQL)
- **CI/CD:** Google Cloud Build

## 📁 Project Structure

```
Web-of-hostel/
├── backend/
│   ├── app_new.py          # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── rental frontend/
│   ├── src/
│   │   ├── app/           # Angular components
│   │   └── services/      # API services
│   ├── package.json       # Node dependencies
│   └── Dockerfile        # Frontend container
├── docker-compose.yml     # Multi-container setup
├── cloudbuild.yaml       # Google Cloud Build
└── README.md             # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- MySQL 8.0+
- Docker (optional)

### 1. Clone Repository
```bash
git clone https://github.com/ashish9630/Talent-Nurture-Program-.git
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Configure MySQL database
mysql -u root -p
CREATE DATABASE rental;

# Update database credentials in app_new.py
python app_new.py
```

### 3. Frontend Setup
```bash
cd "rental frontend"
npm install
ng serve
```

### 4. Access Application
- **Frontend:** http://localhost:4200
- **Backend:** http://localhost:5000

## 🐳 Docker Deployment

### Local Development
```bash
docker-compose up --build
```

### Production Deployment
```bash
# Google Cloud Platform
./deploy-gcp.bat

# Or manual deployment
docker build -t rental-backend ./backend
docker build -t rental-frontend ./rental frontend
```

## 📊 Database Schema

### Tables
- **register** - User accounts and roles
- **flats** - Flat inventory and details
- **booking** - Booking requests and status
- **admin** - Admin management records

### Sample Data
```sql
-- Default Admin
Email: admin@rental.com
Password: admin123

-- Default User
Email: user@rental.com
Password: user123
```

## 🔗 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login

### Flats
- `GET /flats` - Get all flats
- `POST /book-flat` - Book a flat

### User Dashboard
- `GET /my-bookings` - User's bookings

### Admin Panel
- `GET /admin/bookings` - All bookings
- `POST /admin/update-booking-status` - Update booking
- `POST /admin/add-flat` - Add new flat

## 🔧 Configuration

### Environment Variables
```bash
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=rental

# JWT
SECRET_KEY=your_secret_key
```

### Frontend Configuration
```typescript
// src/app/services/api.ts
const API_BASE_URL = 'http://localhost:5000';
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd "rental frontend"
ng test
```

## 📈 Performance & Scalability

- **Database Indexing** for optimized queries
- **JWT Tokens** for stateless authentication
- **Docker Containers** for consistent deployment
- **Cloud-ready** architecture
- **Auto-scaling** with Google Cloud Run

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token expiration
- SQL injection prevention
- CORS configuration
- Input validation
- Role-based access control

## 🌐 Deployment Options

### 1. Google Cloud Platform
- **Cloud Run** for containers
- **Cloud SQL** for MySQL
- **Cloud Build** for CI/CD

### 2. AWS
- **ECS/Fargate** for containers
- **RDS** for MySQL
- **CodePipeline** for CI/CD

### 3. Local/VPS
- **Docker Compose** setup
- **Nginx** reverse proxy
- **SSL** certificates

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Angular team for the robust framework
- MySQL for reliable database solution
- Docker for containerization platform

## 📞 Support

If you have any questions or need help, please:
1. Check the [Issues](https://github.com/your-username/rental-portal/issues) page
2. Create a new issue if needed
3. Contact me directly

---

⭐ **Star this repository if you found it helpful!**


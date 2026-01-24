# Docker Deployment Instructions

## Prerequisites
- Docker installed on your system
- Docker Compose installed

## Quick Start

1. **Clone and navigate to project directory:**
```bash
cd Web-of-hostel
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access the application:**
- Backend API: http://localhost:5000
- MySQL Database: localhost:3306

## Individual Commands

### Build Docker Image
```bash
docker build -t rental-portal-backend .
```

### Run MySQL Container
```bash
docker run -d --name rental_mysql -e MYSQL_ROOT_PASSWORD=Ashish@9630 -e MYSQL_DATABASE=rental -p 3306:3306 mysql:8.0
```

### Run Backend Container
```bash
docker run -d --name rental_backend --link rental_mysql:mysql -p 5000:5000 rental-portal-backend
```

## Environment Variables
- `DB_HOST`: MySQL host (default: mysql)
- `DB_USER`: MySQL user (default: root)
- `DB_PASSWORD`: MySQL password (default: Ashish@9630)
- `DB_NAME`: Database name (default: rental)

## Default Credentials
- Admin: admin@rental.com / admin123
- User: user@rental.com / user123

## Stopping Services
```bash
docker-compose down
```

## Viewing Logs
```bash
docker-compose logs backend
docker-compose logs mysql
```
@echo off
echo Starting Rental Portal Application...

echo Step 1: Stopping any existing containers...
docker-compose down

echo Step 2: Cleaning Docker system...
docker system prune -f

echo Step 3: Building and starting MySQL...
docker-compose up --build -d mysql

echo Step 4: Waiting for MySQL to initialize (90 seconds)...
timeout /t 90

echo Step 5: Building and starting Backend...
docker-compose up --build -d backend

echo Step 6: Waiting for Backend to start (30 seconds)...
timeout /t 30

echo Step 7: Building and starting Frontend...
docker-compose up --build -d frontend

echo.
echo ========================================
echo Application is starting up!
echo ========================================
echo Frontend: http://localhost:4200
echo Backend API: http://localhost:5000
echo.
echo Login credentials:
echo Admin: admin@rental.com / admin123
echo User: user@rental.com / user123
echo.
echo Checking container status...
docker-compose ps

echo.
echo To view logs, run:
echo docker-compose logs -f [service-name]
echo.
pause
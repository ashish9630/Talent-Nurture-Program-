@echo off
echo Deploying Rental Portal to Docker...
echo.

echo Checking Docker installation...
docker --version
if %errorlevel% neq 0 (
    echo Docker is not installed. Please run install-docker.bat first.
    pause
    exit /b 1
)

echo Building and starting containers...
docker-compose up --build -d

echo.
echo Deployment Status:
docker-compose ps

echo.
echo Application URLs:
echo Backend API: http://localhost:5000
echo MySQL Database: localhost:3306
echo.
echo Default Login Credentials:
echo Admin: admin@rental.com / admin123
echo User: user@rental.com / user123
echo.
echo To view logs: docker-compose logs
echo To stop: docker-compose down
echo.
pause
@echo off
echo Fixing Docker setup issues...
echo.

echo Step 1: Stopping existing containers...
docker-compose down

echo Step 2: Cleaning up...
docker system prune -f

echo Step 3: Starting services with proper health checks...
docker-compose up --build -d mysql

echo Step 4: Waiting for MySQL to be ready...
timeout /t 60

echo Step 5: Starting backend...
docker-compose up --build -d backend

echo Step 6: Note about frontend...
echo.
echo IMPORTANT: Frontend requires Node.js v20.19+ or v22.12+
echo Current version is v18.20.8 which is incompatible
echo.
echo Please run update-nodejs.bat first, then:
echo docker-compose up --build frontend
echo.
pause
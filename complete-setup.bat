@echo off
echo Complete Project Setup...

echo Step 1: Updating Node.js...
call auto-update-nodejs.bat

echo Step 2: Fixing Docker setup...
docker-compose down
docker system prune -f

echo Step 3: Starting MySQL...
docker-compose up -d mysql

echo Step 4: Waiting for MySQL (60 seconds)...
timeout /t 60

echo Step 5: Starting Backend...
docker-compose up -d backend

echo Step 6: Starting Frontend...
docker-compose up -d frontend

echo All services started!
echo Frontend: http://localhost:4200
echo Backend: http://localhost:5000
pause
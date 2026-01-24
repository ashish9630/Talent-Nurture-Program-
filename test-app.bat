@echo off
echo Testing Application Services...
echo.

echo Testing Backend (localhost:5000)...
curl -s http://localhost:5000 | findstr "Backend running successfully"
if %errorlevel% == 0 (
    echo ✅ Backend: Working
) else (
    echo ❌ Backend: Not responding
)

echo.
echo Testing Frontend (localhost:4200)...
curl -s -I http://localhost:4200 | findstr "200 OK"
if %errorlevel% == 0 (
    echo ✅ Frontend: Working
) else (
    echo ❌ Frontend: Not responding
)

echo.
echo Testing MySQL (localhost:3307)...
docker exec web-of-hostel-mysql-1 mysqladmin ping -h localhost --silent
if %errorlevel% == 0 (
    echo ✅ MySQL: Working
) else (
    echo ❌ MySQL: Not responding
)

echo.
echo ========================================
echo Application URLs:
echo Frontend: http://localhost:4200
echo Backend:  http://localhost:5000
echo ========================================
echo.
echo Login Credentials:
echo Admin: admin@rental.com / admin123
echo User:  user@rental.com / user123
echo ========================================
pause
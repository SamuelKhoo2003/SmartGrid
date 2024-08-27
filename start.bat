@echo off

REM Start the backend
echo Starting Python backend...
start "Backend" cmd /c "cd buy_sell_algorithm && python main.py"

REM Start the frontend
echo Starting React frontend...
start "Frontend" cmd /c "cd react-front-end && npm start"

REM Wait for both processes to complete
pause

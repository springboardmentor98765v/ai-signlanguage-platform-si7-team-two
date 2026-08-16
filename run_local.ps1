# Run the project locally using Python and Node

Write-Host "Starting Backend Service on port 8000..."
Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory "Backend" -NoNewWindow

Write-Host "Starting Business Logic Service on port 8002..."
Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8002 --reload" -WorkingDirectory "Bussiness_Logic" -NoNewWindow

Write-Host "Starting Frontend on port 5173..."
Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -WorkingDirectory "Frontend" -NoNewWindow

Write-Host "All services started!"
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend API: http://localhost:8000/docs"
Write-Host "Business Logic API: http://localhost:8002/docs"

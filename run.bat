@echo off
cd /d "%~dp0"
echo Starting Supervertaler from: %~dp0Supervertaler.py
echo Using Python: C:\Python312\python.exe
echo Working directory: %CD%
echo.
start wt.exe -p "PowerShell" --title "Supervertaler" cmd /k "cd /d %~dp0 && C:\Python312\python.exe Supervertaler.py && echo. && echo Application closed. Press any key to exit. && pause > nul"

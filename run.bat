@echo off
cd /d "%~dp0"
echo Starting Supervertaler...
echo.

REM Try to run directly - more reliable than Windows Terminal
C:\Python312\python.exe Supervertaler.py

REM If we get here, the app closed - show message
echo.
echo Supervertaler has closed.
pause

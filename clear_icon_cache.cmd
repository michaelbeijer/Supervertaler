@echo off
REM Clear Windows Icon Cache
echo Clearing Windows icon cache...
echo.

REM Stop Explorer
echo Stopping Windows Explorer...
taskkill /f /im explorer.exe

REM Delete icon cache files
echo Deleting icon cache files...
cd /d "%userprofile%\AppData\Local\Microsoft\Windows\Explorer"
attrib -h iconcache_*.db
del iconcache_*.db /a /f /q
del thumbcache_*.db /a /f /q

REM Restart Explorer
echo Restarting Windows Explorer...
start explorer.exe

echo.
echo Icon cache cleared! Please restart Supervertaler.
pause

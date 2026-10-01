@echo off
chcp 65001 >nul
cd /d "%~dp0"
python build.py
if errorlevel 1 (
  echo.
  echo Build failed.
  pause
  exit /b 1
)
echo.
echo Build completed successfully.
echo.
python tools\seo_audit.py
pause

@echo off
cd /d "%~dp0"
set /p USUARIO=Usuario de GitHub (Enter = gustavws12): 
if "%USUARIO%"=="" set USUARIO=gustavws12
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\probar_conexion.ps1" -Usuario %USUARIO%
pause

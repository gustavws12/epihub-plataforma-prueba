@echo off
cd /d "%~dp0"
set /p USUARIO=Cuenta de GitHub DUENA del hub (Enter = gustavws12): 
if "%USUARIO%"=="" set USUARIO=gustavws12
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\subir_a_github.ps1" -Usuario %USUARIO%
pause

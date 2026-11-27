@echo off
cd /d "%~dp0"
python scripts\validar_envio.py --todos
pause

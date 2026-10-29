@echo off
cd /d "%~dp0"
call "%~dp0Start.cmd" --setup-only %*
exit /b %errorlevel%

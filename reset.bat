@echo off

REM Remove the 'registry' directory
rd /s /q registry 2>nul

REM Check if arguments contain '--data' and remove the 'data' directory if found
echo %* | findstr /C:"--data" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    rd /s /q data 2>nul
)

exit /b 0

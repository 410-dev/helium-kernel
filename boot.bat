@echo off

REM Define color variables
REM Windows batch files do not support the same kind of color control as Bash. 
REM You can use 'color' command but it changes the color of the whole console.

REM Check if python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed. Please install it and try again.
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Error: pip is not installed. Please install it and try again.
    exit /b 1
)

echo Starting kernel...
python core.py %*

REM If argument contains --clear-cache then remove all directories named __pycache__
IF "%1"=="--clear-cache" (
    echo Clearing cache...
    FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
    IF EXIST "data\cache" rd /s /q "data\cache"
    echo Cache cleared.
)

echo Kernel stopped.
exit /b 0

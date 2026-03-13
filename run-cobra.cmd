@echo off
setlocal

set "ROOT=%~dp0"
set "ROOT_NOSLASH=%ROOT:~0,-1%"
set "PYTHON_EXE=%ROOT%.venv\Scripts\python.exe"
set "COBRA_EXE=%ROOT%.venv\Scripts\cobra.exe"

if not exist "%PYTHON_EXE%" (
    echo [INFO] Creating Python virtual environment in .venv...
    call :create_venv
    if errorlevel 1 exit /b 1
)

if not exist "%COBRA_EXE%" (
    echo [INFO] Installing local cobra command into .venv...
    "%PYTHON_EXE%" -m pip install -e "%ROOT_NOSLASH%"
    if errorlevel 1 (
        echo [ERROR] Failed to install cobra CLI.
        exit /b 1
    )
)

"%COBRA_EXE%" %*
exit /b %errorlevel%

:create_venv
where py >nul 2>nul
if not errorlevel 1 (
    py -3.12 -m venv "%ROOT%.venv"
    if not errorlevel 1 goto :venv_created

    py -3 -m venv "%ROOT%.venv"
    if not errorlevel 1 goto :venv_created

    py -m venv "%ROOT%.venv"
    if not errorlevel 1 goto :venv_created
)

where python >nul 2>nul
if not errorlevel 1 (
    python -m venv "%ROOT%.venv"
    if not errorlevel 1 goto :venv_created
)

echo [ERROR] Failed to create .venv automatically.
echo Install Python 3.12+ and make sure 'py' or 'python' is available in PATH.
exit /b 1

:venv_created
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment creation finished, but .venv\Scripts\python.exe was not found.
    exit /b 1
)
exit /b 0

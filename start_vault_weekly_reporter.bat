@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=C:\Users\Ciruzz\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%PYTHON_EXE%" (
  "%PYTHON_EXE%" "scripts\vault_weekly_reporter.py" --daemon
) else (
  python "scripts\vault_weekly_reporter.py" --daemon
)

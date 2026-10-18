@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Project Python is missing. See environment.md for installation instructions.
  pause
  exit /b 1
)
set "JUPYTER_CONFIG_DIR=%CD%\tmp\jupyter\config"
set "JUPYTER_DATA_DIR=%CD%\tmp\jupyter\data"
set "JUPYTER_RUNTIME_DIR=%CD%\tmp\jupyter\runtime"
set "IPYTHONDIR=%CD%\tmp\ipython"
set "MPLCONFIGDIR=%CD%\tmp\matplotlib"
set "PYTHONUTF8=1"
rtk proxy "%CD%\.venv\Scripts\python.exe" -m notebook --ServerApp.ip=127.0.0.1 "--ServerApp.root_dir=%CD%" %*
if errorlevel 1 pause
endlocal

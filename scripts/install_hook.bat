/*
 * Author: Kelvin Kabute
 * Last-updated: 2026-04-19
 */


@echo off
REM Installer for Windows: copy pre-commit hook and create venv if missing
SETLOCAL
REM Prefer python if available; create venv only if missing
IF NOT EXIST ".venv\Scripts\python.exe" (
  where python >nul 2>&1
  IF %ERRORLEVEL% EQU 0 (
    echo Creating virtualenv...
    python -m venv .venv
  ) ELSE (
    echo Warning: python not found in PATH; skipping venv creation.
  )
)

copy hooks\pre-commit .git\hooks\pre-commit >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo Failed to copy hook. Ensure you run this from the repo root and have write access to .git\hooks.
  endlocal
  exit /b 1
)
echo Hook installed to .git\hooks\pre-commit
endlocal
exit /b 0

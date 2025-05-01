@echo off
REM Usage: run_test.bat [mode]

set SCRIPT=integration\test_local_zstack_sort.py

CALL mypy %SCRIPT%
IF "%1"=="--only_mypy" (
    exit /b 1
) 
CALL python -m integration.test_local_zstack_sort
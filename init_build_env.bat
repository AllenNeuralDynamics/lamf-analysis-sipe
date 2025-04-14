@echo off
echo Current path is: %CD%
SET ENV_NAME=lamf-analysis-sipe-3_10_9

:: Check if environment exists
conda env list | findstr /C:"%ENV_NAME%" >nul
IF ERRORLEVEL 1 (
    echo Creating environment %ENV_NAME%...
    conda create -n %ENV_NAME% python=3.10.9 -y
) ELSE (
    echo Environment %ENV_NAME% already exists. Skipping creation.
)

:: Activate environment and install packages
CALL conda activate %ENV_NAME%
pip install -r requirements.txt
pip install -r requirements.dev.txt
pip install .

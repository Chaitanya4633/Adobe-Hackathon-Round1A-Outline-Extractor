@echo off
echo Testing PDF Outline Extractor locally...
echo.

REM Check if input directory has PDF files
if not exist "input\*.pdf" (
    echo ERROR: No PDF files found in input\ directory
    echo Please add some PDF files to the input\ folder first
    echo.
    pause
    exit /b 1
)

echo Found PDF files in input directory:
dir input\*.pdf /b

echo.
echo Installing Python dependencies...
cd src
pip install -r requirements.txt

echo.
echo Running PDF extraction...
python main.py

echo.
echo Checking output...
cd ..
if exist "output\*.json" (
    echo SUCCESS: JSON files created in output\ directory:
    dir output\*.json /b
) else (
    echo WARNING: No output files found
)

echo.
echo Test completed!
pause
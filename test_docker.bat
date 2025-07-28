@echo off
echo Testing PDF Outline Extractor with Docker...
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
echo Building Docker image...
docker build -t pdf-extractor:test src

if %ERRORLEVEL% neq 0 (
    echo ERROR: Docker build failed
    pause
    exit /b 1
)

echo.
echo Running Docker container...
docker run --rm -v %CD%\input:/app/input -v %CD%\output:/app/output --network none pdf-extractor:test

echo.
echo Checking output...
if exist "output\*.json" (
    echo SUCCESS: JSON files created in output\ directory:
    dir output\*.json /b
    echo.
    echo Sample output content:
    type output\*.json | more
) else (
    echo WARNING: No output files found
)

echo.
echo Docker test completed!
pause
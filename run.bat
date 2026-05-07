@echo off
echo 🚀 Setting up HashGen - AI Hashtag Generator
echo.

echo � Running pre-flight checks...
python test.py

if %errorlevel% neq 0 (
    echo ❌ Pre-flight checks failed
    echo 💡 Please install missing dependencies and try again
    pause
    exit /b 1
)

echo.
echo 📦 Installing/updating Python dependencies...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo 💡 Try running: pip install flask spacy
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
echo 🎯 Starting the application...
echo 📍 Open http://localhost:5000 in your browser
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
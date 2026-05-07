@echo off
echo 🚀 Installing spaCy for HashGen
echo.

echo 📦 Installing spaCy...
pip install spacy

if %errorlevel% neq 0 (
    echo ❌ Failed to install spaCy
    echo 💡 Try running as Administrator or check your Python installation
    pause
    exit /b 1
)

echo.
echo 📥 Downloading English language model...
python -m spacy download en_core_web_sm

if %errorlevel% neq 0 (
    echo ❌ Failed to download English model
    echo 💡 Try: python -m spacy download en_core_web_sm
    pause
    exit /b 1
)

echo.
echo ✅ spaCy installation complete!
echo 🎯 You can now run: python app.py
echo.

pause
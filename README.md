# HashGen - AI Hashtag Generator

A Flask web application that uses spaCy NLP to automatically generate relevant hashtags from your captions.

## Features

- 🤖 **Real NLP**: Uses spaCy for intelligent keyword extraction
- 📱 **Multi-platform**: Optimized hashtags for Instagram, TikTok, Twitter, LinkedIn
- 🎯 **Smart categorization**: Groups hashtags by specificity (niche/general)
- ⚡ **Fast & clean**: No hardcoded datasets, pure AI-powered generation

## Quick Start

### Option 1: One-Click Setup (Windows)
1. Double-click `install_spacy.bat` to install spaCy
2. Double-click `run.bat` to start the app
3. Open http://localhost:5000

### Option 2: Manual Setup
```bash
# Install spaCy
pip install spacy
python -m spacy download en_core_web_sm

# Install Flask
pip install flask

# Run the app
python app.py
```

## Requirements

- Python 3.8+
- Flask
- spaCy with English model

## How It Works

1. **Input**: Enter your social media caption
2. **NLP Processing**: spaCy analyzes the text and extracts:
   - Nouns (people, places, things)
   - Adjectives (descriptive words)
   - Proper nouns (names, brands)
3. **Hashtag Generation**: Creates relevant hashtags from extracted keywords
4. **Smart Sorting**: Longer, more specific hashtags appear first

## API Usage

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"caption": "Amazing sunset hike in the mountains today!", "platform": "instagram"}'
```

## Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── run.bat            # Windows setup script
├── templates/
│   └── index.html     # Web interface
├── static/
│   ├── css/
│   └── js/            # Frontend assets
└── README.md          # This file
```

## Troubleshooting

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Port 5000 already in use:**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

**Permission errors:**
- Run command prompt as Administrator
- Or use `python -m pip install` instead of `pip`

## License

MIT License - Free to use and modify!

from flask import Flask, render_template, request, jsonify
import re
import spacy
import sys


app = Flask(__name__)

# Load spaCy model
def load_spacy_model():
    """Load spaCy model with fallback options"""
    try:
        
        nlp = spacy.load('en_core_web_sm')
        print(" spaCy model loaded successfully!")
        return nlp
    except OSError:
        print("📥 Downloading spaCy English model...")
        try:
           
            import subprocess
            result = subprocess.run([
                sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'
            ], capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print(" Model downloaded successfully!")
                return spacy.load('en_core_web_sm')
            else:
                print(f" Download failed: {result.stderr}")
                raise Exception("Failed to download spaCy model")

        except (subprocess.TimeoutExpired, Exception) as e:
            print(f" Error downloading model: {e}")
            print(" Please run: python -m spacy download en_core_web_sm")
            sys.exit(1)

# Load the model
try:
    nlp = load_spacy_model()
except Exception as e:
    print(f" Failed to load spaCy: {e}")
    print(" The app will not work without spaCy.")
    print(" Please install spaCy and the English model:")
    print("   pip install spacy")
    print("   python -m spacy download en_core_web_sm")
    sys.exit(1)

# Step 1: Extract keywords using spaCy NLP
def extract_keywords(caption):
    """Use spaCy to extract nouns, adjectives, and proper nouns"""
    try:
        doc = nlp(caption.lower())
        keywords = []

        for token in doc:
            # Keep nouns (NN*), adjectives (JJ*), proper nouns (PROPN)
            if (token.pos_ in ['NOUN', 'ADJ', 'PROPN'] and
                not token.is_stop and
                len(token.text) > 2 and
                token.text.isalnum()): 
                keywords.append(token.lemma_)

        return list(set(keywords)) 
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

# Step 2: Generate hashtags from keywords
def generate_hashtags(caption, platform='instagram'):
    """Generate platform-specific hashtags using spaCy-extracted keywords"""
    try:
        keywords = extract_keywords(caption)
        hashtags = set()

        # Add keywords as hashtags
        for keyword in keywords:
            clean_tag = re.sub(r'[^a-z0-9]', '', keyword.lower())
            if clean_tag and len(clean_tag) >= 3:
                hashtags.add(clean_tag)

        # Create bigrams (two-word combinations) from keywords
        doc = nlp(caption.lower())
        tokens = [t.text for t in doc if not t.is_stop and len(t.text) > 2 and t.text.isalnum()]
        for i in range(len(tokens) - 1):
            bigram = tokens[i] + tokens[i + 1]
            if len(bigram) > 5:
                clean_bigram = re.sub(r'[^a-z0-9]', '', bigram.lower())
                if clean_bigram:
                    hashtags.add(clean_bigram)

        # Format as hashtags with # symbol
        final_hashtags = ['#' + tag for tag in hashtags if tag]

        # Platform-specific strategies
        if platform == 'instagram':
            # Instagram: prioritize long, specific hashtags (niche)
            final_hashtags = sorted(set(final_hashtags), key=lambda x: len(x), reverse=True)
            limit = 30

        elif platform == 'tiktok':
            # TikTok: mix of trending (shorter) and specific tags
            final_hashtags = sorted(set(final_hashtags), key=lambda x: (len(x), x), reverse=False)
            limit = 20

        elif platform == 'twitter':
            # Twitter: short, concise hashtags only
            final_hashtags = [tag for tag in final_hashtags if len(tag) <= 10]
            final_hashtags = sorted(set(final_hashtags), key=lambda x: len(x))
            limit = 8

        elif platform == 'linkedin':
            # LinkedIn: professional, selective hashtags only
            professional_keywords = ['business', 'career', 'professional', 'industry', 'leadership', 
                                   'marketing', 'growth', 'success', 'innovation', 'tech']
            final_hashtags = [tag for tag in final_hashtags 
                            if any(keyword in tag.lower() for keyword in professional_keywords) 
                            or len(tag) > 8]
            final_hashtags = sorted(set(final_hashtags), key=lambda x: len(x), reverse=True)
            limit = 5

        return final_hashtags[:limit]
    except Exception as e:
        print(f"Error generating hashtags: {e}")
        return []

# Step 3: Categorize hashtags for display
def categorize_hashtags(hashtags):
    """Group hashtags by length for UI display"""
    try:
        niche = []
        general = []

        for tag in hashtags:
            tag_word = tag[1:]  # Remove # symbol
            if len(tag_word) > 8:
                niche.append(tag)
            else:
                general.append(tag)

        return {
            'niche': niche[:12],
            'general': general[:12],
            'power': hashtags[:6]  # Top 6 by relevance
        }
    except Exception as e:
        print(f"Error categorizing hashtags: {e}")
        return {'niche': [], 'general': [], 'power': []}

#Routes

@app.route('/')
def index():
    """Render the main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {e}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'HashGen is running!',
        'nlp_model': 'spaCy en_core_web_sm'
    })

@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate hashtags using spaCy NLP"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        caption = data.get('caption', '').strip()
        platform = data.get('platform', 'instagram').lower()

        # Validate input
        if not caption:
            return jsonify({'error': 'Please enter a caption'}), 400

        if len(caption) < 3:
            return jsonify({'error': 'Caption is too short'}), 400

        # Validate platform
        if platform not in ['instagram', 'tiktok', 'twitter', 'linkedin']:
            platform = 'instagram'

        # Generate hashtags using spaCy NLP
        hashtags = generate_hashtags(caption, platform)
        categorized = categorize_hashtags(hashtags)
        all_tags = ' '.join(hashtags)

        return jsonify({
            'hashtags': hashtags,
            'categorized': categorized,
            'all_text': all_tags,
            'count': len(hashtags),
            'platform': platform
        })

    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({'error': f'Error generating hashtags: {str(e)}'}), 500

if __name__ == '__main__':
    print(" Starting HashGen Flask App...")
    print(" Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

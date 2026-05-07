#!/usr/bin/env python3
"""
Test script for HashGen app
Run this to verify everything works before starting the full app
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError:
        print("❌ Flask not found. Install with: pip install flask")
        return False

    try:
        import spacy
        print("✅ spaCy imported successfully")
    except ImportError:
        print("❌ spaCy not found. Install with: pip install spacy")
        return False

    return True

def test_spacy_model():
    """Test if spaCy English model is available"""
    print("\n🔍 Testing spaCy model...")

    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
        print("✅ spaCy English model loaded successfully")

        # Test basic NLP
        doc = nlp("This is a test sentence")
        print(f"✅ NLP processing works: {len(doc)} tokens found")

        return True
    except OSError:
        print("❌ spaCy English model not found")
        print("💡 Download with: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        print(f"❌ Error loading spaCy model: {e}")
        return False

def test_app_import():
    """Test if our app can be imported without errors"""
    print("\n🔍 Testing app import...")

    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())

        # Try to import the app (but don't run it)
        import app
        print("✅ App imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error importing app: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 HashGen - Pre-flight Check")
    print("=" * 40)

    all_good = True

    if not test_imports():
        all_good = False

    if not test_spacy_model():
        all_good = False

    if not test_app_import():
        all_good = False

    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All tests passed! Ready to run the app.")
        print("💡 Run: python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
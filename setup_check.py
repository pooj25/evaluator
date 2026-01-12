"""
Setup verification script - Check if all dependencies are installed correctly
"""
import sys

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} - Installed")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed. Run: pip install {package_name}")
        return False

def check_tesseract():
    """Check if Tesseract OCR is available"""
    try:
        import pytesseract
        # Try to get version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR - Installed (Version: {version})")
        return True
    except Exception as e:
        print(f"⚠️  Tesseract OCR - Not found or not configured")
        print(f"   Error: {str(e)}")
        print(f"   Please install Tesseract OCR:")
        print(f"   Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print(f"   Linux: sudo apt-get install tesseract-ocr")
        print(f"   Mac: brew install tesseract")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Intelligent Evaluator System - Setup Verification")
    print("=" * 60)
    print()
    
    checks = []
    
    print("Python Version:")
    checks.append(check_python_version())
    print()
    
    print("Required Python Packages:")
    packages = [
        ("streamlit", "streamlit"),
        ("pytesseract", "pytesseract"),
        ("Pillow", "PIL"),
        ("opencv-python", "cv2"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("sqlalchemy", "sqlalchemy"),
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("sentence-transformers", "sentence_transformers"),
        ("scikit-learn", "sklearn"),
        ("plotly", "plotly"),
    ]
    
    for package, import_name in packages:
        checks.append(check_package(package, import_name))
    print()
    
    print("External Dependencies:")
    checks.append(check_tesseract())
    print()
    
    print("=" * 60)
    if all(checks):
        print("✅ All checks passed! System is ready to use.")
        print()
        print("Next steps:")
        print("1. Run: streamlit run app.py")
        print("2. Open browser to the URL shown")
        print("3. Start evaluating assignments!")
    else:
        print("⚠️  Some checks failed. Please install missing dependencies.")
        print()
        print("To install all Python packages, run:")
        print("  pip install -r requirements.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()


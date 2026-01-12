# Intelligent Rubric-Based Evaluator System

An AI-powered evaluation system for algorithms, flowcharts, and pseudocodes that provides instant, consistent feedback to students while saving time for teachers.

## Features

- 📷 **Image Processing**: Upload photos of flowcharts/pseudocodes with OCR text extraction
- 🤖 **AI-Powered Evaluation**: Uses transformer models for semantic analysis
- 📊 **Rubric-Based Scoring**: Consistent evaluation using predefined rubrics
- ⚡ **Instant Feedback**: Get immediate results with detailed feedback
- 📈 **Analytics Dashboard**: Track performance and statistics
- 🎨 **Modern UI**: Beautiful Streamlit interface for students and teachers

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** (for image text extraction)
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) and install
   - Linux: `sudo apt-get install tesseract-ocr`
   - Mac: `brew install tesseract`

### Setup

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Note for Python 3.13 users**: If you encounter build errors (especially with Pillow), try:
```bash
pip install -r requirements-python313.txt
```

Or install Pillow separately first:
```bash
pip install --upgrade pip
pip install Pillow>=10.3.0
pip install -r requirements.txt
```

3. (Optional) If Tesseract is not in your system PATH, update the path in `ocr_processor.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser to the URL shown (typically `http://localhost:8501`)

3. **For Students**:
   - Navigate to "Submit Assignment"
   - Enter student ID and name
   - Select assignment type (algorithm/flowchart/pseudocode)
   - Upload image or type text directly
   - Click "Submit for Evaluation" to get instant feedback

4. **For Teachers**:
   - View all submissions in "View Results"
   - Check analytics in "Analytics Dashboard"
   - Manage rubrics in "Rubric Management"

## System Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with SQLAlchemy ORM
- **Database**: SQLite (evaluator.db)
- **OCR**: Tesseract for image text extraction
- **AI Model**: Sentence Transformers (all-MiniLM-L6-v2) for semantic evaluation
- **Evaluation**: Rubric-guided semantic similarity analysis

## Rubric Criteria

The system includes default rubrics for:

### Algorithms
- Correctness (35%)
- Efficiency (20%)
- Clarity (20%)
- Completeness (15%)
- Structure (10%)

### Flowcharts
- Symbols (25%)
- Logic (30%)
- Completeness (25%)
- Clarity (15%)
- Formatting (5%)

### Pseudocode
- Syntax (20%)
- Logic (30%)
- Completeness (20%)
- Readability (15%)
- Correctness (15%)

## File Structure

```
evaluator/
├── app.py                 # Main Streamlit application
├── database.py            # Database models and setup
├── ocr_processor.py       # OCR text extraction
├── rubric_manager.py      # Rubric management
├── evaluator.py           # AI evaluation engine
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── evaluator.db          # SQLite database (created on first run)
└── uploads/              # Uploaded images directory
```

## How It Works

1. **Submission**: Student uploads image or types text
2. **OCR Processing**: If image, extract text using Tesseract OCR
3. **Text Normalization**: Clean and normalize extracted text
4. **Semantic Analysis**: Use transformer model to analyze content
5. **Rubric Evaluation**: Score against predefined criteria
6. **Feedback Generation**: Generate comprehensive feedback with strengths, weaknesses, and suggestions
7. **Storage**: Save submission and evaluation to database

## Benefits

- ✅ **Consistent Evaluation**: Same rubric applied to all students
- ⏱️ **Time Saving**: Instant automated evaluation
- 📊 **Detailed Feedback**: Comprehensive analysis for improvement
- 🎯 **Fair Assessment**: Objective rubric-based scoring
- 📈 **Progress Tracking**: Analytics dashboard for insights

## Troubleshooting

### OCR Not Working
- Ensure Tesseract OCR is installed
- Check image quality (clear, well-lit images work best)
- Verify Tesseract path in `ocr_processor.py`

### Model Loading Issues
- First run downloads the transformer model (~80MB)
- Ensure stable internet connection
- Model is cached after first download

### Database Errors
- Delete `evaluator.db` to reset database
- Ensure write permissions in project directory

## Future Enhancements

- Support for multiple languages
- Advanced flowchart recognition
- Integration with learning management systems
- Custom rubric creation interface
- Batch evaluation for multiple submissions

## License

This project is open source and available for educational use.

## Support

For issues or questions, please check the code comments or create an issue in the repository.


# Quick Start Guide

## Step 1: Install Tesseract OCR

### Windows
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`)
3. The code is already configured for this path

### Linux
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Mac
```bash
brew install tesseract
```

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first time you run the app, it will download the transformer model (~80MB). This is automatic and only happens once.

## Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser automatically at `http://localhost:8501`

## Step 4: Test the System

1. **Submit a Test Assignment**:
   - Go to "Submit Assignment"
   - Enter any Student ID (e.g., "STU001")
   - Enter your name
   - Select "pseudocode" as assignment type
   - Type a simple pseudocode:
     ```
     BEGIN
       READ number
       IF number > 0 THEN
         PRINT "Positive"
       ELSE
         PRINT "Negative"
       END IF
     END
     ```
   - Click "Submit for Evaluation"
   - View your instant feedback!

2. **Try Image Upload**:
   - Take a photo of a flowchart or pseudocode
   - Upload it in the "Submit Assignment" page
   - Click "Extract Text from Image"
   - Review the extracted text
   - Submit for evaluation

3. **View Results**:
   - Go to "View Results" to see all submissions
   - Filter by student ID or assignment type

4. **Check Analytics**:
   - Visit "Analytics Dashboard" to see statistics
   - View score distributions and performance metrics

## Tips for Best Results

### Image Quality
- Use clear, well-lit images
- Ensure text is readable
- Avoid shadows and glare
- Use high resolution if possible

### Text Input
- For pseudocode, use standard conventions
- Include keywords like BEGIN, END, IF, THEN, ELSE
- Structure your code with proper indentation

### Flowcharts
- Describe your flowchart clearly in text
- Mention all symbols used (start, end, decision, process)
- Explain the flow logic

## Troubleshooting

**Problem**: OCR not extracting text properly
- **Solution**: Ensure image is clear and text is readable. Try preprocessing the image or typing directly.

**Problem**: Model download is slow
- **Solution**: This is normal on first run. The model is cached for future use.

**Problem**: Database errors
- **Solution**: Delete `evaluator.db` file and restart the app to create a fresh database.

**Problem**: Tesseract not found
- **Solution**: Check the installation path in `ocr_processor.py` and update if needed.

## Next Steps

- Customize rubrics in "Rubric Management"
- Submit multiple assignments to see analytics
- Experiment with different assignment types
- Review feedback to understand evaluation criteria

Enjoy using the Intelligent Evaluator System! 🚀


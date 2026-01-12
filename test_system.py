"""
Test script to verify system components are working correctly
"""
import os
from database import Database
from rubric_manager import RubricManager
from evaluator import IntelligentEvaluator
from ocr_processor import OCRProcessor

def test_database():
    """Test database initialization"""
    print("Testing database...")
    db = Database('test_evaluator.db')
    rubric_manager = RubricManager(db)
    rubrics = rubric_manager.get_all_rubrics()
    print(f"✅ Database initialized. Found {len(rubrics)} rubrics.")
    db.close()
    os.remove('test_evaluator.db')
    return True

def test_rubric_manager():
    """Test rubric management"""
    print("Testing rubric manager...")
    db = Database('test_evaluator.db')
    rubric_manager = RubricManager(db)
    
    # Test getting rubrics
    algo_rubric = rubric_manager.get_rubric('algorithm')
    flowchart_rubric = rubric_manager.get_rubric('flowchart')
    pseudo_rubric = rubric_manager.get_rubric('pseudocode')
    
    assert algo_rubric is not None, "Algorithm rubric not found"
    assert flowchart_rubric is not None, "Flowchart rubric not found"
    assert pseudo_rubric is not None, "Pseudocode rubric not found"
    
    print("✅ Rubric manager working correctly.")
    db.close()
    os.remove('test_evaluator.db')
    return True

def test_evaluator():
    """Test evaluation engine"""
    print("Testing evaluator...")
    evaluator = IntelligentEvaluator()
    
    # Test evaluation
    sample_answer = """
    BEGIN
      READ number
      IF number > 0 THEN
        PRINT "Positive"
      ELSE
        PRINT "Negative"
      END IF
    END
    """
    
    rubric = {
        'type': 'pseudocode',
        'criteria': {
            'syntax': 'Proper pseudocode syntax',
            'logic': 'Correct logical flow',
            'completeness': 'All steps present'
        },
        'weights': {
            'syntax': 0.33,
            'logic': 0.34,
            'completeness': 0.33
        }
    }
    
    result = evaluator.evaluate(sample_answer, rubric)
    assert 'overall_score' in result
    assert 'feedback' in result
    print(f"✅ Evaluator working. Sample score: {result['overall_score']}/100")
    return True

def test_ocr_processor():
    """Test OCR processor (without actual image)"""
    print("Testing OCR processor...")
    ocr = OCRProcessor()
    print("✅ OCR processor initialized.")
    print("   Note: Full OCR test requires an actual image file.")
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("Intelligent Evaluator System - Component Tests")
    print("=" * 50)
    print()
    
    try:
        test_database()
        test_rubric_manager()
        test_evaluator()
        test_ocr_processor()
        
        print()
        print("=" * 50)
        print("✅ All tests passed! System is ready to use.")
        print("=" * 50)
        print()
        print("Next step: Run 'streamlit run app.py' to start the application.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


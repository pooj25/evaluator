"""
Main Streamlit application for Intelligent Rubric-based Evaluator System
"""
import streamlit as st
import os
import json
from datetime import datetime
from PIL import Image
import plotly.express as px
import pandas as pd
from database import Database, Submission, Evaluation
from ocr_processor import OCRProcessor
from rubric_manager import RubricManager
from evaluator import IntelligentEvaluator

# Page configuration
st.set_page_config(
    page_title="Intelligent Evaluator System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        animation: gradient-shift 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
    }
    
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .feedback-box {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        background-color: #f8f9ff;
    }
    
    .strength-item {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        color: #059669;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .strength-item:hover {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        transform: translateX(5px);
    }
    
    .weakness-item {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        color: #dc2626;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #ef4444;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .weakness-item:hover {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        transform: translateX(5px);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    [data-testid="stSidebar"] h1 {
        color: white;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* File uploader */
    .stFileUploader>div {
        border-radius: 15px;
        border: 2px dashed #667eea;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader>div:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
        border-left: 4px solid #667eea;
    }
    
    /* Radio buttons */
    [data-testid="stRadio"] label {
        font-weight: 500;
        color: #333;
    }
    
    /* Success/Error messages */
    .stSuccess {
        border-radius: 10px;
        border-left: 4px solid #10b981;
    }
    
    .stError {
        border-radius: 10px;
        border-left: 4px solid #ef4444;
    }
    
    .stInfo {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Background pattern */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Card style for sections */
    .info-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        transform: translateY(-3px);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = Database()
if 'ocr' not in st.session_state:
    st.session_state.ocr = OCRProcessor()
if 'rubric_manager' not in st.session_state:
    st.session_state.rubric_manager = RubricManager(st.session_state.db)
if 'evaluator' not in st.session_state:
    st.session_state.evaluator = IntelligentEvaluator()

# Create uploads directory
os.makedirs('uploads', exist_ok=True)

def main():
    # Header with enhanced design
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 class="main-header">📊 Intelligent Rubric-Based Evaluator</h1>
            <p style="font-size: 1.3rem; color: #666; font-weight: 500; margin-top: 0.5rem;">
                ✨ AI-Powered Evaluation for Algorithms, Flowcharts & Pseudocodes ✨
            </p>
            <p style="font-size: 1rem; color: #999; margin-top: 0.5rem;">
                Get instant, consistent feedback with intelligent rubric-based assessment
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced styling
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid rgba(255,255,255,0.2); margin-bottom: 2rem;">
            <h1 style="color: white; font-size: 1.8rem; font-weight: 700; margin: 0;">🧭 Navigation</h1>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Choose a page",
        ["🏠 Submit Assignment", "📈 View Results", "📋 Rubric Management", "📊 Analytics Dashboard"],
        label_visibility="collapsed"
    )
    
    if page == "🏠 Submit Assignment":
        submit_assignment_page()
    elif page == "📈 View Results":
        view_results_page()
    elif page == "📋 Rubric Management":
        rubric_management_page()
    elif page == "📊 Analytics Dashboard":
        analytics_dashboard_page()

def submit_assignment_page():
    st.markdown('<h2 class="sub-header">📝 Submit Your Assignment</h2>', unsafe_allow_html=True)
    
    # Info card
    st.markdown("""
        <div class="info-card">
            <p style="margin: 0; font-size: 1.1rem; color: #667eea; font-weight: 600;">
                💡 Upload a clear image of your flowchart/pseudocode or type it directly for instant AI-powered evaluation!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Student information
    st.markdown("### 👤 Student Information")
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input("Student ID *", placeholder="e.g., STU001", help="Enter your unique student identifier")
    with col2:
        student_name = st.text_input("Student Name *", placeholder="e.g., John Doe", help="Enter your full name")
    
    # Assignment type
    st.markdown("### 📋 Assignment Details")
    assignment_type = st.selectbox(
        "Assignment Type *",
        ["algorithm", "flowchart", "pseudocode"],
        help="Select the type of assignment you're submitting",
        index=None,
        placeholder="Choose assignment type..."
    )
    
    # Input method
    st.markdown("### 📤 Submission Method")
    input_method = st.radio(
        "How would you like to submit?",
        ["📷 Upload Image", "✍️ Type Text Directly"],
        horizontal=True,
        help="Upload a photo or type your answer directly"
    )
    
    student_text = ""
    uploaded_file = None
    
    if input_method == "📷 Upload Image":
        uploaded_file = st.file_uploader(
            "Upload your flowchart/pseudocode image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of your flowchart or pseudocode"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Process image
            if st.button("🔍 Extract Text from Image", type="primary"):
                with st.spinner("🔄 Processing image with advanced OCR (handling blurry images)..."):
                    try:
                        # Save uploaded file
                        file_path = f"uploads/{student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{uploaded_file.name.split('.')[-1]}"
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Extract text with enhanced preprocessing
                        ocr_result = st.session_state.ocr.extract_with_confidence(file_path)
                        student_text = ocr_result['text']
                        
                        # Display results with method info
                        confidence = ocr_result.get('confidence', 0)
                        method_used = ocr_result.get('method_used', 'enhanced')
                        
                        if confidence >= 70:
                            st.success(f"✅ Text extracted successfully! (Confidence: {confidence:.1f}%)")
                        elif confidence >= 50:
                            st.warning(f"⚠️ Text extracted with moderate confidence: {confidence:.1f}%. Please review and edit if needed.")
                        else:
                            st.warning(f"⚠️ Low confidence extraction: {confidence:.1f}%. The image may be blurry. Please review carefully.")
                        
                        # Show method used
                        method_names = {
                            'enhanced': 'Enhanced Preprocessing (Upscaling + Deblurring)',
                            'aggressive': 'Aggressive Preprocessing (3x Upscaling + Strong Sharpening)',
                            'standard': 'Standard Preprocessing'
                        }
                        st.info(f"🔧 Processing Method: {method_names.get(method_used, method_used)}")
                        
                        # Show preprocessed image option
                        with st.expander("🔍 View Preprocessed Image (for debugging)"):
                            try:
                                # Get preprocessed image
                                preprocessed = st.session_state.ocr.preprocess_image(file_path, method=method_used)
                                # Display the preprocessed grayscale image
                                st.image(preprocessed, caption=f"Preprocessed Image (Method: {method_used})", use_container_width=True, clamp=True)
                                st.caption("This is the enhanced image used for OCR extraction. Blurry images are upscaled and sharpened.")
                            except Exception as e:
                                st.info(f"Could not display preprocessed image: {str(e)}")
                        
                        # Editable text area
                        st.markdown("### ✏️ Extracted Text (You can edit if needed)")
                        edited_text = st.text_area(
                            "Review and edit the extracted text",
                            value=student_text,
                            height=250,
                            key="ocr_extracted_text",
                            help="You can manually correct any OCR errors here"
                        )
                        
                        st.session_state.extracted_text = edited_text
                        st.session_state.image_path = file_path
                        
                        if edited_text != student_text:
                            st.success("✅ Text has been edited. Your changes will be used for evaluation.")
                    except Exception as e:
                        st.error(f"❌ Error processing image: {str(e)}")
                        st.info("💡 Tip: For blurry images, the system uses advanced preprocessing. If extraction fails, try:\n"
                               "- Taking a clearer photo with better lighting\n"
                               "- Ensuring text is in focus\n"
                               "- Using higher resolution if possible")
    else:
        student_text = st.text_area(
            "Enter your answer directly",
            height=300,
            placeholder="Type your algorithm, flowchart description, or pseudocode here..."
        )
        st.session_state.extracted_text = student_text
    
    st.markdown("---")
    
    # Submit button with enhanced styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button("🚀 Submit for Evaluation", type="primary", use_container_width=True)
    
    if submit_button:
        if not student_id or not student_name:
            st.error("❌ Please fill in all required fields (Student ID and Name)")
        elif not st.session_state.get('extracted_text', '').strip():
            st.error("❌ Please provide your answer (either upload image or type text)")
        else:
            with st.spinner("🔄 Evaluating your submission..."):
                try:
                    # Get rubric
                    rubric = st.session_state.rubric_manager.get_rubric(assignment_type)
                    if not rubric:
                        st.error("❌ Rubric not found for this assignment type")
                        return
                    
                    # Evaluate
                    evaluation_result = st.session_state.evaluator.evaluate(
                        st.session_state.extracted_text,
                        rubric
                    )
                    
                    # Save submission
                    session = st.session_state.db.get_session()
                    submission = Submission(
                        student_id=student_id,
                        student_name=student_name,
                        assignment_type=assignment_type,
                        image_path=st.session_state.get('image_path'),
                        extracted_text=st.session_state.extracted_text,
                        original_text=st.session_state.extracted_text
                    )
                    session.add(submission)
                    session.flush()
                    
                    # Save evaluation
                    evaluation = Evaluation(
                        submission_id=submission.id,
                        rubric_id=rubric['id'],
                        overall_score=evaluation_result['overall_score'],
                        detailed_scores=json.dumps(evaluation_result['detailed_scores']),
                        feedback=evaluation_result['feedback'],
                        strengths=json.dumps(evaluation_result['strengths']),
                        weaknesses=json.dumps(evaluation_result['weaknesses']),
                        suggestions=json.dumps(evaluation_result['suggestions'])
                    )
                    session.add(evaluation)
                    session.commit()
                    
                    st.balloons()  # Celebration animation
                    st.success("✅ Evaluation completed successfully!")
                    st.session_state.last_evaluation = evaluation_result
                    st.session_state.last_submission_id = submission.id
                    
                    # Display results
                    display_evaluation_results(evaluation_result)
                    
                except Exception as e:
                    st.error(f"❌ Error during evaluation: {str(e)}")
                    st.exception(e)

def display_evaluation_results(evaluation_result):
    """Display evaluation results in an attractive format"""
    st.markdown("---")
    st.markdown('<h2 class="sub-header">📊 Evaluation Results</h2>', unsafe_allow_html=True)
    
    # Overall score with enhanced cards
    score = evaluation_result['overall_score']
    score_color = "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
    
    # Score cards with gradient backgrounds
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, {score_color} 0%, {score_color}dd 100%);">
                <div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0.5rem;">Overall Score</div>
                <div style="font-size: 3rem; font-weight: 800;">{score:.1f}<span style="font-size: 1.5rem;">/100</span></div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
        grade_color = "#10b981" if grade in ["A", "B"] else "#f59e0b" if grade == "C" else "#ef4444"
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, {grade_color} 0%, {grade_color}dd 100%);">
                <div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0.5rem;">Grade</div>
                <div style="font-size: 4rem; font-weight: 800;">{grade}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status = "Excellent" if score >= 90 else "Good" if score >= 80 else "Satisfactory" if score >= 70 else "Needs Improvement"
        status_icon = "🌟" if score >= 90 else "👍" if score >= 80 else "✅" if score >= 70 else "📚"
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0.5rem;">Status</div>
                <div style="font-size: 2rem; font-weight: 800;">{status_icon} {status}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Detailed scores chart
    st.markdown("### 📈 Detailed Scores")
    scores_data = {
        'Criterion': [],
        'Score': []
    }
    for criterion, data in evaluation_result['detailed_scores'].items():
        scores_data['Criterion'].append(criterion.replace('_', ' ').title())
        scores_data['Score'].append(data['score'])
    
    df_scores = pd.DataFrame(scores_data)
    fig = px.bar(
        df_scores, 
        x='Criterion', 
        y='Score',
        color='Score',
        color_continuous_scale='Viridis',
        title="📊 Score Breakdown by Criterion",
        labels={'Score': 'Score (out of 100)', 'Criterion': 'Evaluation Criteria'}
    )
    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins", size=12),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(title_font=dict(size=14, color='#333')),
        yaxis=dict(title_font=dict(size=14, color='#333'))
    )
    fig.update_traces(marker_line_width=2, marker_line_color='white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Feedback
    st.markdown("### 💬 Feedback")
    st.markdown(f'<div class="feedback-box">{evaluation_result["feedback"]}</div>', unsafe_allow_html=True)
    
    # Strengths and Weaknesses with enhanced cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Strengths")
        strengths = evaluation_result.get('strengths', [])
        if strengths:
            for strength in strengths[:5]:
                st.markdown(f'<div class="strength-item">✨ {strength}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-card" style="text-align: center; padding: 2rem;">
                    <p style="color: #999; font-size: 1.1rem;">No specific strengths identified yet.</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ Areas for Improvement")
        weaknesses = evaluation_result.get('weaknesses', [])
        if weaknesses:
            for weakness in weaknesses[:5]:
                st.markdown(f'<div class="weakness-item">📌 {weakness}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);">
                    <p style="color: #10b981; font-size: 1.1rem; font-weight: 600;">🎉 No major weaknesses identified!</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Suggestions
    if evaluation_result.get('suggestions'):
        st.markdown("### 💡 Suggestions")
        for suggestion in evaluation_result['suggestions'][:5]:
            st.info(f"💡 {suggestion}")

def view_results_page():
    st.markdown('<h2 class="sub-header">📈 View Evaluation Results</h2>', unsafe_allow_html=True)
    
    session = st.session_state.db.get_session()
    
    # Search options with enhanced styling
    st.markdown("### 🔍 Search & Filter")
    col1, col2 = st.columns(2)
    with col1:
        search_student_id = st.text_input("Search by Student ID", placeholder="Enter student ID to search...", help="Filter results by student ID")
    with col2:
        search_type = st.selectbox("Filter by Assignment Type", ["All", "algorithm", "flowchart", "pseudocode"], help="Filter by assignment type")
    
    # Get submissions
    query = session.query(Submission).join(Evaluation)
    
    if search_student_id:
        query = query.filter(Submission.student_id == search_student_id)
    if search_type != "All":
        query = query.filter(Submission.assignment_type == search_type)
    
    submissions = query.order_by(Submission.submitted_at.desc()).all()
    
    if not submissions:
        st.markdown("""
            <div class="info-card" style="text-align: center; padding: 3rem;">
                <p style="font-size: 1.5rem; color: #667eea; font-weight: 600; margin-bottom: 1rem;">
                    📭 No Submissions Found
                </p>
                <p style="color: #999; font-size: 1.1rem;">
                    No submissions match your search criteria. Try adjusting your filters or submit a new assignment.
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Display submissions
    for submission in submissions:
        with st.expander(f"📄 {submission.student_name} - {submission.assignment_type.upper()} (Submitted: {submission.submitted_at.strftime('%Y-%m-%d %H:%M')})"):
            # Get evaluation
            evaluation = session.query(Evaluation).filter_by(submission_id=submission.id).first()
            
            if evaluation:
                eval_data = {
                    'overall_score': evaluation.overall_score,
                    'detailed_scores': json.loads(evaluation.detailed_scores),
                    'feedback': evaluation.feedback,
                    'strengths': json.loads(evaluation.strengths) if evaluation.strengths else [],
                    'weaknesses': json.loads(evaluation.weaknesses) if evaluation.weaknesses else [],
                    'suggestions': json.loads(evaluation.suggestions) if evaluation.suggestions else []
                }
                display_evaluation_results(eval_data)
                
                # Show submission details
                st.markdown("### 📝 Submission Details")
                st.text_area("Submitted Answer", submission.extracted_text or submission.original_text, height=150, disabled=True)

def rubric_management_page():
    st.markdown('<h2 class="sub-header">📋 Rubric Management</h2>', unsafe_allow_html=True)
    
    # Display existing rubrics
    rubrics = st.session_state.rubric_manager.get_all_rubrics()
    
    st.markdown("### 📊 Current Rubrics")
    st.markdown("""
        <div class="info-card">
            <p style="margin: 0; color: #667eea; font-weight: 600;">
                💡 These rubrics ensure consistent and fair evaluation for all students
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    for rubric in rubrics:
        type_icon = "🔢" if rubric['type'] == 'algorithm' else "📊" if rubric['type'] == 'flowchart' else "💻"
        with st.expander(f"{type_icon} {rubric['name']} ({rubric['type'].upper()})"):
            st.markdown("#### 📝 Criteria & Weights")
            criteria_df = pd.DataFrame({
                'Criterion': list(rubric['criteria'].keys()),
                'Description': list(rubric['criteria'].values()),
                'Weight': [f"{rubric['weights'][k]*100:.1f}%" for k in rubric['criteria'].keys()]
            })
            st.dataframe(criteria_df, use_container_width=True, hide_index=True)

def analytics_dashboard_page():
    st.markdown('<h2 class="sub-header">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    session = st.session_state.db.get_session()
    
    # Get all evaluations
    evaluations = session.query(Evaluation).all()
    
    if not evaluations:
        st.markdown("""
            <div class="info-card" style="text-align: center; padding: 3rem;">
                <p style="font-size: 1.5rem; color: #667eea; font-weight: 600; margin-bottom: 1rem;">
                    📊 No Analytics Available Yet
                </p>
                <p style="color: #999; font-size: 1.1rem;">
                    Submit some assignments to see detailed analytics and insights!
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Statistics with enhanced cards
    scores = [e.overall_score for e in evaluations]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    st.markdown("### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div style="font-size: 1rem; opacity: 0.9;">Total Evaluations</div>
                <div style="font-size: 2.5rem; font-weight: 800;">{len(evaluations)}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                <div style="font-size: 1rem; opacity: 0.9;">Average Score</div>
                <div style="font-size: 2.5rem; font-weight: 800;">{avg_score:.1f}<span style="font-size: 1.2rem;">/100</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        max_score = max(scores) if scores else 0
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
                <div style="font-size: 1rem; opacity: 0.9;">Highest Score</div>
                <div style="font-size: 2.5rem; font-weight: 800;">{max_score:.1f}<span style="font-size: 1.2rem;">/100</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        min_score = min(scores) if scores else 0
        st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);">
                <div style="font-size: 1rem; opacity: 0.9;">Lowest Score</div>
                <div style="font-size: 2.5rem; font-weight: 800;">{min_score:.1f}<span style="font-size: 1.2rem;">/100</span></div>
            </div>
        """, unsafe_allow_html=True)
    
    # Score distribution
    st.markdown("### 📊 Score Distribution")
    df_scores = pd.DataFrame({'Score': scores})
    fig = px.histogram(
        df_scores, 
        x='Score', 
        nbins=20, 
        title="📈 Distribution of Scores",
        labels={'Score': 'Score (out of 100)', 'count': 'Number of Submissions'},
        color_discrete_sequence=['#667eea']
    )
    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins", size=12),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(title_font=dict(size=14, color='#333')),
        yaxis=dict(title_font=dict(size=14, color='#333'))
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance by assignment type
    st.markdown("### 📋 Performance by Assignment Type")
    type_scores = {}
    for eval_obj in evaluations:
        submission = session.query(Submission).filter_by(id=eval_obj.submission_id).first()
        if submission:
            if submission.assignment_type not in type_scores:
                type_scores[submission.assignment_type] = []
            type_scores[submission.assignment_type].append(eval_obj.overall_score)
    
    type_avg = {k: sum(v)/len(v) for k, v in type_scores.items()}
    df_type = pd.DataFrame({
        'Assignment Type': [t.upper() for t in type_avg.keys()],
        'Average Score': list(type_avg.values())
    })
    fig = px.bar(
        df_type, 
        x='Assignment Type', 
        y='Average Score', 
        title="📊 Average Scores by Assignment Type",
        labels={'Average Score': 'Average Score (out of 100)', 'Assignment Type': 'Type of Assignment'},
        color='Average Score',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins", size=12),
        title_font=dict(size=20, color='#667eea'),
        xaxis=dict(title_font=dict(size=14, color='#333')),
        yaxis=dict(title_font=dict(size=14, color='#333'))
    )
    fig.update_traces(marker_line_width=2, marker_line_color='white')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()


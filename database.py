"""
Database module for storing rubrics, submissions, and evaluations
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Rubric(Base):
    """Rubric template for evaluation"""
    __tablename__ = 'rubrics'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  # 'algorithm', 'flowchart', 'pseudocode'
    criteria = Column(Text, nullable=False)  # JSON string of criteria
    weights = Column(Text, nullable=False)  # JSON string of weights
    created_at = Column(DateTime, default=datetime.utcnow)
    
    evaluations = relationship("Evaluation", back_populates="rubric")

class Submission(Base):
    """Student submission"""
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(100), nullable=False)
    student_name = Column(String(200), nullable=False)
    assignment_type = Column(String(50), nullable=False)  # 'algorithm', 'flowchart', 'pseudocode'
    image_path = Column(String(500))
    extracted_text = Column(Text)
    original_text = Column(Text)  # If text was directly submitted
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    evaluations = relationship("Evaluation", back_populates="submission")

class Evaluation(Base):
    """Evaluation result"""
    __tablename__ = 'evaluations'
    
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    rubric_id = Column(Integer, ForeignKey('rubrics.id'), nullable=False)
    overall_score = Column(Float, nullable=False)
    detailed_scores = Column(Text, nullable=False)  # JSON string
    feedback = Column(Text, nullable=False)
    strengths = Column(Text)  # JSON string
    weaknesses = Column(Text)  # JSON string
    suggestions = Column(Text)  # JSON string
    evaluated_at = Column(DateTime, default=datetime.utcnow)
    
    submission = relationship("Submission", back_populates="evaluations")
    rubric = relationship("Rubric", back_populates="evaluations")

class Database:
    def __init__(self, db_path='evaluator.db'):
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_session(self):
        return self.session
    
    def close(self):
        self.session.close()


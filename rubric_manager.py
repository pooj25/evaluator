"""
Rubric management system for algorithms, flowcharts, and pseudocodes
"""
import json
from database import Database, Rubric
from datetime import datetime

class RubricManager:
    def __init__(self, db):
        self.db = db
        self.session = db.get_session()
        self._initialize_default_rubrics()
    
    def _initialize_default_rubrics(self):
        """Initialize default rubrics if they don't exist"""
        # Check if rubrics already exist
        existing = self.session.query(Rubric).first()
        if existing:
            return
        
        # Algorithm Rubric
        algorithm_criteria = {
            "correctness": "Algorithm correctly solves the problem",
            "efficiency": "Time and space complexity are optimal",
            "clarity": "Algorithm is clearly explained and easy to understand",
            "completeness": "All edge cases and scenarios are handled",
            "structure": "Algorithm follows proper structure and format"
        }
        algorithm_weights = {
            "correctness": 0.35,
            "efficiency": 0.20,
            "clarity": 0.20,
            "completeness": 0.15,
            "structure": 0.10
        }
        
        algo_rubric = Rubric(
            name="Standard Algorithm Evaluation",
            type="algorithm",
            criteria=json.dumps(algorithm_criteria),
            weights=json.dumps(algorithm_weights)
        )
        
        # Flowchart Rubric
        flowchart_criteria = {
            "symbols": "Correct use of flowchart symbols (start/end, process, decision, etc.)",
            "logic": "Logical flow and sequence are correct",
            "completeness": "All steps are included and properly connected",
            "clarity": "Flowchart is clear and easy to follow",
            "formatting": "Proper formatting and visual organization"
        }
        flowchart_weights = {
            "symbols": 0.25,
            "logic": 0.30,
            "completeness": 0.25,
            "clarity": 0.15,
            "formatting": 0.05
        }
        
        flowchart_rubric = Rubric(
            name="Standard Flowchart Evaluation",
            type="flowchart",
            criteria=json.dumps(flowchart_criteria),
            weights=json.dumps(flowchart_weights)
        )
        
        # Pseudocode Rubric
        pseudocode_criteria = {
            "syntax": "Proper pseudocode syntax and conventions",
            "logic": "Correct logical flow and algorithm implementation",
            "completeness": "All required steps are present",
            "readability": "Code is readable and well-structured",
            "correctness": "Algorithm correctly solves the problem"
        }
        pseudocode_weights = {
            "syntax": 0.20,
            "logic": 0.30,
            "completeness": 0.20,
            "readability": 0.15,
            "correctness": 0.15
        }
        
        pseudocode_rubric = Rubric(
            name="Standard Pseudocode Evaluation",
            type="pseudocode",
            criteria=json.dumps(pseudocode_criteria),
            weights=json.dumps(pseudocode_weights)
        )
        
        self.session.add(algo_rubric)
        self.session.add(flowchart_rubric)
        self.session.add(pseudocode_rubric)
        self.session.commit()
    
    def get_rubric(self, assignment_type):
        """Get rubric for a specific assignment type"""
        rubric = self.session.query(Rubric).filter_by(type=assignment_type).first()
        if rubric:
            return {
                'id': rubric.id,
                'name': rubric.name,
                'type': rubric.type,
                'criteria': json.loads(rubric.criteria),
                'weights': json.loads(rubric.weights)
            }
        return None
    
    def create_rubric(self, name, assignment_type, criteria, weights):
        """Create a new rubric"""
        rubric = Rubric(
            name=name,
            type=assignment_type,
            criteria=json.dumps(criteria),
            weights=json.dumps(weights)
        )
        self.session.add(rubric)
        self.session.commit()
        return rubric.id
    
    def get_all_rubrics(self):
        """Get all rubrics"""
        rubrics = self.session.query(Rubric).all()
        return [
            {
                'id': r.id,
                'name': r.name,
                'type': r.type,
                'criteria': json.loads(r.criteria),
                'weights': json.loads(r.weights)
            }
            for r in rubrics
        ]


"""
Transformer-based semantic evaluation engine
"""
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

class IntelligentEvaluator:
    def __init__(self):
        # Load pre-trained transformer model for semantic similarity
        print("Loading transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully!")
    
    def evaluate(self, student_answer, rubric, reference_answer=None):
        """
        Evaluate student answer against rubric
        
        Args:
            student_answer: Text extracted from student's submission
            rubric: Rubric dictionary with criteria and weights
            reference_answer: Optional reference answer for comparison
        
        Returns:
            Dictionary with scores, feedback, strengths, weaknesses, suggestions
        """
        criteria = rubric['criteria']
        weights = rubric['weights']
        assignment_type = rubric['type']
        
        detailed_scores = {}
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Normalize student answer
        student_text = self._normalize_text(student_answer)
        
        # Evaluate each criterion
        for criterion, description in criteria.items():
            score, feedback = self._evaluate_criterion(
                student_text, 
                criterion, 
                description, 
                assignment_type,
                reference_answer
            )
            detailed_scores[criterion] = {
                'score': score,
                'max_score': 100,
                'feedback': feedback
            }
            
            # Collect strengths and weaknesses
            if score >= 80:
                strengths.append(f"{criterion}: {feedback}")
            elif score < 60:
                weaknesses.append(f"{criterion}: {feedback}")
                suggestions.append(self._generate_suggestion(criterion, description, assignment_type))
        
        # Calculate overall score
        overall_score = sum(
            detailed_scores[criterion]['score'] * weights[criterion]
            for criterion in criteria.keys()
        )
        
        # Generate comprehensive feedback
        feedback_text = self._generate_feedback(
            overall_score, 
            detailed_scores, 
            strengths, 
            weaknesses,
            assignment_type
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'detailed_scores': detailed_scores,
            'feedback': feedback_text,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions
        }
    
    def _normalize_text(self, text):
        """Normalize text for evaluation"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep programming-related ones
        text = re.sub(r'[^\w\s\-\+\*\/\=\<\>\(\)\[\]\{\}\.,;:]', '', text)
        
        return text.strip()
    
    def _evaluate_criterion(self, student_text, criterion, description, assignment_type, reference_answer=None):
        """Evaluate a specific criterion using semantic similarity"""
        
        if not student_text or len(student_text.strip()) < 10:
            return 0, "Answer is too short or empty. Please provide a complete solution."
        
        # Create semantic embeddings
        criterion_embedding = self.model.encode(description)
        student_embedding = self.model.encode(student_text)
        
        # Base similarity score
        similarity = cosine_similarity(
            [criterion_embedding], 
            [student_embedding]
        )[0][0]
        
        # Criterion-specific evaluation
        score = 0
        feedback = ""
        
        if criterion == "correctness" or criterion == "logic":
            score, feedback = self._evaluate_correctness(student_text, similarity, assignment_type)
        elif criterion == "completeness":
            score, feedback = self._evaluate_completeness(student_text, similarity, assignment_type)
        elif criterion == "clarity" or criterion == "readability":
            score, feedback = self._evaluate_clarity(student_text, similarity, assignment_type)
        elif criterion == "syntax":
            score, feedback = self._evaluate_syntax(student_text, similarity, assignment_type)
        elif criterion == "efficiency":
            score, feedback = self._evaluate_efficiency(student_text, similarity, assignment_type)
        elif criterion == "symbols":
            score, feedback = self._evaluate_symbols(student_text, similarity, assignment_type)
        elif criterion == "structure" or criterion == "formatting":
            score, feedback = self._evaluate_structure(student_text, similarity, assignment_type)
        else:
            # Generic evaluation based on similarity
            score = int(similarity * 100)
            feedback = f"Evaluation based on semantic similarity: {description}"
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return score, feedback
    
    def _evaluate_correctness(self, text, similarity, assignment_type):
        """Evaluate correctness of the solution"""
        # Check for common algorithm patterns
        keywords = {
            'algorithm': ['start', 'end', 'input', 'output', 'process', 'return'],
            'flowchart': ['start', 'end', 'decision', 'process', 'input', 'output'],
            'pseudocode': ['begin', 'end', 'if', 'then', 'else', 'while', 'for', 'function']
        }
        
        relevant_keywords = keywords.get(assignment_type, [])
        found_keywords = sum(1 for kw in relevant_keywords if kw in text)
        
        keyword_score = (found_keywords / len(relevant_keywords)) * 30 if relevant_keywords else 0
        similarity_score = similarity * 70
        
        score = int(keyword_score + similarity_score)
        feedback = f"Solution demonstrates {'good' if score >= 70 else 'moderate' if score >= 50 else 'limited'} understanding of the problem."
        
        return score, feedback
    
    def _evaluate_completeness(self, text, similarity, assignment_type):
        """Evaluate completeness of the solution"""
        # Check for essential components
        length_score = min(100, (len(text) / 200) * 50)  # Assume 200 chars is good length
        structure_score = similarity * 50
        
        score = int(length_score + structure_score)
        feedback = f"Solution is {'complete' if score >= 70 else 'mostly complete' if score >= 50 else 'incomplete'}."
        
        return score, feedback
    
    def _evaluate_clarity(self, text, similarity, assignment_type):
        """Evaluate clarity and readability"""
        # Check for proper structure
        has_structure = any(marker in text for marker in ['\n', '.', ';', ':', 'step'])
        structure_bonus = 20 if has_structure else 0
        
        similarity_score = similarity * 80
        
        score = int(similarity_score + structure_bonus)
        feedback = f"Solution is {'clear and well-organized' if score >= 70 else 'somewhat clear' if score >= 50 else 'unclear'}."
        
        return score, feedback
    
    def _evaluate_syntax(self, text, similarity, assignment_type):
        """Evaluate syntax for pseudocode"""
        # Check for proper pseudocode syntax
        syntax_markers = ['begin', 'end', 'if', 'then', 'else', 'while', 'for', 'function', 'procedure']
        found_markers = sum(1 for marker in syntax_markers if marker in text)
        
        syntax_score = (found_markers / len(syntax_markers)) * 60 if syntax_markers else 0
        similarity_score = similarity * 40
        
        score = int(syntax_score + similarity_score)
        feedback = f"Syntax is {'correct' if score >= 70 else 'mostly correct' if score >= 50 else 'needs improvement'}."
        
        return score, feedback
    
    def _evaluate_efficiency(self, text, similarity, assignment_type):
        """Evaluate efficiency considerations"""
        # Check for efficiency-related keywords
        efficiency_keywords = ['complexity', 'time', 'space', 'optimize', 'efficient', 'algorithm']
        found_keywords = sum(1 for kw in efficiency_keywords if kw in text)
        
        keyword_score = (found_keywords / len(efficiency_keywords)) * 40
        similarity_score = similarity * 60
        
        score = int(keyword_score + similarity_score)
        feedback = f"Efficiency considerations are {'well addressed' if score >= 70 else 'partially addressed' if score >= 50 else 'not addressed'}."
        
        return score, feedback
    
    def _evaluate_symbols(self, text, similarity, assignment_type):
        """Evaluate use of flowchart symbols"""
        # Check for flowchart-related terms
        symbol_keywords = ['start', 'end', 'decision', 'process', 'input', 'output', 'connector']
        found_keywords = sum(1 for kw in symbol_keywords if kw in text)
        
        keyword_score = (found_keywords / len(symbol_keywords)) * 50
        similarity_score = similarity * 50
        
        score = int(keyword_score + similarity_score)
        feedback = f"Flowchart symbols are {'correctly used' if score >= 70 else 'mostly correct' if score >= 50 else 'incorrectly used'}."
        
        return score, feedback
    
    def _evaluate_structure(self, text, similarity, assignment_type):
        """Evaluate structure and formatting"""
        # Check for proper formatting
        has_line_breaks = '\n' in text or len(text.split()) > 10
        has_punctuation = any(p in text for p in ['.', ';', ':'])
        
        structure_score = 30 if has_line_breaks else 0
        punctuation_score = 20 if has_punctuation else 0
        similarity_score = similarity * 50
        
        score = int(structure_score + punctuation_score + similarity_score)
        feedback = f"Structure is {'well-formatted' if score >= 70 else 'adequately formatted' if score >= 50 else 'poorly formatted'}."
        
        return score, feedback
    
    def _generate_suggestion(self, criterion, description, assignment_type):
        """Generate improvement suggestions"""
        suggestions_map = {
            'correctness': f"Review the problem requirements and ensure your {assignment_type} correctly addresses all aspects.",
            'completeness': f"Make sure to include all necessary steps in your {assignment_type}.",
            'clarity': f"Organize your {assignment_type} with clear structure and proper formatting.",
            'syntax': f"Follow proper {assignment_type} syntax conventions and formatting rules.",
            'efficiency': f"Consider the time and space complexity of your solution.",
            'logic': f"Review the logical flow of your {assignment_type} to ensure correctness.",
            'symbols': f"Use appropriate flowchart symbols correctly for each operation.",
            'structure': f"Improve the formatting and organization of your {assignment_type}."
        }
        
        return suggestions_map.get(criterion, f"Work on improving {criterion}: {description}")
    
    def _generate_feedback(self, overall_score, detailed_scores, strengths, weaknesses, assignment_type):
        """Generate comprehensive feedback"""
        feedback_parts = []
        
        # Overall assessment
        if overall_score >= 90:
            feedback_parts.append("Excellent work! Your solution demonstrates a strong understanding.")
        elif overall_score >= 80:
            feedback_parts.append("Good work! Your solution is well-developed with minor areas for improvement.")
        elif overall_score >= 70:
            feedback_parts.append("Satisfactory work. Your solution meets the basic requirements.")
        elif overall_score >= 60:
            feedback_parts.append("Your solution needs improvement in several areas.")
        else:
            feedback_parts.append("Your solution requires significant improvement.")
        
        # Add strengths
        if strengths:
            feedback_parts.append(f"\nStrengths:\n" + "\n".join(f"• {s}" for s in strengths[:3]))
        
        # Add weaknesses
        if weaknesses:
            feedback_parts.append(f"\nAreas for Improvement:\n" + "\n".join(f"• {w}" for w in weaknesses[:3]))
        
        # Detailed scores
        feedback_parts.append("\nDetailed Scores:")
        for criterion, data in detailed_scores.items():
            feedback_parts.append(f"  {criterion.replace('_', ' ').title()}: {data['score']}/100")
        
        return "\n".join(feedback_parts)


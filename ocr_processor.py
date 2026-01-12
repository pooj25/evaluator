"""
OCR module for extracting text from flowchart and pseudocode images
"""
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
import os

class OCRProcessor:
    def __init__(self):
        # Configure Tesseract path (Windows default)
        # For Linux/Mac, this might not be needed
        try:
            # Common Windows Tesseract path
            tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
        except:
            pass  # Use system default if not found
    
    def enhance_image_quality(self, img):
        """Enhance image quality for blurry images"""
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()
        
        # Upscale image for better OCR (2x upscaling)
        height, width = gray.shape
        upscaled = cv2.resize(gray, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(upscaled)
        
        return enhanced
    
    def deblur_image(self, img):
        """Apply deblurring techniques for blurry images"""
        # Create a sharpening kernel
        sharpen_kernel = np.array([[-1, -1, -1],
                                   [-1,  9, -1],
                                   [-1, -1, -1]])
        sharpened = cv2.filter2D(img, -1, sharpen_kernel)
        
        # Alternative: Unsharp masking
        gaussian = cv2.GaussianBlur(img, (0, 0), 2.0)
        unsharp = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0)
        
        # Use the better result (compare variance)
        if np.var(sharpened) > np.var(unsharp):
            return sharpened
        return unsharp
    
    def preprocess_image(self, image_path, method='enhanced'):
        """Preprocess image for better OCR results with multiple strategies"""
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if method == 'enhanced':
            # Enhanced preprocessing for blurry images
            # Step 1: Enhance image quality (upscale + contrast)
            enhanced = self.enhance_image_quality(gray)
            
            # Step 2: Apply deblurring
            deblurred = self.deblur_image(enhanced)
            
            # Step 3: Apply denoising (reduced strength to preserve details)
            denoised = cv2.fastNlMeansDenoising(deblurred, None, 5, 7, 21)
            
            # Step 4: Apply adaptive thresholding (better for varying lighting)
            thresh = cv2.adaptiveThreshold(
                denoised, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Step 5: Apply morphological operations to clean up
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
            
        elif method == 'aggressive':
            # Aggressive preprocessing for very blurry images
            # Upscale more
            height, width = gray.shape
            upscaled = cv2.resize(gray, (width * 3, height * 3), interpolation=cv2.INTER_CUBIC)
            
            # Strong sharpening
            sharpen_kernel = np.array([[-1, -1, -1, -1, -1],
                                       [-1,  2,  2,  2, -1],
                                       [-1,  2,  8,  2, -1],
                                       [-1,  2,  2,  2, -1],
                                       [-1, -1, -1, -1, -1]]) / 8.0
            sharpened = cv2.filter2D(upscaled, -1, sharpen_kernel)
            
            # CLAHE for contrast
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(sharpened)
            
            # Adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                enhanced, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 15, 5
            )
            
            # Morphological cleanup
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
        else:
            # Standard preprocessing (original method)
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text(self, image_path, preprocess=True, method='enhanced'):
        """Extract text from image with improved preprocessing for blurry images"""
        try:
            if preprocess:
                processed_img = self.preprocess_image(image_path, method=method)
                # Convert back to PIL Image
                pil_img = Image.fromarray(processed_img)
            else:
                pil_img = Image.open(image_path)
            
            # Try multiple PSM modes for better accuracy
            psm_modes = [
                (6, r'--oem 3 --psm 6'),  # Uniform block of text
                (11, r'--oem 3 --psm 11'),  # Sparse text
                (12, r'--oem 3 --psm 12'),  # Sparse text with OSD
                (3, r'--oem 3 --psm 3'),  # Fully automatic page segmentation
            ]
            
            best_text = ""
            best_confidence = 0
            
            for psm_num, config in psm_modes:
                try:
                    text = pytesseract.image_to_string(pil_img, config=config)
                    # Get confidence for this mode
                    data = pytesseract.image_to_data(pil_img, config=config, output_type=pytesseract.Output.DICT)
                    confidences = [int(data['conf'][i]) for i in range(len(data['text'])) if int(data['conf'][i]) > 0]
                    avg_conf = sum(confidences) / len(confidences) if confidences else 0
                    
                    if avg_conf > best_confidence and len(text.strip()) > len(best_text.strip()):
                        best_text = text
                        best_confidence = avg_conf
                except:
                    continue
            
            # If no good result, use default
            if not best_text:
                custom_config = r'--oem 3 --psm 6'
                best_text = pytesseract.image_to_string(pil_img, config=custom_config)
            
            # Clean up extracted text
            text = self.clean_text(best_text)
            
            return text
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def clean_text(self, text):
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep programming-related ones
        # Keep: letters, numbers, spaces, and common programming symbols
        text = re.sub(r'[^\w\s\-\+\*\/\=\<\>\(\)\[\]\{\}\.,;:!?]', '', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    def extract_with_confidence(self, image_path, method='enhanced'):
        """Extract text with confidence scores, trying multiple preprocessing methods"""
        try:
            results = []
            
            # Try different preprocessing methods
            methods = ['enhanced', 'aggressive', 'standard']
            
            for preprocess_method in methods:
                try:
                    processed_img = self.preprocess_image(image_path, method=preprocess_method)
                    pil_img = Image.fromarray(processed_img)
                    
                    # Try multiple PSM modes
                    psm_modes = [
                        (6, r'--oem 3 --psm 6'),
                        (11, r'--oem 3 --psm 11'),
                        (12, r'--oem 3 --psm 12'),
                        (3, r'--oem 3 --psm 3'),
                    ]
                    
                    for psm_num, config in psm_modes:
                        try:
                            # Get text
                            text = pytesseract.image_to_string(pil_img, config=config)
                            
                            # Get detailed data including confidence
                            data = pytesseract.image_to_data(pil_img, config=config, output_type=pytesseract.Output.DICT)
                            
                            text_parts = []
                            confidences = []
                            
                            for i in range(len(data['text'])):
                                if int(data['conf'][i]) > 0:
                                    text_parts.append(data['text'][i])
                                    confidences.append(int(data['conf'][i]))
                            
                            if confidences:
                                full_text = ' '.join(text_parts)
                                avg_confidence = sum(confidences) / len(confidences)
                                
                                results.append({
                                    'text': full_text,
                                    'confidence': avg_confidence,
                                    'word_count': len(text_parts),
                                    'method': preprocess_method,
                                    'psm': psm_num
                                })
                        except:
                            continue
                except:
                    continue
            
            # Select best result based on confidence and text length
            if results:
                # Sort by confidence, then by text length
                best_result = max(results, key=lambda x: (x['confidence'], len(x['text'])))
                return {
                    'text': self.clean_text(best_result['text']),
                    'confidence': best_result['confidence'],
                    'word_count': best_result['word_count'],
                    'method_used': best_result['method']
                }
            else:
                # Fallback to standard method
                processed_img = self.preprocess_image(image_path, method='standard')
                pil_img = Image.fromarray(processed_img)
                data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
                
                text_parts = []
                confidences = []
                
                for i in range(len(data['text'])):
                    if int(data['conf'][i]) > 0:
                        text_parts.append(data['text'][i])
                        confidences.append(int(data['conf'][i]))
                
                full_text = ' '.join(text_parts)
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                
                return {
                    'text': self.clean_text(full_text),
                    'confidence': avg_confidence,
                    'word_count': len(text_parts),
                    'method_used': 'standard'
                }
                
        except Exception as e:
            raise Exception(f"OCR processing with confidence failed: {str(e)}")


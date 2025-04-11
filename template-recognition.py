import json
import os
import cv2
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import pytesseract

class TemplateManager:
    """Manages form templates for efficient recognition"""
    
    def __init__(self, templates_dir: str = 'templates'):
        """
        Initialize the template manager
        
        Args:
            templates_dir: Directory where template definitions are stored
        """
        self.templates_dir = templates_dir
        self.templates = {}
        
        # Create templates directory if it doesn't exist
        os.makedirs(templates_dir, exist_ok=True)
        
        # Load existing templates
        self._load_templates()
    
    def _load_templates(self):
        """Load templates from the templates directory"""
        if not os.path.exists(self.templates_dir):
            return
            
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                template_path = os.path.join(self.templates_dir, filename)
                with open(template_path, 'r') as f:
                    template_data = json.load(f)
                    if 'template_id' in template_data:
                        self.templates[template_data['template_id']] = template_data
    
    def save_template(self, template_data: Dict[str, Any]) -> bool:
        """
        Save a new template or update an existing one
        
        Args:
            template_data: Template definition
            
        Returns:
            True if successful, False otherwise
        """
        if 'template_id' not in template_data:
            return False
            
        template_id = template_data['template_id']
        filename = f"{template_id}.json"
        file_path = os.path.join(self.templates_dir, filename)
        
        try:
            with open(file_path, 'w') as f:
                json.dump(template_data, f, indent=2)
            
            # Update in-memory cache
            self.templates[template_id] = template_data
            return True
        except Exception as e:
            print(f"Error saving template: {str(e)}")
            return False
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """Get a list of all templates"""
        return list(self.templates.values())
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template by ID"""
        if template_id not in self.templates:
            return False
            
        filename = f"{template_id}.json"
        file_path = os.path.join(self.templates_dir, filename)
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove from in-memory cache
            del self.templates[template_id]
            return True
        except Exception as e:
            print(f"Error deleting template: {str(e)}")
            return False

class TemplateRecognizer:
    """Recognizes form templates and extracts data based on templates"""
    
    def __init__(self, template_manager: TemplateManager):
        """
        Initialize the template recognizer
        
        Args:
            template_manager: Manager for accessing templates
        """
        self.template_manager = template_manager
        
    def identify_template(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Identify which template the form image matches
        
        Args:
            image: The form image
            
        Returns:
            Tuple of (template_id, confidence) or (None, 0.0) if no match
        """
        best_match = None
        best_confidence = 0.0
        
        # Get all templates
        templates = self.template_manager.list_templates()
        
        # Extract text from the image
        text = pytesseract.image_to_string(image)
        
        # Extract key feature points from the image
        keypoints, descriptors = self._extract_features(image)
        
        if descriptors is None:
            # Fall back to text-based matching if feature extraction fails
            return self._match_by_text(text, templates)
        
        # Try to match each template
        for template in templates:
            # Skip templates without feature descriptors
            if 'descriptors' not in template:
                continue
                
            # Convert stored descriptors back to numpy array
            template_descriptors = np.array(template['descriptors'], dtype=np.float32)
            
            # Match features using FLANN matcher
            matcher = cv2.FlannBasedMatcher()
            matches = matcher.knnMatch(descriptors, template_descriptors, k=2)
            
            # Apply ratio test
            good_matches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
            
            # Calculate confidence based on number of good matches
            confidence = len(good_matches) / max(len(keypoints), 1)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = template['template_id']
        
        # If confidence is too low, try text-based matching
        if best_confidence < 0.3:
            text_match, text_confidence = self._match_by_text(text, templates)
            if text_confidence > best_confidence:
                return text_match, text_confidence
        
        return best_match, best_confidence
    
    def _match_by_text(self, text: str, templates: List[Dict[str, Any]]) -> Tuple[Optional[str], float]:
        """Match templates based on text content"""
        best_match = None
        best_confidence = 0.0
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        for template in templates:
            if 'keywords' not in template:
                continue
                
            keywords = template['keywords']
            matches = 0
            
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matches += 1
            
            confidence = matches / max(len(keywords), 1)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = template['template_id']
        
        return best_match, best_confidence
    
    def _extract_features(self, image: np.ndarray) -> Tuple[List, np.ndarray]:
        """Extract feature keypoints and descriptors from an image"""
        # Convert to grayscale
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Create SIFT detector
        sift = cv2.SIFT_create()
        
        # Detect keypoints and compute descriptors
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        
        return keypoints, descriptors
    
    def create_template(self, image: np.ndarray, template_id: str, template_name: str, 
                       fields: List[Dict[str, Any]], keywords: List[str] = None) -> Dict[str, Any]:
        """
        Create a new template from an image
        
        Args:
            image: The form image
            template_id: Unique identifier for the template
            template_name: Human-readable name for the template
            fields: List of field definitions
            keywords: List of keywords for text-based matching
            
        Returns:
            The created template definition
        """
        # Extract keypoints and descriptors
        keypoints, descriptors = self._extract_features(image)
        
        # Create template definition
        template = {
            'template_id': template_id,
            'template_name': template_name,
            'fields': fields,
            'keywords': keywords or [],
        }
        
        # Add descriptors if available (convert to list for JSON serialization)
        if descriptors is not None:
            template['descriptors'] = descriptors.tolist()
        
        # Save the template
        self.template_manager.save_template(template)
        
        return template
    
    def extract_data_from_template(self, image: np.ndarray, template_id: str) -> Dict[str, Any]:
        """
        Extract form data based on a specific template
        
        Args:
            image: The form image
            template_id: ID of the template to use
            
        Returns:
            Dictionary of extracted field values
        """
        # Get the template
        template = self.template_manager.get_template(template_id)
        if not template:
            return {}
        
        # Result dictionary
        data = {}
        
        # Extract text from the entire image
        full_text = pytesseract.image_to_string(image)
        text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Process each field in the template
        for field in template['fields']:
            field_type = field.get('type', 'text')
            field_name = field['name']
            
            if field_type == 'text':
                # Try to extract value based on field labels
                value = self._extract_text_field(image, field, text_data)
            elif field_type == 'checkbox':
                # Check if checkbox is selected
                value = self._extract_checkbox_field(image, field)
            elif field_type == 'radio':
                # Check which radio button is selected
                value = self._extract_radio_field(image, field)
            else:
                # Unknown field type
                value = None
            
            # Store extracted value
            data[field_name] = value
        
        return data
    
    def _extract_text_field(self, image: np.ndarray, field: Dict[str, Any], 
                           text_data: Dict[str, Any]) -> Optional[str]:
        """Extract value from a text field"""
        # If we have region coordinates
        if 'region' in field:
            x, y, w, h = field['region']
            
            # Extract region from image
            region = image[y:y+h, x:x+w]
            
            # Perform OCR on the region
            text = pytesseract.image_to_string(region).strip()
            
            return text if text else None
        
        # If we have a label
        elif 'label' in field:
            label = field['label']
            
            # Find the label in the text data
            for i, word in enumerate(text_data['text']):
                if label in word and text_data['conf'][i] > 60:
                    label_x = text_data['left'][i]
                    label_y = text_data['top'][i]
                    label_h = text_data['height'][i]
                    
                    # Look for text to the right or below the label
                    value_candidates = []
                    for j, other_word in enumerate(text_data['text']):
                        if other_word.strip() and text_data['conf'][j] > 60:
                            other_x = text_data['left'][j]
                            other_y = text_data['top'][j]
                            
                            # Text is to the right of the label
                            if (abs(other_y - label_y) < label_h * 1.5 and 
                                other_x > label_x + text_data['width'][i]):
                                value_candidates.append((other_word, other_x))
                            
                            # Text is below the label
                            elif (other_y > label_y + label_h * 1.5 and 
                                  other_y < label_y + label_h * 4 and
                                  abs(other_x - label_x) < text_data['width'][i] * 2):
                                value_candidates.append((other_word, other_y))
                    
                    # Sort candidates by position (closest first)
                    value_candidates.sort(key=lambda x: x[1])
                    
                    if value_candidates:
                        return value_candidates[0][0]
        
        return None
    
    def _extract_checkbox_field(self, image: np.ndarray, field: Dict[str, Any]) -> bool:
        """Extract value from a checkbox field"""
        if 'region' not in field:
            return False
            
        x, y, w, h = field['region']
        
        # Extract checkbox region
        checkbox = image[y:y+h, x:x+w]
        
        # Convert to grayscale and threshold
        if len(checkbox.shape) > 2:
            gray = cv2.cvtColor(checkbox, cv2.COLOR_BGR2GRAY)
        else:
            gray = checkbox
            
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Calculate percentage of filled pixels
        filled_ratio = np.sum(binary > 0) / (w * h)
        
        # Consider checkbox checked if more than 20% is filled
        return filled_ratio > 0.2
    
    def _extract_radio_field(self, image: np.ndarray, field: Dict[str, Any]) -> Optional[str]:
        """Extract value from a radio button field"""
        if 'options' not in field:
            return None
            
        # Check each option
        for option in field['options']:
            if 'region' not in option:
                continue
                
            x, y, w, h = option['region']
            
            # Extract radio button region
            radio = image[y:y+h, x:x+w]
            
            # Convert to grayscale and threshold
            if len(radio.shape) > 2:
                gray = cv2.cvtColor(radio, cv2.COLOR_BGR2GRAY)
            else:
                gray = radio
                
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Calculate percentage of filled pixels
            filled_ratio = np.sum(binary > 0) / (w * h)
            
            # Consider radio button selected if more than 20% is filled
            if filled_ratio > 0.2:
                return option.get('value', None)
        
        return None

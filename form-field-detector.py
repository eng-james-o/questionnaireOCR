import cv2
import numpy as np
from typing import List, Dict, Tuple, Any
import pytesseract

class FormFieldDetector:
    """Class for detecting form fields in images of questionnaires"""
    
    def __init__(self):
        # Initialize any model parameters or resources
        pass
    
    def detect_fields(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect form fields in an image
        
        Args:
            image: The preprocessed image
            
        Returns:
            A list of dictionaries containing field information
        """
        # This implementation combines multiple techniques for robust field detection
        
        # 1. Detect lines to identify form structure
        horizontal_lines, vertical_lines = self._detect_lines(image)
        
        # 2. Detect text regions
        text_regions = self._detect_text_regions(image)
        
        # 3. Identify checkboxes, radio buttons, etc.
        input_elements = self._detect_input_elements(image)
        
        # 4. Combine the information to identify form fields
        fields = self._combine_detections(horizontal_lines, vertical_lines, 
                                         text_regions, input_elements)
        
        return fields
    
    def _detect_lines(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Detect horizontal and vertical lines in the form"""
        # Create copies of the image for horizontal and vertical line detection
        horizontal = image.copy()
        vertical = image.copy()
        
        # Define kernel sizes based on image dimensions
        img_height, img_width = image.shape[:2]
        horizontal_kernel_size = img_width // 30
        vertical_kernel_size = img_height // 30
        
        # Define kernels for morphological operations
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_kernel_size, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_kernel_size))
        
        # Apply morphology operations to extract horizontal lines
        horizontal = cv2.erode(horizontal, horizontal_kernel, iterations=3)
        horizontal = cv2.dilate(horizontal, horizontal_kernel, iterations=3)
        
        # Apply morphology operations to extract vertical lines
        vertical = cv2.erode(vertical, vertical_kernel, iterations=3)
        vertical = cv2.dilate(vertical, vertical_kernel, iterations=3)
        
        return horizontal, vertical
    
    def _detect_text_regions(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect text regions in the form"""
        # Use pytesseract to get bounding boxes of text
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        text_regions = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            if int(data['conf'][i]) > 60 and data['text'][i].strip() != '':
                text_region = {
                    'text': data['text'][i],
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'w': data['width'][i],
                    'h': data['height'][i],
                    'type': 'text'
                }
                text_regions.append(text_region)
        
        return text_regions
    
    def _detect_input_elements(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect input elements like checkboxes, radio buttons, etc."""
        # Convert to grayscale if not already
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Threshold the image
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        input_elements = []
        
        for contour in contours:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter out very small contours (likely noise)
            if w < 10 or h < 10:
                continue
                
            # Calculate aspect ratio
            aspect_ratio = float(w) / h
            
            # Classify the shape based on properties
            if 0.9 < aspect_ratio < 1.1:  # Almost square - checkbox or radio button
                if self._is_circle(contour):
                    element_type = 'radio'
                else:
                    element_type = 'checkbox'
            elif aspect_ratio > 3:  # Very wide - text field
                element_type = 'text_field'
            else:
                element_type = 'unknown'
            
            input_elements.append({
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'type': element_type
            })
        
        return input_elements
    
    def _is_circle(self, contour: np.ndarray) -> bool:
        """Check if a contour is approximately circular"""
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return False
            
        # Circularity = 4*π*area/perimeter²
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Perfect circle has circularity of 1
        return circularity > 0.8
    
    def _combine_detections(self, horizontal_lines: np.ndarray, vertical_lines: np.ndarray, 
                           text_regions: List[Dict[str, Any]], 
                           input_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Combine all detections to identify form fields"""
        fields = []
        
        # Group text regions into lines
        text_lines = self._group_text_by_lines(text_regions)
        
        # For each text line, find associated input elements
        for line in text_lines:
            # Get the y-coordinate range for this line
            min_y = min(region['y'] for region in line)
            max_y = max(region['y'] + region['h'] for region in line)
            
            # Find input elements that are horizontally aligned with this text line
            aligned_elements = []
            for element in input_elements:
                element_center_y = element['y'] + element['h'] / 2
                if min_y <= element_center_y <= max_y:
                    aligned_elements.append(element)
            
            # Construct field information
            if aligned_elements:
                # This is likely a form field with input elements
                field_text = ' '.join(region['text'] for region in line)
                
                field = {
                    'label': field_text,
                    'elements': aligned_elements,
                    'type': aligned_elements[0]['type'],  # Use the type of the first element
                    'y': min_y,
                    'value': None  # Will be filled during value extraction
                }
                fields.append(field)
            elif len(line) == 1 and ':' in line[0]['text']:
                # This might be a field with text input area
                parts = line[0]['text'].split(':', 1)
                if len(parts) == 2:
                    field = {
                        'label': parts[0].strip(),
                        'elements': [],
                        'type': 'text_field',
                        'y': line[0]['y'],
                        'value': parts[1].strip() if parts[1].strip() else None
                    }
                    fields.append(field)
        
        # Sort fields by vertical position
        fields.sort(key=lambda f: f['y'])
        
        return fields
    
    def _group_text_by_lines(self, text_regions: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Group text regions into lines based on vertical position"""
        if not text_regions:
            return []
            
        # Sort by y-coordinate
        text_regions = sorted(text_regions, key=lambda r: r['y'])
        
        lines = []
        current_line = [text_regions[0]]
        
        # Set initial threshold as percentage of the first region's height
        threshold = current_line[0]['h'] * 0.7
        
        for region in text_regions[1:]:
            # Check if this region belongs to the current line
            if abs(region['y'] - current_line[0]['y']) < threshold:
                current_line.append(region)
            else:
                # Sort the current line by x-coordinate
                current_line = sorted(current_line, key=lambda r: r['x'])
                lines.append(current_line)
                current_line = [region]
                threshold = region['h'] * 0.7
        
        # Add the last line
        if current_line:
            current_line = sorted(current_line, key=lambda r: r['x'])
            lines.append(current_line)
        
        return lines

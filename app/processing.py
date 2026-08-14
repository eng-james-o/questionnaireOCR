import cv2
import numpy as np

def preprocess_image(image):
    """Preprocess an image for better OCR results"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) > 2 else image
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((1, 1), np.uint8)
    return cv2.dilate(binary, kernel, iterations=1)

def extract_data_from_fields(image, fields):
    """Extract data from detected form fields"""
    form_data = {}
    for i, field in enumerate(fields):
        field_type = field.get('type', 'unknown')
        field_label = field.get('label', f'Field_{i+1}').replace(':', '').strip()
        if field_type == 'checkbox':
            elements = field.get('elements', [])
            form_data[field_label] = 'Yes' if any(elem.get('value', False) for elem in elements) else 'No'
        elif field_type == 'radio':
            elements = field.get('elements', [])
            form_data[field_label] = next((elem.get('value') for elem in elements if elem.get('value')), 'None')
        else:
            form_data[field_label] = field.get('value', 'N/A')
    return form_data

def convert_detected_to_template_fields(detected_fields):
    """Convert detected fields to template field format"""
    template_fields = []
    for i, field in enumerate(detected_fields):
        field_type = field.get('type', 'text')
        field_label = field.get('label', f'Field_{i+1}').replace(':', '').strip()
        template_field = {'name': field_label, 'type': field_type}
        if 'x' in field and 'y' in field and 'w' in field and 'h' in field:
            template_field['region'] = [field['x'], field['y'], field['w'], field['h']]
        if field_type == 'radio' and 'elements' in field:
            template_field['options'] = [{'value': f'Option_{j+1}', 'region': [elem['x'], elem['y'], elem['w'], elem['h']]} for j, elem in enumerate(field['elements']) if elem.get('type') == 'radio']
        template_fields.append(template_field)
    return template_fields

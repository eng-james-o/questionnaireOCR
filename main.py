import os
import sys
from typing import Dict, Any, List
import argparse
import time
import cv2
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, send_file
import base64
import io
import json

# Import our modules
from form_field_detector import FormFieldDetector
from template_recognition import TemplateManager, TemplateRecognizer

# Initialize Flask app
app = Flask(__name__)

# Initialize components
template_manager = TemplateManager(templates_dir='templates')
template_recognizer = TemplateRecognizer(template_manager)
form_detector = FormFieldDetector()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/process-image', methods=['POST'])
def process_image():
    """Process an image and extract form data"""
    try:
        data = request.json
        if 'image' not in data:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Try to identify a template
        template_id, confidence = template_recognizer.identify_template(processed_image)
        
        # Extract data
        if template_id and confidence > 0.6:
            # Use template-based extraction
            print(f"Using template: {template_id} (confidence: {confidence:.2f})")
            form_data = template_recognizer.extract_data_from_template(processed_image, template_id)
            
            # Add template metadata
            form_data['_template_id'] = template_id
            form_data['_confidence'] = confidence
        else:
            # Fallback to generic form field detection
            print("No matching template found, using generic detection")
            fields = form_detector.detect_fields(processed_image)
            form_data = extract_data_from_fields(processed_image, fields)
        
        return jsonify(form_data)
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/export-excel', methods=['POST'])
def export_excel():
    """Export extracted data to Excel"""
    try:
        data = request.json.get('data', {})
        
        # Create Excel file from data
        df = pd.DataFrame([data])
        
        # Create a BytesIO object to store the Excel file
        output = io.BytesIO()
        
        # Write DataFrame to Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Form Data')
        
        # Seek to the beginning of the BytesIO object
        output.seek(0)
        
        # Return the Excel file as a response
        return send_file(
            output,
            as_attachment=True,
            download_name='form_data.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/create-template', methods=['POST'])
def create_template():
    """Create a new form template"""
    try:
        data = request.json
        
        if not all(key in data for key in ['image', 'template_id', 'template_name']):
            return jsonify({"error": "Missing required template data"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Extract fields if they are not provided
        fields = data.get('fields', [])
        if not fields:
            # Detect fields automatically
            detected_fields = form_detector.detect_fields(processed_image)
            fields = convert_detected_to_template_fields(detected_fields)
        
        # Get keywords if provided
        keywords = data.get('keywords', [])
        
        # Create the template
        template = template_recognizer.create_template(
            processed_image,
            data['template_id'],
            data['template_name'],
            fields,
            keywords
        )
        
        return jsonify({
            "success": True,
            "template_id": template['template_id'],
            "fields_count": len(fields)
        })
    
    except Exception as e:
        print(f"Error creating template: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/templates', methods=['GET'])
def list_templates():
    """List all available templates"""
    templates = template_manager.list_templates()
    
    # Remove large descriptors for response
    for template in templates:
        if 'descriptors' in template:
            del template['descriptors']
    
    return jsonify(templates)

@app.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """Get a specific template"""
    template = template_manager.get_template(template_id)
    
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    # Remove large descriptors for response
    if 'descriptors' in template:
        del template['descriptors']
    
    return jsonify(template)

@app.route('/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete a template"""
    success = template_manager.delete_template(template_id)
    
    if not success:
        return jsonify({"error": "Failed to delete template"}), 404
    
    return jsonify({"success": True})

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Preprocess an image for better OCR results"""
    # Convert to grayscale if needed
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Adaptive threshold to handle different lighting conditions
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    # Dilation to make text clearer
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    
    return dilated

def extract_data_from_fields(image: np.ndarray, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract data from detected form fields"""
    form_data = {}
    
    for i, field in enumerate(fields):
        field_type = field.get('type', 'unknown')
        field_label = field.get('label', f'Field_{i+1}')
        
        # Clean up the field label
        field_label = field_label.replace(':', '').strip()
        
        # Extract value based on field type
        if field_type == 'checkbox':
            elements = field.get('elements', [])
            checked = any(elem.get('value', False) for elem in elements)
            form_data[field_label] = 'Yes' if checked else 'No'
            
        elif field_type == 'radio':
            elements = field.get('elements', [])
            selected = next((elem.get('value') for elem in elements if elem.get('value')), None)
            form_data[field_label] = selected or 'None'
            
        else:  # text fields
            value = field.get('value', None)
            if value:
                form_data[field_label] = value
            else:
                form_data[field_label] = 'N/A'
    
    return form_data

def convert_detected_to_template_fields(detected_fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert detected fields to template field format"""
    template_fields = []
    
    for i, field in enumerate(detected_fields):
        field_type = field.get('type', 'text')
        field_label = field.get('label', f'Field_{i+1}')
        
        template_field = {
            'name': field_label.replace(':', '').strip(),
            'type': field_type
        }
        
        # Add region if available
        if 'x' in field and 'y' in field and 'w' in field and 'h' in field:
            template_field['region'] = [field['x'], field['y'], field['w'], field['h']]
        
        # Add options for radio buttons
        if field_type == 'radio' and 'elements' in field:
            template_field['options'] = []
            for j, element in enumerate(field['elements']):
                if element.get('type') == 'radio':
                    option = {
                        'value': f'Option_{j+1}',
                        'region': [element['x'], element['y'], element['w'], element['h']]
                    }
                    template_field['options'].append(option)
        
        template_fields.append(template_field)
    
    return template_fields

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Form Recognition API')
    parser.add_argument('--host', default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    app.run(host=args.host, port=args.port, debug=args.debug)

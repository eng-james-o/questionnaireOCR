from flask import Flask, request, jsonify, send_file
import numpy as np
import cv2
import pytesseract
import base64
import pandas as pd
import io
import os
from PIL import Image
from openpyxl import Workbook
from typing import Dict, Any, List, Tuple

app = Flask(__name__)

# Configure pytesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# For Linux/Mac, make sure tesseract is installed

@app.route('/process-image', methods=['POST'])
def process_image():
    """Process the image and extract form data"""
    try:
        # Get base64 image from request
        data = request.json
        if 'image' not in data:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Could not decode image"}), 400
        
        # Process the image
        processed_image = preprocess_image(image)
        
        # Extract form data
        form_data = extract_form_data(processed_image)
        
        return jsonify(form_data)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/export-excel', methods=['POST'])
def export_excel():
    """Export extracted data to Excel"""
    try:
        data = request.json.get('data', {})
        
        # Create Excel file
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
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Preprocess the image for better OCR results"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Noise removal
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    return binary

def extract_form_data(image: np.ndarray) -> Dict[str, Any]:
    """Extract data from the form using OCR"""
    # Extract text from the image
    text = pytesseract.image_to_string(image)
    
    # For a structured approach, we can use image_to_data to get bounding boxes
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Initialize result dictionary
    form_data = {}
    
    # Extract form fields based on your questionnaire structure
    # This is a simplified example - you'll need to adapt this to your specific form layout
    field_mapping = identify_form_fields(data, text)
    
    # In a real application, you would analyze text positions, labels, and answers
    # For this example, we'll use a simple line-by-line approach
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            # Assuming format "Field: Value"
            field, value = line.split(':', 1)
            form_data[field.strip()] = value.strip()
    
    # If no fields were found with simple parsing, return some dummy data
    if not form_data:
        # This is just a fallback for demonstration
        form_data = extract_data_with_ml(text)
    
    return form_data

def identify_form_fields(data: Dict[str, Any], text: str) -> Dict[str, str]:
    """Identify form fields based on OCR data structure"""
    fields = {}
    
    # Extract lines with confidence > 60%
    words = []
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:
            words.append({
                'text': data['text'][i],
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i]
            })
    
    # Group words into lines based on vertical position
    lines = {}
    for word in words:
        if word['text'].strip():
            line_key = word['top'] // 10  # Group by vertical position
            if line_key not in lines:
                lines[line_key] = []
            lines[line_key].append(word)
    
    # Sort lines by vertical position
    sorted_lines = sorted(lines.items())
    
    # Extract field-value pairs
    current_field = None
    for _, line_words in sorted_lines:
        # Sort words in line by horizontal position
        line_words.sort(key=lambda w: w['left'])
        
        line_text = ' '.join(w['text'] for w in line_words)
        
        if ':' in line_text:
            # This line contains both field and value
            parts = line_text.split(':', 1)
            fields[parts[0].strip()] = parts[1].strip()
        elif line_text.endswith(':'):
            # This line contains only a field, value might be on next line
            current_field = line_text[:-1].strip()
        elif current_field is not None:
            # This line might be a value for the previous field
            fields[current_field] = line_text.strip()
            current_field = None
    
    return fields

def extract_data_with_ml(text: str) -> Dict[str, str]:
    """
    Extract form data using ML techniques
    This is a placeholder for more advanced extraction methods
    """
    # In a real application, you might use NLP and ML techniques
    # For now, we'll return some dummy data based on common form fields
    
    result = {}
    
    # Look for common patterns in forms
    if "name" in text.lower():
        result["Name"] = "John Doe"  # This would be extracted from the text
    
    if "age" in text.lower():
        result["Age"] = "30"  # This would be extracted from the text
    
    if "address" in text.lower():
        result["Address"] = "123 Main St"  # This would be extracted from the text
    
    if "phone" in text.lower():
        result["Phone"] = "555-123-4567"  # This would be extracted from the text
    
    if "email" in text.lower():
        result["Email"] = "john.doe@example.com"  # This would be extracted from the text
    
    # Add some default fields if nothing was found
    if not result:
        result = {
            "Field1": "Value1",
            "Field2": "Value2",
            "Field3": "Value3"
        }
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

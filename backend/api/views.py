from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import base64
import cv2
import numpy as np
import pandas as pd
import io
from app import (
    FormFieldDetector,
    TemplateManager,
    TemplateRecognizer,
    preprocess_image,
    extract_data_from_fields,
    convert_detected_to_template_fields,
)


# Initialize components
template_manager = TemplateManager(templates_dir='templates')
template_recognizer = TemplateRecognizer(template_manager)
form_detector = FormFieldDetector()

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({"status": "healthy"})

@api_view(['POST'])
def process_image(request):
    """Process an image and extract form data"""
    try:
        data = request.data
        # print("Received data:", request.data)
        if 'image' not in data:
            return Response({"error": "No image provided"}, status=400)

        # Decode base64 image
        try:
            image_data = base64.b64decode(data['image'])
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"Error decoding base64 image: {e}")
            return Response({"error": f"Image decoding failed: {e}"}, status=400)

        if image is None:
            return Response({"error": "Invalid image data"}, status=400)

        # Preprocess the image
        try:
            processed_image = preprocess_image(image)
        except Exception as e:
            print(f"Image preprocessing error: {e}")
            return Response({"error": f"Image preprocessing failed: {e}"}, status=500)

        # Try to identify a template
        try:
            template_id, confidence = template_recognizer.identify_template(processed_image)
            print(f"Identified template ID: {template_id} with confidence: {confidence}")
        except Exception as e:
            print(f"Template recognition error: {e}")
            return Response({"error": f"Template recognition failed: {e}"}, status=500)

        # Extract data
        try:
            if template_id and confidence > 0.6:
                form_data = template_recognizer.extract_data_from_template(processed_image, template_id)
                form_data['_template_id'] = template_id
                form_data['_confidence'] = confidence
            else:
                fields = form_detector.detect_fields(processed_image)
                form_data = extract_data_from_fields(processed_image, fields)
        except Exception as e:
            print(f"Data extraction error: {e}")
            return Response({"error": f"Data extraction failed: {e}"}, status=500)

        return Response(form_data)

    except Exception as e:
        print(f"Unexpected error: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def export_excel(request):
    """Export extracted data to Excel"""
    try:
        data = request.data.get('data', {})

        # Create Excel file
        df = pd.DataFrame([data])
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Form Data')

        output.seek(0)
        response = JsonResponse({"message": "Excel file created successfully"})
        response['Content-Disposition'] = 'attachment; filename=form_data.xlsx'
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def create_template(request):
    """Create a new form template"""
    try:
        data = request.data

        if not all(key in data for key in ['image', 'template_id', 'template_name']):
            return Response({"error": "Missing required template data"}, status=400)

        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return Response({"error": "Invalid image data"}, status=400)

        # Preprocess the image
        processed_image = preprocess_image(image)

        # Extract fields if they are not provided
        fields = data.get('fields', [])
        if not fields:
            detected_fields = form_detector.detect_fields(processed_image)
            fields = convert_detected_to_template_fields(detected_fields)

        # Create the template
        template = template_recognizer.create_template(
            processed_image,
            data['template_id'],
            data['template_name'],
            fields
        )

        return Response({"success": True, "template_id": template['template_id'], "fields_count": len(fields)})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def list_templates(request):
    """List all available templates"""
    templates = template_manager.list_templates()
    for template in templates:
        if 'descriptors' in template:
            del template['descriptors']
    return Response(templates)

@api_view(['GET'])
def get_template(request, template_id):
    """Get a specific template"""
    template = template_manager.get_template(template_id)
    if not template:
        return Response({"error": "Template not found"}, status=404)
    if 'descriptors' in template:
        del template['descriptors']
    return Response(template)

@api_view(['DELETE'])
def delete_template(request, template_id):
    """Delete a template"""
    success = template_manager.delete_template(template_id)
    if not success:
        return Response({"error": "Failed to delete template"}, status=404)
    return Response({"success": True})


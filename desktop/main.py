import sys
import os
import json
import cv2

# Add parent directory of desktop/ to sys.path so we can import 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from app import (
    TemplateManager,
    TemplateRecognizer,
    FormFieldDetector,
    preprocess_image,
    extract_data_from_fields
)

class FormProcessor(QObject):
    def __init__(self):
        super().__init__()
        templates_dir = os.path.join(parent_dir, 'templates')
        self.template_manager = TemplateManager(templates_dir=templates_dir)
        self.template_recognizer = TemplateRecognizer(self.template_manager)
        self.form_detector = FormFieldDetector()

    @Slot(str, result=dict)
    def processImage(self, image_url):
        try:
            # Strip file:// prefix if present
            if image_url.startswith("file:///"):
                if os.name == 'nt':
                    path = image_url[8:]
                else:
                    path = image_url[7:]
            elif image_url.startswith("file://"):
                path = image_url[7:]
            else:
                path = image_url

            # URL decode the path
            import urllib.parse
            path = urllib.parse.unquote(path)

            if not os.path.exists(path):
                return {"error": f"File does not exist: {path}"}

            image = cv2.imread(path)
            if image is None:
                return {"error": f"Failed to load image: {path}"}

            processed_image = preprocess_image(image)

            # Try template recognition
            template_id, confidence = self.template_recognizer.identify_template(processed_image)

            if template_id and confidence > 0.6:
                form_data = self.template_recognizer.extract_data_from_template(processed_image, template_id)
                form_data['_template_id'] = template_id
                form_data['_confidence'] = confidence
                form_data['_method'] = "Template-based Extraction"
            else:
                fields = self.form_detector.detect_fields(processed_image)
                form_data = extract_data_from_fields(processed_image, fields)
                form_data['_method'] = "Field Detection (No template)"

            return form_data
        except Exception as e:
            return {"error": str(e)}

def main():
    app = QGuiApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Questionnaire OCR Desktop")
    app.setOrganizationName("QuestionnaireOCR")

    engine = QQmlApplicationEngine()

    # Expose python processor to QML
    processor = FormProcessor()
    engine.rootContext().setContextProperty("formProcessor", processor)

    # Load main QML file
    qml_file = os.path.join(current_dir, "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

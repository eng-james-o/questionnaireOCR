from django.test import TestCase, Client
from django.urls import reverse
import base64

from unittest.mock import patch

class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.process_image_url = reverse('process_image')
        self.create_template_url = reverse('create_template')

        # Patch pytesseract calls to decouple tests from system binaries
        self.patcher1 = patch('pytesseract.image_to_string')
        self.patcher2 = patch('pytesseract.image_to_data')
        self.mock_image_to_string = self.patcher1.start()
        self.mock_image_to_data = self.patcher2.start()

        # Set default mocked return values
        self.mock_image_to_string.return_value = "Mocked text"
        self.mock_image_to_data.return_value = {
            'text': [],
            'conf': [],
            'left': [],
            'top': [],
            'width': [],
            'height': []
        }

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_process_image_valid(self):
        # Valid base64 100x100 pixel PNG image
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAIAAAD/gAIDAAAAxUlEQVR4Ae3BAQEAAACCIP1/ugsOCOQyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8sGqJ8AZeonWEsAAAAASUVORK5CYII="
        response = self.client.post(self.process_image_url, {
            'image': base64_image
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_process_image_invalid(self):
        response = self.client.post(self.process_image_url, {
            'image': 'invalid_base64'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_create_template(self):
        # Valid base64 100x100 pixel PNG image
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAIAAAD/gAIDAAAAxUlEQVR4Ae3BAQEAAACCIP1/ugsOCOQyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8vkMrlMLpPL5DK5TC6Ty+QyuUwuk8sGqJ8AZeonWEsAAAAASUVORK5CYII="
        response = self.client.post(self.create_template_url, {
            'image': base64_image,
            'template_id': 'test_template',
            'template_name': 'Test Template'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())

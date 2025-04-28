from django.test import TestCase, Client
from django.urls import reverse
import base64

class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.process_image_url = reverse('process_image')
        self.create_template_url = reverse('create_template')

    def test_process_image_valid(self):
        # Example base64 image (replace with actual base64 string for testing)
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAUA..."
        response = self.client.post(self.process_image_url, {
            'image': base64_image
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

    def test_process_image_invalid(self):
        response = self.client.post(self.process_image_url, {
            'image': 'invalid_base64'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_create_template(self):
        # Example base64 image (replace with actual base64 string for testing)
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAUA..."
        response = self.client.post(self.create_template_url, {
            'image': base64_image,
            'template_id': 'test_template',
            'template_name': 'Test Template'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())

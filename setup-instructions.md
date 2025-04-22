# Questionnaire Scanner App - Setup Guide

This guide will walk you through setting up the Questionnaire Scanner application. The app consists of two main components:

1. React Native mobile app (frontend)
2. Python Flask server (backend)

## Prerequisites

- Node.js and npm (for React Native)
- Python 3.8+ (for the backend)
- Tesseract OCR
- Android Studio (for Android development) or Xcode (for iOS development)

## Backend Setup

### 1. Install Tesseract OCR

#### On Windows

- Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
- Add the Tesseract installation directory to your PATH

#### On MacOS

```bash
brew install tesseract
```

#### On Linux

```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

### 2. Set up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create requirements.txt file with the following content:

```
flask==2.0.1
numpy==1.21.4
opencv-python==4.5.4.60
pytesseract==0.3.9
pandas==1.3.4
openpyxl==3.0.9
Pillow==8.4.0
scikit-image==0.18.3
```

### 4. Create Project Structure

```
backend/
├── __init__.py
├── app.py
├── form_field_detector.py
├── template_recognition.py
├── templates/  # For storing form templates
└── requirements.txt
```

### 5. Start the Backend Server

```bash
python app.py --port 5000
```

The server will start on http://localhost:5000

## Frontend Setup

### 1. Initialize React Native Project

```bash
# Install Expo CLI
npm install -g expo-cli

# Create a new project
expo init questionnaire-scanner

# Navigate to project directory
cd questionnaire-scanner
```

### 2. Install Required Dependencies

```bash
npm install expo-camera expo-image-picker expo-file-system axios
```

### 3. Copy the App.js File

Replace the content of `App.js` with the React Native code provided in this guide.

### 4. Update API Endpoint

In `App.js`, replace `http://YOUR_BACKEND_API/process-image` with your actual backend URL.

If running on a physical device, use your computer's IP address instead of localhost, e.g.:

```javascript
const response = await axios.post('http://192.168.1.100:5000/process-image', {
    image: base64Image
});
```

### 5. Run the App

```bash
expo start
```

Then, use the Expo Go app on your mobile device to scan the QR code, or press 'a' to open on an Android emulator or 'i' for iOS simulator.

## Using the App

1. Launch the app on your device
2. Use the camera to take a picture of a form or select an image from the gallery
3. Tap "Process Image" to extract data from the form
4. View the extracted data on screen
5. Export to Excel if needed

## Creating Form Templates

Templates help improve recognition accuracy for repeated form types:

1. Scan a form by taking a photo
2. Send a POST request to `/create-template` with:

   ```json
   {
     "image": "base64_encoded_image",
     "template_id": "my_form_template",
     "template_name": "My Form Template"
   }
   ```

3. Future scans of similar forms will automatically use this template

## Troubleshooting

- **OCR Not Working Well**: Try adjusting the lighting when taking photos, ensure good contrast between text and background
- **App Crashes**: Check logs for error messages, ensure all dependencies are installed
- **Connection Errors**: Verify backend server is running and accessible, check IP address and port
- **Blurry Images**: Hold the camera steady and ensure good lighting when capturing forms

## Advanced Configuration

### Customizing OCR

Edit the `preprocess_image` function in `app.py` to adjust preprocessing parameters:

```python
def preprocess_image(image):
    # Adjust parameters here
    binary = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2  # Try different values
    )
```

### Adding Custom Form Fields

For complex forms, you can manually define fields in template creation:

```json
{
  "image": "base64_encoded_image",
  "template_id": "custom_form",
  "template_name": "Custom Form",
  "fields": [
    {
      "name": "Full Name",
      "type": "text",
      "region": [100, 200, 400, 50]  // [x, y, width, height]
    },
    {
      "name": "Age",
      "type": "text",
      "region": [100, 300, 100, 50]
    }
  ]
}
```

## Deployment

### Backend Deployment (Example for Docker)

1. Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

2. Build and run the Docker image:

```bash
docker build -t questionnaire-scanner-backend .
docker run -p 5000:5000 questionnaire-scanner-backend
```

### Frontend Deployment

1. For production, build the React Native app:

```bash
expo build:android  # or expo build:ios
```

2. Follow Expo documentation for publishing to app stores.

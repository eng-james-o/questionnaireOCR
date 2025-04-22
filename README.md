# questionnaireOCR

The goal of the project is to develop an OCR application that extracts information from questionnaires, codes the data, and outputs them in tabular format.

## Features

- Extracts text and data from scanned questionnaires using OCR.
- Supports template-based recognition for improved accuracy.
- Detects form fields such as text inputs, checkboxes, and radio buttons.
- Exports extracted data to Excel format.
- React Native frontend for capturing images and displaying results.
- Python Flask backend for processing images and managing templates.

## Stack

- **Backend**: Python with Flask, OpenCV, and Tesseract OCR.
- **Frontend**: React Native with Expo.

## Setup Instructions

### Prerequisites

- Node.js and npm (for React Native frontend).
- Python 3.8+ (for the backend).
- Tesseract OCR installed on your system.
- Android Studio (for Android development) or Xcode (for iOS development).

### Backend Setup

1. Install Tesseract OCR:
   - **Windows**: Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki).
   - **MacOS**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr libtesseract-dev`

2. Set up Python environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the backend server:

   ```bash
   python main.py --port 5000
   ```

### Frontend Setup

1. Install Expo CLI:

   ```bash
   npm install -g expo-cli
   ```

2. Initialize and set up the React Native project:

   ```bash
   expo init questionnaireOCR
   cd questionnaireOCR
   npm install expo-camera expo-image-picker expo-file-system axios
   ```

3. <i>Replace the `App.js` file with the provided frontend code</i>.

4. Update the backend API endpoint in `App.js` to match your backend server URL.

5. Start the app:

   ```bash
   expo start
   ```

## Usage

1. Launch the app on your mobile device or emulator.
2. Use the camera to capture a form image or select one from the gallery.
3. Tap "Process Image" to extract data from the form.
4. View the extracted data and export it to Excel if needed.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License.

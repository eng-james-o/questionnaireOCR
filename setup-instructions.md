# Questionnaire Scanner App - Setup Guide

This guide will walk you through setting up the Questionnaire Scanner application. The app consists of two main components:

1. React web app (frontend)
2. Python Django server (backend)

## Prerequisites

- Node.js and npm (for the React frontend)
- Python 3.8+ (for the backend)
- Tesseract OCR

## Backend Setup

### 1. Install Tesseract OCR

#### On Windows

- Download and install from: [Tesseract - Github](https://github.com/UB-Mannheim/tesseract/wiki)
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

### 3. Configure the Django Secret Key

The Django application requires a secret key for cryptographic operations. To securely store the key:

#### On Windows

1. Open Command Prompt or PowerShell.
2. Run the following command to set the environment variable:

   ```cmd
   setx DJANGO_SECRET_KEY "your-actual-secret-key"
   ```

   or in PowerShell:

   ```powershell
   [Environment]::SetEnvironmentVariable("DJANGO_SECRET_KEY", "your-actual-secret-key", "User")
   ```

3. Restart your Command Prompt or PowerShell to apply the changes.

#### On Linux

1. Open a terminal.
2. Add the following line to your `~/.bashrc` or `~/.zshrc` file:

   ```bash
   export DJANGO_SECRET_KEY="your-actual-secret-key"
   ```

3. Run `source ~/.bashrc` or `source ~/.zshrc` to apply the changes.

### 4. Start the Backend Server

```bash
python manage.py runserver
```

The server will start on [http://localhost:8000](http://localhost:8000)

## Frontend Setup

### 1. Install Dependencies

Navigate to the `frontend` directory and install the required dependencies:

```bash
npm install
```

### 2. Start the React App

```bash
npm start
```

The app will start on [http://localhost:3000](http://localhost:3000)

## Using the App

1. Launch the app on your browser.
2. Use the app to upload images of forms.
3. Tap "Process Image" to extract data from the form.
4. View the extracted data and export it to Excel if needed.

## Troubleshooting

- **OCR Not Working Well**: Ensure Tesseract OCR is installed and accessible.
- **Connection Errors**: Verify the backend server is running and accessible at [http://localhost:8000](http://localhost:8000).
- **Frontend Issues**: Ensure the React development server is running at [http://localhost:3000](http://localhost:3000).

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

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

1. Build and run the Docker image:

```bash
docker build -t questionnaire-scanner-backend .
docker run -p 8000:8000 questionnaire-scanner-backend
```

### Frontend Deployment

1. Build the React app:

```bash
npm run build
```

1. Serve the `build` folder using a static file server or integrate it with the Django backend.

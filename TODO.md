# QuestionnaireOCR Project - Status & To-Do List

This document outlines the current state of development for the **QuestionnaireOCR** application and details the remaining steps required to fully realize the goals of the project as described in the README.

---

## 📊 Project Status: Architecture & Accomplishments

The project has been successfully restructured into a clean, modern, and modular architecture. Core image processing and OCR logic has been decoupled from application frameworks, allowing simultaneous reuse in both web and desktop environments.

### 1. Unified Modular Directory Structure
- **`app/`**: Contain core business, image-processing, and OCR logics (completely decoupled from web/desktop frameworks).
- **`backend/`**: Python Django REST API backend acting as the web-service wrapper.
- **`frontend/`**: React web application communicating with the Django backend.
- **`desktop/`**: Self-contained PySide6 QML desktop application utilizing the `app/` core logics directly for offline usage.

### 2. Accomplished Work & Features
- [x] **Core Business Logic (`app/`)**:
  - **Form Field Detection (`app/form_field_detector.py`)**: Detects lines, filters contours, analyzes aspect ratios, classifies shapes (checkboxes, radio buttons, text fields), and groups label text with inputs vertically/horizontally.
  - **Template-Based Matching (`app/template_recognition.py`)**: Extracts SIFT descriptors, matches templates via FLANN matcher, and falls back to text keyword matching via PyTesseract.
  - **OCR Preprocessing (`app/processing.py`)**: Converts to grayscale, applies fast NlMeans denoising, adaptive thresholding, and dilation to maximize OCR accuracy.
- [x] **Django Backend (`backend/`)**:
  - Exposes RESTful endpoints for image processing (`/process-image/`), Excel exporting (`/export-excel/`), and template CRUD operations (`/create-template/`, `/templates/`).
  - Added robust Django unit tests (`backend/api/tests.py`) using a mocked PyTesseract pipeline to make tests deterministic and system-independent.
- [x] **React Frontend (`frontend/`)**:
  - Responsive single-page application for uploading/previewing multiple images.
  - Connects to the backend via Axios to extract data and triggers Excel downloads.
- [x] **PySide6 Desktop App (`desktop/`)**:
  - Implements a modern native UI using Qt Quick (QML) and PySide6.
  - Connects directly to the `app/` package for instant, local OCR and template extraction.

---

## 🚀 Remaining Steps & Future Roadmap

To achieve the ultimate goal of a production-ready OCR application that extracts, codes, and structures questionnaire data accurately, the following steps must be completed:

### Phase 1: Robust Data Extraction & Advanced OCR
- [ ] **Handwriting Recognition (HTR)**:
  - Integrate a handwriting-optimized OCR engine (such as EasyOCR, PaddleOCR, or a custom TrOCR transformer model) for hand-filled text fields since standard Tesseract is optimized for printed text.
- [ ] **Smart Denoising & Alignment**:
  - Implement perspective correction and auto-rotation (using OpenCV Hough transform) to fix tilted/skewed scanned pages before processing.
  - Normalize brightness and contrast automatically for mobile-captured images.

### Phase 2: Interactive Template Designer
- [ ] **Visual Template Creator (Web & Desktop)**:
  - Develop an interactive frontend UI where users can upload a blank questionnaire, drag and draw bounding boxes over input fields, choose field types (text, checkbox, radio button), and save them as reusable templates.
  - Connect this interface directly to the backend/desktop template managers.

### Phase 3: Data Coding & Tabular Structuring
- [ ] **Standardized Coding System**:
  - Implement a mapping dictionary module to "code" raw text results into discrete data values (e.g., mapping unchecked/checked boxes to `0`/`1`, or hand-written gender values `M`/`F` to standard `1`/`2` integer codes).
- [ ] **Multi-Page Sheet Aggregation**:
  - Develop logic to stitch together multi-page questionnaires, ensuring all answers from a single respondent are merged into a single database row.
  - Enhance the Excel exporter to handle batch processing of hundreds of questionnaires into a single spreadsheet.

### Phase 4: Security, Authentication, & Deployment
- [ ] **Security & Multi-Tenancy**:
  - Add user login, role-based access control, and user-owned templates inside Django.
  - Encrypt sensitive questionnaire uploads to maintain privacy of collected survey data.
- [ ] **Packaging & Native Distribution**:
  - Create a Docker Compose setup for simple deployment of the Web Frontend & Django Backend.
  - Bundle the PySide6 QML desktop application into a standalone executable (using `PyInstaller` or `Briefcase`) so users can run it without installing Python or dependencies locally.

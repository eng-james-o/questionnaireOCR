# QuestionnaireOCR Project - Status & To-Do List

This document outlines the current state of development for the QuestionnaireOCR application and details the remaining steps required to fully realize the goals of the project as described in the README and documentation.

---

## Project Status & Accomplishments

### 1. Unified Modular Directory Structure
- **`app/`**: Shared framework-agnostic Python package for core image processing, form field detection, template recognition, and OCR preprocessing.
- **`backend/`**: Django REST API backend acting as the web service wrapper.
- **`frontend/`**: React web application communicating with the Django backend.
- **`desktop/`**: Self-contained PySide6 QML desktop application utilizing the `app/` core logics directly for offline usage.
- **`experiments/`**: AI model training, benchmarking, and experiment tracking suite with MLflow, PyTorch, TensorFlow, LangChain, LangGraph, and PaddleOCR.
- **`documentation/`**: Comprehensive guides for the Questionnaire Workflow and Analysis Suggestion Engine.

### 2. Accomplished Core Features
- [x] **Core Business Logic (`app/`)**:
  - **Form Field Detection (`app/form_field_detector.py`)**: Detects lines, contours, checkboxes, radio buttons, and text input regions.
  - **Template-Based Matching (`app/template_recognition.py`)**: SIFT feature extraction, FLANN matcher, and keyword text matching.
  - **OCR Preprocessing (`app/processing.py`)**: Denoising, thresholding, and morphological operations.
- [x] **Django Backend (`backend/`)**:
  - Exposes RESTful endpoints for image processing, template CRUD operations, and Excel exporting.
  - Unit tests with `unittest.mock` for `pytesseract` to ensure system-independent execution.
- [x] **React Frontend (`frontend/`)**:
  - Responsive single-page application for uploading/previewing multiple images and downloading Excel exports.
- [x] **PySide6 Desktop App (`desktop/`)**:
  - Native UI built with Qt Quick (QML) and PySide6 connected directly to `app/`.
- [x] **AI Experiments Suite (`experiments/`)**:
  - Integrated MLflow tracking environment with Jupyter notebooks comparing PaddleOCR, Gemini API, PyTorch/TensorFlow CRNN models, and LangChain vs LangGraph orchestration.
- [x] **Comprehensive Documentation (`documentation/`)**:
  - End-to-end Questionnaire Workflow specification (`documentation/WORKFLOW.md`).
  - Analysis Suggestion Engine architecture specification (`documentation/ANALYSIS_SUGGESTION_ENGINE.md`).
  - Community guidelines (`CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`, `PULL_REQUEST_TEMPLATE.md`).

---

## Remaining Steps & Future Roadmap

### Phase 1: Unfilled Schema Learning & Intermediate Review Interface
- [ ] **Blank Form Schema Extractor**:
  - Enhance `app/form_field_detector.py` to auto-detect question labels and assign default variable names (`Q1`, `Q2`, etc.) when processing unfilled forms.
- [ ] **Interactive Schema Review Component**:
  - Build UI components in React and PySide6 QML to allow researchers to review, rename columns, set coding dictionaries (e.g., `1 = Male`, `2 = Female`), and validate spreadsheet structure before batch scanning.
- [ ] **Batch Questionnaire Scanner Pipeline**:
  - Implement sequential batch scanning worker that applies a validated schema to hundreds of filled questionnaire pages, appending each respondent as a row in the master spreadsheet.

### Phase 2: Analysis Suggestion Engine Implementation
- [ ] **Goal Taxonomy Knowledge Base**:
  - Build a JSON/SQLite statistical rule database mapping research intents (comparison, association, prediction, clustering) to appropriate analytical techniques (t-test, ANOVA, Regression, Factor Analysis, PCA).
- [ ] **NLU Research Objectives Parser**:
  - Develop an NLU module (using spaCy / Transformers / Regex intent classification) to parse user project titles, objectives, and research questions into structured query representations.
- [ ] **Automated Recommendations Generator**:
  - Implement a recommendation scoring engine that matches parsed research objectives against extracted questionnaire variable types (nominal, ordinal, continuous) and generates step-by-step statistical analysis suggestions.

### Phase 3: Handwriting Recognition & Accuracy Enhancements
- [ ] **Handwritten Text Recognition (HTR)**:
  - Integrate EasyOCR or PaddleOCR as fallback options for reading handwritten open-response fields.
- [ ] **Automatic Deskewing & Alignment**:
  - Add automatic rotation and perspective alignment using OpenCV Hough lines to handle tilted phone camera captures.

### Phase 4: Packaging & Security
- [ ] **Authentication & Security**:
  - Implement JWT user authentication in Django and secure secret key handling.
- [ ] **Distribution & Containerization**:
  - Provide Docker Compose configurations for backend/frontend web deployment.
  - Package the PySide6 QML desktop application into standalone binary executables via PyInstaller or Briefcase.

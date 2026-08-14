# Changelog

All notable changes to the **QuestionnaireOCR** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2025-08-14

### Added
- **Unified `app/` Core Logic Package**: Extracted framework-agnostic image processing, OCR, and form field detection into a top-level shared module.
- **PySide6 QML Desktop App (`desktop/`)**: Added native self-contained desktop application importing shared core processing logic.
- **Analysis Suggestion Engine Specification**: Added detailed architecture spec (`documentation/ANALYSIS_SUGGESTION_ENGINE.md`) covering Goal Taxonomy knowledge base, NLU objectives parsing, and automated recommendations.
- **Questionnaire Workflow Documentation**: Added end-to-end workflow documentation (`documentation/WORKFLOW.md`) covering blank schema learning, intermediate schema review interface, and batch questionnaire scanning.
- **Repository Documentation Package**: Added `CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`, and `.github/PULL_REQUEST_TEMPLATE.md`.

### Changed
- **Directory Restructuring**: Moved Django backend files into `backend/`.
- **System-Independent Unit Tests**: Updated `backend/api/tests.py` using `unittest.mock` for `pytesseract` to allow tests to run on machines without Tesseract binaries.
- **Cross-Platform Compatibility**: Updated `app/template_recognition.py` to conditionally configure Windows Tesseract binary path only when running on Windows.

---

## [0.1.0] - 2025-05-01

### Added
- Initial release of QuestionnaireOCR with Django backend REST API and React frontend.
- Basic template matching using SIFT features and FLANN matcher.
- Contour-based form field detector for checkboxes, radio buttons, and text input boxes.

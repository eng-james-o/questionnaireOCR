# QuestionnaireOCR

QuestionnaireOCR is an end-to-end optical character recognition and intelligent survey analytics platform. It automatically extracts structured data from paper questionnaires, provides interactive schema validation, scans batch responses, and recommends tailored statistical and machine learning analytical techniques based on user research objectives.

---

## Key Features

### Questionnaire Processing Workflow
- **Unfilled Questionnaire Schema Learning**: Scans blank questionnaire forms to learn field layouts, labels, and data types automatically.
- **Interactive Schema Review Interface**: Intermediate interface allowing researchers to inspect, rename, adjust data types, and validate spreadsheet column structures before batch scanning.
- **Batch Scanning of Filled Forms**: Performs template matching, alignment, and high-precision extraction (checkboxes, radio buttons, handwritten text) on filled questionnaires to populate spreadsheets.
- **Data Export**: Exports extracted survey datasets directly to Microsoft Excel (.xlsx) or CSV.

### Analysis Suggestion Engine
- **Goal Taxonomy Knowledge Base**: Matches research objectives to parametric/non-parametric tests, regression models, ANOVA, factor analysis, and machine learning techniques.
- **Natural Language Understanding (NLU)**: Parses project titles, objectives, and research questions to identify research intent and variable relationships.
- **Automated Recommendations**: Generates tailored statistical analysis recommendations and step-by-step guidance based on survey data types and study scope.

---

## Modular Architecture

```
QuestionnaireOCR/
├── app/            # Shared core business logic (field detection, OCR, preprocessing)
├── backend/        # Python Django REST API backend
├── frontend/       # React web frontend
├── desktop/        # Native PySide6 + QML desktop client
└── documentation/  # Comprehensive architectural & specification guides
```

- **Core Logic (`app/`)**: Framework-agnostic Python package shared across web and desktop platforms.
- **Django Backend (`backend/`)**: REST API server wrapper exposing OCR processing, template management, and export endpoints.
- **React Frontend (`frontend/`)**: Modern web application for uploading forms, reviewing schemas, and exporting datasets.
- **PySide6 Desktop App (`desktop/`)**: Offline, native desktop application built with Qt Quick (QML) and PySide6.

---

## Documentation Links

For detailed guides, please refer to:
- [Questionnaire Workflow Guide](documentation/WORKFLOW.md)
- [Analysis Suggestion Engine Spec](documentation/ANALYSIS_SUGGESTION_ENGINE.md)
- [Setup Instructions](setup-instructions.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)

---

## Stack

- **Backend & Core Logic**: Python 3.12+, Django REST Framework, OpenCV, PyTesseract, Pandas, OpenPyXL.
- **Desktop Client**: PySide6 (Qt 6), Qt Quick (QML).
- **Web Frontend**: React, Axios, CSS3.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

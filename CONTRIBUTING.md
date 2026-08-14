# Contributing to QuestionnaireOCR

Thank you for your interest in contributing to QuestionnaireOCR! We welcome contributions from developers, researchers, and open-source enthusiasts.

---

## How to Get Started

1. **Fork the Repository**: Create your own copy of the project on GitHub.
2. **Clone the Project**:
   ```bash
   git clone https://github.com/your-username/QuestionnaireOCR.git
   cd QuestionnaireOCR
   ```
3. **Set Up Environments**:
   - Backend: Refer to [`setup-instructions.md`](setup-instructions.md) to set up Python and virtualenv.
   - Frontend: Run `npm install` inside the `frontend/` directory.
   - Desktop: Install PySide6 via `pip install PySide6`.

---

## Code Structure Guidelines

* **`app/`**: Framework-agnostic core logic. Any image processing, OCR, or statistical suggestion algorithms belong here. Do not introduce Django or UI-specific dependencies inside `app/`.
* **`backend/`**: Django REST framework API endpoints and serializers wrapping `app/` features.
* **`frontend/`**: React web user interface components.
* **`desktop/`**: PySide6 QML desktop application interface.
* **`documentation/`**: Architectural specifications and user workflows.

---

## Testing Guidelines

Before submitting code, always run the backend test suite to verify no regressions were introduced:

```bash
python backend/manage.py test api
```

Ensure all unit tests pass cleanly before creating a Pull Request.

---

## Submitting Pull Requests

1. Create a descriptive feature branch (`git checkout -b feature/amazing-feature`).
2. Commit your changes with concise, informative commit messages.
3. Push to your branch (`git push origin feature/amazing-feature`).
4. Open a Pull Request using our standard PR template.

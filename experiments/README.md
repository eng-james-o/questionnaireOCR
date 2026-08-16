# AI Training & Experimentation (`experiments/`)

This directory contains Jupyter notebooks and experimental pipelines for training, benchmarking, and evaluating AI models and APIs for QuestionnaireOCR. All experiments leverage **MLflow** for tracking metrics, hyperparameters, artifacts, and model versions.

---

## Experimental Tracks

### 1. Document Parsing & Structure Extraction (`01_document_parsing_paddleocr_gemini.ipynb`)
Compares different document parsing backends for identifying blank and filled questionnaire structures:
- **Tesseract OCR**: Baseline open-source OCR.
- **PaddleOCR**: Open-source deep learning OCR optimized for document layout analysis.
- **Google Gemini API**: Multimodal LLM API for zero-shot questionnaire layout and field extraction.
- **MLflow Tracking**: Logs layout accuracy, IOUs of detected bounding boxes, processing latency, and cost estimates.

### 2. NLU Objectives & Goal Taxonomy Parsing (`02_nlu_goal_taxonomy_langchain_langgraph.ipynb`)
Evaluates orchestration frameworks for parsing user research objectives into statistical technique recommendations:
- **LangChain**: Sequential chain architecture for intent extraction and variable matching.
- **LangGraph**: Stateful, graph-based agent architecture supporting cyclic feedback and multi-step reasoning.
- **MLflow Tracking**: Logs prompt templates, intent classification F1-scores, token usage, and latency.

### 3. Handwriting Recognition Models (`03_handwriting_ocr_pytorch_tensorflow.ipynb`)
Trains and benchmarks custom computer vision models for handwritten text recognition (HTR) on open-ended questionnaire response fields:
- **PyTorch Architecture**: CRNN (CNN + BiLSTM) with CTC Loss.
- **TensorFlow / Keras Architecture**: Convolutional Recurrent Network with CTC Decoding.
- **MLflow Tracking**: Logs training/validation loss curves, Character Error Rate (CER), Word Error Rate (WER), and exports trained model checkpoints.

---

## Setup & Environment

1. Install experimentation dependencies:
   ```bash
   pip install -r experiments/requirements-experiments.txt
   ```

2. Launch MLflow Tracking UI:
   ```bash
   mlflow ui --port 5000
   ```
   Open `http://localhost:5000` in your browser to view experiment runs, metrics, and parameters.

3. Launch JupyterLab / Notebook:
   ```bash
   jupyter lab
   ```

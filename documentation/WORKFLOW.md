# Questionnaire Workflow Architecture

This document describes the end-to-end operational workflow of the **QuestionnaireOCR** application, covering schema generation from blank templates, interactive user review, and batch data extraction from filled questionnaires.

---

## 🔄 End-to-End Workflow Overview

```
 ┌─────────────────────────┐
 │ 1. Blank Questionnaire  │
 │    Image Upload          │
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 2. Automated Schema     │
 │    Learning Engine      │
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 3. Interactive Schema   │
 │    Review Interface     │ (User approves / modifies schema)
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 4. Batch Scanning of    │
 │    Filled Questionnaires│
 └────────────┬────────────┘
              │
              ▼
 ┌─────────────────────────┐
 │ 5. Tabular Data Export  │
 │    (Excel / CSV)        │
 └─────────────────────────┘
```

---

## 1. Unfilled Questionnaire Schema Learning
When an unfilled (blank) questionnaire is uploaded, the system identifies the structural skeleton without noise from handwritten or filled responses:
* **Region Detection**: OpenCV line and contour detection identify checkboxes, radio buttons, grid cells, and text response boxes.
* **Question Label Extraction**: OCR parses label text adjacent to bounding boxes to associate questions with input controls.
* **Data Type Inferencing**: Automatically assigns initial data types (e.g., Boolean for checkboxes, Categorical/Single-Choice for radio groups, Text/Numeric for open response fields).
* **Template Storage**: Saves bounding box coordinates (`x, y, w, h`), field types, and question labels as a reusable template JSON schema.

---

## 2. Interactive Schema Review Interface
Before processing filled forms, users are presented with an intermediate review interface (available in both Web and Desktop applications):
* **Visual Bounding Box Overlay**: Renders detected field bounding boxes directly over the original questionnaire image.
* **Schema Table Editor**: Allows users to:
  * Rename column headers / variable names (e.g., `Field_1` ➔ `Q1_Age`).
  * Modify field data types (Numeric, String, Likert Scale, Multiple Choice).
  * Set valid value ranges and coding dictionaries (e.g., `1 = Strongly Disagree`, `5 = Strongly Agree`).
  * Add missed fields or delete false positives.
* **Schema Validation**: Ensures column uniqueness and structural integrity before persisting the finalized spreadsheet schema.

---

## 3. Batch Scanning of Filled Questionnaires
Once the questionnaire schema is confirmed, users can upload single or batch scans of filled questionnaires:
* **Alignment & Template Matching**: Uses SIFT descriptors and FLANN feature matching to align scanned forms against the validated template, compensating for rotation and scale variations.
* **Targeted OCR & Mark Detection**:
  * **Checkboxes & Radios**: Evaluates pixel density / fill ratios within exact target bounding boxes to recognize marks (`Yes`/`No` or option values).
  * **Text/Numeric Inputs**: Applies region-restricted OCR to read handwritten or typed entries.
* **Spreadsheet Generation**: Populates each filled questionnaire as a single row under the validated schema columns and exports the complete dataset to Microsoft Excel (`.xlsx`) or CSV.

# Medical Report Analyzer - Quick Start Guide

This project features a modern FastAPI backend and a React frontend for analyzing medical reports.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ and Node.js installed.

### 2. Setup
Install all Python dependencies from the root directory:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Run the Application

#### **Backend (FastAPI)**
```bash
cd backend
python app/main.py
```
The API will be available at `http://localhost:8000`.

#### **Frontend (React)**
```bash
cd frontend
npm install
npm run dev
```
The dashboard will be available at `http://localhost:5173` (or similar).

---

## 🛠️ Alternative Interfaces

### Streamlit Web UI
If you prefer a simpler, all-in-one Python web interface:
```bash
streamlit run backend/app/app.py
```

---

## 🔍 Features
- **PDF & Text Support**: Extract data from medical PDFs or plain text.
- **Disease & Symptom Detection**: Advanced NLP to identify medical conditions.
- **Lab Value Validation**: Automatic flagging of High/Low lab results.
- **Inference Engine**: Deduced diagnoses based on lab abnormalities.

Results are also automatically logged to `output/analysis_results.txt`.

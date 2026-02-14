# Medical Report Analyzer (FastAPI + React)

A modern, full-stack medical report analyzer that extracts diseases, symptoms, and lab values from text or PDF files.

## Architecture

- **Backend**: FastAPI (Python 3.9+)
  - Modular medical analysis logic.
  - RESTful API endpoints.
  - Spacy for NLP tasks.
- **Frontend**: React + Vite
  - Premium UI with Glassmorphism aesthetic.
  - Interactive analysis dashboard.
  - Responsive design.

## Getting Started

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The website will be available at `http://localhost:3000` (or `3001` if 3000 is occupied).

## Features
- **PDF Extraction**: Automatically parses medical reports in PDF format.
- **NLP Analysis**: Detects possible diagnoses and symptoms with negation detection.
- **Lab Validation**: Validates lab values against standard reference ranges and flags High/Low results.
- **Privacy First**: All processing is done locally; no medical data leaves your machine.

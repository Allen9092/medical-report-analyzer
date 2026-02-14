# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import os
import sys

# Ensure local imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocess import preprocess_text
from ner_extraction import extract_entities
from rule_extraction import extract_lab_values
from pdf_handler import extract_text_from_pdf
from inference import infer_diseases

app = FastAPI(title="Medical Report Analyzer API")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/text")
async def analyze_text(text: str = Body(..., embed=True)):
    print(f"Received analysis request for text: {text[:50]}...")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    clean_text = preprocess_text(text)
    diseases, symptoms = extract_entities(clean_text)
    labs = extract_lab_values(clean_text)
    
    # Infer additional diseases
    diseases = infer_diseases(diseases, symptoms, labs)
    
    return {
        "status": "success",
        "data": {
            "diseases": [d.title() for d in diseases] if diseases else [],
            "symptoms": [s.title() for s in symptoms] if symptoms else [],
            "labs": labs if labs else {}
        }
    }

@app.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    file_path = Path("temp_upload" + Path(file.filename).suffix)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        report_text = ""
        if file.filename.lower().endswith('.pdf'):
            report_text = extract_text_from_pdf(str(file_path))
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                report_text = f.read()
        
        if file_path.exists():
            file_path.unlink() # Cleanup
        
        if not report_text:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
            
        clean_text = preprocess_text(report_text)
        diseases, symptoms = extract_entities(clean_text)
        labs = extract_lab_values(clean_text)
        
        # Infer additional diseases
        diseases = infer_diseases(diseases, symptoms, labs)
        
        return {
            "status": "success",
            "filename": file.filename,
            "data": {
                "diseases": [d.title() for d in diseases] if diseases else [],
                "symptoms": [s.title() for s in symptoms] if symptoms else [],
                "labs": labs if labs else {}
            }
        }
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

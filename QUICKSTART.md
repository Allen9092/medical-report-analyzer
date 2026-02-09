# Medical Report Analyzer - Quick Start Guide

## 🚀 How to Use

### Method 1: Interactive Menu (Easiest)
```bash
python src/main.py
```
Then choose from the menu:
- Option 1: Use sample report
- Option 2: Load from a file
- Option 3: Paste text directly

### Method 2: Command Line
```bash
# Analyze a specific file
python src/main.py --file path/to/your/report.txt

# Use sample report
python src/main.py --sample

# Interactive paste mode
python src/main.py --interactive
```

## 📝 Supported Report Formats

The analyzer works with **ANY text format**:
- ✅ Structured medical reports
- ✅ Clinical notes
- ✅ Lab results printouts
- ✅ Doctor's notes
- ✅ Plain text descriptions

## 🔍 What It Detects

- **50+ Diseases**: diabetes, hypertension, heart disease, cancer, etc.
- **40+ Symptoms**: fatigue, pain, fever, dizziness, etc.
- **Lab Values**: blood sugar, cholesterol, blood pressure, HbA1c, vitals, etc.

## 📊 Example Output

```
╔══════════════════════════════════════════════════════════╗
║               PATIENT REPORT SUMMARY                     ║
╚══════════════════════════════════════════════════════════╝

🏥 POSSIBLE DIAGNOSES:
   Hypertension, Coronary Artery Disease, Angina

📋 SYMPTOMS OBSERVED:
   Fatigue, Chest Pain, Shortness Of Breath

🔬 LABORATORY VALUES:
   • Blood Pressure: 160/95
   • Total Cholesterol: 245 mg/dL
   • LDL Cholesterol: 165 mg/dL
   • Heart Rate: 92 bpm
```

Results are saved to: `output/analysis_results.txt`

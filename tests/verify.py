# tests/verify.py
import sys
from pathlib import Path

# Add backend/app to python path
sys.path.append(str(Path(__file__).parent.parent / "backend" / "app"))

from ner_extraction import extract_entities
from rule_extraction import extract_lab_values

def test_negation():
    print("\nTesting Negation Detection...")
    text = "Patient denies chest pain and no fever. Reports fatigue."
    diseases, symptoms = extract_entities(text)
    
    print(f"Input: '{text}'")
    print(f"Symptoms found: {symptoms}")
    
    if "fatigue" in symptoms and "chest pain" not in symptoms and "fever" not in symptoms:
        print("✓ Negation logic PASSED")
    else:
        print("✗ Negation logic FAILED")

def test_range_validation():
    print("\nTesting Range Validation...")
    text = "Blood Sugar: 200 mg/dL. Blood Pressure: 110/70."
    labs = extract_lab_values(text)
    
    print(f"Input: '{text}'")
    print(f"Labs found: {labs}")
    
    sugar_status = labs.get("Blood Sugar", {}).get("status")
    bp_status = labs.get("Blood Pressure", {}).get("status")
    
    if sugar_status == "High" and bp_status == "Normal":
        print("✓ Range validation PASSED")
    else:
        print("✗ Range validation FAILED")

if __name__ == "__main__":
    test_negation()
    test_range_validation()

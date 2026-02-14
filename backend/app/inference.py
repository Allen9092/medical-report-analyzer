# backend/app/inference.py

def infer_diseases(diseases, symptoms, labs):
    """
    Suggest additional diagnoses based on lab results and symptoms.
    
    Args:
        diseases: List of strings (found diseases)
        symptoms: List of strings (found symptoms)
        labs: Dict of lab objects
        
    Returns:
        list: Updated list of diseases
    """
    inferred = set(diseases)
    
    # Diabetes Inference
    glucose = labs.get("Blood Sugar", {})
    pp_glucose = labs.get("PP Blood Sugar", {})
    hba1c = labs.get("HbA1c", {})
    
    if glucose.get("status") == "High" or pp_glucose.get("status") == "High" or hba1c.get("status") == "High":
        inferred.add("Diabetes Mellitus")
        
    # Thyroid Inference
    tsh = labs.get("TSH", {})
    if tsh.get("status") == "High":
        inferred.add("Hypothyroidism")
    elif tsh.get("status") == "Low":
        inferred.add("Hyperthyroidism")
        
    # PCOD/PCOS Inference (Simple heuristic)
    if "pcos" not in [d.lower() for d in inferred]:
        has_pcos_symptoms = any(s in [sym.lower() for sym in symptoms] for s in ["irregular periods", "acne", "hirsutism"])
        bmi = labs.get("BMI", {})
        if has_pcos_symptoms and bmi.get("status") == "High":
            inferred.add("Polycystic Ovary Syndrome (PCOS)")

    return sorted(list(inferred))

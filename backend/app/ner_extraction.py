# src/ner_extraction.py
import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# Comprehensive medical keywords
DISEASES = [
    # Metabolic & Endocrine
    "diabetes", "type 1 diabetes", "type 2 diabetes", "prediabetes", "diabetic",
    "hyperthyroidism", "hypothyroidism", "thyroid disorder", "thyroid dysfunction",
    "metabolic syndrome", "obesity", "pcod", "pcos", "polycystic ovary syndrome",
    
    # Cardiovascular
    "hypertension", "high blood pressure", "heart disease", "coronary artery disease",
    "arrhythmia", "atrial fibrillation", "heart failure", "myocardial infarction",
    "stroke", "atherosclerosis", "angina",
    
    # Respiratory
    "asthma", "copd", "chronic obstructive pulmonary disease", "pneumonia",
    "bronchitis", "tuberculosis", "lung disease",
    
    # Cancer
    "cancer", "carcinoma", "tumor", "malignancy", "leukemia", "lymphoma",
    "breast cancer", "lung cancer", "prostate cancer", "colon cancer",
    
    # Infectious
    "infection", "viral infection", "bacterial infection", "covid-19", "influenza",
    "hepatitis", "hiv", "aids",
    
    # Gastrointestinal
    "gastritis", "ulcer", "ibs", "irritable bowel syndrome", "crohn's disease",
    "colitis", "gerd", "acid reflux", "liver disease", "cirrhosis",
    
    # Neurological
    "alzheimer's", "dementia", "parkinson's", "epilepsy", "migraine",
    "multiple sclerosis", "neuropathy",
    
    # Renal
    "kidney disease", "renal failure", "chronic kidney disease", "ckd",
    "kidney stones", "nephropathy",
    
    # Other
    "arthritis", "rheumatoid arthritis", "osteoporosis", "anemia",
    "depression", "anxiety", "insomnia"
]

SYMPTOMS = [
    # General
    "fatigue", "weakness", "tiredness", "malaise", "lethargy",
    "fever", "chills", "sweating", "night sweats", "weight loss", "weight gain",
    
    # Pain
    "pain", "headache", "chest pain", "abdominal pain", "back pain",
    "joint pain", "muscle pain", "neck pain",
    
    # Cardiovascular
    "palpitations", "dizziness", "shortness of breath", "dyspnea",
    "edema", "swelling",
    
    # Gastrointestinal
    "nausea", "vomiting", "diarrhea", "constipation", "bloating",
    "abdominal discomfort", "loss of appetite", "heartburn",
    
    # Respiratory
    "cough", "wheezing", "difficulty breathing", "sore throat",
    
    # Urinary
    "frequent urination", "painful urination", "blood in urine",
    "urinary urgency", "incontinence",
    
    # Neurological
    "confusion", "memory loss", "numbness", "tingling", "tremor",
    "seizures", "vision changes", "blurred vision",
    
    # Skin
    "rash", "itching", "bruising", "skin discoloration",
    
    # Other
    "insomnia", "difficulty sleeping", "anxiety", "depression",
    "increased thirst", "dry mouth"
]

def extract_entities(text):
    """
    Extract medical entities (diseases and symptoms) from text.
    Uses basic negation detection to exclude absent findings.
    
    Args:
        text: Medical report text (string)
    
    Returns:
        tuple: (list of diseases found, list of symptoms found)
    """
    doc = nlp(text)
    text_lower = text.lower()
    
    negation_triggers = ["no", "not", "denies", "without", "negative for", "absent"]
    
    found_diseases = []
    found_symptoms = []
    
    # Helper to check if a term is negated in the text
    def is_negated(term, text_lower):
        # Find all occurrences of the term
        start = 0
        while True:
            idx = text_lower.find(term, start)
            if idx == -1:
                break
                
            # Check the window before the term (e.g., 5 words back)
            # This is a heuristic; dependency parsing would be more accurate but requires 
            # the term to be a proper entity in spacy which isn't guaranteed with this keyword list.
            window_start = max(0, idx - 30)
            preceding_text = text_lower[window_start:idx]
            
            for trigger in negation_triggers:
                # Check if trigger is present and not part of another word (e.g. "not" in "nothing")
                # Simple check: trigger + space
                if f"{trigger} " in preceding_text or preceding_text.endswith(trigger):
                    return True
            
            start = idx + len(term)
        return False

    sentences = text_lower.split('.')
    
    # Check diseases
    for disease in DISEASES:
        # Check if disease is in text
        if disease.lower() in text_lower:
            # Check negation
            if not is_negated(disease.lower(), text_lower):
                found_diseases.append(disease)
                
    # Check symptoms
    for symptom in SYMPTOMS:
        if symptom.lower() in text_lower:
            if not is_negated(symptom.lower(), text_lower):
                found_symptoms.append(symptom)
    
    # Remove duplicates while preserving order
    found_diseases = list(dict.fromkeys(found_diseases))
    found_symptoms = list(dict.fromkeys(found_symptoms))
    
    return found_diseases, found_symptoms

# Example usage
if __name__ == "__main__":
    sample_text = "Patient shows fatigue and frequent urination. Possible diabetes."
    diseases, symptoms = extract_entities(sample_text)
    print("Diseases:", diseases)
    print("Symptoms:", symptoms)

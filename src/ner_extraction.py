# src/ner_extraction.py
import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# Comprehensive medical keywords
DISEASES = [
    # Metabolic & Endocrine
    "diabetes", "type 1 diabetes", "type 2 diabetes", "prediabetes",
    "hyperthyroidism", "hypothyroidism", "thyroid disorder",
    "metabolic syndrome", "obesity",
    
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
    Uses case-insensitive matching for better detection.
    
    Args:
        text: Medical report text (string)
    
    Returns:
        tuple: (list of diseases found, list of symptoms found)
    """
    doc = nlp(text)
    text_lower = text.lower()
    
    # Case-insensitive matching
    diseases_found = [disease for disease in DISEASES if disease.lower() in text_lower]
    symptoms_found = [symptom for symptom in SYMPTOMS if symptom.lower() in text_lower]
    
    # Remove duplicates while preserving order
    diseases_found = list(dict.fromkeys(diseases_found))
    symptoms_found = list(dict.fromkeys(symptoms_found))
    
    return diseases_found, symptoms_found

# Example usage
if __name__ == "__main__":
    sample_text = "Patient shows fatigue and frequent urination. Possible diabetes."
    diseases, symptoms = extract_entities(sample_text)
    print("Diseases:", diseases)
    print("Symptoms:", symptoms)

# src/preprocess.py

def preprocess_text(text):
    """
    Cleans medical report text.
    """
    text = text.lower().strip()              # Lowercase and remove spaces
    text = text.replace("\n", " ")           # Remove newlines
    text = " ".join(text.split())            # Remove extra spaces
    return text

# Example usage
if __name__ == "__main__":
    sample_text = "Patient has Elevated blood sugar levels of 180 mg/dL.\nSymptoms include frequent urination."
    print(preprocess_text(sample_text))

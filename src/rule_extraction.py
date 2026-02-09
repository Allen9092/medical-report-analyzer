# src/rule_extraction.py
import re

def extract_lab_values(text):
    """
    Extract laboratory values and vital signs from medical report text.
    Supports various formats and units.
    
    Args:
        text: Medical report text (string)
    
    Returns:
        dict: Dictionary of lab values found
    """
    labs = {}
    text_lower = text.lower()
    
    # Blood Sugar / Glucose (mg/dL or mmol/L)
    sugar_patterns = [
        r'(?:blood sugar|glucose|fasting glucose|blood glucose)[\s:]*(\d+)\s*mg/dl',
        r'(?:blood sugar|glucose|fasting glucose|blood glucose)[\s:]*(\d+)',
        r'(\d+)\s*mg/dl'
    ]
    for pattern in sugar_patterns:
        match = re.search(pattern, text_lower)
        if match and "Blood Sugar" not in labs:
            labs["Blood Sugar"] = match.group(1) + " mg/dL"
            break
    
    # HbA1c (%)
    hba1c_patterns = [
        r'hba1c[\s:]*(\d+\.?\d*)\s*%',
        r'a1c[\s:]*(\d+\.?\d*)\s*%',
        r'hba1c[\s:]*(\d+\.?\d*)'
    ]
    for pattern in hba1c_patterns:
        match = re.search(pattern, text_lower)
        if match:
            labs["HbA1c"] = match.group(1) + "%"
            break
    
    # Blood Pressure (systolic/diastolic)
    bp_patterns = [
        r'(?:blood pressure|bp)[\s:]*(\d+/\d+)',
        r'(\d{2,3}/\d{2,3})\s*(?:mmhg)?'
    ]
    for pattern in bp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            labs["Blood Pressure"] = match.group(1)
            break
    
    # Cholesterol (Total, LDL, HDL)
    cholesterol_patterns = [
        (r'(?:total cholesterol|cholesterol)[\s:]*(\d+)\s*mg/dl', "Total Cholesterol"),
        (r'ldl[\s:]*(\d+)\s*mg/dl', "LDL Cholesterol"),
        (r'hdl[\s:]*(\d+)\s*mg/dl', "HDL Cholesterol"),
        (r'triglycerides[\s:]*(\d+)\s*mg/dl', "Triglycerides")
    ]
    for pattern, name in cholesterol_patterns:
        match = re.search(pattern, text_lower)
        if match:
            labs[name] = match.group(1) + " mg/dL"
    
    # Heart Rate (bpm)
    hr_patterns = [
        r'(?:heart rate|pulse|hr)[\s:]*(\d+)\s*bpm',
        r'(?:heart rate|pulse|hr)[\s:]*(\d+)'
    ]
    for pattern in hr_patterns:
        match = re.search(pattern, text_lower)
        if match:
            labs["Heart Rate"] = match.group(1) + " bpm"
            break
    
    # Temperature (°F or °C)
    temp_patterns = [
        r'(?:temperature|temp)[\s:]*(\d+\.?\d*)\s*°?f',
        r'(?:temperature|temp)[\s:]*(\d+\.?\d*)\s*°?c',
        r'(\d{2,3}\.\d)\s*°?f'
    ]
    for pattern in temp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            unit = "°F" if "f" in pattern else "°C"
            labs["Temperature"] = match.group(1) + unit
            break
    
    # Weight (kg or lbs)
    weight_patterns = [
        r'(?:weight|wt)[\s:]*(\d+\.?\d*)\s*(?:kg|kgs)',
        r'(?:weight|wt)[\s:]*(\d+\.?\d*)\s*(?:lb|lbs|pounds)'
    ]
    for pattern in weight_patterns:
        match = re.search(pattern, text_lower)
        if match:
            unit = "kg" if "kg" in pattern else "lbs"
            labs["Weight"] = match.group(1) + " " + unit
            break
    
    # Height (cm or ft/in)
    height_patterns = [
        r'(?:height|ht)[\s:]*(\d+\.?\d*)\s*cm',
        r'(?:height|ht)[\s:]*(\d+)\s*ft\s*(\d+)\s*in'
    ]
    match = re.search(height_patterns[0], text_lower)
    if match:
        labs["Height"] = match.group(1) + " cm"
    else:
        match = re.search(height_patterns[1], text_lower)
        if match:
            labs["Height"] = f"{match.group(1)}'{match.group(2)}\""
    
    # BMI
    bmi_match = re.search(r'bmi[\s:]*(\d+\.?\d*)', text_lower)
    if bmi_match:
        labs["BMI"] = bmi_match.group(1)
    
    # Creatinine (mg/dL)
    creat_match = re.search(r'creatinine[\s:]*(\d+\.?\d*)', text_lower)
    if creat_match:
        labs["Creatinine"] = creat_match.group(1) + " mg/dL"
    
    # Hemoglobin (g/dL)
    hb_match = re.search(r'(?:hemoglobin|hb)[\s:]*(\d+\.?\d*)', text_lower)
    if hb_match:
        labs["Hemoglobin"] = hb_match.group(1) + " g/dL"
    
    # White Blood Cell Count
    wbc_match = re.search(r'(?:wbc|white blood cell)[\s:]*(\d+\.?\d*)', text_lower)
    if wbc_match:
        labs["WBC"] = wbc_match.group(1) + " K/uL"
    
    return labs

# Example usage
if __name__ == "__main__":
    sample_text = "Blood sugar is 180 mg/dL. BP recorded as 140/90."
    labs = extract_lab_values(sample_text)
    print(labs)

# src/rule_extraction.py
import re

def check_range(value, min_val, max_val):
    """
    Check if a value is within a reference range.
    Returns: "Normal", "High", or "Low"
    """
    try:
        val = float(value)
        if val < min_val:
            return "Low"
        elif val > max_val:
            return "High"
        return "Normal"
    except ValueError:
        return "Unknown"

def extract_lab_values(text):
    """
    Extract laboratory values and vital signs from medical report text.
    Supports various formats and units. Returns status (Normal/High/Low).
    
    Args:
        text: Medical report text (string)
    
    Returns:
        dict: Dictionary of lab values found with format:
              {"Lab Name": {"value": "120", "unit": "mg/dL", "status": "High"}}
    """
    labs = {}
    text_lower = text.lower()
    
    # Blood Sugar / Glucose (mg/dL) - Normal: 70-140
    sugar_patterns = [
        r'(?:blood sugar|glucose|fasting glucose|blood glucose)[\s:]*(\d+)\s*mg/dl',
        r'(?:blood sugar|glucose|fasting glucose|blood glucose)[\s:]*(\d+)',
        r'(\d+)\s*mg/dl'
    ]
    for pattern in sugar_patterns:
        match = re.search(pattern, text_lower)
        if match and "Blood Sugar" not in labs:
            val = match.group(1)
            status = check_range(val, 70, 140)
            labs["Blood Sugar"] = {"value": val, "unit": "mg/dL", "status": status}
            break
            
    # Post Prandial Blood Glucose (mg/dL) - Normal: < 140
    pp_patterns = [
        r'(?:post prandial blood glucose|pp blood glucose|ppbg|ppbs)[\s:]*(\d+)\s*mg/dl',
        r'(?:post prandial|pp)[\s:]*(\d+)\s*mg/dl',
        r'pp[\s:]*(\d+)'
    ]
    for pattern in pp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = match.group(1)
            status = check_range(val, 0, 140)
            labs["PP Blood Sugar"] = {"value": val, "unit": "mg/dL", "status": status}
            break
    
    # HbA1c (%) - Normal: < 5.7
    hba1c_patterns = [
        r'hba1c[\s:]*(\d+\.?\d*)\s*%',
        r'a1c[\s:]*(\d+\.?\d*)\s*%',
        r'hba1c[\s:]*(\d+\.?\d*)'
    ]
    for pattern in hba1c_patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = match.group(1)
            status = check_range(val, 0, 5.7) # Simplified upper limit check
            labs["HbA1c"] = {"value": val, "unit": "%", "status": status}
            break
    
    # Blood Pressure (systolic/diastolic) - Normal: < 120/80
    bp_patterns = [
        r'(?:blood pressure|bp)[\s:]*(\d+)/(\d+)',
        r'(\d{2,3})/(\d{2,3})\s*(?:mmhg)?'
    ]
    for pattern in bp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            systolic = int(match.group(1))
            diastolic = int(match.group(2))
            
            status = "Normal"
            if systolic > 130 or diastolic > 80:
                status = "High"
            elif systolic < 90 or diastolic < 60:
                status = "Low"
                
            labs["Blood Pressure"] = {"value": f"{systolic}/{diastolic}", "unit": "mmHg", "status": status}
            break
    
    # Cholesterol (Total, LDL, HDL)
    # Total < 200, LDL < 100, HDL > 40
    cholesterol_patterns = [
        (r'(?:total cholesterol|cholesterol)[\s:]*(\d+)\s*mg/dl', "Total Cholesterol", 0, 200),
        (r'ldl[\s:]*(\d+)\s*mg/dl', "LDL Cholesterol", 0, 100),
        (r'hdl[\s:]*(\d+)\s*mg/dl', "HDL Cholesterol", 40, 100), # HDL needs to be high, so logic is inverted below
        (r'triglycerides[\s:]*(\d+)\s*mg/dl', "Triglycerides", 0, 150)
    ]
    for pattern, name, min_ref, max_ref in cholesterol_patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = match.group(1)
            
            # Special case for HDL (Higher is better)
            if name == "HDL Cholesterol":
                if float(val) < min_ref:
                    status = "Low" # Bad for HDL
                else:
                    status = "Normal"
            else:
                status = check_range(val, min_ref, max_ref)
                
            labs[name] = {"value": val, "unit": "mg/dL", "status": status}
    
    # Heart Rate (bpm) - Normal: 60-100
    hr_patterns = [
        r'(?:heart rate|pulse|hr)[\s:]*(\d+)\s*bpm',
        r'(?:heart rate|pulse|hr)[\s:]*(\d+)'
    ]
    for pattern in hr_patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = match.group(1)
            status = check_range(val, 60, 100)
            labs["Heart Rate"] = {"value": val, "unit": "bpm", "status": status}
            break
    
    # Temperature (°F or °C) - Normal: 97-99°F, 36-37.5°C
    temp_patterns = [
        (r'(?:temperature|temp)[\s:]*(\d+\.?\d*)\s*°?f', "°F", 97, 99.5),
        (r'(?:temperature|temp)[\s:]*(\d+\.?\d*)\s*°?c', "°C", 36, 37.5),
        (r'(\d{2,3}\.\d)\s*°?f', "°F", 97, 99.5)
    ]
    for pattern, unit, min_ref, max_ref in temp_patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = match.group(1)
            status = check_range(val, min_ref, max_ref)
            labs["Temperature"] = {"value": val, "unit": unit, "status": status}
            break

    # Thyroid Stimulating Hormone (TSH) (µIU/mL) - Normal: 0.4 - 4.0
    tsh_patterns = [
        r'(?:thyroid stimulating hormone|tsh)[\s:]*(\d+\.?\d*)\s*µ?iu/ml',
        r'tsh[\s:]*(\d+\.?\d*)'
    ]
    for pattern in tsh_patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = match.group(1)
            status = check_range(val, 0.4, 4.0)
            labs["TSH"] = {"value": val, "unit": "µIU/mL", "status": status}
            break
            
    # Simple extraction without range validation for others
    
    # Weight (kg or lbs)
    weight_patterns = [
        r'(?:weight|wt)[\s:]*(\d+\.?\d*)\s*(?:kg|kgs)',
        r'(?:weight|wt)[\s:]*(\d+\.?\d*)\s*(?:lb|lbs|pounds)'
    ]
    for pattern in weight_patterns:
        match = re.search(pattern, text_lower)
        if match:
            unit = "kg" if "kg" in pattern else "lbs"
            labs["Weight"] = {"value": match.group(1), "unit": unit, "status": "Normal"}
            break

    # BMI
    bmi_match = re.search(r'bmi[\s:]*(\d+\.?\d*)', text_lower)
    if bmi_match:
        val = bmi_match.group(1)
        status = check_range(val, 18.5, 24.9)
        labs["BMI"] = {"value": val, "unit": "", "status": status}
    
    return labs

# Example usage
if __name__ == "__main__":
    sample_text = "Blood sugar is 180 mg/dL. BP recorded as 140/90."
    labs = extract_lab_values(sample_text)
    print(labs)

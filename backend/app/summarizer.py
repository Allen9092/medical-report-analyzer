# src/summarizer.py

def generate_summary(diseases, symptoms, labs):
    """
    Generate a structured summary from extracted medical information.
    
    Args:
        diseases: List of diseases found
        symptoms: List of symptoms found
        labs: Dictionary of lab values found
    
    Returns:
        str: Formatted summary
    """
    summary_lines = []
    summary_lines.append("PATIENT REPORT SUMMARY")
    summary_lines.append("-" * 22)
    summary_lines.append("")
    
    # Diseases section
    if diseases:
        summary_lines.append("🏥 POSSIBLE DIAGNOSES:")
        summary_lines.append("   " + ", ".join(diseases).title())
        summary_lines.append("")
    else:
        summary_lines.append("🏥 POSSIBLE DIAGNOSES:")
        summary_lines.append("   No specific diseases detected")
        summary_lines.append("")
    
    # Symptoms section
    if symptoms:
        summary_lines.append("📋 SYMPTOMS OBSERVED:")
        summary_lines.append("   " + ", ".join(symptoms).title())
        summary_lines.append("")
    else:
        summary_lines.append("📋 SYMPTOMS OBSERVED:")
        summary_lines.append("   No specific symptoms detected")
        summary_lines.append("")
    


    # Lab values section
    if labs:
        summary_lines.append("🔬 LABORATORY VALUES:")
        for key, data in labs.items():
            # Handle new dict structure
            if isinstance(data, dict) and "value" in data:
                val = data["value"]
                unit = data.get("unit", "")
                status = data.get("status", "Unknown")
                
                # Add status icon
                icon = ""
                if status == "High":
                    icon = " 🔴 HIGH"
                elif status == "Low":
                    icon = " 🔵 LOW"
                    
                summary_lines.append(f"   • {key}: {val} {unit}{icon}")
            else:
                # Fallback for old string format if any
                summary_lines.append(f"   • {key}: {data}")
        summary_lines.append("")
    else:
        summary_lines.append("🔬 LABORATORY VALUES:")
        summary_lines.append("   No lab values detected")
        summary_lines.append("")
    
    return "\n".join(summary_lines)

# Example usage
if __name__ == "__main__":
    diseases = ["diabetes"]
    symptoms = ["fatigue", "frequent urination"]
    labs = {"Blood Sugar": "180 mg/dL", "Blood Pressure": "140/90"}
    print(generate_summary(diseases, symptoms, labs))

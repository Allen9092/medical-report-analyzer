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
    summary_lines.append("╔" + "═"*58 + "╗")
    summary_lines.append("║" + " "*15 + "PATIENT REPORT SUMMARY" + " "*21 + "║")
    summary_lines.append("╚" + "═"*58 + "╝")
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
        for key, value in labs.items():
            summary_lines.append(f"   • {key}: {value}")
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

# src/app.py
import streamlit as st
import sys
from pathlib import Path

# Add src to python path to allow imports
sys.path.append(str(Path(__file__).parent))

from preprocess import preprocess_text
from ner_extraction import extract_entities
from rule_extraction import extract_lab_values
from pdf_handler import extract_text_from_pdf

st.set_page_config(
    page_title="Medical Report Analyzer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical Report Analyzer")
st.markdown("""
Upload a medical report or paste text to extract diseases, symptoms, and lab values.
**Privacy Note:** All processing is done locally. No data is sent to external servers.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Input Report")
    
    input_method = st.radio("Choose input method:", ["Upload File", "Paste Text"])
    
    report_text = ""
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload a medical report", type=["txt", "pdf"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.lower().endswith('.pdf'):
                    # Save temp file for pypdf
                    with open("temp_upload.pdf", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    report_text = extract_text_from_pdf("temp_upload.pdf")
                    Path("temp_upload.pdf").unlink() # Cleanup
                else:
                    # Text file
                    stringio = uploaded_file.getvalue().decode("utf-8")
                    report_text = stringio
                    
                st.success(f"Loaded {uploaded_file.name}")
                with st.expander("View Raw Text"):
                    st.text(report_text)
            except Exception as e:
                st.error(f"Error reading file: {e}")
                
    else:
        report_text = st.text_area("Paste medical report here:", height=300)

    analyze_btn = st.button("🔍 Analyze Report", type="primary")

if analyze_btn and report_text:
    with st.spinner("Analyzing..."):
        # Process
        clean_text = preprocess_text(report_text)
        diseases, symptoms = extract_entities(clean_text)
        labs = extract_lab_values(clean_text)
        
    # Display Results in Col2
    with col2:
        st.subheader("📊 Analysis Results")
        
        # Diseases
        st.markdown("### 🏥 Possible Diagnoses")
        if diseases:
            for d in diseases:
                st.markdown(f"- **{d.title()}**")
        else:
            st.info("No specific diseases detected.")
            
        # Symptoms
        st.markdown("### 📋 Symptoms")
        if symptoms:
            for s in symptoms:
                st.markdown(f"- {s.title()}")
        else:
            st.info("No specific symptoms detected.")
            
        # Lab Values
        st.markdown("### 🔬 Laboratory Values")
        if labs:
            # Convert labs dict to dataframe-like display
            for name, data in labs.items():
                if isinstance(data, dict):
                    val = f"{data['value']} {data.get('unit', '')}"
                    status = data.get('status', 'Unknown')
                    
                    # Color coding
                    if status == 'High':
                        st.error(f"**{name}**: {val} (HIGH)")
                    elif status == 'Low':
                        st.warning(f"**{name}**: {val} (LOW)")
                    else:
                        st.success(f"**{name}**: {val} (Normal)")
                else:
                    st.write(f"**{name}**: {data}")
        else:
            st.info("No lab values detected.")

elif analyze_btn and not report_text:
    st.error("Please provide a report to analyze.")

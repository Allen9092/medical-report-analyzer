# src/pdf_handler.py
import pypdf

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file.
    
    Args:
        file_path (str or Path): Path to the PDF file
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF cannot be read
    """
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Failed to read PDF file: {e}")

if __name__ == "__main__":
    # Test stub
    pass

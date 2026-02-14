# src/input_handler.py
import sys
from pathlib import Path

from pdf_handler import extract_text_from_pdf

def get_text_from_file(file_path):
    """
    Read text from a file (supports .txt and .pdf).
    
    Args:
        file_path: Path to the file (string or Path object)
    
    Returns:
        str: Content of the file
    
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file extension
        if path.suffix.lower() == '.pdf':
            return extract_text_from_pdf(path)
            
        # Default to text file reading
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.strip():
            raise ValueError("File is empty")
        
        return content
    except Exception as e:
        raise IOError(f"Error reading file: {e}")


def get_text_interactive():
    """
    Get text input interactively from user.
    User can paste or type text, then press Ctrl+Z (Windows) or Ctrl+D (Unix) and Enter to finish.
    
    Returns:
        str: User-provided text
    """
    print("\n" + "="*60)
    print("INTERACTIVE MODE - Paste or type your medical report")
    print("="*60)
    print("Instructions:")
    print("  1. Paste or type your medical report text below")
    print("  2. When finished, press Ctrl+Z (Windows) or Ctrl+D (Unix)")
    print("  3. Then press Enter")
    print("="*60)
    print("\nEnter your report:\n")
    
    try:
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        text = "\n".join(lines)
        
        if not text.strip():
            raise ValueError("No text was entered")
        
        return text
    except KeyboardInterrupt:
        print("\n\nInput cancelled by user.")
        sys.exit(0)


def show_menu():
    """
    Display a menu for input selection.
    
    Returns:
        str: User's choice ('1', '2', or '3')
    """
    print("\n" + "="*60)
    print("MEDICAL REPORT ANALYZER")
    print("="*60)
    print("\nHow would you like to provide the medical report?\n")
    print("  1. Use sample report (default)")
    print("  2. Load from a file")
    print("  3. Paste/type text interactively")
    print("\n" + "="*60)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3) [default: 1]: ").strip()
            
            if not choice:
                choice = "1"
            
            if choice in ["1", "2", "3"]:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def get_file_path_from_user():
    """
    Prompt user to enter a file path.
    
    Returns:
        str: File path entered by user
    """
    print("\n" + "="*60)
    while True:
        try:
            file_path = input("Enter the path to your medical report file: ").strip()
            
            if not file_path:
                print("Error: File path cannot be empty. Please try again.")
                continue
            
            # Remove quotes if user wrapped path in quotes
            file_path = file_path.strip('"').strip("'")
            
            return file_path
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


# Example usage
if __name__ == "__main__":
    choice = show_menu()
    
    if choice == "1":
        print("\nUsing sample report...")
    elif choice == "2":
        path = get_file_path_from_user()
        try:
            text = get_text_from_file(path)
            print(f"\nSuccessfully loaded {len(text)} characters from file.")
        except Exception as e:
            print(f"\nError: {e}")
    elif choice == "3":
        try:
            text = get_text_interactive()
            print(f"\nSuccessfully received {len(text)} characters.")
        except Exception as e:
            print(f"\nError: {e}")

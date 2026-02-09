# src/main.py
from pathlib import Path
import argparse
import sys
from preprocess import preprocess_text
from ner_extraction import extract_entities
from rule_extraction import extract_lab_values
from summarizer import generate_summary
from input_handler import get_text_from_file, get_text_interactive, show_menu, get_file_path_from_user

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Medical Report Analyzer - Extract diseases, symptoms, and lab values from medical reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Use interactive menu
  python main.py --file report.txt         # Analyze specific file
  python main.py --interactive             # Paste text directly
  python main.py --sample                  # Use sample report
        """
    )
    
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '--file', '-f',
        type=str,
        help='Path to medical report file'
    )
    input_group.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Enter text interactively'
    )
    input_group.add_argument(
        '--sample', '-s',
        action='store_true',
        help='Use sample report from data/sample_reports.txt'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: output/analysis_results.txt)'
    )
    
    return parser.parse_args()

def get_report_text(args, project_root):
    """
    Get the medical report text based on command-line arguments or user menu choice.
    
    Args:
        args: Parsed command-line arguments
        project_root: Path to project root directory
    
    Returns:
        str: Medical report text
    """
    # If command-line arguments provided, use them
    if args.file:
        print(f"\nLoading report from: {args.file}")
        return get_text_from_file(args.file)
    
    elif args.interactive:
        return get_text_interactive()
    
    elif args.sample:
        data_file = project_root / "data" / "sample_reports.txt"
        print(f"\nUsing sample report from: {data_file}")
        return get_text_from_file(data_file)
    
    # No arguments provided - show menu
    else:
        choice = show_menu()
        
        if choice == "1":
            # Use sample report
            data_file = project_root / "data" / "sample_reports.txt"
            print(f"\nUsing sample report from: {data_file}")
            return get_text_from_file(data_file)
        
        elif choice == "2":
            # Load from file
            file_path = get_file_path_from_user()
            print(f"\nLoading report from: {file_path}")
            return get_text_from_file(file_path)
        
        elif choice == "3":
            # Interactive input
            return get_text_interactive()

def main():
    """
    Main function to run the medical report analyzer.
    """
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    # Parse command-line arguments
    args = parse_arguments()
    
    try:
        # Get report text
        report = get_report_text(args, project_root)
        
        print("\n" + "="*60)
        print("ANALYZING MEDICAL REPORT...")
        print("="*60)
        
        # Step 1: Preprocess
        clean_text = preprocess_text(report)
        
        # Step 2: Extract diseases and symptoms
        diseases, symptoms = extract_entities(clean_text)
        
        # Step 3: Extract lab values
        labs = extract_lab_values(clean_text)
        
        # Step 4: Generate summary
        summary = generate_summary(diseases, symptoms, labs)
        
        # Prepare full output
        output = []
        output.append("="*60)
        output.append("PREPROCESSED TEXT:")
        output.append(clean_text[:200] + "..." if len(clean_text) > 200 else clean_text)
        output.append("="*60)
        output.append("\nEXTRACTED ENTITIES:")
        output.append(f"Diseases found: {diseases}")
        output.append(f"Symptoms found: {symptoms}")
        output.append("="*60)
        output.append("\nLAB VALUES:")
        output.append(f"Labs extracted: {labs}")
        output.append("="*60)
        output.append("\nFINAL SUMMARY:")
        output.append(summary)
        
        full_output = "\n".join(output)
        
        # Print to console
        print("\n" + full_output)
        
        # Save to file
        if args.output:
            output_file = Path(args.output)
        else:
            output_file = project_root / "output" / "analysis_results.txt"
        
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_output)
        
        print(f"\n\n✓ Results saved to: {output_file}")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

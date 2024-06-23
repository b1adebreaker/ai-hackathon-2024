#brew install poppler
import os
import logging  # For logging the errors
from pdfminer.high_level import extract_text

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

def extract_text_from_doc(path):
    """Extracts text from a PDF document."""
    text = extract_text(path)
    return text

def process_pdfs(companies_dir, output_dir):
    """Processes PDF files in company folders and saves the text."""
    os.makedirs(output_dir, exist_ok=True)

    for company_name in os.listdir(companies_dir):
        company_path = os.path.join(companies_dir, company_name)
        if os.path.isdir(company_path):
            company_output_dir = os.path.join(output_dir, company_name)
            os.makedirs(company_output_dir, exist_ok=True)

            for filename in os.listdir(company_path):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(company_path, filename)
                    print(pdf_path)
                    try:
                        text = extract_text_from_doc(pdf_path)
                    except Exception as e:  # Catch any exceptions
                        logging.error(f"Error processing {pdf_path}: {e}")
                        continue  # Skip this file and move on to the next

                    txt_filename = filename.replace(".pdf", ".txt")
                    output_path = os.path.join(company_output_dir, txt_filename)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(text)

if __name__ == "__main__":
    companies_dir = "../server/companies"
    output_dir = "../textFiles/companies"
    process_pdfs(companies_dir, output_dir)

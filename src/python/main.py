import os
import sys
import logging
from pdf_downloader import download_pdfs_first_page
from pdf_processor import process_pdfs
from db_uploader import recreate_database_and_upload

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def update_database():
    """Main function that executes the entire update process"""
    try:
        logging.info("Starting database update process")
        
        # Settings
        download_dir = "/app/pdfs"
        text_output_dir = "/app/extracted_texts"
        
        # Clear existing directories
        for dir_path in [download_dir, text_output_dir]:
            if os.path.exists(dir_path):
                for file in os.listdir(dir_path):
                    os.remove(os.path.join(dir_path, file))
            else:
                os.makedirs(dir_path)
        
        # Download PDFs
        logging.info("Starting PDF download...")
        download_pdfs_first_page(
            url="https://www.mpc.pa.gov.br/transparencia/portarias",
            output_dir=download_dir
        )
        
        # Process PDFs
        logging.info("Processing PDFs...")
        process_pdfs(
            pdf_dir=download_dir,
            output_dir=text_output_dir
        )
        
        # Recreate database and upload
        logging.info("Updating database...")
        recreate_database_and_upload(
            text_dir=text_output_dir,
            database_name="text_mpc"
        )
        
        logging.info("Update process completed successfully")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error during update: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    update_database()
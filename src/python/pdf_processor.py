import fitz
import pytesseract
from PIL import Image
import io
import os
import logging
from concurrent.futures import ThreadPoolExecutor
    
def process_single_pdf(pdf_path, output_dir):
        """Process a single PDF file, only the first page"""
        try:
            filename = os.path.basename(pdf_path)
            output_file = os.path.splitext(filename)[0] + '.txt'
            output_path = os.path.join(output_dir, output_file)
            
            # Open PDF
            with fitz.open(pdf_path) as pdf:
                text = ""
                if pdf.page_count > 0:  # Check if there is at least one page
                    page = pdf[0]  # Get only the first page
                    page_text = page.get_text()
                    
                    # If no text found, try OCR
                    if not page_text.strip():
                        pix = page.get_pixmap()
                        img = Image.open(io.BytesIO(pix.tobytes()))
                        page_text = pytesseract.image_to_string(img, lang='por')
                    
                    text += f"\n--- Página 1 ---\n{page_text}"
            
            # Save extracted text
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text.strip())
                
            logging.info(f"Processed: {filename}")
            return True
                    
        except Exception as e:
            logging.error(f"Error processing {filename}: {str(e)}")
            return False
    
def process_pdfs(pdf_dir, output_dir, max_workers=3):
        """
        Process all PDFs in parallel
        """
        os.makedirs(output_dir, exist_ok=True)
        
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        total_files = len(pdf_files)
        logging.info(f"Starting to process {total_files} PDF files")
        
        success_count = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    process_single_pdf,
                    os.path.join(pdf_dir, pdf_file),
                    output_dir
                )
                for pdf_file in pdf_files
            ]
            
            for i, future in enumerate(futures, 1):
                if future.result():
                    success_count += 1
                
                if i % 5 == 0:  # Log progress every 5 files
                    logging.info(f"Processing progress: {i}/{total_files} ({(i/total_files)*100:.1f}%)")
        
        logging.info(f"PDF processing completed. Successfully processed {success_count} of {total_files} files")
        return success_count

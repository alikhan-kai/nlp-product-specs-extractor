import os
import pandas as pd
import pdfplumber
from docx import Document

class DocumentParser:
    # A class to handle extraction of tables from various document formats (.docx, .pdf).
    def __init__(self, data_folder):
        self.data_folder = data_folder
    
    def read_all_files(self):

        # Iterates through the data folder and extracts tables from all supported files.
        # Returns:
        #list: A list of pandas DataFrames containing the extracted tables.
        all_tables = []

        # Check if the source directory exists
        if not os.path.exists(self.data_folder):
            print(f"Error: The folder '{self.data_folder}' was not found.")
            return all_tables
        
        # Loop through each file in the directory
        for filename in os.listdir(self.data_folder):
            filepath = os.path.join(self.data_folder, filename)

            # Skip temporary Office files (usually starting with ~$)
            if filename.startswith('~'):
                continue

            # Process Word documents
            if filename.lower().endswith('.docx'):
                print(f"Processing Word document: {filename}")
                tables = self._parse_docx(filepath)
                all_tables.extend(tables)

            # Process PDF documents
            elif filename.lower().endswith('.pdf'):
                print(f"Processing PDF document: {filename}")
                tables = self._parse_pdf(filepath)
                all_tables.extend(tables)
        
        return all_tables

    def _parse_docx(self, filepath): 
        # Extracts tables from a Word (.docx) file.
        doc = Document(filepath)
        tables = []
        for table in doc.tables:
            data = []
            for row in table.rows:
                # Extract and clean text from each cell in the row
                row_data = [cell.text.strip() for cell in row.cells]
                data.append(row_data)
            
            # If table has data, convert it to a DataFrame using the first row as header
            if data and len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                tables.append(df)
        return tables

    def _parse_pdf(self, filepath):
        # Extracts tables from a PDF (.pdf) file using pdfplumber.
        tables = []
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                for table in extracted_tables:
                    # Clean the table data: replace None with empty strings and remove newlines
                    cleaned_table = [
                        [str(cell).replace('\n', ' ').strip() if cell is not None else "" for cell in row] 
                        for row in table
                    ]
                    
                    # Create DataFrame if the table contains more than just a header
                    if cleaned_table and len(cleaned_table) > 1:
                        df = pd.DataFrame(cleaned_table[1:], columns=cleaned_table[0])
                        tables.append(df)
        return tables
    
# Entry point for testing the parser module
if __name__ == "__main__":
    parser = DocumentParser("data")
    dfs = parser.read_all_files()
    print(f"\n--- Extraction Summary ---")
    print(f"Total tables successfully extracted: {len(dfs)}")
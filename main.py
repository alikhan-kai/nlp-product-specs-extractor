import pandas as pd
import datetime
import os
import re
from file_parser import DocumentParser
from nlp_mapping import ColumnMapper
from text_extraction import TextExtractor

def main():
    # Initialize core modules for document parsing, NLP mapping, and regex extraction
    parser = DocumentParser("data")
    mapper = ColumnMapper(threshold=75)
    extractor = TextExtractor()
    
    print("Processing all documents...")
    all_dfs = parser.read_all_files()
    
    final_results = []
    # Keywords to filter only relevant products (Lamps and Batteries) as required by the assignment
    keywords = ['светильник', 'аккумулятор', 'лампа', 'прожектор', 'led', 'акб', 'light', 'battery']

    for df in all_dfs:
        # NLP TASK 1: Intelligent Column Mapping
        # Dynamically rename inconsistent headers from different files into standardized names
        mapping_dict = {col: mapper.map_column(col) for col in df.columns}
        df = df.rename(columns=mapping_dict)

        for _, row in df.iterrows():
            row_dict = row.to_dict()
            
            # Extract basic identifiers for validation and filtering
            product_name = str(row_dict.get("Наименование товара", "")).strip()
            raw_id = str(row_dict.get("ID", "")).strip()
            raw_qty = str(row_dict.get("Количество", "")).lower().strip()

            # --- DATA CLEANING ---
            # Standardize ID and Quantity by removing non-numeric characters (noise reduction)
            clean_id = re.sub(r'[^\d]', '', raw_id)
            if clean_id: row_dict["ID"] = clean_id

            clean_qty = re.sub(r'[^\d]', '', raw_qty)
            if clean_qty:
                row_dict["Количество"] = clean_qty
            elif raw_qty in ["шт", "ед"] and not product_name:
                continue # Skip metadata rows that contain units but no product data

            # Filter out non-product rows (like table headers or empty rows)
            if not product_name or product_name.lower() in ["наименование", "товар"]:
                continue

            # --- GLOBAL CONTEXT PREPARATION ---
            # Merge all cell values into one string to handle cases where specs are split across columns
            raw_values = [str(val) for val in row_dict.values() if val and not pd.isna(val)]
            full_row_text = " ".join(raw_values)
            
            # Normalize text for Regex: replace special characters that break number recognition
            full_row_text = full_row_text.replace('\xa0', ' ').replace('≤', ' ').replace('≥', ' ')

            # --- NLP TASK 2: Unstructured Text Parsing ---
            # Extract characteristics using Regex only if the row matches our product keywords
            if any(key in product_name.lower() for key in keywords) or any(key in full_row_text.lower() for key in keywords):
                specs = extractor.extract_all(full_row_text)
                
                for spec_name, value in specs.items():
                    # Align extracted spec name with the final target columns
                    target_key = spec_name
                    if spec_name not in mapper.target_columns:
                        potential_keys = [c for c in mapper.target_columns if spec_name in c]
                        if potential_keys:
                            target_key = potential_keys[0]
                    
                    # LOGIC FOR OVERWRITING:
                    # Fill the column only if it's empty, contains 'nan', or has a long descriptive text (noise)
                    # This ensures technical specs like "Capacity" replace long table descriptions
                    current_val = str(row_dict.get(target_key, "")).strip()
                    if current_val.lower() in ["", "nan", "none"] or \
                       len(current_val) > 12 or \
                       not re.search(r'\d', current_val):
                        row_dict[target_key] = value
                
                final_results.append(row_dict)

    # --- OUTPUT GENERATION ---
    if final_results:
        # Create DataFrame and ensure final column order matches the Assignment requirements
        result_df = pd.DataFrame(final_results)
        result_df = result_df.reindex(columns=mapper.target_columns)
        
        # Save to Excel using the required naming convention: params-YYYY-MM-DD-HH-MM-SS.xlsx
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_name = f"params-{timestamp}.xlsx"
        
        result_df.to_excel(output_name, index=False)
        print(f"\nSUCCESS! Found {len(result_df)} items.")
        print(f"Report saved: {output_name}")
    else:
        print("\nNothing found. Check the data directory.")

if __name__ == "__main__":
    main()
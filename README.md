<!-- Product Extraction System Documentation -->
This application is a specialized NLP tool designed to extract technical characteristics for Lamps and Batteries from unstructured documents. The system automates the transition from fragmented Word and PDF tables into a standardized, production-ready Excel format.

<!-- Environment Requirements -->
The system is optimized for Python 3.12. Using this version ensures the highest performance for regex processing and full compatibility with all integrated libraries.

<!-- Mandatory Dependencies Installation -->
To ensure the application functions correctly, you must install the following libraries. Each package serves a specific role in the extraction pipeline:

1.pandas: Used for high-level data manipulation and structuring extracted information into dataframes.

2.openpyxl: Required for engine-level operations to save and format the final .xlsx output.

3.python-docx: Enables the system to traverse and parse complex table structures within Word documents.

4.pdfplumber: Utilized for precise coordinate-based table extraction from PDF files.

5.fuzzywuzzy: The core NLP component for Task 1, performing intelligent column mapping via fuzzy string matching.

6.python-Levenshtein: A critical extension that accelerates matching operations by providing a fast C-based implementation of Levenshtein distance.

To install all dependencies at once, run the following command:
pip install pandas openpyxl python-docx pdfplumber fuzzywuzzy python-Levenshtein

<!-- Project Structure and Data Preparation -->
The system expects a specific directory layout to function correctly. Ensure that your project folder contains a subfolder named data. Place all source documents—including .docx and .pdf files—into this directory. The DocumentParser module is configured to automatically iterate through this folder, ignoring temporary system files and focusing strictly on valid datasets.

<!-- Execution and Processing -->
To initiate the extraction process, run the primary entry point of the application from the command line:

python main.py

Upon execution, the terminal will display real-time logs indicating which files are currently being processed. The application performs a multi-stage workflow: first, it identifies table structures; second, it applies fuzzy logic to map inconsistent headers to standardized fields; and third, it uses regular expressions to extract technical specifications from unstructured text blocks.

<!-- Verification of Results -->
Once the process reaches 100% completion, a success message will appear in the console. The system generates a consolidated Excel report following the naming convention params-YYYY-MM-DD-HH-MM-SS.xlsx. To verify the output, open the generated file and inspect the standardized columns such as Voltage, Capacity, and Dimensions. A successful run is characterized by the accurate migration of values from various document formats into a single, formatted spreadsheet where each row represents an identified battery or lamp component.

<!-- Technical Approach Overview -->
The extraction logic is built on traditional NLP principles. It avoids the latency of external APIs by using Levenshtein distance for semantic header alignment and complex pattern matching for entity recognition. This ensures the tool remains lightweight, private, and capable of operating in offline environments while maintaining high precision across diverse document layouts.

# nlp-product-specs-extractor
An automated NLP-based system for extracting technical specifications (Voltage, Capacity, Dimensions) from unstructured .docx and .pdf documents using fuzzy matching and regex.

# NLP Technical Specs Extractor 🚀

## 🌟 Key Features
- **Intelligent Column Mapping:** Uses Fuzzy String Matching (Levenshtein Distance) to align inconsistent headers across different files.
- **Unstructured Text Parsing:** Employs advanced Regular Expressions (Regex) to capture specifications like Voltage, Capacity, and Dimensions from dense text blocks.
- **Multi-Format Support:** Automatically processes tables and paragraphs from both Word and PDF documents.
- **Automated Structuring:** Consolidates data from multiple sources into a single, standardized Excel report.

## 🛠 Tech Stack
- **Language:** Python 3.12
- **Data Handling:** Pandas, OpenPyXL
- **Document Parsing:** Python-docx, PDFPlumber
- **NLP Techniques:** FuzzyWuzzy (Fuzzy Matching), Re (Regex)
🧠 Technical Approach
NLP Task 1: Column Mapping
The system uses Fuzzy String Matching to recognize that headers like "Qty", "Amount", and "Количество" refer to the same attribute. This ensures robustness regardless of how the table was formatted by the supplier.

NLP Task 2: Specification Extraction
We use Anchor-based Regex. For instance, instead of just searching for numbers, the algorithm looks for numeric patterns anchored to units of measurement (e.g., Ah, Ампер-час, V). This allows the tool to ignore "noise" like technical OKPD/KTRU codes.

📊 Requirements Met
✅ No LLM APIs used (Traditional NLP only)
✅ Automatic processing of multiple files
✅ Clean Excel output with bold headers and auto-adjusted columns
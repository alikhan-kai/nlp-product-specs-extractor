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

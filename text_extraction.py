import re

class TextExtractor:
    def __init__(self):
        # Define extraction rules using Regular Expressions (Regex) - NLP Task 2 Requirement
        self.patterns = {
            # Matches specific voltage values (12, 24, etc.) preceded by keywords like 'voltage'
            "Напряжение, В": r'(?:напряжен|питан|вольт).*?(\b(?:12|24|110|127|220|230|380)\b)',
            
            # Anchor-based extraction: Looks for numbers immediately followed by capacity units (Ah/Ampere-hour)
            # The .*? allows the engine to skip noise like comparison symbols (≤) or extra words in Word tables
            "Емкость": r'(\d+(?:[\.,]\d+)?)\s*(?:Ah|Ач|мАч|ампер(?:-?час)?)',
            
            # Patterns for dimensional data: Handles both 'Length x Width x Height' formats and keyword-based lists
            "Длина, мм": r'(\d+)\s*[xхXХ*×]\s*\d+\s*[xхXХ*×]\s*\d+|(?:длина|length).*?(\d+)', 
            "Ширина, мм": r'\d+\s*[xхXХ*×]\s*(\d+)\s*[xхXХ*×]\s*\d+|(?:ширина|width).*?(\d+)',
            "Высота, мм": r'\d+\s*[xхXХ*×]\s*\d+\s*[xхXХ*×]\s*(\d+)|(?:высота|глубина|height|толщина).*?(\d+)',
            
            # Identifies technical diameters using specific structural keywords
            "Диаметр": r'(?:диаметр|сечение).*?(\d+)',
            
            # Captures numeric weight values and handles decimal commas/dots for standardization
            "Вес г/кг": r'(?:вес|масса|weight).*?(\d+(?:[\.,]\d+)?)\s*(?:kg|кг|г|g)?'
        }

    def extract_all(self, text):
        # Basic validation to ensure input is a valid string for the regex engine
        if not text or not isinstance(text, str):
            return {}
        
        extracted_data = {}
        
        # Pre-processing/Normalization: Removes non-breaking spaces (\xa0), soft hyphens (\xad),
        # and tab characters that often break regex matching in Word/PDF documents
        clean_text = text.replace('\xa0', ' ').replace('\xad', '').replace('\t', ' ')
        
        # Flatten the text: Replaces line breaks and multiple whitespaces with a single space
        # This is critical for PDF parsing where text is often fragmented across lines
        clean_text = clean_text.replace('\n', ' ').replace('\r', ' ')
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        # Iterate through defined specifications to find matches in the normalized string
        for feature, pattern in self.patterns.items():
            # Perform case-insensitive search (re.IGNORECASE)
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                # Filter out None values from capture groups to isolate the actual numeric data
                groups = [g for g in match.groups() if g is not None]
                if groups:
                    # Data Standardization: Converts decimal commas to dots to ensure valid Excel/Numeric format
                    val = groups[0] 
                    extracted_data[feature] = val.replace(',', '.')
        
        return extracted_data
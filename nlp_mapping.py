from fuzzywuzzy import process
from fuzzywuzzy import fuzz

class ColumnMapper:
    """
    NLP-based class to map various input column names to standardized fields 
    using Fuzzy String Matching (Levenshtein Distance).
    """

    def __init__(self, threshold=70):
        # Sensitivity threshold (0-100). 70 is the optimal "sweet spot".
        self.threshold = threshold

        # Standardized field names required for the final output
        self.target_columns = [
            "ID", "Наименование товара", "Количество", "Напряжение, В", 
            "Емкость", "Длина, мм", "Ширина, мм", "Высота, мм", "Диаметр", "Вес г/кг"
        ]

        # Dictionary of possible variations found in your 1.docx - 5.docx files
        self.column_variations = {
            "ID": ["id", "номер", "№", "no", "№ п/п", "№п/п", "артикул", "п/п"],
            "Наименование товара": [
                "наименование", "наименования", "название", "товар", 
                "описание", "product name", "наименование товара", "наименование-"
            ],
            "Количество": [
                "количество", "кол-во", "кол - во", "кол- во", "кол-во-5", 
                "шт", "штук", "объем", "amount", "quantity"
            ],
            "Напряжение, В": ["напряжение", "вольтаж", "в", "volts", "v", "рабочее напряжение", "номинальное напряжение"],
            "Емкость": ["емкость", "ёмкость", "заряд", "ач", "ампер-час", "capacity"],
            "Длина, мм": ["длина", "длинна", "length", "длина светильника"],
            "Ширина, мм": ["ширина", "width", "ширина светильника"],
            "Высота, мм": ["высота", "height", "высота светильника", "глубина", "толщина"],
            "Диаметр": ["диаметр", "сечение", "diameter", "установочный диаметр"],
            "Вес": ["вес", "масса", "кг", "weight", "вес нетто", "масса, кг"]
        }

    def map_column(self, input_col):
        """Matches an input column name against the dictionary of variations."""
        if not input_col or str(input_col).strip() == "":
            return None
        
        input_clean = str(input_col).lower().strip()
        
        # If the header contains 'OKPD' or 'KTRU', we treat it as technical data, not a simple ID
        if "окпд" in input_clean or "ктру" in input_clean:
            return "Technical_Code"

        best_target = None
        highest_score = 0

        for target, syn_list in self.column_variations.items():
            # token_set_ratio handles multi-word headers perfectly
            match, score = process.extractOne(input_clean, syn_list, scorer=fuzz.token_set_ratio)
            
            if score > highest_score:
                highest_score = score
                best_target = target

        if highest_score >= self.threshold:
            return best_target
        
        return "Description_Source"
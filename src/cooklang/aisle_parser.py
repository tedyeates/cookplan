from dataclasses import dataclass
from typing import Dict, List
import re


class AisleParser:
    sections: List[str] = []
    ingredients: Dict[str, str] = {}
    DEFAULT_SECTION = 'Other'
    DEFAULT_COOKWARE_SECTION = 'Cookware'
    
    def __init__(self, raw_aisle_data: str):
        rows = list(filter(None, map(str.strip, raw_aisle_data.split('\n'))))
        current_section = None
        
        for row in rows:
            row = row.strip()
            if row == '':
                continue
            
            section = re.search(r"\[(.*)\]", row)
            if current_section == None and not section:
                raise ValueError("String should start with a section")
            
            if section:
                current_section = section.group(1)
                self.sections.append(current_section)
                continue
            
            self.ingredients[row] = current_section
            
        self.sections.append(self.DEFAULT_SECTION)
        self.sections.append(self.DEFAULT_COOKWARE_SECTION)
        
    def get_ingredient_aisle(self, ingredient_name):
        if ingredient_name in self.ingredients:
            return self.ingredients[ingredient_name]
        
        return self.DEFAULT_SECTION
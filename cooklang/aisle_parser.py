from dataclasses import dataclass
from typing import Dict, List
import re


class AisleParser:
    sections: List[str]
    
    def __init__(self, raw_aisle_data: str):
        rows = list(filter(None, map(str.strip, raw_aisle_data.split('\n'))))
        current_section = None
        
        for row in rows:
            row = row.strip()
            if row == '':
                continue
            
            section = re.search(r"\[(*.)\]", row)
            if current_section == None and not section:
                raise ValueError("String should start with a section")
            
            if section:
                current_section = section
                self.sections.append(section)
                continue
            
    def get_sections(self) -> List[str]:
        return self.sections
    
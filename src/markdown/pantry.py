import json
from os.path import dirname as up, join
from typing import List

from cooklang.aisle_parser import AisleParser
from src.cooklang.cooklang_types import Cookware, Ingredient, AisleParser
from todoist_api_python.api import Task

from src.todoist.todoist import UNIT_SEPARATOR

CONFIGS_BASE = join(up(up(__file__)), 'configs')
PANTRY_CONF = join(CONFIGS_BASE, 'pantry.json')
MARKDOWN_CONF = join(CONFIGS_BASE, 'markdown.json')
INVENTORY_CONF = join(CONFIGS_BASE, 'inventory.conf')

class Pantry:
    
    PANTRY_PATH: str
    pantry: List[Ingredient | Cookware] = []
    
    def __init__(self, pantry_path: str, cookware_section_id: str):
        self.PANTRY_PATH = pantry_path
        self.cookware_section_id = cookware_section_id
        self.load_pantry()
        
        with open(INVENTORY_CONF, 'r') as file:
            self.aisle_parser = AisleParser(file.read())

    def load_pantry(self) -> str:
        with open(PANTRY_CONF, 'r') as file:
            self.pantry = json.load(file)
            
    def save_pantry(self):
        with open(PANTRY_CONF, 'w') as file:
            json.dump(self.pantry, file)
            
    def add_item(self, **item: Ingredient | Cookware):
        self.pantry.append(item)
        
    def add_completed_items(self, completed_tasks: List[Task]):
        for task in completed_tasks:
            item = {
                "name": task.content,
                "quantity": task.description.strip(),
                "step": -1,
                "aisle": self.aisle_parser.get_ingredient_aisle(task.content)
            }
            
            description = task.description.split(UNIT_SEPARATOR) 
            if len(description) == 2:
                quantity, unit = description
                item["quantity"] = quantity.strip()
                item["units"] = unit.strip()
            
            self.pantry.append(item)
            self.save_pantry()
            
    def get_format_pantry_markdown(self):
        markdown_content = ''
        with open(MARKDOWN_CONF, 'r') as file:
            markdown_layout = json.load(file)
            markdown_content = markdown_layout['pantry_header']
            
            for item in self.pantry:
                markdown_content += markdown_layout['pantry_row'].format(
                    item['name'],
                    f"{item['quantity']} {item['units'] if 'units' in item else ''}"
                )
            
        return markdown_content 
    
    def write_to_markdown(self, content:str):
        with open(self.PANTRY_PATH, 'w') as file:
            file.write(content)
            
    def write_pantry_markdown(self):
        markdown_content = self.get_format_pantry_markdown()
        self.write_to_markdown(markdown_content)
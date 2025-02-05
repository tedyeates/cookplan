import re
from typing import Dict, List, Optional, TypedDict

from .cooklang_types import Ingredient, Cookware, Timer
from src.cooklang.aisle_parser import AisleParser
    
    
DEFAULT_COOKWARE = '1'
DEFAULT_INGREDIENT = 'some'

COMMENT = '--.*\n'
NOT_CURLY = '[^\{{~@#%\.]*'
BLOCK_COMMENT = '\[\-[\S\s]*\-\]\s*'
UNIT='%(?P<unit>\S*)'
BASIC_QUANTITY = '(?P<basic_quantity>\S*)'
STANDARD_QUANTITY = f'(?P<quantity>\S*){UNIT}'
QUANTITY = f'\{{({STANDARD_QUANTITY}|{BASIC_QUANTITY})\}}'
INGREDIENT = f'@(?P<ingredient>{NOT_CURLY})({QUANTITY})|@(?P<basic_ingredient>\S*)'
COOKWARE = f'#(?P<cookware>{NOT_CURLY})(\{{{BASIC_QUANTITY}\}})|#(?P<basic_cookware>\S*)'
TIMER=f'~(?P<name>{NOT_CURLY})\{{{STANDARD_QUANTITY}\}}'
METADATA = f'>>\s*(?P<name>[^:]*)\s*:\s*(?P<value>.*)'
STEP = f'@|#|~{NOT_CURLY}|\{{{NOT_CURLY}\}}'
    
class CooklangParser:
    ingredients: List[Ingredient]
    cookwares: List[Cookware]
    timers: List[Timer]
    metadata: Dict[str, str]
    steps: List[str]
    
    aisle_parser: AisleParser
    
    def __init__(self, raw_cooklang_data: str, aisle_parser: AisleParser):
        self.aisle_parser = aisle_parser
        self.ingredients = []
        self.cookwares = []
        self.timers = []
        self.metadata = {}
        self.steps = []
        
        stripped_data = self.strip_comments(raw_cooklang_data)
        steps = stripped_data.split('\n')
        
        step_number = 1
        for step in steps:
            is_meta = self.get_metadata(step)
            self.get_ingredients(step, step_number)
            self.get_cookwares(step, step_number)
            self.get_timers(step, step_number)

            if not is_meta:
                step_number += 1
                self.get_step(step)

    def get_step(self, step):
        stripped_step = re.sub(STEP, '', step)
        self.steps.append(stripped_step)

    def strip_comments(self, raw_data):
        comment_less_data = re.sub(COMMENT, '', raw_data)
        return re.sub(BLOCK_COMMENT, '', comment_less_data)


    def get_ingredients(self, step: str, step_number: int):
        ingredients = re.finditer(INGREDIENT, step)
        
        for ingredient in ingredients:
            name = ingredient.group('ingredient') or ingredient.group('basic_ingredient')
            self.ingredients.append({
                'type': 'ingredient',
                'name': name,
                'quantity': ingredient.group('quantity') or 
                            ingredient.group('basic_quantity') or 
                            DEFAULT_INGREDIENT,
                'unit': ingredient.group('unit') or '',
                'step': step_number,
                'aisle': self.aisle_parser.get_ingredient_aisle(name)
            })
            
    
    def get_cookwares(self, step: str, step_number: int):
        cookwares = re.finditer(COOKWARE, step)
        
        for cookware in cookwares:
            self.cookwares.append({
                'type': 'cookware',
                'name': cookware.group('cookware') or 
                        cookware.group('basic_cookware'),
                'quantity': cookware.group('basic_quantity') or 
                            DEFAULT_COOKWARE,
                'step': step_number,
                'aisle': self.aisle_parser.DEFAULT_COOKWARE_SECTION
            })
            
    def get_timers(self, step: str, step_number: int):
        timers = re.finditer(TIMER, step)
        
        for timer in timers:
            self.timers.append({
                'type': 'timer',
                'name': timer.group('name'),
                'quantity': timer.group('quantity'),
                'unit': timer.group('unit'),
                'step': step_number
            })
            
    
    def get_metadata(self, step: str):
        meta = re.search(METADATA, step)
        if meta is None: return False
        
        self.metadata[meta.group('name')] = meta.group('value')
        return True
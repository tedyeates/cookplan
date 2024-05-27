from src.cooklang.aisle_parser import AisleParser
from src.cooklang.cooklang_parser import CooklangParser
from src.todoist.todoist import Todoist
from os.path import dirname as up, join

CONFIGS_BASE = join(up(__file__), 'configs')
AISLE_CONF = join(CONFIGS_BASE, 'aisle.conf')

class Parser:
    FOOD_BASE: str
    RECIPE_BASE: str
    def __init__(self, food_base_path: str):
        self.FOOD_BASE = food_base_path
        self.RECIPE_BASE = f'{self.FOOD_BASE}/recipes'
        self.aisle_parser = AisleParser(self.read_aisle_conf())      
        self.todoist = Todoist(self.aisle_parser)
    
    def read_aisle_conf(self) -> str:
        with open(AISLE_CONF, 'r') as file:
            return file.read()
        
    def create_project(self):
        self.todoist.create_shopping_project()
        self.todoist.create_aisle_sections()
        
    def create_shopping_list(self, recipe_path):
        with open(f'{self.RECIPE_BASE}/{recipe_path}', 'r') as file: 
            cooklang = CooklangParser(file.read(), self.aisle_parser)
            shopping_items = cooklang.ingredients + cooklang.cookwares
            self.todoist.create_shopping_tasks(shopping_items)
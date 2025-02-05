from src.parser_manager import Parser
from src.cooklang.cooklang_parser import CooklangParser
from src.todoist.todoist import Todoist

def setup():
    parser = Parser('C:/Users/Ted_Y/iCloudDrive/iCloud~md~obsidian/SecondBrain/🌮 Food')
    parser.create_project()
    meal_plan = [
        'Hoisin Chicken Wings',
        'Spaghetti alla Carrettiere',
        'Chicken and Pineapple'
    ]
    
    for plan in meal_plan:
        parser.create_shopping_list(f'{plan}/{plan}.cook')
    

if __name__ == '__main__':
    setup()
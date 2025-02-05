from src.markdown.pantry import Pantry
from src.parser_manager import Parser


if __name__ == '__main__':
    parser = Parser('C:/Users/Ted_Y/iCloudDrive/iCloud~md~obsidian/SecondBrain/🌮 Food')
    completed = parser.todoist.get_shopping_completed_tasks()
    pantry = Pantry('C:/Users/Ted_Y/iCloudDrive/iCloud~md~obsidian/SecondBrain/🌮 Food/Pantry.md', '156668860')
    # pantry.add_completed_items(completed)
    pantry.write_pantry_markdown()
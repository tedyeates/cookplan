import json
import logging
from os.path import dirname as up, join
from typing import Dict, List
from environs import Env
from requests import HTTPError
from todoist_api_python.api import TodoistAPI, Project, Section

from src.cooklang.aisle_parser import AisleParser

PROJECT_ID = 'project_id'
HAS_SECTIONS = 'has_sections'
TASKS = 'shopping_list'

CONFIGS_BASE = join(up(up(__file__)), 'configs')
TODOIST_CONF = join(CONFIGS_BASE, 'todoist.json')
AISLE_CONF = join(CONFIGS_BASE, 'aisle.conf')

UNIT_SEPARATOR = '|'

class Todoist:
    project: Project = None
    save_values: Dict[str,str] = {}
    sections: Dict[str, Section] = {}
    aisle_parser: AisleParser

    def __init__(self, aisle_parser: AisleParser):
        env = Env()
        env.read_env()
        
        self.aisle_parser = aisle_parser
        
        self.session = TodoistAPI(env.str('TODOIST_API_TOKEN'))
        self.logger = logging.getLogger(__name__)
        
        self.load_progress()
        if TASKS not in self.save_values:
            self.save_values[TASKS] = []
        
    
    def load_progress(self) -> str:
        with open(TODOIST_CONF, 'r') as file:
            self.save_values = json.load(file)
        
        
    def save_progress(self):
        with open(TODOIST_CONF, 'w') as file:
            json.dump(self.save_values, file)
    
    
    def create_shopping_project(self):
        if PROJECT_ID in self.save_values:
            self.project = self.session.get_project(self.save_values[PROJECT_ID])
            return
        
        self.project = self.session.add_project(name="Shopping List")
        self.save_values[PROJECT_ID] = self.project.id
        self.save_progress()
    
    
    def create_aisle_sections(self):
        if HAS_SECTIONS in self.save_values:
            sections = self.session.get_sections(project_id=self.project.id)
            for section in sections:
                self.sections[section.name] = section
            return
            
        section_names = self.aisle_parser.sections
        for section_name in section_names:
            section = self.session.add_section(name=section_name, project_id=self.project.id)
            self.sections[section.name] = section
            self.save_values[HAS_SECTIONS] = True
            self.save_progress()


    def create_shopping_tasks(self, shopping_items):
        for shopping_item in shopping_items:
            description = shopping_item['quantity']
            if 'unit' in shopping_item and shopping_item['unit'] != '':
                description += UNIT_SEPARATOR + shopping_item['unit']

            task = self.session.add_task(
                content=shopping_item['name'],
                description=description,
                project_id=self.project.id,
                section_id=self.sections[shopping_item['aisle']].id
            )
            
            self.save_values[TASKS].append(task.id)
        self.save_progress()
            
            
    def get_shopping_completed_tasks(self):
        if TASKS not in self.save_values:
            raise Exception('No shopping list tasks exists')
        
        completed_tasks = []
        uncompleted_tasks = []
        for task_id in self.save_values[TASKS]:
            try:
                task = self.session.get_task(task_id=task_id)
            except HTTPError:
                # Task was deleted
                continue
            
            if task.is_completed:
                completed_tasks.append(task)
                continue
            
            uncompleted_tasks.append(task_id)
            
        self.save_values[TASKS] = uncompleted_tasks
        self.save_progress()
                
        return completed_tasks
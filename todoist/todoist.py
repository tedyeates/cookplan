import json
import logging
from environs import Env
from todoist_api_python.api import TodoistAPI, Project

from cooklang.aisle_parser import AisleParser

PROJECT_ID = 'project_id'
HAS_SECTIONS = 'has_sections'
class Todoist:
    project: Project = None
    save_values = {}

    def __init__(self):
        env = Env()
        env.read_env()
        
        self.session = TodoistAPI(env.str('TODOIST_API_TOKEN'))
        self.logger = logging.getLogger(__name__)
        
        self.load_progress()
        self.aisle_parser = AisleParser(self.read_aisle_conf())
            
        self.create_shopping_project()
        self.create_aisle_sections()
        
    
    def read_aisle_conf(self) -> str:
        with open('/configs/aisle.conf', 'r') as file:
            return file.read()
        
    
    def load_progress(self) -> str:
        with open('/configs/todoist.conf', 'r') as file:
            self.save_values = json.load(file)
        
        
    def save_progress(self):
        with open('/configs/todoist.conf', 'r') as file:
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
            self.sections = self.session.get_sections(project_id=self.project_id)
            return
            
        section_names = self.aisle_parser.get_sections()
        for section_name in section_names:
            section = self.session.add_section(name=section_name, project_id=self.project.id)
            self.sections.append(section)
            self.save[HAS_SECTIONS] = True
            self.save_progress()
            
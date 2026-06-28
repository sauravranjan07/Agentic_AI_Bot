from configparser import ConfigParser
import os
class Config:
    def __init__(self,config_file='src/langgrapghagenticai/UI/uiconfigfile.ini'):
        if config_file is None:
            # This finds the directory this script is in and joins it to the .ini filename
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, 'uiconfigfile.ini')

        self.config=ConfigParser()
        self.config.read(config_file)
    
    def get_llm_option(self):
        return self.config["DEFAULT"].get("LLM_OPTION").split(',')
    
    def get_use_case_options(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(',') 
    
    def get_groq_model_option(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTION").split(',')
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
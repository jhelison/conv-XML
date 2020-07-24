import json
import os

class Config():
    def __init__(self):
        if not os.path.isdir('./config'):
            os.makedirs('./config')
            
        try:
            self.getConfig()
        except:
            self.config = {}
            self.init()
            
  
    def init(self):
        self.config['cert_path'] = ""
        self.config['input_folder'] = ""
        self.config['output_folder'] = ""
        self.config['cert_password'] = ""
           
        with open('./config/config.json', 'w') as f:     
            json.dump(self.config, f)
            f.close()
            
    def get(self, key):
        with open('./config/config.json', 'r') as f:
            text = f.read()
            config = json.loads(text)
            f.close()
        
        return config[key]
    
    def save(self, key, value):
        self.config[key] = value
        
        with open('./config/config.json', 'w') as f:
            json.dump(self.config, f)
            f.close()
            
    def getConfig(self):
        with open('./config/config.json', 'r') as f:
            text = f.read()
            config = json.loads(text)
            f.close()
            
        self.config = config
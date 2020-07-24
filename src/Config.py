import json
import os

class Config():
    def __init__(self):
        if not os.path.isdir('./config'):
            os.makedirs('./config')
            
        self.f = open('./config/config.json', 'w+')
        
        try:
            self.config = json.load(self.f)
        except:
            self.config = {}
            
        if not self.config.keys():
            self.init()
  
    def init(self):
        self.config['cert_path'] = ""
        self.config['input_folder'] = ""
        self.config['output_folder'] = ""
        self.config['cert_password'] = ""
        
        json.dump(self.config, self.f)
        
        self.f.close()
            
    def get(self, key):
        with open('./config/config.json', 'r') as f:
            text = f.read()
            print(text)
            config = json.loads(text)
            f.close()
        
        return config[key]
    
    def save(self, key, value):
        self.config[key] = value
        
        json.dump(self.config, self.f)
class FieldNotFoundError(Exception):
    def __init__(self, field, module):
        err_str = f"\"{field}\" field must be declared in \"{module}\" module"
        super().__init__(err_str)

class AttributeNotFoundError(Exception):
    def __init__(self, attr, module):
        err_str = f"\"{attr}\" attribute must be declared in \"{module}\" module"
        super().__init__(err_str)

class Module():
    def __init__(self, plugin_man):
        self.plugin_man = plugin_man
    
    def prepare(self, data):
        pass
    
    def run(self, data):
        pass

class Plugin():
    def __init__(self):
        self.modules = {}
    
    def register_module(self, name, module):
        self.modules[name] = module
        
    def get_modules(self):
        return self.modules
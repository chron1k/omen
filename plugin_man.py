import os, importlib

class PluginManager():
    def __init__(self):
        self.modules = {}

        self.load_plugins()
        self.start_modules()
        
    def load_plugins(self):
        for filename in os.listdir("./plugins"):
            if not filename.endswith(".py"): continue
            
            plugin_module = importlib.import_module(f"plugins.{filename[:-3]}")
            
            plugin = plugin_module.init()
            
            self.modules.update(plugin.get_modules())
            
    def parse_modules(self, node, parent_node, data):
        if node.tag in self.modules.keys():
                data.update({
                    "node": node,
                    "parent_node": parent_node
                })

                self.run_module(node.tag, data)

        for child in node.findall("./"):
            self.parse_modules(child, node, data)
            
    def start_modules(self):
        for mod_name in self.modules.keys():
            self.modules[mod_name] = self.modules[mod_name](self)
            
    def prepare_modules(self, data):
        for mod_name in self.modules.keys():
            self.modules[mod_name].prepare(data)
            
    def run_module(self, name, data):
        self.modules[name].run(data)
                
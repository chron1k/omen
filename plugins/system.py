import sys
sys.path.append("../")

from plugin_sdk import *

class System(Module):
    def prepare(self, data):
        scenario_root = data['xml_tree'].getroot()

        provider = scenario_root.find("provider")
        if provider == None: raise Exception("Provider must be defined in scenario root")
        else: self.provider = provider.text

        for sys_node in scenario_root.findall(".//system"):
            if sys_node not in scenario_root.findall("./system"): 
                raise Exception("Systems must be defined in scenario root")
        
    def run(self, data):
        node = data['node']
        packer_schema = data["packer_schema"]
        vagrant_schema = data["vagrant_schema"]
        
        sys_name = node.find("name")
        if sys_name == None: raise FieldNotFoundError("name", "system")
        else: sys_name = sys_name.text
        
        base = node.find("base")
        if base == None: raise FieldNotFoundError("base", "system")
        else: base = base.text

        synced_folders = []

        for folder in node.findall("./synced_folder"):
            host = folder.get("host")
            if host == None: raise AttributeNotFoundError("host", "synced_folder")

            guest = folder.get("guest")
            if guest == None: raise AttributeNotFoundError("guest", "synced_folder")

            synced_folders.append({
                "host": host,
                "guest": guest
            })
        
        packer_schema["builders"].append({
            "name": sys_name, 
            "box_name": sys_name,
            "source_path": base, 
            "type": "vagrant", 
            "provider": self.provider, 
            "communicator": "ssh", 
            "add_force": True,
        })

        vagrant_schema.append({
            "hostname": sys_name,
            "box": sys_name,
            "box_url": f"file://./boxes/{sys_name}.box",
            "synced_folders": synced_folders
        })

def init():
    plugin = Plugin()
    plugin.register_module("system", System)
    
    return plugin

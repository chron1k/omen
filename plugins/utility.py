import sys
sys.path.append("../")

from plugin_sdk import *
import os, shutil

class Utility(Module):
    def validate_util(self, util_node, scenario_root):
        for sys_node in scenario_root.findall(".//system"):
                if util_node in sys_node.findall("./utility"): return

                raise Exception("Utility must be defined within system")

    def prepare(self, data):
        scenario_root = data['xml_tree'].getroot()
        project_path = data['project_path']

        for util_node in scenario_root.findall(".//utility"):
            self.validate_util(util_node, scenario_root)

        self.utils_path = "./modules/utilities"

        if not os.path.exists(self.utils_path): os.makedirs(self.utils_path)

        os.makedirs(f"{project_path}/utilities")

    def run(self, data):
        node = data['node']
        project_path = data['project_path']
        packer_schema = data['packer_schema']
        parent_sys = data['parent_node']

        sys_name = parent_sys.find("name").text

        util_name = node.get("name")
        if util_name == None: raise AttributeNotFoundError("name", "utility")

        util_path = f"{self.utils_path}/{util_name}.yml"

        if not os.path.exists(util_path):
            raise Exception(f"Couldn't find utility \"{util_name}\"")

        if not os.path.exists(f"{project_path}/utilities/{util_name}.yml"):
            shutil.copy(util_path, f"{project_path}/utilities/")

        args = []

        if node.find("args") != None:
            for arg in node.find("args").findall("./"):
                args.append(f"{arg.tag}={arg.text}")

        provisioner = {
            "type": "ansible",
            "playbook_file": f"./utilities/{util_name}.yml"
        }

        if len(args) != 0:
            provisioner["extra_arguments"] = ["--extra-vars"] + args

        packer_schema['provisioners'].append(provisioner)

def init():
    plugin = Plugin()
    plugin.register_module("utility", Utility)
    
    return plugin
import sys
sys.path.append("../")

from plugin_sdk import *
import json

class Network(Module):
    def validate_network(self, net_node, scenario_root):
        for sys_node in scenario_root.findall(".//system"):
                if len(sys_node.findall("./network")) > 1:
                    raise Exception("System can't have more than one network")

                if net_node in sys_node.findall("./network"): return

                raise Exception("Network must be defined within system")

    def prepare(self, data):
        scenario_root = data['xml_tree'].getroot()

        for net_node in scenario_root.findall(".//network"):
            self.validate_network(net_node, scenario_root)

    def run(self, data):
        node = data['node']
        vagrant_schema = data['vagrant_schema']
        parent_sys = data['parent_node']

        sys_name = parent_sys.find("name").text

        for sys in vagrant_schema:
            if sys['hostname'] != sys_name: continue
            
            ip = node.find("ip")
            if ip != None: sys['ip'] = ip.text

            for port in node.findall("port"):
                if "forwarded_ports" not in sys: sys["forwarded_ports"] = []

                host_port = port.get("host")
                if host_port == None: raise AttributeNotFoundError("host", "port")

                guest_port = port.get("guest")
                if guest_port == None: raise AttributeNotFoundError("guest", "port")

                sys["forwarded_ports"].append({
                    "host": host_port,
                    "guest": guest_port
                })

def init():
    plugin = Plugin()
    plugin.register_module("network", Network)
    
    return plugin

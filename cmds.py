import json, os, time, subprocess, sys, shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from rich.console import Console

def build(scenario, plugin_man):
    console = Console()

    with console.status("[bold green]Building scenario...") as status:
        try:
            console.log(f"[green]Starting build for scenario: {scenario}")

            time_now = datetime.now().strftime('%H-%M-%S')
            project_path = f"./projects/omen_{time_now}"
            os.makedirs(project_path)

            xml_tree = ET.parse(scenario)
            
            data = {
                "xml_tree": xml_tree,
                "project_path": project_path
            }

            for module in plugin_man.modules.values():
                module.prepare(data)
            
            packer_schema = {
                "builders": [], 
                "provisioners": []
            }
            vagrant_schema = []
            
            scenario_root = xml_tree.getroot()

            data.update({
                "packer_schema": packer_schema,
                "vagrant_schema": vagrant_schema
            })

            console.log("[green]Parsing scenario")

            plugin_man.parse_modules(scenario_root, None, data)

            with open(f"./{project_path}/packer.json", "w") as f:
                json.dump(packer_schema, f, indent = 2)

            with open(f"./{project_path}/vagrant.json", "w") as f:
                json.dump(vagrant_schema, f, indent = 2)

            os.chdir(project_path)

            console.log("[green]Starting packer build")

            packer_proc = subprocess.Popen(["packer", "build", "packer.json"], stdout = subprocess.PIPE, stdin = subprocess.PIPE, bufsize = 1, universal_newlines = True)
            try:
                for line in packer_proc.stdout:
                    print(line, end = "")

            except KeyboardInterrupt:
                packer_proc.terminate()
                shutil.rmtree(f"../../{project_path}")
                console.log("[bold][red]Canceled build")
                sys.exit(0)

            sys_names = [ sys['name'] for sys in packer_schema['builders'] ]

            os.makedirs(f"./boxes")

            for sys_name in sys_names:
                shutil.copyfile(f"./output-{sys_name}/package.box", f"./boxes/{sys_name}.box")
                shutil.rmtree(f"./output-{sys_name}")

            shutil.copy(f"../../Vagrantfile", "./")

            console.log("[bold][red]Finished building scenario")

        except Exception:
            console.log("[bold][red]Build unsuccessful")
    
def cmdhandler(args, plugin_man):
    console = Console()

    if args.command == "build":
        build(args.scenario, plugin_man)
    
    else:
        console.log("[bold][red]Error: Unknown command")
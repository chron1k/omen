import argparse, sys, cmds, subprocess
from plugin_man import PluginManager

def build(scenario):
    print(f"Building scenario: {scenario}")

def main():
    plugin_man = PluginManager()
    
    parser = argparse.ArgumentParser(description = "OMEN: Extensible orchestration engine for vulnerable VM networks")
    parser.add_argument(
        "command",
        type = str,
        help = "Command to run"
    )
    parser.add_argument(
        "-s", "--scenario",
        required = True,
        dest = "scenario",
        type = str,
        help = "Path of the scenario file"
    )
    
    args = parser.parse_args()
    
    cmds.cmdhandler(args, plugin_man)

if __name__ == "__main__":
    main()
import json
import os
import importlib
import traceback

from typing import List
import kernel.registry as Registry

def launch(command: str, commandlineArgs: list) -> int:
    # Find executable bundle
    commandPaths: List[str] = json.loads(Registry.read("SOFTWARE.Helium.KernelSettings.Programs.Paths"))['data']
    appropriateCommandPath: str = ""
    for commandPath in commandPaths:
        try:
            with open(os.path.join(commandPath, command, "main.py"), 'r') as f:
                appropriateCommandPath = commandPath
                break
        except:
            pass
    
    # If not found, return command not found.
    if appropriateCommandPath == "":
        return Registry.read("SOFTWARE.Helium.Kernel.Proc.CommandNotFound")

    # If found, import the module and execute it
    try:
        module_name = f"{appropriateCommandPath.replace('/', '.')}{command}.main"
        module = importlib.import_module(module_name)
        
        # Reload
        importlib.reload(module)

        # Get the class
        CommandClass = getattr(module, command.capitalize())

        # Instantiate the command and execute it
        command_instance = CommandClass(commandlineArgs)
        command_instance.exec()
        
    except Exception as e:
        if Registry.read("SOFTWARE.Helium.KernelSettings.PrintErrors") == "1": print(f"Error executing command '{command}': {e}")
        if Registry.read("SOFTWARE.Helium.KernelSettings.PrintTraceback") == "1": traceback.print_exc()
        return Registry.read("SOFTWARE.Helium.Kernel.Proc.CommandExitFailure")
        
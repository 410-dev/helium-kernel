import json
import os
import importlib
import traceback
import inspect

from typing import List
import kernel.registry as Registry

def launch(command: str, commandlineArgs: list, returnRaw: bool = False) -> int:
    # Find executable bundle
    commandPaths: List[str] = json.loads(Registry.read("SOFTWARE.Helium.Settings.Programs.Paths"))['data']
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
        return Registry.read("SOFTWARE.Helium.Values.Proc.CommandNotFound")

    # If found, import the module and execute it
    try:
        className = command.split("-")
        capitalized_words = [word.capitalize() for word in className]

        # Join the capitalized words without any separator
        className = "".join(capitalized_words)
        return exec(f"{appropriateCommandPath.replace('/', '.')}{command}.main.py", className, commandlineArgs, returnRaw=returnRaw)
    except Exception as e:
        if Registry.read("SOFTWARE.Helium.Settings.PrintErrors") == "1": print(f"Error executing command '{command}': {e}")
        if Registry.read("SOFTWARE.Helium.Settings.PrintTraceback") == "1": traceback.print_exc()
        return Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitFailure")

def exec(commandPath: str, className: str, commandlineArgs: list, executeMethodName: str = None, returnRaw: bool = False) -> int:
    module_name = f"{commandPath.replace('/', '.')}".split(".py")[0]
    module = importlib.import_module(module_name)
    
    # Reload
    importlib.reload(module)

    # Get the class
    CommandClass = getattr(module, className)

    # Instantiate the command and execute it
    command_instance = CommandClass(commandlineArgs)
    if executeMethodName == None:
        result = command_instance.main()
    else:
        # Complete this
        executeMethod = getattr(command_instance, executeMethodName)
        result = executeMethod()
    successCode = Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess")
    if returnRaw and result != None:
        return result

    if result == None or result == successCode:
        return int(successCode)
    else:
        return int(result)

def execScript(scriptPath: str, functionArgs: list, functionName: str = "main", returnRaw: bool = False) -> int:
    module_name = f"{scriptPath.replace('/', '.')}".split(".py")[0]
    module = importlib.import_module(module_name)
    
    # Reload
    importlib.reload(module)

    # Get the function
    function = getattr(module, functionName)

    # Execute the function with the provided arguments
    result = function(functionArgs)

    if returnRaw and result != None:
        return result

    successCode = Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess")
    if result == None or result == successCode:
        return int(successCode)
    else:
        return int(result)


def getParentScript(nameOnly: bool = False, recursion: bool = True) -> str:
    # Get the parent process
    processName = inspect.stack()[1].filename

    # If nameOnly is true, return only the name of the process
    if nameOnly:
        processName = processName.split("/")[-1].split(".py")[0]
    
    # If recursion is true, return the name of the process that called the parent process
    if recursion:
        originalProcessName = copy.deepcopy(processName)
        stackLevel = 1
        while processName == originalProcessName:
            processName = inspect.stack()[stackLevel].filename
            if nameOnly:
                processName = processName.split("/")[-1].split(".py")[0]
            stackLevel += 1

    return processName
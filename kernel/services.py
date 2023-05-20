import asyncio
import threading
import os
import importlib

import kernel.registry as Registry
import kernel.procmgr as procmgr
from kernel.ipcmemory import IPCMemory

class Services():

    servicesLoaded = []

def kill(serviceName, usePID = True) -> bool:

    if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
        return

    pid = None
    object = None
    if not usePID:
        for i in range(0, len(Services.servicesLoaded)):
            if Services.servicesLoaded[i]["name"] == serviceName:
                pid = Services.servicesLoaded[i]["pid"]
                object = Services.servicesLoaded[i]
                if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
                    print(f"Killing service {serviceName} with PID {pid}")
                break
            
    if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1" and usePID:
        print(f"Killing service id: {serviceName}")

    if object != None:
        for i in range(0, len(Services.servicesLoaded)):
            if Services.servicesLoaded[i]["pid"] == pid:
                object = Services.servicesLoaded.pop(i)
                break
    
    if object == None:
        if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
            print(f"Service {serviceName} not found")
        return False

    if object["thread"] != None:
        object["stop_event"].set()  # Ask the thread to stop
        object["thread"].join()  # Wait for the thread to stop
        return True
    return False


def launch(commandPath: str, commandlineArgs: list, functionName: str = "main", returnRaw: bool = False, asynchronous: bool = True) -> int:

    if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
        return

    if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
        print(f"Launching service {commandPath}")

    module_name = f"{commandPath.replace(os.sep, '.')}".split(".py")[0]

    if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
        print(f"Loading module {module_name}")

    module = importlib.import_module(module_name)
    
    # Reload
    if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
        print(f"Updating module {module_name}")
    importlib.reload(module)

    # Get the class
    executeMethod = getattr(module, functionName)

    # Check if argument has a dictionary of "runas" field
    if IPCMemory.getObj(f"System.kernel.services.execInfo:{functionName}") == None:
        # Create information object
        pid = int(IPCMemory.getObj("System.kernel.session"))
        argObj = {
            "scriptPath": commandPath,
            "executedBy": procmgr.getParentScript(),
            "args": commandlineArgs,
            "runas": "service",
            "pid": pid
        }
        IPCMemory.setObj(f"System.kernel.services.execInfo:{commandPath}", argObj, permission="1112")
        IPCMemory.setObj(f"System.kernel.session", (pid + 1), permission="1112", persistent=True)
        
        if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
            print(f"Module {module_name} related information object copied to IPC memory")


    # Run asynchronously if needed
    if asynchronous:
        if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
            print(f"Running module {module_name} asynchronously")

        
        loop = asyncio.get_event_loop()
        stop_event = threading.Event()  # This event will be set when the thread should stop

        def run_in_executor():
            async def executeMethodWrapper():
                while not stop_event.is_set():
                    try:
                        await executeMethod(commandlineArgs)
                    except Exception:
                        break

            loop.run_until_complete(executeMethodWrapper())

        thread = threading.Thread(target=run_in_executor)
        
        argObj["thread"] = thread
        argObj["stop_event"] = stop_event
        argObj["thread"].start()
        Services.servicesLoaded.append(argObj)

        if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
            print(f"Module {module_name} thread started")
        result = None
    else:
        if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
            print(f"Running module {module_name} synchronously")
        result = asyncio.run(executeMethod(commandlineArgs))
        if Registry.read("SOFTWARE.Helium.Services.VerboseLoad") == "1":
            print(f"Module {module_name} finished with result {result}")


    successCode = Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess")
    if returnRaw and result != None:
        return result

    if result == None or result == successCode:
        return int(successCode)
    else:
        return int(result)

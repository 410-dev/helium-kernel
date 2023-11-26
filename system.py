import kernel.argsParser as argsParser
import kernel.procmgr as procmgr
import kernel.registry as Registry
import kernel.services as Service

from kernel.ipcmemory import IPCMemory
from typing import List


# This is a very simple interactive user interface directly connected to kernel process manager.
class System():
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def main(args: List[str]) -> int:
        val = 0
        userIn = Registry.read("USERS.System.Shell.RunOnLogin")
        while True:
            if userIn == None:
                userIn: str = input(f"{val} >>> ")
            if userIn == Registry.read("SYSTEM.Helium.SystemQuitOn"):
                if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") == "1":
                    for service in Service.Services.servicesLoaded:
                        Service.kill(service["pid"])
                
                if Registry.read("USERS.System.Shell.RunOnLogout"):
                    System.execute(Registry.read("USERS.System.Shell.RunOnLogout"))
                break

            if len(userIn.strip()) == 0:
                continue

            val = System.execute(userIn)
            userIn = None
            
            
    def execute(args):
        if args == None:
            return 0
        args = argsParser.parse(args.split())
        return procmgr.launch(args[0], args[1:], Registry.read("SYSTEM.Helium.Settings.RawReturnFlag") == "1")
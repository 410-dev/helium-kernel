
from typing import List

import json
import os
import kernel.registry as Registry


class Help:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def exec(self):
        try: 
            commandPaths: List[str] = json.loads(Registry.read("SOFTWARE.Helium.KernelSettings.Programs.Paths"))['data']
            
            if len(self.args) == 0:
                # Print current manual
                with open("kernel/commands/help/manual.txt", 'r') as f:
                    print(f.read())
                    return;
            
            # Find executable bundle
            helpString: str = ""
            for commandPath in commandPaths:
                try:
                    with open(os.path.join(commandPath, self.args[0], "manual.txt"), 'r') as f:
                        helpString = f.read()
                        break
                except:
                    pass
            
            # If not found, return command not found.
            if helpString == "":
                return Registry.read("SOFTWARE.Helium.Kernel.Proc.CommandNotFound")
            
            print(helpString)
        except Exception as e:
            print(f"Error opening config.json e: {e}")
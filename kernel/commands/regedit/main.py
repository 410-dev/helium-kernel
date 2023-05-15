import traceback
import kernel.registry as Registry
import kernel.argsParser as argsParser


class Regedit:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs
        
    def editor(self) -> int:
        try: 
            # Check number of arguments
            if len(self.args) == 0:
                print(f"Invalid number of arguments. Expected 1 or 2, got 0")
                return
            key = self.args[0]
            if len(self.args) == 2:
                var = Registry.read(key)
                val = self.args[1]
                Registry.write(key, val)
                print(f"Registry Updated: {key} = {var} -> {val}")
                
            elif len(self.args) == 1:
                regType = Registry.isKey(key)
                if regType == 2:
                    print(f"{key}: {Registry.read(key)}")
                elif regType == 1:
                    l = Registry.read(key)
                    for i in range(len(l)):
                        if l[i].find("=") != -1:
                            l[i] = "[Val] " + l[i].replace("=", ": ")
                        else:
                            l[i] = "[Sub] " + l[i]
                    l = "\n".join(l)
                    print(f"{l}")
                else:
                    print(f"Registry key does not exist.")
                
            else:
                print(f"Invalid number of arguments. Expected 1 or 2, got {len(self.args)}")
            
        except Exception as e:
            if Registry.read("SOFTWARE.Helium.Settings.PrintTraceback") == "1": traceback.print_exc()
            print(f"Error in settings. e: {e}")
        
    def interactive(self):
        while True: 
            command: str = input("regedit >>> ")
            
            if command == "exit":
                break
            
            command: list = command.split(" ")
            command = argsParser.parse(command)
            self.args = command
            self.editor()
    
    def exec(self):
        if len(self.args) == 0:
            self.interactive()
        else:
            self.editor()
        
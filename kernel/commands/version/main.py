import kernel.registry as Registry

class Version:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def exec(self):
        try: 
            baseName = Registry.read("SOFTWARE.CordOS.KernelSettings.Profiles.Foundation")
            baseVersion = Registry.read("SOFTWARE.CordOS.KernelSettings.Profiles.Version")
            osName = Registry.read("SOFTWARE.CordOS.System.Profiles.Name")
            osVersion = Registry.read("SOFTWARE.CordOS.System.Profiles.Version")
            print(f"Version Profiling:\nBaseSystem: {baseName} {baseVersion}\nOS: {osName} {osVersion}")
        except Exception as e:
            print(f"Error opening config.json e: {e}")
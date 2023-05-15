import kernel.registry as Registry
import json
import os

class DataBuild():
    
    def __init__(self, args):
        self.args = args
    
    def exec(self) -> int:
        masterList: str = Registry.read("SOFTWARE.Helium.Values.Data.Struct.MasterList")
        masterList = json.loads(masterList)
        masterList = masterList['data']
        
        for item in masterList:
            path: str = Registry.read(f"SOFTWARE.Helium.Values.Data.Struct.{item}")
            path: list = path.split("/")
            builtSoFar: str = ""
            for parents in path:
                builtSoFar = os.path.join(builtSoFar, parents)
                if not os.path.exists(builtSoFar):
                    os.mkdir(builtSoFar)
        
        return int(Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess"))
        
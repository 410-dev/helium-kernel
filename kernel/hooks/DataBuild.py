import kernel.registry as Registry
import json
import os

def main(args) -> int:
    if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
        print("Building data directories")

    masterList: str = Registry.read("SOFTWARE.Helium.Values.Data.Struct.MasterList")
    masterList = json.loads(masterList)
    masterList = masterList['data']

    if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
        print(f"Building {len(masterList)} directories")
    
    buildCount = 0
    for item in masterList:
        path: str = Registry.read(f"SOFTWARE.Helium.Values.Data.Struct.{item}")
        path: list = path.split(os.sep)
        builtSoFar: str = ""
        for parents in path:
            builtSoFar = os.path.join(builtSoFar, parents)
            if not os.path.exists(builtSoFar):
                os.mkdir(builtSoFar)
                buildCount += 1
                if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                    print(f"Built {builtSoFar}")
    
    if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
        print(f"Done building {buildCount} directories")
    
    return int(Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess"))
    
import kernel.registry as Registry
import json
import os

def main(args) -> int:
    if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
        print("[HOOK] [DataBuild] Building data directories")

    Index: str = Registry.read("SYSTEM.Helium.Values.Paths.Data.Index")
    Index = json.loads(Index)
    Index = Index['data']

    if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
        print(f"[HOOK] [DataBuild] Building {len(Index)} directories")
    
    buildCount = 0
    for item in Index:
        path: str = Registry.read(f"SYSTEM.Helium.Values.Paths.Data.{item}")
        path: list = path.split(os.sep)
        builtSoFar: str = ""
        for parents in path:
            builtSoFar = os.path.join(builtSoFar, parents)
            if not os.path.exists(builtSoFar):
                os.mkdir(builtSoFar)
                buildCount += 1
                if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                    print(f"[HOOK] [DataBuild] Built {builtSoFar}")
    
    if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
        print(f"[HOOK] [DataBuild] Done building {buildCount} directories")
    
    return int(Registry.read("SYSTEM.Helium.Values.Proc.CommandExitSuccess"))
    
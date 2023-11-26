import kernel.services as Service
import kernel.registry as Registry

import os
import json

def main(args) -> int:

    # if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
    #     return int(Registry.read("SYSTEM.Helium.Values.Proc.CommandExitSuccess"))

    # Run kernel services first
    serviceFiles = os.listdir(os.path.join("kernel", "coreservices"))
    blacklist: list = json.loads(Registry.read("SOFTWARE.Helium.Services.KernelBlacklist"))["data"]
    if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
        print("[HOOK] [ServiceLauncher] Loading kernel services")

    # Load kernel services
    for serviceFile in serviceFiles:

        # Skip blacklisted services
        if serviceFile in blacklist:
            if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                print(f"[HOOK] [ServiceLauncher] Skipping {serviceFile} because it is blacklisted")
            continue

        if serviceFile.startswith("_") or serviceFile.startswith("."):
            if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                print(f"[HOOK] [ServiceLauncher] Skipping {serviceFile} because it is a hidden file")
            continue

        # Load services if they are python files
        if serviceFile.endswith(".py"):
            if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                print(f"[HOOK] [ServiceLauncher] Loading {serviceFile[:-3]} from kernel/coreservices/{serviceFile}")
            
            Service.launch(os.path.join("kernel", "coreservices", serviceFile), args)

    # Run user services second
    serviceFiles = os.listdir(Registry.read("SYSTEM.Helium.Values.Paths.Data.Services"))
    blacklist: list = json.loads(Registry.read("SOFTWARE.Helium.Services.OtherBlacklist"))["data"]
    if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
        print("[HOOK] [ServiceLauncher] Loading user services")

    # Load user services
    for serviceFile in serviceFiles:
        
        # Skip blacklisted services
        if serviceFile in blacklist:
            if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                print(f"[HOOK] [ServiceLauncher] Skipping {serviceFile} because it is blacklisted")
            continue

        if serviceFile.startswith("_") or serviceFile.startswith("."):
            if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                print(f"[HOOK] [ServiceLauncher] Skipping {serviceFile} because it is a hidden file")
            continue

        # Load services if they are python files
        if serviceFile.endswith(".py"):
            if Registry.read("SYSTEM.Helium.Hooks.VerboseLoad") == "1":
                print(f"[HOOK] [ServiceLauncher] Loading {serviceFile[:-3]} from {Registry.read('SYSTEM.Helium.Values.Paths.Data.Services')}/{serviceFile}")
            
            Service.launch(os.path.join(Registry.read('SYSTEM.Helium.Values.Paths.Data.Services'), serviceFile), args)
    
    return int(Registry.read("SYSTEM.Helium.Values.Proc.CommandExitSuccess"))

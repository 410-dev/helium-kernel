import kernel.services as Service
import kernel.registry as Registry

import os
import json

def main(args) -> int:

    if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
        return int(Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess"))

    # Run kernel services first
    serviceFiles = os.listdir(os.path.join("kernel", "sysservices"))
    blacklist: list = json.loads(Registry.read("SOFTWARE.Helium.Services.KernelBlacklist"))["data"]
    if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
        print("Services: Loading kernel services")

    # Load kernel services
    for serviceFile in serviceFiles:

        # Skip blacklisted services
        if serviceFile in blacklist:
            if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                print(f"Services: Skipping {serviceFile} because it is blacklisted")
            continue

        if serviceFile.startswith("_") or serviceFile.startswith("."):
            if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                print(f"Services: Skipping {serviceFile} because it is a hidden file")
            continue

        # Load services if they are python files
        if serviceFile.endswith(".py"):
            if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                print(f"Services: Loading {serviceFile[:-3]} from kernel/sysservices/{serviceFile}")
            
            Service.launch(os.path.join("kernel", "sysservices", serviceFile), args)

    # Run user services second
    serviceFiles = os.listdir(Registry.read("SOFTWARE.Helium.Values.Data.Struct.Services"))
    blacklist: list = json.loads(Registry.read("SOFTWARE.Helium.Services.OtherBlacklist"))["data"]
    if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
        print("Services: Loading user services")

    # Load user services
    for serviceFile in serviceFiles:
        
        # Skip blacklisted services
        if serviceFile in blacklist:
            if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                print(f"Services: Skipping {serviceFile} because it is blacklisted")
            continue

        if serviceFile.startswith("_") or serviceFile.startswith("."):
            if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                print(f"Services: Skipping {serviceFile} because it is a hidden file")
            continue

        # Load services if they are python files
        if serviceFile.endswith(".py"):
            if Registry.read("SOFTWARE.Helium.Hooks.VerboseLoad") == "1":
                print(f"Services: Loading {serviceFile[:-3]} from {Registry.read('SOFTWARE.Helium.Values.Data.Struct.Services')}/{serviceFile}")
            
            Service.launch(os.path.join(Registry.read('SOFTWARE.Helium.Values.Data.Struct.Services'), serviceFile), args)
    
    return int(Registry.read("SOFTWARE.Helium.Values.Proc.CommandExitSuccess"))

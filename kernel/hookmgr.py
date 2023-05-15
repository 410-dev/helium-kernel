import kernel.registry as Registry
import kernel.procmgr as procmgr

import os
import json

def runHooks(parameters: list, kernelHooks: bool) -> list:
    # Returns list of hooks executed with the exit code
    # If kernelHooks is True, it will run kernel hooks, otherwise it will run user hooks
    
    hooksPath: str = ""
    blacklists: list = []
    if kernelHooks:
        hooksPath = "kernel/hooks/"
        blacklistData = Registry.read("SOFTWARE.Helium.Hooks.KernelBlacklist")
        if blacklistData != None:
            blacklistData = json.loads(blacklistData)
            blacklists = blacklistData['data']
    else:
        hooksPath = Registry.read("SOFTWARE.Helium.Values.Data.Struct.Hooks")
        blacklistData = Registry.read("SOFTWARE.Helium.Hooks.OtherBlacklist")
        if blacklistData != None:
            blacklistData = json.loads(blacklistData)
            blacklists = blacklistData['data']

    hooks: list = os.listdir(hooksPath)
    
    report: list = []
    
    for hook in hooks:
        if hook.startswith("_") or hook.startswith("."):
            continue
        
        if hook in blacklists:
            if Registry.read("SOFTWARE.Helium.Settings.KernelModulesVerbose") == "1": 
                print(f"Hook '{hook}' is blacklisted, skipping...")
            continue
        
        if Registry.read("SOFTWARE.Helium.Settings.KernelModulesVerbose") == "1":
            print(f"Running hook '{hook}'...")
        
        hookPath: str = os.path.join(hooksPath, hook)
        try:
            with open(hookPath, 'r') as f:
                exitcode = procmgr.exec(hookPath, hook.split(".py")[0], parameters)
                reportRow = [hook, exitcode]
                report.append(reportRow)
                if Registry.read("SOFTWARE.Helium.Settings.KernelModulesVerbose") == "1":
                    print(f"Hook '{hook}' exited with code {exitcode}")
        except:
            print(f"ERROR: Failed opening {hookPath}")